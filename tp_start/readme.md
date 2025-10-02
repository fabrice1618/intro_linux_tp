### TP “Commandes de base Linux” — parcours progressif, guidé, et vérifié automatiquement

— Contexte: vous démarrez sous Linux et vous souhaitez "apprendre en faisant". Ce TP vous guide pas à pas pour manipuler le système de fichiers, rechercher, filtrer, archiver, gérer des liens, variables, et observer les processus.
— Contraintes: pas de sudo; tout se fait dans votre dossier personnel ($HOME, supposé être /home/user).
— Vérification: un script Python vérifie à chaque étape l'état final (résultat concret).
— Philosophie: l'énoncé ne donne pas forcément la commande exacte. Vous trouverez la commande via le manuel (man) et les indices fournis.

Divisez l’écran: à gauche votre terminal, à droite l’énoncé. Avancez calmement, lisez les intros, cherchez les commandes dans man, exécutez, puis validez avec le script.

---

### Installation locale 

1) Cloner le TP

```bash
git clone https://github.com/fabrice1618/intro_linux_tp.git
cd intro_linux_tp/tp_start
```

2) Initialiser les fichiers de départ
- Exécutez: bash setup.sh
- Puis test rapide: python3 verify.py --step 1

3) Vérifier une étape
- Exemple: python3 verify.py --step 3
- Mode tout-en-un: python3 verify.py --all

Astuce man: utilisez man <commande>, /mot pour chercher dans la page, n pour “suivant”, q pour quitter.

---

## Parcours progressif

Chaque étape inclut: introduction (concept), tâche à réaliser (objectif observable), indices (comment trouver les commandes dans man), et validation (commande de vérification).

---

#### Étape 1 — Se repérer dans l’arborescence
- Concept: le “répertoire courant” est l’endroit où vous travaillez. Savoir où l’on est et lister ce qui s’y trouve est la base de toute manipulation.
- À réaliser (résultat attendu):
  1) Savoir afficher le chemin absolu du répertoire courant (juste le faire une fois pour vous).
  2) Savoir lister les entrées, y compris cachées, et un listing détaillé (juste le faire pour vous).
- Indices:
  - Cherchez dans man (section 1): “print name of current working directory”.
  - Cherchez la commande de listage dont les options incluent “-a” (inclure fichiers cachés) et “-l”.
- Validation: python3 verify.py --step 1

Questions (théorie/pratique):
1) Quelle variable contient le chemin du dossier personnel courant ? (A) $HOME (B) $PWD (C) $USER (D) $PATH  
2) Quelle option de la commande de listage affiche les fichiers cachés ? (A) -l (B) -h (C) -a (D) -t  
3) Un chemin qui commence par “/” est… (A) relatif (B) absolu (C) invalide (D) un lien  
4) Comment compter le nombre d’entrées listées sans ouvrir un éditeur ? (A) via wc (B) via man (C) via less (D) via help  
5) Quelle commande affiche l’utilisateur courant ? (A) id -g (B) whoami (C) users (D) groups

---

#### Étape 2 — Créer dossiers et fichiers
- Concept: créer une arborescence de travail, initialiser des fichiers, écrire et ajouter du contenu.
- À réaliser (résultat attendu):
  1) Créer un fichier vide dans workspace/data et un fichier “caché” (nom commençant par “.”) dans workspace/tmp.  
  2) Créer workspace/docs/bonjour.txt avec 2 lignes de texte.
- Indices:
  - man: “make directories”, “create empty files or update times”, “write arguments to the standard output” (utilisable avec redirection > et >>).
  - Astuce: pour numéroter/visualiser les lignes, cherchez la commande qui “number lines”.
- Validation: python3 verify.py --step 2

Questions:
1) Quel caractère au début du nom rend un fichier “caché” ? (A) . (B) _ (C) ~ (D) -  
2) Quelle redirection écrase le fichier cible ? (A) >> (B) > (C) < (D) |  
3) Quelle commande peut créer un fichier vide ? (A) touch (B) cat (C) echo (D) less  
4) Que signifie l’option -p lors de la création d’un dossier ? (A) parallèle (B) permissions (C) parents (D) portable  
5) Quelle commande affiche le contenu d’un fichier sans pager ? (A) cat (B) less (C) head (D) nl

---

#### Étape 3 — Copier, déplacer, renommer, supprimer
- Concept: “copier” duplique, “déplacer/renommer” change l’emplacement/nom, “supprimer” efface.
- À réaliser (résultat attendu):
  1) Copier récursivement le dossier data vers workspace/backup_data.  
  2) Renommer la copie de bonjour en bonjour.renomme.txt et la déplacer à la racine de workspace.  
  3) Supprimer workspace/docs/bonjour.txt et supprimer un dossier vide via la commande dédiée aux dossiers vides.
