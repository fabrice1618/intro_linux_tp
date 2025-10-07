### TP "Commandes de base Linux" — parcours progressif, guidé, et vérifié automatiquement

**Présentation** :

- **Contexte** : vous démarrez sous Linux et vous souhaitez "apprendre en faisant". Ce TP vous guide pas à pas pour manipuler le système de fichiers, rechercher, filtrer, archiver, gérer des liens, variables, et observer les processus.
- **Contraintes** : pas de sudo; tout se fait dans votre dossier personnel ($HOME, supposé être /home/user).
- **Vérification** : un script Python vérifie à chaque étape l'état final (résultat concret).
- **Philosophie** : l'énoncé ne donne pas forcément la commande exacte. Vous trouverez la commande via le manuel (man) et les indices fournis.

Divisez l’écran: à gauche votre terminal, à droite l’énoncé. Avancez calmement, lisez les intros, cherchez les commandes dans man, exécutez, puis validez avec le script.

---

### Installation locale

**1) Cloner le TP**

```bash
git clone https://github.com/fabrice1618/intro_linux_tp.git
cd intro_linux_tp/tp_start
```

**2) Initialiser les fichiers de départ**

- Exécutez : `bash setup.sh`
- Puis test rapide : `python3 verify.py --step 1`

**3) Vérifier une étape**

- Exemple : `python3 verify.py --step 3`
- Mode tout-en-un : `python3 verify.py --all`

**Astuce man** : utilisez `man <commande>`, `/mot` pour chercher dans la page, `n` pour "suivant", `q` pour quitter.

---

## Parcours progressif

Chaque étape inclut: introduction (concept), tâche à réaliser (objectif observable), indices (comment trouver les commandes dans man), et validation (commande de vérification).

---

#### Étape 1 — Trouver de l'aide, historique, horloge

**Contexte et concepts** :
Un bon développeur Linux sait **s'auto-documenter** : trouver de l'aide rapidement, réutiliser des commandes précédentes, et utiliser les outils système.

Concepts clés :
- **Pages de manuel (man)** : documentation complète de toutes les commandes
  - Structure standard : NAME, SYNOPSIS, DESCRIPTION, OPTIONS, EXAMPLES...
  - Navigation : espace (page suivante), `/mot` (rechercher), `n` (occurrence suivante), `q` (quitter)
  - Sections : man 1 (commandes), man 3 (fonctions C), man 5 (formats de fichiers)...
- **Aide rapide (--help)** : résumé court, affiché directement dans le terminal
  - Plus rapide que man pour une référence rapide
  - Exemple : `ls --help` affiche les options de ls
- **Historique des commandes** : Bash garde en mémoire vos commandes précédentes
  - `history` : affiche l'historique complet
  - Flèche ↑/↓ : naviguer dans l'historique
  - `!n` : ré-exécuter la commande numéro n
  - `!!` : ré-exécuter la dernière commande
  - `!grep` : ré-exécuter la dernière commande commençant par "grep"
  - Ctrl+R : recherche interactive dans l'historique
- **Utilitaires système** :
  - `date` : affiche/configure date et heure

**À réaliser (résultat attendu)** :
  1) Ouvrir la page de manuel de `ls`, chercher le mot "starting", puis quitter
  2) Afficher l'aide rapide d'une commande avec `--help` (ex: `grep --help`)
  3) Afficher les 10 dernières commandes de votre historique
  4) Afficher la date et l'heure actuelles

**Indices** :
  - man man : lisez la section "SEARCHING" pour apprendre à chercher dans une page man
  - `history` est une commande intégrée (builtin) de Bash
  - Pour limiter l'historique : `history 10` ou `history | tail -10`
  - `date` fonctionne partout
  - **Commandes utilisées** : `man`, `--help`, `history`, `tail`, `date`

**Validation** : `python3 verify.py --step 1`

**Astuce** : Consultez la section "Guide d'utilisation de man" en fin de document pour plus de détails !

