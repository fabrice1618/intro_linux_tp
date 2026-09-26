#!/usr/bin/env python3
"""Vérification automatique du TP « Commandes de base Linux ».

    python3 verify.py           tableau de progression de toutes les étapes
    python3 verify.py 3         vérification détaillée de l'étape 3 (ou : --step 3)
    python3 verify.py --all     vérification détaillée de toutes les étapes

Chaque tâche est contrôlée sur son résultat concret (fichiers, contenus,
permissions, processus...). En cas d'erreur, le script explique ce qu'il a
trouvé et donne une piste, sans donner la commande.

Codes de retour : 0 = validé, 2 = à corriger, 1 = environnement non prêt.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import textwrap
from pathlib import Path

BASE = Path(__file__).resolve().parent      # le script fonctionne depuis n'importe quel dossier
DATA = BASE / "data"                        # données sources : jamais modifiées par l'étudiant
WS = BASE / "workspace"                     # espace de travail de l'étudiant
WD = WS / "data"
PREUVES = WS / "preuves"                    # résultats enregistrés avec une redirection >
ETAT = WS / ".verify"                       # état du script (créé par setup.sh)
EMPREINTES = ETAT / "data.sha256"
REPONSES_JSON = ETAT / "reponses.json"
ARCHIVE = WS / "data_archive.tgz"

REPONSES = {}        # réponses correctes déjà données aux questions d'observation
INTERACTIF = False   # les questions ne sont posées qu'en vérification détaillée

# ---------------------------------------------------------------- affichage

COULEUR = sys.stdout.isatty() and "NO_COLOR" not in os.environ
LARGEUR = max(60, min(100, shutil.get_terminal_size((100, 24)).columns))


def _couleur(code):
    return lambda texte: f"\033[{code}m{texte}\033[0m" if COULEUR else str(texte)


VERT, ROUGE, JAUNE, CYAN, GRIS, GRAS = (_couleur(c) for c in ("92", "91", "93", "96", "90", "1"))


def imprimer(prefixe, texte, retrait):
    """Affiche un texte replié à la largeur du terminal, aligné après son préfixe."""
    # espaces insécables de la typographie française : pas de retour à la ligne après « ni avant : ; ? ! »
    texte = re.sub(r"« ", "«\u00a0", texte)
    texte = re.sub(r" ([:;?!»])", "\u00a0\\1", texte)
    lignes_texte = textwrap.wrap(texte, LARGEUR - retrait, break_long_words=False,
                                 break_on_hyphens=False) or [""]
    print(prefixe + lignes_texte[0])
    for suite in lignes_texte[1:]:
        print(" " * retrait + suite)


class Resultat:
    """Résultat d'une tâche : réussie ou non, message, explications ou remarques."""

    def __init__(self, ok, message, notes):
        self.ok = ok
        self.message = message
        self.notes = [n for n in notes if n]


def OK(message, *remarques):
    return Resultat(True, message, remarques)


def KO(message, *indices):
    return Resultat(False, message, indices)


def afficher(r):
    imprimer(f"  {VERT('✔') if r.ok else ROUGE('✘')} ", r.message, 4)
    for note in r.notes:
        imprimer(f"      {CYAN('↳')} ", note, 8)

# ---------------------------------------------------------------- outils


def rel(chemin):
    """Chemin relatif au dossier du TP, tel que l'étudiant le tape."""
    try:
        return Path(chemin).relative_to(BASE).as_posix()
    except ValueError:
        return str(chemin)


def lire(chemin):
    """Contenu texte d'un fichier, ou None s'il est absent ou illisible."""
    try:
        return Path(chemin).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def lignes(chemin):
    """Lignes non vides d'un fichier (espaces de fin retirés), ou None."""
    texte = lire(chemin)
    if texte is None:
        return None
    return [l.rstrip() for l in texte.splitlines() if l.strip()]


def source_data(nom):
    """Lignes non vides d'un fichier source (liste vide s'il manque : l'altération de data/ est signalée à part)."""
    return lignes(DATA / nom) or []


def identiques(a, b):
    try:
        return Path(a).read_bytes() == Path(b).read_bytes()
    except OSError:
        return False


def droits(chemin):
    """Droits d'un fichier en octal et en symbolique, par exemple « 640 (rw-r-----) »."""
    mode = Path(chemin).stat().st_mode
    return f"{mode & 0o777:o} ({stat.filemode(mode)[1:]})"


def plage(numeros):
    if numeros == list(range(numeros[0], numeros[-1] + 1)) and len(numeros) > 1:
        return f"{numeros[0]} à {numeros[-1]}"
    return ", ".join(map(str, numeros))


def lire_empreintes():
    """[(sha256, chemin relatif à data/)] enregistrés par setup.sh."""
    res = []
    for ligne in (lire(EMPREINTES) or "").splitlines():
        m = re.match(r"([0-9a-f]{64}) [ *](?:\./)?(.+)$", ligne)
        if m:
            res.append((m.group(1), m.group(2)))
    return res


def fichiers_data():
    """Fichiers sources créés par setup.sh, relatifs à data/ (ex. « logs/app.log »)."""
    noms = [nom for _, nom in lire_empreintes()]
    return noms or sorted(p.relative_to(DATA).as_posix() for p in DATA.rglob("*") if p.is_file())


def ailleurs(nom, attendu):
    """Fichiers de même nom à un autre endroit : erreur de répertoire courant fréquente."""
    trouves = []
    for racine, dossiers, fichiers in os.walk(BASE):
        dossiers[:] = [d for d in dossiers if d not in (".git", ".verify")]
        if nom in fichiers or nom in dossiers:
            if Path(racine) / nom != attendu:
                trouves.append(rel(Path(racine) / nom))
    if not nom.startswith(".") and (Path.home() / nom).exists() and Path.home() / nom != attendu:
        trouves.append(f"~/{nom}")
    return trouves


def absent(chemin, *indices):
    """Échec standard pour un fichier attendu mais introuvable."""
    autres = ailleurs(chemin.name, chemin)
    piste = None
    if autres:
        piste = (f"Un « {chemin.name} » existe ailleurs : {', '.join(autres[:3])}. Mauvais répertoire "
                 "courant ? Vérifiez avec pwd, puis placez le fichier au bon endroit.")
    return KO(f"{rel(chemin)} introuvable", piste, *indices)


def processus(pid):
    """(nom, uid) du processus pid, ou None s'il n'existe pas."""
    try:
        nom = Path(f"/proc/{pid}/comm").read_text().strip()
        return nom, os.stat(f"/proc/{pid}").st_uid
    except OSError:
        pass
    try:
        r = subprocess.run(["ps", "-o", "comm=,uid=", "-p", str(pid)], capture_output=True, text=True)
    except OSError:
        return None
    champs = r.stdout.split()
    return (champs[0], int(champs[1])) if r.returncode == 0 and len(champs) >= 2 else None