- Indices:
  - man: “copy files and directories” (option pour récursif), “move/rename files”, “remove files or directories”, “remove empty directories”.
- Validation: python3 verify.py --step 3

Questions:
1) Quelle option rend la copie “récursive” ? (A) -a (B) -R (C) -p (D) -v  
2) Renommer un fichier utilise la commande… (A) rename (B) mv (C) cp (D) ln  
3) Pour supprimer un dossier non vide on utilise… (A) rm -r (B) rmdir (C) del (D) unlink  
4) Quel drapeau affiche les opérations effectuées (mode verbeux) ? (A) -v (B) -q (C) -x (D) -t  
5) Que devient l’horodatage lors d’une copie par défaut ? (A) conservé (B) perdu (C) aléatoire (D) inchangé et immuable

---

#### Étape 4 — Rechercher des fichiers et du texte
- Concept: rechercher des fichiers par nom, motif, casse; chercher du texte dans des fichiers.
- À réaliser (résultat attendu):
  1) Sous workspace, trouver tout fichier dont le nom contient “fruits” (insensible à la casse).  
  2) Dans data/fruits.txt, trouver les lignes contenant “pomme” avec numéros de lignes.  
  3) Savoir localiser un exécutable dans le PATH (ex.: l’interpréteur Python).
- Indices:
  - man: commande qui “search for files in a directory hierarchy”; commande qui “print lines matching a pattern”; “show full path of shell commands” et builtin pour connaître la nature d’un nom de commande.
- Validation: python3 verify.py --step 4

Questions:
1) Quelle option rend la recherche insensible à la casse pour la recherche texte ? (A) -n (B) -i (C) -v (D) -w  
2) Quelle option affiche le numéro de ligne ? (A) -n (B) -c (C) -H (D) -r  
3) Quelle commande trouve un binaire dans le PATH ? (A) where (B) which (C) locate (D) type  
4) Quel utilitaire indique si un nom est builtin, alias ou fichier ? (A) file (B) type (C) which (D) whatis  
5) Quelle action liste la hiérarchie et filtre par motif de nom ? (A) find -name (B) ls -R (C) grep -r (D) locate -p

---

#### Étape 5 — Filtres et redirections (pipes)
- Concept: combiner des commandes: entrée standard → filtre → sortie standard. Trier, dédupliquer, compter, transformer.
- À réaliser (résultat attendu):
  1) Extraire les 5 premières et 3 dernières lignes de data/lorem.txt (visualisation, pas forcément fichier).  
  2) Créer workspace/data/fruits_uniques.txt en triant data/fruits.txt puis en supprimant les doublons.  
  3) Créer workspace/data/lorem_wc.txt contenant le nombre de mots de lorem.txt.  
  4) Créer workspace/data/fruits_upper.txt contenant fruits.txt en MAJUSCULES.  
  5) Extraire la 2e colonne d’un CSV (séparateur “,”) vers workspace/data/col2.txt.
- Indices:
  - man: “output the first part of files”, “output the last part…”, “sort lines of text files”, “report or omit repeated lines”, “print newline, word, and byte counts”, “translate or delete characters”, “remove sections from each line of files”.
- Validation: python3 verify.py --step 5

Questions:
1) Quelle commande supprime les doublons consécutifs après tri ? (A) uniq (B) sort (C) cut (D) tr  
2) Quelle option de cut choisit le délimiteur ? (A) -d (B) -f (C) -c (D) -s  
3) Quel utilitaire compte les mots ? (A) wc -w (B) wc -l (C) awk -c (D) sed -n  
4) Quel transformateur convertit minuscules ↔ majuscules ? (A) sed (B) awk (C) tr (D) paste  
5) Le “|” signifie… (A) redirection de sortie vers fichier (B) pipe entre commandes (C) OU logique (D) substitution

---

#### Étape 6 — Archiver et compresser
- Concept: empaqueter plusieurs fichiers dans une archive, puis compresser; lister et extraire.
- À réaliser (résultat attendu):
  1) Créer une archive tar.gz du dossier data dans workspace/data_archive.tgz.  
  2) Lister le contenu de l’archive.  
  3) Extraire l’archive sous workspace/tmp.
- Indices:
  - man: utilitaire “tar” (voir options pour créer, compresser gzip, lister, extraire).
- Validation: python3 verify.py --step 6