Questions:
1) Dans man, quel raccourci cherche un mot ? (A) ?mot (B) /mot (C) :mot (D) @mot
2) Quelle commande affiche l'historique Bash ? (A) history (B) bash --history (C) hist (D) fc -l uniquement
3) L'option fréquente pour l'aide courte est… (A) -a (B) -h (C) -v (D) -q
4) Quelle variable contrôle la langue des pages man ? (A) LANG (B) PATH (C) LC_ALL/LANG (D) PWD
5) Commande date/heure universelle : (A) clock (B) hwclock (C) date (D) time

---

#### Étape 2 — Se repérer dans l'arborescence

**Contexte et concepts** :
Sous Linux, tout est organisé en arborescence de fichiers et dossiers, à partir de la racine `/`. Lorsque vous travaillez dans un terminal, vous êtes toujours "quelque part" dans cette arborescence : c'est le **répertoire courant** (ou répertoire de travail).

Concepts clés :
- **Chemin absolu** : commence par `/` et décrit le chemin complet depuis la racine (ex: `/home/user/Documents`)
- **Chemin relatif** : décrit le chemin depuis le répertoire courant (ex: `Documents/projet`)
- **Variables d'environnement** : `$HOME` contient le chemin de votre dossier personnel, `$PWD` contient le répertoire courant
- **Fichiers cachés** : sous Linux, tout fichier dont le nom commence par `.` est considéré comme "caché" (ex: `.bashrc`)

**À réaliser (résultat attendu)** :
  1) Afficher le chemin absolu du répertoire courant (pour savoir où vous êtes)
  2) Lister toutes les entrées du répertoire courant, y compris les fichiers cachés
  3) Afficher un listing détaillé montrant les permissions, propriétaires, tailles et dates

**Indices** :
  - Cherchez dans man (section 1): "print name of current working directory"
  - Cherchez la commande de listage dont les options incluent "-a" (all, inclure fichiers cachés) et "-l" (long format)
  - Astuce : vous pouvez combiner plusieurs options, par exemple `-la` ou `-l -a`
  - **Commandes utilisées** : `pwd`, `ls`

**Validation** : `python3 verify.py --step 2`

Questions (théorie/pratique):
1) Quelle variable contient le chemin du dossier personnel courant ? (A) $HOME (B) $PWD (C) $USER (D) $PATH
2) Quelle option de la commande de listage affiche les fichiers cachés ? (A) -l (B) -h (C) -a (D) -t
3) Un chemin qui commence par "/" est… (A) relatif (B) absolu (C) invalide (D) un lien
4) Comment compter le nombre d'entrées listées sans ouvrir un éditeur ? (A) via wc (B) via man (C) via less (D) via help
5) Quelle commande affiche l'utilisateur courant ? (A) id -g (B) whoami (C) users (D) groups

---

#### Étape 3 — Créer dossiers et fichiers

**Contexte et concepts** :
Pour organiser votre travail, vous devez savoir créer des dossiers et des fichiers. Linux distingue plusieurs façons de créer et manipuler des fichiers texte.

Concepts clés :
- **Créer des dossiers** : utile pour organiser vos fichiers en arborescence
- **Option -p** : crée les dossiers parents manquants (ex: `docs/rapports/2024` crée les trois niveaux d'un coup)
- **Fichiers vides** : parfois on a besoin de créer un fichier sans contenu (pour le remplir plus tard)
- **Redirections** :
  - `>` : écrit dans un fichier (écrase le contenu existant)
  - `>>` : ajoute à la fin d'un fichier (sans écraser)
- **Fichiers cachés** : nommer un fichier `.cache` ou `.config` le rend invisible au listage normal

**À réaliser (résultat attendu)** :
  1) Créer un fichier vide nommé `todo.txt` dans `workspace/data`
  2) Créer un fichier caché nommé `.cache` dans `workspace/tmp`
  3) Créer le fichier `workspace/docs/bonjour.txt` contenant au moins 2 lignes de texte

**Indices** :
  - man: "make directories", "create empty files or update times", "write arguments to the standard output"
  - Les redirections `>` et `>>` permettent d'écrire la sortie d'une commande dans un fichier
  - Pour visualiser avec numéros de ligne : cherchez "number lines" dans man
  - Exemple d'utilisation : `echo "première ligne" > fichier.txt` puis `echo "deuxième ligne" >> fichier.txt`
  - **Commandes utilisées** : `touch`, `echo`