def sleeps_actifs():
    """PID des processus sleep de l'utilisateur encore actifs."""
    try:
        r = subprocess.run(["pgrep", "-u", str(os.getuid()), "-x", "sleep"], capture_output=True, text=True)
    except OSError:
        return []
    return r.stdout.split()


def est_trie(chemin):
    """Vrai si le fichier est trié selon la langue du shell, l'ordre ASCII ou sans tenir compte de la casse."""
    for options, env in ((["-c"], {}), (["-c"], {"LC_ALL": "C"}), (["-fc"], {})):
        try:
            r = subprocess.run(["sort", *options, str(chemin)], env={**os.environ, **env}, capture_output=True)
        except OSError:
            return True
        if r.returncode == 0:
            return True
    return False

# ---------------------------------------------------------------- questions d'observation


def charger_reponses():
    try:
        return json.loads(REPONSES_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def enregistrer_reponse(cle, valeur):
    REPONSES[cle] = valeur
    try:
        ETAT.mkdir(parents=True, exist_ok=True)
        REPONSES_JSON.write_text(json.dumps(REPONSES, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        pass


def question(cle, libelle, enonce, valider, indice):
    """Question dont la réponse s'obtient en exécutant les commandes de l'étape.

    valider(reponse) renvoie (bonne, remarque). Une bonne réponse est mémorisée :
    elle n'est plus redemandée, et le tableau de progression la prend en compte.
    """
    if cle in REPONSES:
        return OK(f"{libelle} : {REPONSES[cle]}")
    if not INTERACTIF:
        return KO(f"{libelle} : question pas encore répondue",
                  f"Lancez python3 verify.py {cle.split('.')[0]} pour y répondre.")
    imprimer(f"  {JAUNE('?')} ", enonce, 4)
    try:
        reponse = input("    > ").strip()
        if not sys.stdin.isatty():
            print(reponse)   # réponses lues dans un fichier ou un pipe : les afficher
    except EOFError:
        reponse = ""
        print()
    if not reponse:
        return KO(f"{libelle} : pas de réponse", indice)
    bonne, remarque = valider(reponse)
    if bonne:
        enregistrer_reponse(cle, reponse)
        return OK(f"{libelle} : {reponse}", remarque)
    return KO(f"{libelle} : « {reponse} » n'est pas la bonne réponse", remarque, indice)

# ---------------------------------------------------------------- étape 1 : aide


def e1_man():
    def valider(r):
        if r in ("-S", "S", "--sort=size"):
            return True, None
        if r in ("-s", "s"):
            return False, "-s (minuscule) affiche la taille de chaque fichier sans trier : les options sont sensibles à la casse."
        if r in ("-t", "t"):
            return False, "-t trie par date de modification, pas par taille."
        return False, None
    return question("1.tri_taille", "Option de ls qui trie par taille",
                    "Dans la page de manuel de ls, quelle option courte trie les fichiers par taille, "
                    "du plus gros au plus petit ?",
                    valider, "Ouvrez man ls, tapez /size puis Entrée ; n passe à l'occurrence suivante.")


JOURS = [("lundi", "monday"), ("mardi", "tuesday"), ("mercredi", "wednesday"), ("jeudi", "thursday"),
         ("vendredi", "friday"), ("samedi", "saturday"), ("dimanche", "sunday")]


def e1_date():
    bon = JOURS[datetime.date(2030, 1, 1).weekday()]

    def valider(r):
        r = r.lower().strip(" .")
        return r in bon or r in (bon[0][:3], bon[1][:3]), None
    return question("1.date", "Jour de la semaine du 1er janvier 2030",
                    "D'après la commande date, quel jour de la semaine sera le 1er janvier 2030 ?",
                    valider, "date --help : cherchez l'option qui affiche une date décrite par une chaîne "
                    "(« not 'now' »), puis donnez-lui 2030-01-01.")


def e1_apropos():
    def valider(r):
        if r == "pwd":
            return True, None
        if r == "cd":
            return False, "cd change de répertoire courant, il n'affiche pas son nom."
        return False, None
    return question("1.apropos", "Commande trouvée avec man -k",
                    "Avec man -k, trouvez la commande dont la description est « print name of "
                    "current/working directory ». Quel est son nom ?",
                    valider, "man -k directory liste toutes les commandes dont la description contient "
                    "« directory » ; un mot plus précis (working) réduit la liste.")


def e1_historique():
    f = PREUVES / "historique.txt"
    contenu = lignes(f)
    if contenu is None:
        return absent(f, "Depuis le dossier du TP : history 10 > workspace/preuves/historique.txt")
    if not contenu:
        return KO(f"{rel(f)} est vide",
                  "La redirection > a créé le fichier, mais la commande n'a rien affiché.")
    if not all(re.match(r"\s*\d+\*?\s", l) for l in contenu):
        return KO(f"{rel(f)} ne ressemble pas à une sortie de history",
                  "history affiche des lignes numérotées, par exemple « 42  ls -la ».")
    note = None
    if len(contenu) > 10:
        note = f"{len(contenu)} lignes : avec l'argument 10, history n'affiche que les 10 dernières commandes."
    return OK(f"{rel(f)} : {len(contenu)} commandes de l'historique", note)

# ---------------------------------------------------------------- étape 2 : se repérer


def e2_pwd():
    def valider(r):
        chemin = os.path.expanduser(r)
        if not chemin.startswith("/"):
            return False, "Un chemin absolu commence par / (la racine)."
        p = Path(chemin).resolve()
        if p == BASE:
            return True, None
        if p in BASE.parents:
            return False, ("C'est un dossier parent du TP : entrez dans le dossier tp_start avec cd, "
                           "puis affichez à nouveau le répertoire courant.")
        return False, None
    return question("2.pwd", "Chemin absolu du dossier du TP",
                    "Placé dans le dossier du TP (tp_start), affichez le chemin absolu du répertoire "
                    "courant. Quel est-il ?",
                    valider, "Relisez l'extrait de help pwd.")


def e2_secret():
    m = re.search(r"Mot secret\s*:\s*(\S+)", lire(DATA / ".bienvenue") or "")
    if not m:
        return KO("data/.bienvenue introuvable", "Relancez bash setup.sh pour recréer les données.")
    secret = m.group(1)
    return question("2.secret", "Mot secret du fichier caché",
                    "Un fichier caché se trouve dans data/. Trouvez-le et affichez son contenu : "
                    "quel est le mot secret ?",
                    lambda r: (r.lower() == secret.lower(), None),
                    "ls n'affiche pas les fichiers dont le nom commence par un point : cherchez l'option "
                    "de ls qui les montre, puis affichez le fichier avec cat.")


def e2_taille():
    f = DATA / "sample.csv"
    if not f.is_file():
        return KO("data/sample.csv introuvable", "Relancez bash setup.sh pour recréer les données.")
    taille = f.stat().st_size

    def valider(r):
        m = re.fullmatch(r"(\d+)\s*(octets?)?", r.lower())
        if m and int(m.group(1)) == taille:
            return True, None
        if re.fullmatch(r"[\d.,]+\s*[kKmM]\w*", r):
            return False, "Avec -h la taille est arrondie : sans -h, ls -l affiche le nombre exact d'octets."
        if m and int(m.group(1)) == 4096:
            return False, "4096 est la taille d'un dossier : regardez la ligne du fichier sample.csv."
        return False, None
    return question("2.taille", "Taille de data/sample.csv",
                    "D'après le listage détaillé de data/, quelle est la taille de sample.csv, en octets ?",
                    valider, "Dans un listage détaillé, la taille en octets est la colonne juste avant la date.")


def e2_relatif():
    cible = (DATA / "fruits.txt").resolve()

    def valider(r):
        if r.startswith(("/", "~")):
            return False, ("C'est un chemin absolu. Un chemin relatif part du répertoire courant : "
                           "il ne commence ni par / ni par ~.")
        p = (PREUVES / r).resolve()
        if p == cible:
            return True, None
        if not p.exists():
            return False, f"Depuis workspace/preuves, ce chemin désigne {rel(p)}, qui n'existe pas."
        return False, f"Depuis workspace/preuves, ce chemin désigne {rel(p)}."
    return question("2.relatif", "Chemin relatif de workspace/preuves vers data/fruits.txt",
                    "Placez-vous dans workspace/preuves. Depuis ce dossier, quel chemin RELATIF désigne "
                    "le fichier data/fruits.txt ? Testez-le avec cat avant de répondre.",
                    valider, ".. désigne le dossier parent : combien de fois faut-il remonter pour revenir "
                    "au dossier du TP ?")

# ---------------------------------------------------------------- étape 3 : créer


def etape4_commencee():
    return (WS / "backup_data").exists() or (WS / "bonjour.renomme.txt").exists()


def e3_dossiers():
    manquants = [d for d in ("docs", "data", "tmp") if not (WS / d).is_dir()]
    if not manquants:
        return OK("Dossiers workspace/docs, workspace/data et workspace/tmp présents")
    indices = []
    for d in manquants:
        if (WS / d).exists():
            indices.append(f"workspace/{d} existe mais c'est un fichier, pas un dossier : "
                           "supprimez-le, puis créez le dossier.")
        elif d != "data" and (BASE / d).is_dir():
            indices.append(f"Un dossier {d} a été créé à la racine du TP au lieu de workspace/ : "
                           "vérifiez votre répertoire courant avec pwd.")
    if (WS / "workspace").is_dir():
        indices.append("Un dossier workspace/workspace existe : la commande a été lancée depuis "
                       "workspace/ avec un chemin qui commençait déjà par workspace/.")
    indices.append("mkdir accepte plusieurs dossiers dans une même commande.")
    return KO("Dossier(s) manquant(s) : " + ", ".join(f"workspace/{d}" for d in manquants), *indices)


def e3_arborescence():
    janvier = WS / "projets" / "2026" / "janvier"
    if janvier.is_dir():
        return OK(f"Arborescence {rel(janvier)} créée")
    if janvier.parent.is_dir() and etape4_commencee():
        return OK("workspace/projets/2026 présent (janvier a été supprimé à l'étape 4)")
    return KO(f"{rel(janvier)} introuvable",
              "Sans option, mkdir refuse de créer janvier tant que projets/2026 n'existe pas : cherchez "
              "dans l'extrait de man mkdir l'option qui crée aussi les dossiers parents manquants.")


def e3_todo():
    f = WD / "todo.txt"
    if f.is_dir():
        return KO(f"{rel(f)} est un dossier", "Ici on veut un fichier : mkdir crée des dossiers, pas des fichiers.")
    if not f.is_file():
        return absent(f, "Cherchez dans l'extrait de la documentation la commande qui crée un fichier vide.")
    note = None if f.stat().st_size == 0 else "Le fichier n'est pas vide (la tâche demandait un fichier vide) : pas bloquant."
    return OK(f"{rel(f)} créé", note)


def e3_cache():
    f = WS / "tmp" / ".cache"
    if f.exists():
        return OK(f"Fichier caché {rel(f)} créé", "ls workspace/tmp ne l'affiche pas ; ls -a workspace/tmp, si.")
    if (WS / "tmp" / "cache").exists():
        return KO(f"{rel(f)} introuvable, mais workspace/tmp/cache existe",
                  "Le nom d'un fichier caché commence par un point : créez .cache.")
    return absent(f)


def e3_bonjour():
    f = WS / "docs" / "bonjour.txt"
    deplace = WS / "bonjour.renomme.txt"
    source = f if f.exists() else deplace if deplace.exists() else None
    if source is None:
        return absent(f, "echo affiche un texte ; la redirection > envoie cet affichage dans un fichier.")
    n = len(lignes(source) or [])
    if n >= 2:
        suffixe = " (renommé et déplacé à l'étape 4)" if source == deplace else ""
        return OK(f"{rel(f)} : {n} lignes{suffixe}")
    if n == 1:
        return KO(f"{rel(source)} ne contient qu'une ligne",
                  "La redirection > remplace tout le contenu du fichier : pour ajouter une ligne "
                  "à la fin, utilisez >>.")
    return KO(f"{rel(source)} est vide", "Écrivez-y deux lignes avec echo et les redirections > puis >>.")

# ---------------------------------------------------------------- étape 4 : copier, déplacer, supprimer


def e4_copie():
    copie = WS / "backup_data"
    if not copie.is_dir():
        return KO(f"{rel(copie)} introuvable",
                  "Sans option, cp refuse de copier un dossier (« -r non spécifié ») : cherchez l'option "
                  "de copie récursive dans l'extrait de man cp.")
    if (copie / "data").is_dir():
        return KO("La copie se trouve dans workspace/backup_data/data",
                  "workspace/backup_data existait déjà : cp a donc copié data À L'INTÉRIEUR de ce dossier. "
                  "Supprimez workspace/backup_data, puis refaites la copie une seule fois.")
    noms = [n for n in fichiers_data() if "/" not in n]
    manquants = [n for n in noms if not (copie / n).is_file()]
    if manquants:
        return KO("Fichiers absents de la sauvegarde : " + ", ".join(manquants))
    differents = [n for n in noms if not identiques(DATA / n, copie / n)]
    if differents:
        return KO("Fichiers différents de l'original : " + ", ".join(differents))
    return OK(f"{rel(copie)} : copie de data/ ({len(noms)} fichiers, dont le fichier caché .bienvenue)")


def e4_renommer():
    ancien = WS / "docs" / "bonjour.txt"
    dans_docs = WS / "docs" / "bonjour.renomme.txt"
    final = WS / "bonjour.renomme.txt"
    if dans_docs.exists() or final.exists():
        if ancien.exists():
            return KO(f"{rel(ancien)} existe encore",
                      "Renommer ne laisse pas l'ancien fichier : vous avez sans doute copié au lieu de "
                      "renommer. Supprimez l'ancien fichier.")
        return OK("bonjour.txt renommé en bonjour.renomme.txt")
    if (WS / "bonjour.txt").exists():
        return KO("workspace/bonjour.txt : le fichier a été déplacé mais porte toujours son ancien nom",
                  "La destination de mv peut être un nouveau nom de fichier.")
    if ancien.exists():
        return KO(f"{rel(ancien)} n'a pas encore été renommé",
                  "Relisez la DESCRIPTION de man mv dans l'extrait : « Rename SOURCE to DEST ».")
    return absent(final, "Si bonjour.txt a été perdu, recréez-le (étape 3) avant de le renommer.")


def e4_deplacer():
    dans_docs = WS / "docs" / "bonjour.renomme.txt"
    final = WS / "bonjour.renomme.txt"
    if final.is_file():
        if dans_docs.exists():
            return KO("bonjour.renomme.txt est à la fois dans workspace/docs et dans workspace/",
                      "Déplacer ne laisse pas de copie derrière soi : supprimez celui de workspace/docs.")
        if len(lignes(final) or []) < 2:
            return KO(f"{rel(final)} a perdu son contenu",
                      "Le fichier doit toujours contenir les lignes écrites à l'étape 3.")
        return OK("bonjour.renomme.txt déplacé dans workspace/")
    if dans_docs.exists():
        return KO("bonjour.renomme.txt est encore dans workspace/docs",
                  "Quand la destination de mv est un dossier existant, le fichier y est déplacé "
                  "en gardant son nom.")
    return KO(f"{rel(final)} introuvable", "Renommez d'abord workspace/docs/bonjour.txt (tâche précédente).")


def e4_rmdir():
    annee = WS / "projets" / "2026"
    janvier = annee / "janvier"
    if janvier.is_dir():
        if any(janvier.iterdir()):
            return KO(f"{rel(janvier)} n'est pas vide",
                      "La commande qui supprime les dossiers vides refuse un dossier qui contient "
                      "quelque chose : videz-le d'abord.")
        return KO(f"{rel(janvier)} existe encore",
                  "Cherchez dans l'extrait de la documentation la commande qui supprime un dossier VIDE.")
    if not annee.is_dir():
        return KO(f"{rel(annee)} introuvable",
                  "Seul le dossier janvier devait disparaître. Si vous avez supprimé trop de choses, "
                  "recréez workspace/projets/2026 ; si l'étape 3 n'est pas faite, commencez par elle.")
    return OK(f"Dossier vide {rel(janvier)} supprimé")


def e4_rm():
    copie = WS / "backup_data"
    if not (DATA / "logs" / "app.log").is_file():
        return KO("data/logs a disparu : c'est l'ORIGINAL qui a été supprimé, pas la copie",
                  "Relancez bash setup.sh pour restaurer data/ (workspace/ est conservé), puis "
                  "supprimez workspace/backup_data/logs.")
    if not copie.is_dir():
        return KO(f"{rel(copie)} introuvable", "Faites d'abord la copie (tâche 1).")
    if (copie / "logs").exists():
        return KO(f"{rel(copie / 'logs')} existe encore",
                  "Un dossier non vide ne se supprime pas avec rmdir : cherchez l'option récursive de rm. "
                  "La suppression est définitive : relisez la commande avant de valider.")
    return OK(f"{rel(copie / 'logs')} supprimé (l'original data/logs est intact)")

# ---------------------------------------------------------------- étape 5 : rechercher


def e5_find():
    f = PREUVES / "find_fruits.txt"
    contenu = lignes(f)
    if contenu is None:
        return absent(f, "Redirigez la sortie de find vers ce fichier.")
    attendus = sorted(p.name for p in DATA.rglob("*") if p.is_file() and "fruits" in p.name.lower())
    trouves = {Path(l.strip()).name for l in contenu if not l.startswith("find:")}
    if not trouves:
        return KO(f"{rel(f)} est vide", "find n'a rien trouvé : vérifiez le dossier de départ et le motif.")
    intrus = sorted(n for n in trouves if "fruits" not in n.lower())
    if intrus:
        return KO(f"La liste contient des noms sans « fruits » : {', '.join(intrus[:4])}",
                  "Sans critère, find liste tout : ajoutez un critère sur le nom du fichier.")
    manquants = [n for n in attendus if n not in trouves]
    if manquants:
        if all(n != n.lower() for n in manquants):
            indice = ("-name distingue majuscules et minuscules : « *fruits* » ne correspond pas à "
                      f"« {manquants[0]} ». Cherchez la variante insensible à la casse.")
        else:
            indice = ("Le motif doit contenir des jokers (*fruits*), entre guillemets pour que le shell "
                      "ne le remplace pas lui-même.")
        return KO("Fichier(s) non trouvé(s) : " + ", ".join(manquants), indice)
    return OK("find a trouvé " + " et ".join(attendus))


def e5_grep():
    f = PREUVES / "grep_poire.txt"
    contenu = lignes(f)
    if contenu is None:
        return absent(f, "Redirigez la sortie de grep vers ce fichier.")
    source = (lire(DATA / "fruits.txt") or "").splitlines()
    attendu = [f"{i}:{l}" for i, l in enumerate(source, 1) if "poire" in l.lower()]
    obtenu = [re.sub(r"^\S*fruits\.txt:", "", l) for l in contenu]
    if obtenu == attendu:
        return OK("grep a trouvé les lignes " + ", ".join(attendu))
    if not obtenu:
        return KO(f"{rel(f)} est vide", "grep n'a trouvé aucune ligne : vérifiez le mot cherché et le fichier.")
    if not all(re.match(r"\d+:", l) for l in obtenu):
        return KO("Les lignes ne sont pas précédées de leur numéro",
                  "Cherchez dans l'extrait de man grep l'option qui préfixe chaque ligne par son numéro.")
    if set(obtenu) < set(attendu):
        return KO(f"{len(obtenu)} ligne(s) trouvée(s) sur {len(attendu)}",
                  "grep distingue majuscules et minuscules : cherchez l'option qui ignore la casse.")
    return KO("Résultat inattendu : " + ", ".join(obtenu[:4]),
              "Seules les lignes de data/fruits.txt contenant « poire » (quelle que soit la casse) sont attendues.")


def e5_which():
    f = PREUVES / "which_python3.txt"
    texte = lire(f)
    if texte is None:
        return absent(f, "Redirigez vers ce fichier la commande qui affiche le chemin complet d'un exécutable.")
    m = re.search(r"(/[^\s()]+)", texte)
    if not m:
        return KO(f"{rel(f)} ne contient pas de chemin", "Un chemin complet commence par /.")
    chemin, attendu = m.group(1), shutil.which("python3")
    if attendu and os.path.realpath(chemin) == os.path.realpath(attendu):
        note = "C'est la sortie de type ; which affiche seulement le chemin." if re.search(r"\b(est|is)\b", texte) else None
        return OK(f"python3 se trouve dans {chemin}", note)
    return KO(f"{chemin} n'est pas le python3 trouvé dans votre PATH",
              "which cherche la commande dans les dossiers de la variable PATH.")

# ---------------------------------------------------------------- étape 6 : filtres et pipes


def e6_extrait():
    f = WD / "lorem_extrait.txt"
    obtenu = lignes(f)
    if obtenu is None:
        return absent(f, "Enchaînez deux commandes avec un pipe |, puis redirigez le résultat vers ce fichier.")
    source = source_data("lorem.txt")
    if obtenu == source[1:4]:
        return OK(f"{rel(f)} : lignes 2 à 4 de lorem.txt")
    if not obtenu:
        return KO(f"{rel(f)} est vide")
    numeros = [source.index(l) + 1 for l in obtenu if l in source]
    if len(numeros) != len(obtenu):
        return KO(f"{rel(f)} contient des lignes qui ne viennent pas de data/lorem.txt")
    return KO(f"{rel(f)} contient les lignes {plage(numeros)} de lorem.txt au lieu des lignes 2 à 4",
              "head -n 4 garde les 4 premières lignes ; il reste à ne conserver que les 3 dernières "
              "de celles-ci, avec une deuxième commande reliée par un pipe |.")


def e6_uniques():
    f = WD / "fruits_uniques.txt"
    obtenu = lignes(f)
    if obtenu is None:
        return absent(f)
    source = source_data("fruits.txt")
    if not obtenu:
        return KO(f"{rel(f)} est vide")
    if any(re.match(r"\s*\d+\s", l) for l in obtenu):
        return KO("Les lignes commencent par un nombre",
                  "uniq -c ajoute le nombre d'occurrences : ici on veut seulement la liste sans doublons.")
    intrus = [l for l in obtenu if l not in source]
    if intrus:
        return KO("Lignes absentes de data/fruits.txt : " + ", ".join(intrus[:3]),
                  "Le fichier doit être produit à partir de data/fruits.txt, sans autre transformation.")
    doublons = sorted({l for l in obtenu if obtenu.count(l) > 1})
    if doublons:
        return KO("Doublons restants : " + ", ".join(doublons),
                  "uniq ne supprime que les doublons CONSÉCUTIFS : triez d'abord avec sort, puis "
                  "transmettez le résultat à uniq avec un pipe |.")
    presents = {l.lower() for l in obtenu}
    manquants = [l for l in dict.fromkeys(source) if l.lower() not in presents]
    if manquants:
        return KO("Fruits manquants : " + ", ".join(manquants))
    if not est_trie(f):
        return KO("Les lignes ne sont pas triées", "uniq ne trie pas : c'est le rôle de sort.")
    note = None
    if len(obtenu) < len(set(source)):
        note = "Majuscules et minuscules ont été fusionnées (banane/Banane) : effet de -f ou -i, accepté."
    return OK(f"{rel(f)} : {len(obtenu)} fruits, triés, sans doublon", note)


def e6_wc():
    f = WD / "lorem_wc.txt"
    texte = lire(f)
    if texte is None:
        return absent(f)
    nombres = [int(n) for n in re.findall(r"\b\d+\b", texte)]
    if not nombres:
        return KO(f"{rel(f)} ne contient aucun nombre")
    contenu = (DATA / "lorem.txt").read_text(encoding="utf-8")
    mots = len(contenu.split())
    if len(nombres) >= 3 and mots in nombres:
        return KO(f"{rel(f)} contient {' '.join(map(str, nombres[:3]))}",
                  "Sans option, wc affiche lignes, mots et octets : choisissez l'option qui n'affiche que les mots.")
    n = nombres[0]
    if n == mots:
        return OK(f"{rel(f)} : {n} mots")
    autres = {len(contenu.encode()): "le nombre d'OCTETS (-c)", len(contenu): "le nombre de CARACTÈRES (-m)",
              contenu.count("\n"): "le nombre de LIGNES (-l)"}
    if n in autres:
        return KO(f"{rel(f)} contient {n} : c'est {autres[n]} de lorem.txt, pas le nombre de mots",
                  "Cherchez dans l'extrait de man wc l'option qui compte les mots.")
    return KO(f"{rel(f)} contient {n}, qui n'est pas le nombre de mots de data/lorem.txt")


def e6_upper():
    f = WD / "fruits_upper.txt"
    obtenu = lignes(f)
    if obtenu is None:
        return absent(f)
    source = source_data("fruits.txt")
    minuscules = [l for l in obtenu if re.search(r"[a-z]", l)]
    if minuscules:
        return KO("Lignes encore en minuscules : " + ", ".join(minuscules[:3]),
                  "tr remplace chaque caractère de la 1re liste par le caractère correspondant de la 2e : "
                  "voyez les classes [:lower:] et [:upper:] dans l'extrait de man tr.")
    if len(obtenu) != len(source):
        return KO(f"{len(obtenu)} lignes au lieu de {len(source)}",
                  "Convertissez tout data/fruits.txt, sans trier ni supprimer les doublons.")

    def ascii_maj(s):
        return "".join(c.upper() if "a" <= c <= "z" else c for c in s)
    if sorted(obtenu) in (sorted(s.upper() for s in source), sorted(ascii_maj(s) for s in source)) \
            and obtenu not in ([s.upper() for s in source], [ascii_maj(s) for s in source]):
        return KO("Les lignes sont en majuscules mais dans le désordre",
                  "Convertissez data/fruits.txt en gardant l'ordre des lignes, sans trier.")
    for o, s in zip(obtenu, source):
        if o not in (s.upper(), ascii_maj(s)):
            return KO(f"Ligne inattendue : « {o} » à la place de « {s} » en majuscules")
    note = None
    if obtenu != [s.upper() for s in source]:
        note = ("« PêCHE » : tr traite les octets un par un et ne convertit pas les lettres accentuées, "
                "codées sur plusieurs octets en UTF-8. C'est une limite connue de tr.")
    return OK(f"{rel(f)} : fruits.txt en majuscules", note)


def e6_cut():
    f = WD / "col2.txt"
    obtenu = lignes(f)
    if obtenu is None:
        return absent(f)
    tableau = [l.split(",") for l in source_data("sample.csv")]

    def colonne(k):
        return [r[k] if len(r) > k else "" for r in tableau]
    if obtenu in (colonne(1), colonne(1)[1:]):
        return OK(f"{rel(f)} : 2e colonne de sample.csv ({', '.join(colonne(1)[1:4])}…)")
    if any("," in l for l in obtenu):
        return KO("Les lignes contiennent encore des virgules : elles ont été conservées entières",
                  "Sans -d, cut découpe sur la tabulation : indiquez la virgule comme délimiteur.")
    for k in (0, 2):
        if obtenu in (colonne(k), colonne(k)[1:]):
            return KO(f"C'est la colonne {k + 1} (« {colonne(k)[0]} »), pas la 2e",
                      "Les champs sont numérotés à partir de 1 : vérifiez le numéro donné à -f.")
    return KO("Contenu inattendu : " + ", ".join(obtenu[:3]),
              "Attendu : la 2e colonne de data/sample.csv, une valeur par ligne.")


def e6_info():
    f = WD / "nb_info.txt"
    texte = lire(f)
    if texte is None:
        return absent(f)
    journal = source_data("logs/app.log")
    attendu = sum("INFO" in l for l in journal)
    if "[INFO]" in texte:
        return KO(f"{rel(f)} contient les lignes elles-mêmes, pas leur nombre",
                  "Transmettez la sortie de grep, avec un pipe |, à la commande qui compte les lignes.")
    m = re.search(r"\d+", texte)
    if not m:
        return KO(f"{rel(f)} ne contient aucun nombre")
    n = int(m.group())
    if n == attendu:
        return OK(f"{rel(f)} : {n} lignes INFO dans app.log")
    if n == len(journal):
        return KO(f"{rel(f)} contient {n} : c'est le nombre total de lignes du journal",
                  "Filtrez d'abord les lignes INFO avec grep, puis comptez-les.")
    return KO(f"{rel(f)} contient {n}, qui n'est pas le nombre de lignes INFO de app.log")

# ---------------------------------------------------------------- étape 7 : archiver


def membres_archive():
    """Noms contenus dans l'archive (sans « ./ » initial), ou None si elle est illisible."""
    try:
        with tarfile.open(ARCHIVE) as t:
            return [m.name[2:] if m.name.startswith("./") else m.name for m in t.getmembers()]
    except (OSError, tarfile.TarError):
        return None


def e7_archive():
    if not ARCHIVE.is_file():
        return absent(ARCHIVE, "Cherchez dans l'extrait de man tar les options create, gzip et file.")
    noms = membres_archive()
    if noms is None:
        return KO(f"{rel(ARCHIVE)} n'est pas une archive tar lisible",
                  "-f doit être immédiatement suivi du nom de l'archive ; viennent ensuite les fichiers à archiver.")
    if ARCHIVE.read_bytes()[:2] != b"\x1f\x8b":
        return KO(f"{rel(ARCHIVE)} n'est pas compressée",
                  "Le nom .tgz ne compresse rien par lui-même : ajoutez l'option qui fait passer l'archive par gzip.")
    if "data/fruits.txt" not in noms:
        longs = [n for n in noms if n.endswith("/data/fruits.txt")]
        if longs:
            return KO(f"Les chemins de l'archive commencent par « {longs[0][:-len('data/fruits.txt')]} »",
                      "L'archive a été créée avec un chemin absolu : tar retire le / initial mais conserve "
                      "tout le reste du chemin. Depuis le dossier du TP, archivez le chemin relatif data.")
        if "fruits.txt" in noms:
            return KO("L'archive contient les fichiers de data/ mais pas le dossier data/ lui-même",
                      "Depuis le dossier du TP, archivez le dossier data : les chemins doivent commencer par data/.")
        return KO("data/fruits.txt absent de l'archive", "Contenu trouvé : " + ", ".join(noms[:6]))
    attendus = ["data/" + n for n in fichiers_data()]
    manquants = [n for n in attendus if n not in noms]
    if manquants:
        return KO("Fichiers absents de l'archive : " + ", ".join(manquants))
    return OK(f"{rel(ARCHIVE)} : archive tar compressée par gzip, {len(attendus)} fichiers de data/")


def e7_liste():
    f = PREUVES / "contenu_archive.txt"
    texte = lire(f)
    if texte is None:
        return absent(f, "Redirigez vers ce fichier la sortie de la commande qui LISTE le contenu de l'archive.")
    if "data/fruits.txt" not in texte:
        return KO(f"{rel(f)} ne mentionne pas data/fruits.txt",
                  "tar doit savoir quoi faire (lister), avec quel filtre (gzip) et sur quelle archive (-f).")
    return OK(f"{rel(f)} : liste du contenu de l'archive")


def e7_extraction():
    tmp = WS / "tmp"
    cible = tmp / "data" / "fruits.txt"
    if cible.is_file():
        if not identiques(cible, DATA / "fruits.txt"):
            return KO(f"{rel(cible)} diffère de data/fruits.txt")
        return OK("Archive extraite dans workspace/tmp/data/")
    if (tmp / "fruits.txt").is_file():
        return KO("fruits.txt a été extrait directement dans workspace/tmp/, sans le dossier data/",
                  "L'archive ne contient pas le dossier data/ : recréez-la (tâche 1), puis extrayez-la à nouveau.")
    if tmp.is_dir():
        autres = sorted(tmp.glob("**/data/fruits.txt"))
        if autres:
            return KO(f"Archive extraite dans {rel(autres[0].parent.parent)}",
                      "L'archive contient des chemins absolus : recréez-la depuis le dossier du TP (tâche 1).")
    elif not tmp.exists():
        return KO("workspace/tmp introuvable", "Ce dossier est créé à l'étape 3.")
    return KO("Rien n'a été extrait dans workspace/tmp",
              "Sans -C, tar extrait dans le répertoire courant : -C indique le dossier de destination.")

# ---------------------------------------------------------------- étape 8 : liens et permissions


def e8_lien():
    lien = WD / "link_fruits.txt"
    cible = DATA / "fruits.txt"
    if not lien.is_symlink():
        if lien.is_file():
            if os.path.samefile(lien, cible):
                return KO(f"{rel(lien)} est un lien PHYSIQUE, pas symbolique",
                          "Sans option, ln crée un lien physique : ajoutez l'option des liens symboliques.")
            return KO(f"{rel(lien)} est un fichier ordinaire (une copie ?), pas un lien",
                      "Supprimez-le, puis créez un lien symbolique avec ln.")
        return absent(lien)
    destination = os.readlink(lien)
    if not lien.exists():
        return KO(f"Lien cassé : {rel(lien)} → {destination}, qui n'existe pas",
                  "Un chemin relatif enregistré dans un lien se lit depuis le dossier du LIEN "
                  "(workspace/data/), pas depuis votre répertoire courant. Supprimez le lien et recréez-le "
                  "avec un chemin valable depuis workspace/data/, ou avec un chemin absolu.")
    if lien.resolve() != cible.resolve():
        return KO(f"{rel(lien)} pointe vers {rel(lien.resolve())} au lieu de data/fruits.txt")
    note = ("Chemin absolu : le lien cassera si le dossier du TP est déplacé ou renommé."
            if destination.startswith("/") else
            "Chemin relatif : le lien restera valable si tout le dossier du TP est déplacé.")
    return OK(f"{rel(lien)} → {destination}", note)


def e8_chmod():
    f = WD / "fruits_uniques.txt"
    if not f.is_file():
        return KO(f"{rel(f)} introuvable", "Ce fichier est créé à l'étape 6.")
    if f.stat().st_mode & 0o777 == 0o640:
        return OK(f"{rel(f)} : {droits(f)}")
    return KO(f"{rel(f)} : {droits(f)} au lieu de 640 (rw-r-----)",
              "Chaque chiffre additionne r=4, w=2, x=1 : le 1er pour vous, le 2e pour le groupe, le 3e pour les autres.")


def e8_script():
    f = WS / "salut.sh"
    if f.is_symlink():
        return KO(f"{rel(f)} est un lien", "Copiez le fichier pour avoir votre propre exemplaire.")
    if not f.is_file():
        return KO(f"{rel(f)} introuvable", "Copiez data/salut.sh dans workspace/.")
    if not identiques(f, DATA / "salut.sh"):
        return KO(f"{rel(f)} diffère de data/salut.sh", "Copiez le fichier au lieu de le réécrire.")
    mode = f.stat().st_mode & 0o777
    if mode == 0o755:
        return OK(f"{rel(f)} : {droits(f)}, exécutable",
                  "Pour le lancer, précisez son chemin (./salut.sh depuis workspace/) : le shell ne cherche "
                  "pas les commandes dans le répertoire courant.")
    if mode & 0o002:
        return KO(f"{rel(f)} : {droits(f)}, tout le monde peut MODIFIER votre script",
                  "Le w pour « les autres » est dangereux : n'importe qui pourrait y ajouter des commandes "
                  "que vous exécuteriez ensuite. 755 attendu.")
    if not mode & 0o100:
        return KO(f"{rel(f)} : {droits(f)}, pas exécutable",
                  "Sans le droit x, le shell répond « Permission non accordée ». 755 = rwx pour vous, "
                  "r-x pour le groupe et les autres.")
    return KO(f"{rel(f)} : {droits(f)} au lieu de 755 (rwxr-xr-x)", "7 = 4+2+1 (rwx), 5 = 4+1 (r-x).")

# ---------------------------------------------------------------- étape 9 : variables et alias


def e9_myvar():
    valeur = os.environ.get("MYVAR")
    if valeur:
        return OK(f"MYVAR = « {valeur} », reçue de votre shell",
                  "Ce script est un processus ENFANT de votre shell : il ne reçoit que les variables exportées.")
    if valeur == "":
        return KO("MYVAR est exportée mais vide", "Donnez-lui une valeur.")
    return KO("MYVAR n'est pas visible par ce script",
              "Ce script est lancé par votre shell : il ne reçoit que les variables EXPORTÉES. Une variable "
              "créée par MYVAR=valeur, sans export, reste locale au shell.",
              "Lancez le script depuis le terminal où MYVAR a été définie : chaque terminal a son propre shell.")


def e9_alias():
    f = PREUVES / "alias.txt"
    texte = lire(f)
    if texte is None:
        return absent(f, "Sans argument, la commande alias affiche vos alias : redirigez sa sortie vers ce fichier.")
    m = re.search(r"^\s*(?:alias\s+)?verif=(.*)$", texte, re.M)
    if not m:
        return KO(f"L'alias verif n'apparaît pas dans {rel(f)}",
                  "Un alias n'existe que dans le shell où il a été défini : créez-le dans le terminal "
                  "où vous lancez ensuite la commande alias.")
    valeur = m.group(1).strip().strip("'\"")
    if "verify.py" not in valeur:
        return KO(f"verif vaut « {valeur} »", "L'alias doit lancer python3 verify.py --step.")
    note = None
    if re.search(r"^\s*alias\s+verif=", lire(Path.home() / ".bashrc") or "", re.M):
        note = "Bonus : l'alias est dans ~/.bashrc, il existera dans chaque nouveau terminal."
    return OK(f"Alias verif = « {valeur} »", note)

# ---------------------------------------------------------------- étape 10 : processus


SHELLS = {"bash", "sh", "dash", "zsh", "fish", "ksh"}


def e10_shell():
    def valider(r):
        if not r.isdigit():
            return False, "Un PID est un nombre entier."
        info = processus(int(r))
        if info is None:
            return False, f"Aucun processus n'a le PID {r} en ce moment."
        nom, uid = info
        if nom not in SHELLS:
            return False, f"Le processus {r} est « {nom} », pas un shell."
        if uid != os.getuid():
            return False, "Ce shell appartient à un autre utilisateur."
        if int(r) != os.getppid():
            return True, "C'est un de vos shells, mais pas celui qui a lancé ce script (plusieurs terminaux ouverts ?)."
        return True, None
    return question("10.shell", "PID du shell de ce terminal",
                    "Avec ps, trouvez le PID du shell (bash) de ce terminal. Quel est-il ?",
                    valider, "Sans option, ps affiche les processus du terminal courant : repérez la ligne "
                    "bash, colonne PID.")


def e10_sleep():
    f = PREUVES / "sleep.pid"
    contenu = lignes(f)
    if contenu is None:
        return absent(f, "Après avoir lancé sleep 1000 &, redirigez vers ce fichier la sortie de pgrep "
                      "(limitée à vos processus), AVANT de terminer le processus.")
    pids = []
    for l in contenu:
        m = re.match(r"\s*(?:\[\d+\][+-]?\s+)?(\d+)\b", l)
        if m:
            pids.append(int(m.group(1)))
    if not pids:
        return KO(f"{rel(f)} ne contient aucun PID", "pgrep affiche un PID par ligne.")
    actifs = [p for p in pids if processus(p) == ("sleep", os.getuid())]
    if actifs:
        return KO(f"Le processus sleep {actifs[0]} tourne toujours",
                  "Terminez-le en lui envoyant un signal : par son PID (kill) ou par son nom (pkill).")
    notes = []
    etrangers = [p for p in pids if (processus(p) or ("", os.getuid()))[1] != os.getuid()]
    if etrangers:
        notes.append(f"PID {', '.join(map(str, etrangers))} : processus d'un autre utilisateur. "
                     "Limitez pgrep à vos processus (-u).")
    autres = sleeps_actifs()
    if autres:
        notes.append(f"D'autres processus sleep tournent encore (PID {', '.join(autres)}).")
    return OK(f"Processus sleep {', '.join(map(str, pids))} enregistré puis terminé", *notes)


def e10_df():
    f = PREUVES / "disque.txt"
    texte = lire(f)
    if texte is None:
        return absent(f, "Redirigez la sortie de df vers ce fichier.")
    if "%" not in texte:
        return KO(f"{rel(f)} ne ressemble pas à une sortie de df",
                  "df affiche une ligne par système de fichiers, avec le pourcentage utilisé.")
    sans_entete = "\n".join(texte.splitlines()[1:])   # l'en-tête « blocs de 1K » ne compte pas
    if re.search(r"\s\d+(?:[.,]\d+)?[KMGTP]\s", sans_entete):
        return OK(f"{rel(f)} : espace disque en format lisible (K, M, G…)")
    return KO(f"{rel(f)} : tailles en blocs de 1 Ko, difficiles à lire",
              "Cherchez dans l'extrait de man df l'option « human-readable ».")

# ---------------------------------------------------------------- déroulement


ETAPES = [
    (1, "Trouver de l'aide, historique, horloge", [e1_man, e1_date, e1_apropos, e1_historique]),
    (2, "Se repérer dans l'arborescence", [e2_pwd, e2_secret, e2_taille, e2_relatif]),
    (3, "Créer dossiers et fichiers", [e3_dossiers, e3_arborescence, e3_todo, e3_cache, e3_bonjour]),
    (4, "Copier, déplacer, renommer, supprimer", [e4_copie, e4_renommer, e4_deplacer, e4_rmdir, e4_rm]),
    (5, "Rechercher des fichiers et du texte", [e5_find, e5_grep, e5_which]),
    (6, "Filtres et redirections (pipes)", [e6_extrait, e6_uniques, e6_wc, e6_upper, e6_cut, e6_info]),
    (7, "Archiver et compresser", [e7_archive, e7_liste, e7_extraction]),
    (8, "Liens symboliques et permissions", [e8_lien, e8_chmod, e8_script]),
    (9, "Variables d'environnement et alias", [e9_myvar, e9_alias]),
    (10, "Processus et ressources", [e10_shell, e10_sleep, e10_df]),
]


def evaluer(tache):
    try:
        return tache()
    except Exception as e:  # un étudiant ne doit jamais voir une trace Python
        return KO(f"Vérification impossible ({type(e).__name__} : {e})", "Signalez ce message à l'enseignant.")


def verifier_installation():
    """Arrête si setup.sh n'a pas été lancé ; signale les données sources modifiées par erreur."""
    if not (DATA / "fruits.txt").is_file() or not PREUVES.is_dir():
        print(ROUGE("✘ L'environnement du TP n'est pas prêt.") + " Lancez d'abord :  bash setup.sh")
        sys.exit(1)
    alteres = []
    for empreinte, nom in lire_empreintes():
        p = DATA / nom
        if not p.is_file():
            alteres.append(f"data/{nom} (supprimé)")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != empreinte:
            alteres.append(f"data/{nom} (modifié)")
    if alteres:
        imprimer(JAUNE("⚠ "), "Données sources altérées : " + ", ".join(alteres), 2)
        imprimer("  ", "Les exercices lisent data/ sans jamais le modifier. Relancez bash setup.sh pour "
                 "le restaurer : votre travail dans workspace/ est conservé.", 2)


def verifier_etape(num, suggerer_suite=True):
    _, titre, taches = ETAPES[num - 1]
    print(GRAS(f"\nÉtape {num} — {titre}"))
    reussies = 0
    for tache in taches:
        r = evaluer(tache)
        afficher(r)
        reussies += r.ok
    if reussies == len(taches):
        suite = f" Étape suivante : {num + 1}." if suggerer_suite and num < len(ETAPES) else ""
        print(VERT(f"  → Étape {num} validée ({reussies}/{len(taches)}).") + suite)
        return True
    print(JAUNE(f"  → {reussies}/{len(taches)} : corrigez les points ✘ puis relancez "
                f"python3 verify.py {num}"))
    return False


def tableau():
    print(GRAS("\nTP « Commandes de base Linux » — progression"))
    prochaine, faites, total = None, 0, 0
    for num, titre, taches in ETAPES:
        n = sum(evaluer(t).ok for t in taches)
        faites, total = faites + n, total + len(taches)
        symbole = VERT("✔") if n == len(taches) else JAUNE("◐") if n else GRIS("·")
        print(f"  {symbole} {num:>2}  {titre:<40} {n}/{len(taches)}")
        if n < len(taches) and prochaine is None:
            prochaine = num
    print(f"\n  {faites}/{total} tâches réussies.")
    if prochaine is None:
        print(VERT("  Toutes les étapes sont validées. Bravo !"))
        return True
    print(f"  Prochaine étape : {prochaine}  →  python3 verify.py {prochaine}")
    return False


def main():
    global INTERACTIF, REPONSES
    ap = argparse.ArgumentParser(
        description="Vérification du TP « Commandes de base Linux ».",
        epilog="Sans argument : tableau de progression de toutes les étapes.")
    ap.add_argument("etape", nargs="?", type=int, help=f"numéro de l'étape à vérifier en détail (1 à {len(ETAPES)})")
    ap.add_argument("--step", type=int, metavar="N", help="identique à ETAPE")
    ap.add_argument("--all", action="store_true", help="vérifier toutes les étapes en détail")
    args = ap.parse_args()
    etape = args.etape if args.etape is not None else args.step
    if etape is not None and not 1 <= etape <= len(ETAPES):
        ap.error(f"étape inconnue : {etape} (1 à {len(ETAPES)})")

    verifier_installation()
    REPONSES = charger_reponses()
    INTERACTIF = etape is not None or args.all
    if args.all:
        for num, _, _ in ETAPES:
            verifier_etape(num, suggerer_suite=False)
        ok = tableau()
    elif etape is not None:
        ok = verifier_etape(etape)
    else:
        ok = tableau()
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu.")
        sys.exit(1)