Questions:
1) Quelle option de tar crée une archive ? (A) -x (B) -t (C) -c (D) -z  
2) Quel drapeau active gzip dans tar ? (A) -g (B) -z (C) -Z (D) -j  
3) Que fait -t avec tar ? (A) teste (B) liste (C) extrait (D) compresse  
4) Où extrait-on avec -C ? (A) vers / (B) vers répertoire courant (C) vers le chemin indiqué (D) vers $HOME  
5) Une archive tar.gz est… (A) un seul fichier (B) plusieurs fichiers (C) un lien (D) un device

---

#### Étape 7 — Liens symboliques et permissions
- Concept: un lien symbolique est un “raccourci” vers un autre fichier; les permissions contrôlent lecture/écriture/exécution pour user:groupe:autres.
- À réaliser (résultat attendu):
  1) Créer un lien symbolique workspace/data/link_fruits.txt pointant vers data/fruits.txt.  
  2) Régler les permissions de workspace/data/fruits_uniques.txt sur 640 (rw‑r-----).
- Indices:
  - man: “make links between files” (option pour symlink), “change file mode bits”.
  - Pour lire les permissions: listage détaillé; repérez rwx en trois triplets.
- Validation: python3 verify.py --step 7

Questions:
1) Quelle option crée un lien symbolique ? (A) -h (B) -s (C) -L (D) -P  
2) 640 signifie… (A) rw‑r‑‑‑x (B) rw‑r‑‑‑‑ (C) r‑wxr‑‑ (D) rwxr‑‑r‑‑  
3) Les permissions s’appliquent à… (A) user uniquement (B) user,groupe,autres (C) groupe uniquement (D) root uniquement  
4) Un lien symbolique pointe vers… (A) l’inode directement (B) un chemin (C) un device (D) un socket  
5) Quelle commande affiche les permissions lisiblement ? (A) ls -l (B) stat -p (C) getfacl (D) toutes

---

#### Étape 8 — Variables d’environnement et alias
- Concept: variables (clé → valeur) qui influencent les programmes; exportation au sous‑processus; alias pour abréger une commande (valables dans la session).
- À réaliser (résultat attendu):
  1) Définir puis exporter une variable MYVAR avec une courte valeur (session courante).  
  2) Créer un alias ll équivalent à un listage détaillé incluant les fichiers cachés; l’utiliser au moins une fois.
- Indices:
  - man bash (cherchez “Shell Variables”, “export”, “alias”).  
  - help export, help alias dans bash.
- Validation: python3 verify.py --step 8 (tolérant: les alias/variables sont propres au shell interactif; le script donne des conseils s’il ne les “voit” pas).

Questions:
1) Quelle commande exporte MYVAR ? (A) env MYVAR (B) export MYVAR (C) set MYVAR (D) declare -x sans export  
2) Un alias est… (A) un binaire (B) une fonction shell (C) un remplacement de texte du shell (D) une variable  
3) Où mettre des alias persistants ? (A) /etc/shadow (B) ~/.bashrc (C) ~/.profile sans sourcer (D) /usr/bin  
4) Quelle commande affiche toutes les variables d’environnement ? (A) env (B) set (C) export -p (D) printenv  
5) Une variable non exportée est visible… (A) partout (B) dans les sous‑processus (C) seulement dans le shell courant (D) dans cron

---

#### Étape 9 — Processus et ressources
- Concept: observer les processus de l’utilisateur, trouver/terminer un processus, lire l’espace disque.
- À réaliser (résultat attendu):
  1) Lister vos processus.  
  2) Lancer un processus court en arrière‑plan (ex.: sommeil), retrouver son PID, puis le terminer.  
  3) Afficher l’espace disque en format lisible.
- Indices:
  - man: “report a snapshot of current processes”, “look up or signal processes based on name”, “report file system disk space usage”.
- Validation: python3 verify.py --step 9

Questions:
1) Quelle commande liste les processus de l’utilisateur actuel ? (A) ps -u $(whoami) (B) top (C) jobs -l (D) pstree  
2) Quelle commande trouve un PID par nom ? (A) pidof (B) pgrep (C) psfind (D) pkill -p  
3) Quelle commande termine par nom ? (A) killall (B) pkill (C) kill -9 (D) pstop  
4) df -h affiche… (A) RAM (B) réseaux (C) disques (D) CPU  
5) Le “&” placé après une commande… (A) la relance (B) la met en arrière‑plan (C) la tue (D) l’ignore

---

#### Étape 10 — Trouver de l’aide, historique, horloge
- Concept: s’auto‑documenter efficacement: pages de manuel, aide intégrée, historique pour rejouer des commandes, date/calendrier.
- À réaliser (résultat attendu):
  1) Lire une page de manuel et y chercher un mot‑clé.  
  2) Afficher l’aide d’une commande avec --help.  
  3) Afficher quelques lignes d’historique.  
  4) Afficher la date et, si disponible, le calendrier.