**Validation** : `python3 verify.py --step 3`

Questions:
1) Quel caractère au début du nom rend un fichier "caché" ? (A) . (B) _ (C) ~ (D) -
2) Quelle redirection écrase le fichier cible ? (A) >> (B) > (C) < (D) |
3) Quelle commande peut créer un fichier vide ? (A) touch (B) cat (C) echo (D) less
4) Que signifie l'option -p lors de la création d'un dossier ? (A) parallèle (B) permissions (C) parents (D) portable
5) Quelle commande affiche le contenu d'un fichier sans pager ? (A) cat (B) less (C) head (D) nl

---

#### Étape 4 — Copier, déplacer, renommer, supprimer

**Contexte et concepts** :
Une fois vos fichiers créés, vous devez pouvoir les réorganiser : faire des copies de sauvegarde, déplacer des fichiers entre dossiers, renommer, ou nettoyer ce qui ne sert plus.

Concepts clés :
- **Copier** : crée un duplicata du fichier/dossier source, l'original reste intact
  - Copie récursive (`-R` ou `-r`) : nécessaire pour copier un dossier avec tout son contenu
- **Déplacer/Renommer** : sous Linux, c'est la même opération ! Déplacer un fichier dans le même dossier = le renommer
- **Supprimer** :
  - Fichiers : avec la commande de suppression classique
  - Dossiers vides : commande spécifique dédiée aux répertoires vides
  - Dossiers non vides : nécessite l'option récursive (`-r`)
- **Mode verbeux** (`-v`) : affiche ce qui est fait, utile pour suivre les opérations

**À réaliser (résultat attendu)** :
  1) Copier le dossier `data` (avec tout son contenu) vers `workspace/backup_data`
  2) Dans `workspace/backup_data/`, renommer `bonjour.txt` en `bonjour.renomme.txt`, puis le déplacer à la racine de `workspace/`
  3) Supprimer le fichier original `workspace/docs/bonjour.txt`

**Indices** :
  - man: "copy files and directories" (cherchez l'option pour copie récursive)
  - man: "move/rename files" (une seule commande pour déplacer ET renommer)
  - man: "remove files or directories"
  - Attention : il n'y a pas de "corbeille" en ligne de commande, la suppression est définitive !
  - Note : vous pouvez aussi explorer "remove empty directories" pour supprimer des dossiers vides (optionnel)
  - **Commandes utilisées** : `cp`, `mv`, `rm`

**Validation** : `python3 verify.py --step 4`

Questions:
1) Quelle option rend la copie "récursive" ? (A) -a (B) -R (C) -p (D) -v
2) Renommer un fichier utilise la commande… (A) rename (B) mv (C) cp (D) ln
3) Pour supprimer un dossier non vide on utilise… (A) rm -r (B) rmdir (C) del (D) unlink
4) Quel drapeau affiche les opérations effectuées (mode verbeux) ? (A) -v (B) -q (C) -x (D) -t
5) Que devient l'horodatage lors d'une copie par défaut ? (A) conservé (B) perdu (C) aléatoire (D) inchangé et immuable

---

#### Étape 5 — Rechercher des fichiers et du texte

**Contexte et concepts** :
Dans un système avec des milliers de fichiers, savoir chercher efficacement est essentiel. Linux offre des outils puissants pour trouver des fichiers par leur nom et pour chercher du texte à l'intérieur des fichiers.

Concepts clés :
- **Recherche de fichiers** : parcourt l'arborescence pour trouver des fichiers selon des critères (nom, type, taille, date...)
  - Recherche insensible à la casse : ignore majuscules/minuscules (ex: "Fruits" = "fruits" = "FRUITS")
  - Jokers : `*` remplace n'importe quelle séquence de caractères
- **Recherche de texte** : analyse le contenu des fichiers ligne par ligne
  - Numéros de ligne : utile pour localiser précisément où se trouve le texte
  - Expressions régulières : motifs de recherche puissants (avancé)
- **Variable PATH** : liste des répertoires où le shell cherche les commandes exécutables
  - `which` : trouve le chemin complet d'un exécutable
  - `type` : indique si un nom est un alias, un builtin, ou un fichier exécutable

