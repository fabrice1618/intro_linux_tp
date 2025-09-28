#!/usr/bin/env python3
import os, sys, argparse, re, shutil, subprocess, random
from pathlib import Path

BASE = Path.cwd().resolve()

GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"; CYAN = "\033[96m"; RESET = "\033[0m"

def ok(msg): print(f"{GREEN}✔ {msg}{RESET}")
def ko(msg): print(f"{RED}✘ {msg}{RESET}")
def info(msg): print(f"{CYAN}i {msg}{RESET}")

def run(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def file_has_lines(p, min_lines=1):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f) >= min_lines
    except Exception:
        return False

# Banque de QCM: {step: [(question, ["A)","B)","C)","D)"], "B"] }
QCM = {
  1: [("Quelle variable pointe sur le répertoire courant affiché par la commande qui l'imprime ?", ["A) $HOME","B) $PWD","C) $USER","D) $PATH"], "B"),
      ("Quelle option liste aussi les fichiers cachés ?", ["A) -l","B) -h","C) -a","D) -t"], "C"),
      ("Un chemin commençant par / est…", ["A) relatif","B) absolu","C) invalide","D) un lien"], "B"),
      ("Compter des lignes via un pipe se fait avec…", ["A) wc","B) man","C) less","D) help"], "A"),
      ("Afficher l’utilisateur courant :", ["A) id -g","B) whoami","C) users","D) groups"], "B")],
  2: [("Quel préfixe rend un nom de fichier caché ?", ["A) .","B) _","C) ~","D) -"], "A"),
      ("> écrase, >> …", ["A) ajoute","B) supprime","C) copie","D) renomme"], "A"),
      ("Créer un fichier vide :", ["A) touch","B) cat","C) echo","D) less"], "A"),
      ("-p lors de la création de dossiers :", ["A) parents","B) permissions","C) portable","D) parallèle"], "A"),
      ("Numéroter les lignes :", ["A) nl","B) cat","C) head","D) more"], "A")],
  3: [("Copie récursive :", ["A) -a","B) -R","C) -p","D) -v"], "B"),
      ("Renommer/déplacer :", ["A) rename","B) mv","C) cp","D) ln"], "B"),
      ("Supprimer un dossier vide :", ["A) rm -r","B) rmdir","C) del","D) unlink"], "B"),
      ("Mode verbeux :", ["A) -v","B) -q","C) -x","D) -t"], "A"),
      ("Horodatage conservé par défaut avec cp ?", ["A) oui","B) non","C) aléatoire","D) immuable"], "B")],
  4: [("Ignorer la casse dans la recherche texte :", ["A) -n","B) -i","C) -v","D) -w"], "B"),
      ("Afficher numéros de lignes :", ["A) -n","B) -c","C) -H","D) -r"], "A"),
      ("Trouver un binaire dans le PATH :", ["A) where","B) which","C) locate","D) type"], "B"),
      ("Identifier builtin/alias/fichier :", ["A) file","B) type","C) which","D) whatis"], "B"),
      ("Parcourir la hiérarchie et filtrer par nom :", ["A) find -name","B) ls -R","C) grep -r","D) locate -p"], "A")],
  5: [("Supprimer doublons consécutifs :", ["A) uniq","B) sort","C) cut","D) tr"], "A"),
      ("Délimiteur de colonnes dans cut :", ["A) -d","B) -f","C) -c","D) -s"], "A"),
      ("Compter les mots :", ["A) wc -w","B) wc -l","C) awk -c","D) sed -n"], "A"),
      ("Convertir la casse :", ["A) sed","B) awk","C) tr","D) paste"], "C"),
      ("Le symbole | est :", ["A) redirection fichier", "B) pipe", "C) OU logique", "D) substitution"], "B")],
  6: [("Créer une archive tar :", ["A) -x","B) -t","C) -c","D) -z"], "C"),
      ("Compression gzip avec tar :", ["A) -g","B) -z","C) -Z","D) -j"], "B"),
      ("Lister contenu d'une archive :", ["A) -t","B) -x","C) -c","D) -v"], "A"),
      ("Option -C sert à :", ["A) racine","B) courant","C) chemin indiqué","D) $HOME"], "C"),
      ("Une tar.gz est :", ["A) un seul fichier","B) plusieurs fichiers","C) un lien","D) un device"], "A")],
  7: [("Créer un lien symbolique :", ["A) -h","B) -s","C) -L","D) -P"], "B"),
      ("Mode 640 équivaut à :", ["A) rw-r---x","B) rw-r-----","C) r-wxr--","D) rwxr--r--"], "B"),
      ("Les permissions s'appliquent à :", ["A) user","B) user,groupe,autres","C) groupe","D) root"], "B"),
      ("Un lien symbolique pointe vers :", ["A) inode","B) chemin","C) device","D) socket"], "B"),
      ("Afficher permissions :", ["A) ls -l","B) stat -p","C) getfacl","D) toutes"], "D")],
  8: [("Exporter une variable :", ["A) env","B) export","C) set","D) declare sans -x"], "B"),
      ("Un alias est :", ["A) binaire","B) fonction","C) remplacement de texte","D) variable"], "C"),
      ("Aliases persistants :", ["A) /etc/shadow","B) ~/.bashrc","C) ~/.profile sans source","D) /usr/bin"], "B"),
      ("Lister les variables d'environnement :", ["A) env","B) set","C) export -p","D) printenv"], "A"),
      ("Variable non exportée est visible :", ["A) partout","B) sous-processus","C) shell courant","D) cron"], "C")],
  9: [("Lister processus utilisateur :", ["A) ps -u $(whoami)","B) top","C) jobs -l","D) pstree"], "A"),
      ("Trouver PID par nom :", ["A) pidof","B) pgrep","C) psfind","D) pkill -p"], "B"),
      ("Terminer par nom :", ["A) killall","B) pkill","C) kill -9","D) pstop"], "B"),
      ("df -h affiche :", ["A) RAM","B) réseaux","C) disques","D) CPU"], "C"),
      ("& après une commande :", ["A) relance","B) arrière-plan","C) tue","D) ignore"], "B")],
 10: [("Rechercher dans man :", ["A) ?mot","B) /mot","C) :mot","D) @mot"], "B"),
      ("Afficher l'historique :", ["A) history","B) bash --history","C) hist","D) fc -l uniquement"], "A"),
      ("Option usuelle d'aide courte :", ["A) -a","B) -h","C) -v","D) -q"], "B"),
      ("Variable de langue des pages man :", ["A) LANG","B) PATH","C) LC_ALL/LANG","D) PWD"], "C"),
      ("Commande date/heure universelle :", ["A) clock","B) hwclock","C) date","D) time"], "C")]
}

def ask_quiz(step, given_answer=None):
    qs = QCM.get(step, [])
    if not qs:
        return True
    q, options, correct = random.choice(qs)
    print(f"\n{YELLOW}QCM Étape {step}:{RESET} {q}")
    print("   " + "  ".join(options))
    if given_answer:
        ans = given_answer.strip().upper()
        print(f"Votre réponse: {ans}")
    else:
        try:
            ans = input("Votre réponse (A/B/C/D) > ").strip().upper()
        except EOFError:
            ans = ""
    if ans == correct:
        ok("Bonne réponse")
        return True
    else:
        ko(f"Mauvaise réponse (attendu: {correct})")
        return False

def step1():
    passed = True
    if BASE.exists():
        ok("Répertoire du TP présent")
    else:
        ko(f"{BASE} introuvable"); passed = False
    # existence basique d'outils
    for cmd in ["pwd","ls","wc","whoami","uname"]:
        if shutil.which(cmd): pass
        else:
            ko(f"Commande requise absente: {cmd}"); passed = False
    return passed

def step2():
    passed = True
    ws = BASE / "workspace"
    for d in ["docs","data","tmp"]:
        if (ws/d).is_dir(): ok(f"Dossier présent: {d}")
        else: ko(f"Dossier manquant: {d}"); passed = False
    if (ws / "data" / "todo.txt").exists(): ok("todo.txt créé")
    else: ko("todo.txt absent"); passed = False
    if (ws / "tmp" / ".cache").exists(): ok("fichier caché .cache créé")
    else: ko(".cache absent"); passed = False
    bj = ws / "docs" / "bonjour.txt"
    if bj.exists() and file_has_lines(bj, 2): ok("bonjour.txt a ≥2 lignes")
    else: ko("bonjour.txt absent/incomplet"); passed = False
    return passed

def step3():
    passed = True
    ws = BASE / "workspace"
    if (ws / "backup_data").is_dir(): ok("Copie récursive data -> workspace/backup_data OK")
    else: ko("workspace/backup_data absent"); passed = False
    if (ws / "bonjour.renomme.txt").exists(): ok("Renommage + déplacement OK")
    else: ko("workspace/bonjour.renomme.txt introuvable"); passed = False
    if not (ws / "docs" / "bonjour.txt").exists(): ok("Suppression de docs/bonjour.txt OK")
    else: ko("docs/bonjour.txt existe encore"); passed = False
    return passed

def step4():
    passed = True
    out = run(f'find "{BASE}/workspace" -iname "*fruits*"').stdout.strip()
    if out: ok("Recherche de *fruits* trouvée sous workspace")
    else: ko("find n'a rien trouvé"); passed = False
    out2 = run(f'grep -n "pomme" "{BASE}/data/fruits.txt"').stdout
    if out2: ok('grep a trouvé "pomme" dans data/fruits.txt')
    else: ko('grep n\'a pas trouvé "pomme"'); passed = False
    if shutil.which("python3"):
        ok("python3 présent dans le PATH (which/type utilisables)")
    else:
        ko("python3 absent du PATH"); passed = False
    return passed

def step5():
    passed = True
    ws = BASE / "workspace" / "data"
    targets = {
        "fruits_uniques.txt": None,
        "lorem_wc.txt": r"\b\d+\b",
        "fruits_upper.txt": None,
        "col2.txt": None
    }
    for fname, pattern in targets.items():
        p = ws / fname
        if not p.exists():
            ko(f"{fname} manquant"); passed = False
        else:
            ok(f"{fname} généré")
            if pattern and not re.search(pattern, p.read_text()):
                ko(f"{fname} ne contient pas le motif attendu"); passed = False
    return passed

def step6():
    passed = True
    arch = BASE / "workspace" / "data_archive.tgz"
    extr = BASE / "workspace" / "tmp" / "data" / "fruits.txt"
    if arch.exists(): ok("Archive tar.gz créée")
    else: ko("Archive absente"); passed = False
    if extr.exists(): ok("Archive extraite dans workspace/tmp")
    else: ko("Extraction non détectée"); passed = False
    return passed

def step7():
    passed = True
    link = BASE / "workspace" / "data" / "link_fruits.txt"
    target = BASE / "data" / "fruits.txt"
    if link.is_symlink() and link.resolve() == target: ok("Lien symbolique OK")
    else: ko("Lien symbolique manquant ou incorrect"); passed = False
    fu = BASE / "workspace" / "data" / "fruits_uniques.txt"
    try:
        mode = fu.stat().st_mode & 0o777
        if mode == 0o640: ok("Permissions 640 sur fruits_uniques.txt")
        else: ko(f"Permissions attendues 640, trouvées {oct(mode)}"); passed = False
    except FileNotFoundError:
        ko("fruits_uniques.txt introuvable"); passed = False
    return passed

def step8():
    passed = True
    # Meilleure-effort: l'environnement du script n'hérite pas de votre shell interactif
    if os.environ.get("MYVAR"):
        ok("MYVAR exportée dans cet environnement")
    else:
        info("MYVAR non détectée ici (définie dans votre shell ? c'est attendu).")
    info("Les alias ne sont pas visibles depuis ce script (shell séparé).")
    return True

def step9():
    passed = True
    if run("ps -u $(whoami)").returncode == 0: ok("ps fonctionne")
    else: ko("ps a échoué"); passed = False
    if run("df -h").returncode == 0: ok("df fonctionne")
    else: ko("df a échoué"); passed = False
    # Conseillé: ne laissez pas de 'sleep' traîner
    sleeps = run("pgrep sleep").stdout.strip()
    if sleeps:
        info(f"'sleep' encore présent (pid: {sleeps}). Ce n'est pas bloquant.")
    else:
        ok("Aucun 'sleep' résiduel")
    return passed

def step10():
    passed = True
    if shutil.which("man"): ok("man disponible")
    else: ko("man indisponible"); passed = False
    if shutil.which("date"): ok("date disponible")
    else: ko("date indisponible"); passed = False
    return passed

STEPS = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5, 6: step6, 7: step7, 8: step8, 9: step9, 10: step10}

def main():
    ap = argparse.ArgumentParser(description="Vérification TP Linux (états + QCM)")
    ap.add_argument("--step", type=int, help="Numéro d'étape à vérifier (1-10)")
    ap.add_argument("--all", action="store_true", help="Tout vérifier (1→10)")
    ap.add_argument("--quiz", action="store_true", help="Poser une question QCM même si non nécessaire")
    ap.add_argument("--no-quiz", action="store_true", help="Ne pas poser de question QCM")
    ap.add_argument("--answer", type=str, help="Réponse QCM automatique (A/B/C/D)")
    args = ap.parse_args()

    if not BASE.exists():
        ko(f"{BASE} introuvable"); sys.exit(1)

    def verify_one(i):
        print(f"\n=== Étape {i} ===")
        passed = STEPS[i]()
        # Politique QCM: poser si --quiz, ou toujours (sauf --no-quiz) pour renforcer l'apprentissage
        ask = args.quiz or not args.no_quiz
        if ask:
            qok = ask_quiz(i, given_answer=args.answer)
            passed = passed and qok
        print("Résultat:", "✅ OK" if passed else "❌ À corriger")
        return passed

    if args.all:
        overall = True
        for i in range(1, 11):
            overall = verify_one(i) and overall
        print("\nRésumé:", "✅ Tout est validé" if overall else "⚠️ Des étapes sont à corriger")
        sys.exit(0 if overall else 2)

    if args.step:
        i = args.step
        if i not in STEPS:
            ko("Étape inconnue"); sys.exit(1)
        ok("Début de la vérification")
        res = verify_one(i)
        sys.exit(0 if res else 2)

    ap.print_help()

if __name__ == "__main__":
    main()