- Indices:
  - man man (cherchez “SEARCHING”), “history” est un builtin Bash, date et cal sont des utilitaires usuels.
- Validation: python3 verify.py --step 10

Questions:
1) Dans man, quel raccourci cherche un mot ? (A) ?mot (B) /mot (C) :mot (D) @mot  
2) Quelle commande affiche l’historique Bash ? (A) history (B) bash --history (C) hist (D) fc -l uniquement  
3) L’option fréquente pour l’aide courte est… (A) -a (B) -h (C) -v (D) -q  
4) Quelle variable contrôle la langue des pages man ? (A) LANG (B) PATH (C) LC_ALL/LANG (D) PWD  
5) cal peut ne pas être installé; quelle commande marche partout pour l’heure/date ? (A) clock (B) hwclock (C) date (D) time

---

### Mode d’emploi rapide

- Préparer: bash setup.sh
- Travailler: lisez l'intro de l'étape, trouvez les commandes via man et les indices, réalisez l'objectif observable (résultat concret dans les fichiers).
- Vérifier: python3 verify.py --step N
- Consolider: python3 verify.py --all pour tout rejouer.

---

### Guide d'utilisation de man (pages de manuel)

Le système `man` (manual) est votre référence principale pour comprendre les commandes Linux. Chaque page de manuel suit une structure standardisée et offre des fonctions de navigation et de recherche puissantes.

#### Utilisation de base

```bash
man <commande>        # Ouvrir la page de manuel d'une commande
man man              # Afficher l'aide sur man lui-même
man -k <mot-clé>     # Chercher des commandes par mot-clé (apropos)
whatis <commande>    # Description courte d'une commande
```

#### Structure d'une page de manuel

Les pages man sont organisées en sections standardisées :

- **NAME** : Nom de la commande et brève description
- **SYNOPSIS** : Syntaxe d'utilisation (entre [] = optionnel, <> = obligatoire)
- **DESCRIPTION** : Description détaillée de la commande et de ses fonctionnalités
- **OPTIONS** : Liste et explication de toutes les options disponibles (-a, --verbose, etc.)
- **EXAMPLES** : Exemples d'utilisation concrets (pas toujours présent)
- **SEE ALSO** : Commandes et pages de manuel connexes
- **AUTHOR** : Auteur(s) de la commande
- **BUGS** : Bugs connus et limitations

#### Navigation dans man

Une fois dans une page de manuel (affichée via `less` par défaut) :

| Touche | Action |
|--------|--------|
| `Espace` ou `f` | Page suivante |
| `b` | Page précédente |
| `↓` ou `Entrée` | Ligne suivante |
| `↑` | Ligne précédente |
| `g` | Début du document |
| `G` | Fin du document |
| `h` | Afficher l'aide de navigation |
| `q` | Quitter man |

#### Fonctions de recherche

La recherche est l'outil le plus puissant dans man :

| Commande | Action |
|----------|--------|
| `/mot` | Chercher "mot" vers l'avant (en descendant) |
| `?mot` | Chercher "mot" vers l'arrière (en remontant) |
| `n` | Occurrence suivante de la recherche |
| `N` | Occurrence précédente de la recherche |

**Exemples pratiques** :
```bash
man ls          # Ouvrir la page de ls
/hidden         # Chercher le mot "hidden"
n               # Passer à l'occurrence suivante
q               # Quitter
```

#### Sections du manuel

Le manuel Linux est divisé en sections numérotées :

1. Commandes utilisateur (ls, cat, grep...)
2. Appels système (fork, exec...)
3. Fonctions de bibliothèque C (printf, malloc...)
4. Fichiers spéciaux et périphériques (/dev/...)
5. Formats de fichiers et conventions (/etc/passwd...)
6. Jeux et économiseurs d'écran
7. Divers (protocoles, systèmes de fichiers...)
8. Commandes d'administration système (mount, useradd...)

Pour accéder à une section spécifique :
```bash
man 1 printf    # printf en tant que commande shell
man 3 printf    # printf en tant que fonction C
```

#### Astuces pour ce TP

Lorsque les indices vous orientent vers man :
1. Ouvrez la page avec `man <commande>`
2. Utilisez `/` suivi du mot-clé suggéré dans l'indice
3. Parcourez les occurrences avec `n` jusqu'à trouver l'option pertinente
4. Lisez la section DESCRIPTION pour comprendre le contexte
5. Vérifiez les EXAMPLES si disponibles

**Exemple pour l'étape 1** :
- Indice : "print name of current working directory"
- `man -k directory | grep print` ou `man -k "print.*directory"`
- Trouvez `pwd` dans les résultats
- `man pwd` pour confirmer

Bon TP, et bonne exploration de la ligne de commande !