**À réaliser (résultat attendu)** :
  1) Rechercher sous `data/` tous les fichiers dont le nom contient "fruits" (sans tenir compte de la casse)
  2) Dans le fichier `data/fruits.txt`, afficher les lignes contenant le mot "pomme" avec leurs numéros de lignes
  3) Trouver le chemin complet de l'interpréteur Python (`python3`)

**Indices** :
  - man: commande qui "search for files in a directory hierarchy" (option `-iname` pour ignorer la casse)
  - man: commande qui "print lines matching a pattern" (option `-n` pour les numéros de ligne, `-i` pour ignorer la casse)
  - man: "show full path of shell commands"
  - Le builtin `type` peut aussi identifier la nature d'une commande
  - **Commandes utilisées** : `find`, `grep`, `which`

**Validation** : `python3 verify.py --step 5`

Questions:
1) Quelle option rend la recherche insensible à la casse pour la recherche texte ? (A) -n (B) -i (C) -v (D) -w
2) Quelle option affiche le numéro de ligne ? (A) -n (B) -c (C) -H (D) -r
3) Quelle commande trouve un binaire dans le PATH ? (A) where (B) which (C) locate (D) type
4) Quel utilitaire indique si un nom est builtin, alias ou fichier ? (A) file (B) type (C) which (D) whatis
5) Quelle action liste la hiérarchie et filtre par motif de nom ? (A) find -name (B) ls -R (C) grep -r (D) locate -p

---

#### Étape 6 — Filtres et redirections (pipes)

**Contexte et concepts** :
La puissance de Linux réside dans la capacité à **combiner des commandes simples** pour réaliser des traitements complexes. C'est la philosophie Unix : chaque outil fait une chose, mais la fait bien, et on les combine.

Concepts clés :
- **Pipe (`|`)** : connecte la sortie d'une commande à l'entrée de la suivante
  - Exemple : `cat fichier.txt | grep "mot"` (affiche le fichier puis filtre les lignes contenant "mot")
- **Filtres** : commandes qui lisent l'entrée, la transforment, et produisent une sortie
- **Opérations courantes** :
  - Extraire des portions : premières/dernières lignes, colonnes spécifiques
  - Trier : ordre alphabétique, numérique, inverse
  - Dédupliquer : enlever les doublons (nécessite un tri préalable avec `uniq`)
  - Compter : lignes, mots, caractères
  - Transformer : changer la casse, remplacer des caractères
- **Redirections** : `>` envoie le résultat dans un fichier au lieu de l'écran

**À réaliser (résultat attendu)** :
  1) Afficher les 5 premières lignes de `data/lorem.txt`, puis les 3 dernières lignes
  2) Créer `workspace/data/fruits_uniques.txt` : trier `data/fruits.txt` et enlever les doublons
  3) Créer `workspace/data/lorem_wc.txt` contenant le nombre de mots du fichier `lorem.txt`
  4) Créer `workspace/data/fruits_upper.txt` : convertir `data/fruits.txt` en MAJUSCULES
  5) Extraire la 2ème colonne de `data/sample.csv` vers `workspace/data/col2.txt`

**Indices** :
  - man: "output the first part of files" et "output the last part"
  - man: "sort lines of text files" (tri alphabétique par défaut)
  - man: "report or omit repeated lines" (attention : `uniq` ne fonctionne que sur des lignes **consécutives**, d'où le tri préalable)
  - man: "print newline, word, and byte counts" (option `-w` pour les mots)
  - man: "translate or delete characters" (peut convertir minuscules → majuscules)
  - man: "remove sections from each line of files" (pour extraire des colonnes, options `-d` pour le délimiteur et `-f` pour le champ)
  - **Commandes utilisées** : `head`, `tail`, `sort`, `uniq`, `wc`, `tr`, `cut`

**Validation** : `python3 verify.py --step 6`

Questions:
1) Quelle commande supprime les doublons consécutifs après tri ? (A) uniq (B) sort (C) cut (D) tr
2) Quelle option de cut choisit le délimiteur ? (A) -d (B) -f (C) -c (D) -s
3) Quel utilitaire compte les mots ? (A) wc -w (B) wc -l (C) awk -c (D) sed -n
4) Quel transformateur convertit minuscules ↔ majuscules ? (A) sed (B) awk (C) tr (D) paste
5) Le "|" signifie… (A) redirection de sortie vers fichier (B) pipe entre commandes (C) OU logique (D) substitution

---

#### Étape 7 — Archiver et compresser

**Contexte et concepts** :
Pour partager ou sauvegarder plusieurs fichiers/dossiers, on les regroupe dans une **archive** unique, souvent **compressée** pour économiser de l'espace.

Concepts clés :
- **Archive** : regroupe plusieurs fichiers et dossiers en un seul fichier (comme un "sac")
  - Format `tar` (Tape ARchive) : le standard sous Linux
- **Compression** : réduit la taille des données
  - `gzip` : algorithme de compression courant (extension `.gz`)
  - Une archive tar compressée = `.tar.gz` ou `.tgz`
- **Opérations sur les archives** :
  - **Créer** : rassembler des fichiers dans une archive
  - **Lister** : voir le contenu sans extraire
  - **Extraire** : récupérer les fichiers originaux
- **Options tar** : souvent combinées (ex: `-czf` = create + gzip + file)
  - `-c` : create (créer)
  - `-x` : extract (extraire)
  - `-t` : test/list (lister)
  - `-z` : gzip (compresser/décompresser)
  - `-f` : file (spécifier le nom de l'archive)
  - `-C` : change directory (extraire vers un répertoire spécifique)

**À réaliser (résultat attendu)** :
  1) Créer une archive compressée `workspace/data_archive.tgz` contenant tout le dossier `data/`
  2) Lister le contenu de l'archive pour vérifier
  3) Extraire l'archive dans `workspace/tmp/`

**Indices** :
  - man tar : cherchez les sections CREATE, LIST, EXTRACT
  - Pour créer : `tar -czf archive.tgz dossier_source/`
  - Pour lister : cherchez l'option qui affiche le contenu
  - Pour extraire : option `-x` avec `-C` pour spécifier la destination
  - **Commandes utilisées** : `tar`

**Validation** : `python3 verify.py --step 7`

Questions:
1) Quelle option de tar crée une archive ? (A) -x (B) -t (C) -c (D) -z
2) Quel drapeau active gzip dans tar ? (A) -g (B) -z (C) -Z (D) -j
3) Que fait -t avec tar ? (A) teste (B) liste (C) extrait (D) compresse
4) Où extrait-on avec -C ? (A) vers / (B) vers répertoire courant (C) vers le chemin indiqué (D) vers $HOME
5) Une archive tar.gz est… (A) un seul fichier (B) plusieurs fichiers (C) un lien (D) un device

---

#### Étape 8 — Liens symboliques et permissions

**Contexte et concepts** :
Sous Linux, les **liens symboliques** permettent de créer des raccourcis, et les **permissions** contrôlent qui peut lire, écrire ou exécuter chaque fichier.

Concepts clés :
- **Lien symbolique (symlink)** : un "pointeur" vers un autre fichier ou dossier
  - Comme un raccourci Windows, mais plus puissant
  - Si on supprime la cible, le lien devient "cassé"
  - Utile pour : accès rapide, compatibilité, organisation
- **Permissions Linux** : système rwx (read, write, execute) pour 3 catégories
  - **Propriétaire (user)** : le créateur du fichier
  - **Groupe (group)** : les utilisateurs du même groupe
  - **Autres (others)** : tout le reste du monde
- **Notation octale** : représentation numérique des permissions
  - r (read) = 4, w (write) = 2, x (execute) = 1
  - Exemples :
    - `640` = `rw-r-----` (user: lecture+écriture, group: lecture, others: rien)
    - `755` = `rwxr-xr-x` (user: tout, group: lecture+exécution, others: lecture+exécution)
    - `644` = `rw-r--r--` (user: lecture+écriture, tous: lecture seule)

**À réaliser (résultat attendu)** :
  1) Créer un lien symbolique `workspace/data/link_fruits.txt` qui pointe vers le fichier `data/fruits.txt` (utilisez le chemin absolu ou relatif approprié)
  2) Changer les permissions de `workspace/data/fruits_uniques.txt` en `640` (rw-r-----)

**Indices** :
  - man: "make links between files" (option `-s` pour symbolic link)
  - man: "change file mode bits" (accepte notation octale ou symbolique)
  - Pour voir les permissions : `ls -l` affiche le format `-rwxrwxrwx`
  - Syntaxe lien : `commande -s chemin_cible nom_du_lien`
  - Astuce : pour un lien depuis `workspace/data/` vers `data/fruits.txt`, vous pouvez utiliser un chemin absolu (commence par `/`) ou un chemin relatif (ex: `../../data/fruits.txt`)
  - **Commandes utilisées** : `ln`, `chmod`

**Validation** : `python3 verify.py --step 8`

Questions:
1) Quelle option crée un lien symbolique ? (A) -h (B) -s (C) -L (D) -P
2) 640 signifie… (A) rw‑r‑‑‑x (B) rw‑r‑‑‑‑ (C) r‑wxr‑‑ (D) rwxr‑‑r‑‑
3) Les permissions s'appliquent à… (A) user uniquement (B) user,groupe,autres (C) groupe uniquement (D) root uniquement
4) Un lien symbolique pointe vers… (A) l'inode directement (B) un chemin (C) un device (D) un socket
5) Quelle commande affiche les permissions lisiblement ? (A) ls -l (B) stat -p (C) getfacl (D) toutes

---

#### Étape 9 — Variables d'environnement et alias

**Contexte et concepts** :
Le shell Bash vous permet de personnaliser votre environnement de travail avec des **variables** et des **alias** pour gagner du temps et adapter le comportement des programmes.

Concepts clés :
- **Variables shell** : stockent des valeurs (texte, nombres, chemins...)
  - Déclaration : `MYVAR="valeur"` (sans espaces autour du `=`)
  - Utilisation : `$MYVAR` ou `${MYVAR}`
  - Scope : par défaut, visible uniquement dans le shell courant
- **Export** : rend une variable visible par les programmes lancés depuis le shell
  - Sans export : la variable reste locale au shell
  - Avec export : les sous-processus (programmes enfants) peuvent la lire
  - Exemple : `export PATH=/usr/local/bin:$PATH`
- **Variables importantes** :
  - `HOME` : votre dossier personnel
  - `PATH` : où chercher les exécutables
  - `USER` : votre nom d'utilisateur
- **Alias** : raccourcis pour des commandes fréquentes
  - Syntaxe : `alias nom='commande complète'`
  - Exemples courants :
    - `alias ll='ls -la'`
    - `alias ..='cd ..'`
  - Valable uniquement dans la session courante (sauf si ajouté à `~/.bashrc`)

**À réaliser (résultat attendu)** :
  1) Créer une variable `MYVAR` avec une valeur de votre choix, puis l'exporter
  2) Créer un alias `ll` qui exécute un listage détaillé avec fichiers cachés
  3) Utiliser l'alias `ll` pour vérifier qu'il fonctionne
  4) Afficher la valeur de `MYVAR` avec `echo $MYVAR`

**Indices** :
  - man bash : cherchez les sections "Shell Variables", "ENVIRONMENT", "ALIASES"
  - Commandes intégrées (builtins) : tapez `help export` et `help alias` directement dans bash
  - Pour voir toutes les variables exportées : `env` ou `printenv`
  - Pour voir tous les alias : `alias` sans argument
  - **Commandes utilisées** : `export`, `alias`, `echo`

**Validation** : `python3 verify.py --step 9`

**Note** : Le script de vérification ne peut pas "voir" vos variables/alias car il s'exécute dans un processus séparé. C'est normal ! L'important est de comprendre comment les créer et les utiliser.

Questions:
1) Quelle commande exporte MYVAR ? (A) env MYVAR (B) export MYVAR (C) set MYVAR (D) declare -x sans export
2) Un alias est… (A) un binaire (B) une fonction shell (C) un remplacement de texte du shell (D) une variable
3) Où mettre des alias persistants ? (A) /etc/shadow (B) ~/.bashrc (C) ~/.profile sans sourcer (D) /usr/bin
4) Quelle commande affiche toutes les variables d'environnement ? (A) env (B) set (C) export -p (D) printenv
5) Une variable non exportée est visible… (A) partout (B) dans les sous‑processus (C) seulement dans le shell courant (D) dans cron

---

#### Étape 10 — Processus et ressources

**Contexte et concepts** :
Sous Linux, chaque programme en cours d'exécution est un **processus**. Savoir les observer, les contrôler et surveiller les ressources système est essentiel pour gérer votre environnement.

Concepts clés :
- **Processus** : instance d'un programme en cours d'exécution
  - Chaque processus a un **PID** (Process ID) unique
  - Hiérarchie parent/enfant : chaque processus (sauf init) a un parent
- **États d'un processus** :
  - **Avant-plan (foreground)** : occupe le terminal, vous ne pouvez rien faire d'autre
  - **Arrière-plan (background)** : s'exécute en parallèle, vous gardez la main sur le terminal
  - Syntaxe : ajouter `&` à la fin d'une commande pour la lancer en arrière-plan
- **Gestion des processus** :
  - Lister : voir tous les processus en cours (ps, top, htop...)
  - Filtrer : trouver un processus par nom ou critère
  - Terminer : envoyer un signal pour arrêter un processus (proprement ou brutalement)
- **Signaux courants** :
  - `SIGTERM` (15) : demande d'arrêt propre (par défaut)
  - `SIGKILL` (9) : arrêt brutal, sans nettoyage
- **Ressources système** :
  - Espace disque : voir l'occupation des systèmes de fichiers
  - Option `-h` : affichage "human-readable" (Ko, Mo, Go...)

**À réaliser (résultat attendu)** :
  1) Afficher la liste de vos processus en cours
  2) Lancer un processus simple en arrière-plan : `sleep 300 &`
  3) Trouver le PID de ce processus `sleep`
  4) Terminer ce processus en utilisant son nom ou son PID
  5) Afficher l'espace disque disponible en format lisible (humain)

**Indices** :
  - man: "report a snapshot of current processes" (option `-u` pour filtrer par utilisateur)
  - man: "look up or signal processes based on name" (cherchez `pgrep` pour trouver, `pkill` pour terminer)
  - man: "report file system disk space usage" (option `-h` pour format lisible)
  - Pour lister vos processus : `ps -u $(whoami)` ou `ps -u $USER`
  - `$(whoami)` est une substitution de commande : exécute `whoami` et utilise le résultat
  - **Commandes utilisées** : `ps`, `pgrep`, `pkill`, `df`

**Validation** : `python3 verify.py --step 10`

Questions:
1) Quelle commande liste les processus de l'utilisateur actuel ? (A) ps -u $(whoami) (B) top (C) jobs -l (D) pstree
2) Quelle commande trouve un PID par nom ? (A) pidof (B) pgrep (C) psfind (D) pkill -p
3) Quelle commande termine par nom ? (A) killall (B) pkill (C) kill -9 (D) pstop
4) df -h affiche… (A) RAM (B) réseaux (C) disques (D) CPU
5) Le "&" placé après une commande… (A) la relance (B) la met en arrière‑plan (C) la tue (D) l'ignore

---

### Mode d'emploi rapide

- Préparer: bash setup.sh
- Travailler: lisez l'intro de l'étape, trouvez les commandes via man et les indices, réalisez l'objectif observable (résultat concret dans les fichiers).
- Vérifier: python3 verify.py --step N
- Consolider: python3 verify.py --all pour tout rejouer.

---

### Quiz de validation

Chaque étape inclut un **quiz QCM** (Questions à Choix Multiples) pour renforcer vos connaissances. Le quiz est un outil séparé que vous pouvez lancer manuellement après avoir validé une étape.

#### Utilisation du quiz

**Lancer le quiz** :
```bash
./quiz/quiz -q linux
```
Le script quiz vous permet de tester vos connaissances sur les concepts abordés dans chaque étape.

#### Format des questions

Les questions portent sur :
- Les concepts théoriques de l'étape
- Les commandes et leurs options
- Les bonnes pratiques Linux

**Astuce** : Les questions sont listées à la fin de chaque étape dans ce document. Vous pouvez les consulter pour vous préparer !

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