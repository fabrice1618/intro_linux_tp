### TP "Commandes de base Linux" — parcours progressif, guidé, et vérifié automatiquement

**Présentation** :

- **Contexte** : vous démarrez sous Linux et vous souhaitez "apprendre en faisant". Ce TP vous guide pas à pas pour manipuler le système de fichiers, rechercher, filtrer, archiver, gérer des liens, variables, et observer les processus.
- **Contraintes** : pas de sudo; tout se fait dans votre dossier personnel ($HOME, supposé être /home/user).
- **Vérification** : un script Python vérifie à chaque étape l'état final (résultat concret) et, en cas d'erreur, explique ce qu'il a trouvé et donne une piste pour corriger.
- **Philosophie** : l'énoncé ne donne pas forcément la commande exacte. Vous trouverez la commande et ses options dans les extraits de documentation fournis et dans le manuel (man).

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
- Puis affichez votre progression : `python3 verify.py`

**3) Vérifier une étape**

- Exemple : `python3 verify.py 3` (ou `python3 verify.py --step 3`)
- Mode tout-en-un : `python3 verify.py --all`

**Astuce man** : utilisez `man <commande>`, `/mot` pour chercher dans la page, `n` pour "suivant", `q` pour quitter.

---

### Le script de vérification

| Commande | Effet |
|---|---|
| `python3 verify.py` | Tableau de progression : étapes validées (✔), commencées (◐), à faire (·), et prochaine étape |
| `python3 verify.py 3` | Vérification détaillée de l'étape 3 |
| `python3 verify.py --all` | Vérification détaillée de toutes les étapes |

Pour chaque tâche, le script affiche ✔ (réussie) ou ✘ (à corriger), suivi d'explications ↳ : ce qu'il a trouvé, pourquoi ce n'est pas le résultat attendu, et une piste. Il ne donne pas la commande : c'est à vous de la trouver.

- **Preuves** : le script ne voit pas votre écran. Quand une tâche ne laisse pas de trace, l'énoncé demande d'enregistrer ce qu'elle affiche dans `workspace/preuves/` avec une redirection : `commande > workspace/preuves/fichier.txt`.
- **Questions** : certaines tâches se vérifient par une question (un mot secret, une taille, un chemin...) dont la réponse s'obtient en exécutant les commandes. Le script la pose lors de `python3 verify.py N` et retient les bonnes réponses.
- **Données sources** : `data/` ne doit jamais être modifié. Si c'est arrivé par erreur, le script le signale : relancez `bash setup.sh` pour restaurer `data/`, votre travail dans `workspace/` est conservé. Pour recommencer le TP de zéro : `bash setup.sh --reset`.
- Le script fonctionne quel que soit votre répertoire courant.

---

## Parcours progressif

Chaque étape inclut: introduction (concept), tâche à réaliser (objectif observable), extraits de la documentation (les options utiles, telles que les affichent `man` ou `help`), et validation (commande de vérification).

---

#### Étape 1 — Trouver de l'aide, historique, horloge

**Contexte et concepts** :
Un bon développeur Linux sait **s'auto-documenter** : trouver de l'aide rapidement, réutiliser des commandes précédentes, et utiliser les outils système.

Concepts clés :
- **Pages de manuel (man)** : documentation complète de toutes les commandes
  - Structure standard : NAME, SYNOPSIS, DESCRIPTION, OPTIONS, EXAMPLES...
  - Navigation : espace (page suivante), `/mot` (rechercher), `n` (occurrence suivante), `q` (quitter)
  - Sections : man 1 (commandes), man 3 (fonctions C), man 5 (formats de fichiers)...
  - Recherche par mot-clé : `man -k mot` liste les commandes dont la description contient ce mot, utile quand on ne connaît pas encore le nom de la commande
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
- **Redirection `>`** (aperçu, détaillée à l'étape 3) : `commande > fichier` enregistre dans un fichier ce que la commande aurait affiché à l'écran. C'est ainsi que vous transmettez un résultat au script de vérification.

**À réaliser (résultat attendu)** :
  1) Ouvrir la page de manuel de `ls`, y chercher le mot "size", trouver l'option courte qui trie les fichiers par taille (du plus gros au plus petit), puis quitter
  2) Avec l'aide rapide `date --help`, trouver comment afficher une autre date que celle du jour, puis afficher le jour de la semaine du 1er janvier 2030
  3) Avec `man -k`, trouver la commande dont la description est "print name of current/working directory"
  4) Enregistrer vos 10 dernières commandes dans un fichier : `history 10 > workspace/preuves/historique.txt`

**Extraits de la documentation** :

```text
$ man man
SYNOPSIS
       man [man options] [[section] page ...] ...
       man -k [apropos options] regexp ...
       man -K [man options] [section] term ...

       -k, --apropos
              Approximately equivalent to apropos.  Search the short manual
              page descriptions for keywords and display any matches.

       -K, --global-apropos
              Search for text in all manual pages.  This is a brute-force
              search, and is likely to take some time; ...

$ help history
history: history [-c] [-d décalage] [n] ou history -anrw [nomfichier] ou history -ps arg [arg...]
    Affiche ou manipule l'historique.

    Affiche l'historique avec les numéros de lignes en préfixant chaque élément
    modifié d'un « * ».  Un argument égal à N limite la liste aux N derniers éléments.
```

  - `man -k mot` cherche dans les descriptions courtes (la ligne NAME de chaque page) : rapide. `man -K mot` cherche dans le texte complet de toutes les pages : lent.
  - `history` est une commande intégrée (builtin) de Bash : elle n'a pas de page man, son aide s'obtient avec `help history` (en français si le système est en français).
  - **Commandes utilisées** : `man`, `--help`, `help`, `history`, `date`

**Validation** : `python3 verify.py 1` (le script vous demande les réponses des tâches 1 à 3)

**Astuce** : Consultez la section "Guide d'utilisation de man" en fin de document pour plus de détails !

---

#### Étape 2 — Se repérer dans l'arborescence

**Contexte et concepts** :
Sous Linux, tout est organisé en arborescence de fichiers et dossiers, à partir de la racine `/`. Lorsque vous travaillez dans un terminal, vous êtes toujours "quelque part" dans cette arborescence : c'est le **répertoire courant** (ou répertoire de travail).

Concepts clés :
- **Chemin absolu** : commence par `/` et décrit le chemin complet depuis la racine (ex: `/home/user/Documents`)
- **Chemin relatif** : décrit le chemin depuis le répertoire courant (ex: `Documents/projet`)
- **Variables d'environnement** : `$HOME` contient le chemin de votre dossier personnel, `$PWD` contient le répertoire courant
- **Fichiers cachés** : sous Linux, tout fichier dont le nom commence par `.` est considéré comme "caché" (ex: `.bashrc`)
- **Se déplacer** : `cd dossier` entre dans un dossier, `cd ..` remonte au dossier parent, `cd` seul ramène au dossier personnel, `cd -` revient au dossier précédent
- **Noms spéciaux** : `.` désigne le dossier courant, `..` le dossier parent, `~` votre dossier personnel

**À réaliser (résultat attendu)** :
  1) Depuis le dossier du TP, afficher le chemin absolu du répertoire courant (pour savoir où vous êtes)
  2) Lister toutes les entrées de `data/`, y compris les fichiers cachés, puis afficher le contenu du fichier caché qui s'y trouve
  3) Afficher un listing détaillé de `data/` montrant les permissions, propriétaires, tailles et dates, et relever la taille de `sample.csv` en octets
  4) Se placer dans `workspace/preuves`, afficher le fichier `data/fruits.txt` avec un chemin **relatif** depuis ce dossier, puis revenir au dossier du TP

**Extraits de la documentation** :

```text
$ help pwd
pwd: pwd [-LP]
    Affiche le nom du répertoire de travail courant.

$ help cd
cd: cd [-L|[-P [-e]] [-@]] [rép]
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is the value of the
    HOME shell variable. If DIR is "-", it is converted to $OLDPWD.

$ man ls
SYNOPSIS
       ls [OPTION]... [FILE]...

       -a, --all
              do not ignore entries starting with .

       -l     use a long listing format

$ man cat
SYNOPSIS
       cat [OPTION]... [FILE]...
DESCRIPTION
       Concatenate FILE(s) to standard output.
```

  - `ls -a` n'ignore pas les entrées commençant par un point ; `ls -l` utilise le format long (détaillé)
  - `cat` affiche le contenu des fichiers donnés en argument
  - Astuce : vous pouvez combiner plusieurs options, par exemple `-la` ou `-l -a`
  - **Commandes utilisées** : `pwd`, `cd`, `ls`, `cat`

**Validation** : `python3 verify.py 2` (le script vous demande le chemin absolu, le mot secret, la taille et le chemin relatif)

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
  1) Créer les dossiers `docs`, `data` et `tmp` dans `workspace/` (une seule commande suffit)
  2) Créer en une seule commande l'arborescence `workspace/projets/2026/janvier`
  3) Créer un fichier vide nommé `todo.txt` dans `workspace/data`
  4) Créer un fichier caché nommé `.cache` dans `workspace/tmp`
  5) Créer le fichier `workspace/docs/bonjour.txt` contenant au moins 2 lignes de texte, puis l'afficher avec les numéros de ligne

**Extraits de la documentation** :

```text
$ man mkdir
SYNOPSIS
       mkdir [OPTION]... DIRECTORY...

       -p, --parents
              no error if existing, make parent directories as needed

$ man touch
SYNOPSIS
       touch [OPTION]... FILE...

       A FILE argument that does not exist is created empty, unless -c or -h
       is supplied.

$ help echo
echo: echo [-neE] [arg ...]
    Écrit les arguments sur la sortie standard.

    Affiche les ARGs, séparés par une espace, sur la sortie standard, suivis
    d'un retour à la ligne.

$ man cat
       -n, --number
              number all output lines
```

  - `mkdir -p` crée aussi les dossiers parents manquants, sans erreur s'ils existent déjà
  - `touch` crée vide un fichier qui n'existe pas
  - Les redirections `>` et `>>` permettent d'écrire la sortie d'une commande dans un fichier
  - Exemple d'utilisation : `echo "première ligne" > fichier.txt` puis `echo "deuxième ligne" >> fichier.txt`
  - **Commandes utilisées** : `mkdir`, `touch`, `echo`, `cat`

**Validation** : `python3 verify.py 3`

---

#### Étape 4 — Copier, déplacer, renommer, supprimer

**Contexte et concepts** :
Une fois vos fichiers créés, vous devez pouvoir les réorganiser : faire des copies de sauvegarde, déplacer des fichiers entre dossiers, renommer, ou nettoyer ce qui ne sert plus.

Concepts clés :
- **Copier** : crée un duplicata du fichier/dossier source, l'original reste intact
  - Copie récursive (`-R` ou `-r`) : nécessaire pour copier un dossier avec tout son contenu
- **Déplacer/Renommer** : sous Linux, c'est la même opération ! Déplacer un fichier dans le même dossier = le renommer
- **Destination existante** : si la destination est un dossier qui existe déjà, `cp` et `mv` placent la source **à l'intérieur** de ce dossier
- **Supprimer** :
  - Fichiers : avec la commande de suppression classique
  - Dossiers vides : commande spécifique dédiée aux répertoires vides
  - Dossiers non vides : nécessite l'option récursive (`-r`)
- **Mode verbeux** (`-v`) : affiche ce qui est fait, utile pour suivre les opérations

**À réaliser (résultat attendu)** :
  1) Sauvegarder le dossier `data` : le copier, avec tout son contenu, vers `workspace/backup_data`
  2) Renommer `workspace/docs/bonjour.txt` en `bonjour.renomme.txt` (dans le même dossier)
  3) Déplacer `workspace/docs/bonjour.renomme.txt` à la racine de `workspace/`
  4) Supprimer le dossier vide `workspace/projets/2026/janvier` (créé à l'étape 3)
  5) La sauvegarde n'a pas besoin des journaux : supprimer le dossier `workspace/backup_data/logs` et son contenu

Une fois l'étape validée, cherchez comment faire les tâches 2 et 3 en une seule commande.

**Extraits de la documentation** :

```text
$ man cp
SYNOPSIS
       cp [OPTION]... [-T] SOURCE DEST
       cp [OPTION]... SOURCE... DIRECTORY

       -i, --interactive
              prompt before overwrite (overrides a previous -n option)

       -R, -r, --recursive
              copy directories recursively

       -v, --verbose
              explain what is being done

$ man mv
SYNOPSIS
       mv [OPTION]... [-T] SOURCE DEST
       mv [OPTION]... SOURCE... DIRECTORY
DESCRIPTION
       Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.

$ man rm
SYNOPSIS
       rm [OPTION]... [FILE]...

       -i     prompt before every removal

       -r, -R, --recursive
              remove directories and their contents recursively

$ man rmdir
SYNOPSIS
       rmdir [OPTION]... DIRECTORY...
DESCRIPTION
       Remove the DIRECTORY(ies), if they are empty.
```

  - `cp -R` copie un dossier et tout son contenu ; `-i` demande confirmation avant d'écraser ; `-v` affiche ce qui est fait
  - `mv` renomme SOURCE en DEST, ou déplace les SOURCEs dans DIRECTORY
  - `rm -r` supprime un dossier et son contenu ; `rmdir` ne supprime que les dossiers vides
  - Attention : il n'y a pas de "corbeille" en ligne de commande, la suppression est définitive !
  - **Commandes utilisées** : `cp`, `mv`, `rm`, `rmdir`

**Validation** : `python3 verify.py 4`

---

#### Étape 5 — Rechercher des fichiers et du texte

**Contexte et concepts** :
Dans un système avec des milliers de fichiers, savoir chercher efficacement est essentiel. Linux offre des outils puissants pour trouver des fichiers par leur nom et pour chercher du texte à l'intérieur des fichiers.

Concepts clés :
- **Recherche de fichiers** : parcourt l'arborescence pour trouver des fichiers selon des critères (nom, type, taille, date...)
  - Recherche insensible à la casse : ignore majuscules/minuscules (ex: "Fruits" = "fruits" = "FRUITS")
  - Jokers : `*` remplace n'importe quelle séquence de caractères
  - Guillemets : écrivez le motif entre guillemets (`"*fruits*"`), sinon le shell remplace lui-même `*` par les noms de fichiers du dossier courant avant de lancer la commande
- **Recherche de texte** : analyse le contenu des fichiers ligne par ligne
  - Numéros de ligne : utile pour localiser précisément où se trouve le texte
  - Expressions régulières : motifs de recherche puissants (avancé)
- **Variable PATH** : liste des répertoires où le shell cherche les commandes exécutables
  - `which` : trouve le chemin complet d'un exécutable
  - `type` : indique si un nom est un alias, un builtin, ou un fichier exécutable

**À réaliser (résultat attendu)** :
  1) Rechercher sous `data/` tous les fichiers dont le nom contient "fruits" (sans tenir compte de la casse), et enregistrer le résultat dans `workspace/preuves/find_fruits.txt`
  2) Dans le fichier `data/fruits.txt`, trouver les lignes contenant "poire" (quelle que soit la casse) avec leurs numéros de ligne, et enregistrer le résultat dans `workspace/preuves/grep_poire.txt`
  3) Trouver le chemin complet de l'interpréteur Python (`python3`) et l'enregistrer dans `workspace/preuves/which_python3.txt`
  4) Comparer ce qu'affichent `type cd`, `type ls` et `type python3` (non vérifié)

**Extraits de la documentation** :

```text
$ man find
SYNOPSIS
       find [-H] [-L] [-P] [-D debugopts] [-Olevel] [starting-point...] [ex‐
       pression]

       -iname pattern
              Like  -name,  but the match is case insensitive.  For example,
              the patterns `fo*' and  `F??'  match  the  file  names  `Foo',
              `FOO', `foo', `fOo', etc.

       -name pattern
              Base  of  file name (the path with the leading directories re‐
              moved) matches shell pattern pattern.

$ man grep
SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]

       -i, --ignore-case
              Ignore  case  distinctions in patterns and input data, so that
              characters that differ only in case match each other.

       -n, --line-number
              Prefix each line of output with the 1-based line number within
              its input file.

$ man which
SYNOPSIS
       which [-as] filename ...
DESCRIPTION
       which  returns  the  pathnames of the files (or links) which would be
       executed in the current environment, [...] It does this by
       searching the PATH for executable files matching the names of the ar‐
       guments.

$ help type
type: type [-afptP] nom [nom ...]
    Affiche des informations sur le type de commande.

    Pour chaque NOM, indique comment il serait interprété s'il était
    utilisé comme un nom de commande.
```

  - `find DÉPART -name MOTIF` cherche les fichiers dont le nom correspond au motif ; `-iname` fait de même sans tenir compte de la casse
  - `grep -i` ignore la casse ; `grep -n` préfixe chaque ligne par son numéro
  - `which` cherche un exécutable dans les dossiers de la variable `PATH` ; `type` indique si un nom est un alias, une commande intégrée (primitive) ou un fichier
  - **Commandes utilisées** : `find`, `grep`, `which`, `type`

**Validation** : `python3 verify.py 5`

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
  - Attention : ne redirigez jamais vers le fichier que vous lisez. `sort f > f` vide `f`, car le shell vide le fichier de destination avant même que `sort` ne commence à le lire
  - `<` fait l'inverse : il fournit le contenu d'un fichier comme entrée d'une commande (`tr ... < fichier`)

**À réaliser (résultat attendu)** :
  1) Créer `workspace/data/lorem_extrait.txt` contenant les lignes 2 à 4 de `data/lorem.txt` (combinez deux commandes avec un pipe)
  2) Créer `workspace/data/fruits_uniques.txt` : trier `data/fruits.txt` et enlever les doublons
  3) Créer `workspace/data/lorem_wc.txt` contenant le nombre de mots du fichier `lorem.txt`
  4) Créer `workspace/data/fruits_upper.txt` : convertir `data/fruits.txt` en MAJUSCULES, sans changer l'ordre des lignes
  5) Extraire la 2ème colonne de `data/sample.csv` vers `workspace/data/col2.txt`
  6) Créer `workspace/data/nb_info.txt` contenant le nombre de lignes `INFO` du journal `data/logs/app.log`

**Extraits de la documentation** :

```text
$ man head
DESCRIPTION
       Print  the first 10 lines of each FILE to standard output.

       -n, --lines=[-]NUM
              print the first NUM lines instead of the first  10;  with  the
              leading '-', print all but the last NUM lines of each file

$ man tail
       -n, --lines=[+]NUM
              output the last NUM lines, instead of the last 10; or  use  -n
              +NUM to skip NUM-1 lines at the start

$ man sort
DESCRIPTION
       Write sorted concatenation of all FILE(s) to standard output.

       -f, --ignore-case
              fold lower case to upper case characters

       -r, --reverse
              reverse the result of comparisons

$ man uniq
DESCRIPTION
       Filter  adjacent matching lines from INPUT (or standard input), writ‐
       ing to OUTPUT (or standard output).

       -c, --count
              prefix lines by the number of occurrences

$ man wc
       -c, --bytes
              print the byte counts

       -l, --lines
              print the newline counts

       -w, --words
              print the word counts

$ man tr
SYNOPSIS
       tr [OPTION]... STRING1 [STRING2]
DESCRIPTION
       Translate,  squeeze,  and/or  delete  characters from standard input,
       writing to standard output.

       [:lower:]
              all lower case letters

       [:upper:]
              all upper case letters

$ man cut
       -d, --delimiter=DELIM
              use DELIM instead of TAB for field delimiter

       -f, --fields=LIST
              select only these fields
```

  - `head -n N` / `tail -n N` : les N premières / dernières lignes
  - `uniq` ne supprime que les lignes identiques **adjacentes** (consécutives), d'où le tri préalable avec `sort`
  - `wc` compte les lignes (`-l`), les mots (`-w`) ou les octets (`-c`)
  - `tr` lit uniquement son entrée standard (pipe ou `<`) : il ne prend pas de nom de fichier en argument
  - `cut -d` choisit le délimiteur (tabulation par défaut), `-f` le numéro du champ, en commençant à 1
  - **Commandes utilisées** : `head`, `tail`, `sort`, `uniq`, `wc`, `tr`, `cut`, `grep`

**Validation** : `python3 verify.py 6`

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
  1) Depuis le dossier du TP, créer une archive compressée `workspace/data_archive.tgz` contenant tout le dossier `data/`
  2) Lister le contenu de l'archive et enregistrer cette liste dans `workspace/preuves/contenu_archive.txt`
  3) Extraire l'archive dans `workspace/tmp/`

**Extraits de la documentation** :

```text
$ man tar
SYNOPSIS
       tar -c [-f ARCHIVE] [OPTIONS] [FILE...]
       tar -t [-f ARCHIVE] [OPTIONS] [MEMBER...]
       tar -x [-f ARCHIVE] [OPTIONS] [MEMBER...]

       -c, --create
              Create a new archive.  Arguments supply the names of the files
              to  be archived.  Directories are archived recursively, unless
              the --no-recursion option is given.

       -t, --list
              List the contents of  an  archive.   Arguments  are  optional.

       -x, --extract, --get
              Extract files from an archive.  Arguments are optional.

       -f, --file=ARCHIVE
              Use archive file or device ARCHIVE.

       -z, --gzip, --gunzip, --ungzip
              Filter the archive through gzip(1).

       -C, --directory=DIR
              Change  to  DIR before performing any operations.
```

  - Les options se combinent : `-czf` = create + gzip + file ; `-f` doit être suivi du nom de l'archive
  - L'archive garde les chemins tels qu'ils ont été donnés à la création : archivez `data` depuis le dossier du TP pour que les chemins commencent par `data/`
  - **Commandes utilisées** : `tar`

**Validation** : `python3 verify.py 7`

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
- **Exécuter un script** : un fichier ne peut être lancé comme une commande que s'il a le droit `x`, sinon le shell répond « Permission non accordée ». Le shell ne cherche les commandes que dans les dossiers du `PATH` : pour lancer un script du dossier courant, on précise son chemin (`./salut.sh`)

**À réaliser (résultat attendu)** :
  1) Créer un lien symbolique `workspace/data/link_fruits.txt` qui pointe vers le fichier `data/fruits.txt` (utilisez le chemin absolu ou relatif approprié)
  2) Changer les permissions de `workspace/data/fruits_uniques.txt` en `640` (rw-r-----)
  3) Copier le script `data/salut.sh` dans `workspace/`, essayer de le lancer (`./workspace/salut.sh`), lui donner les permissions `755` (rwxr-xr-x), puis le relancer

**Extraits de la documentation** :

```text
$ man ln
SYNOPSIS
       ln [OPTION]... [-T] TARGET LINK_NAME
DESCRIPTION
       In the 1st form, create a link to TARGET with the name LINK_NAME.
       [...] Create hard links by default, symbolic links with --symbolic.
       [...] Symbolic links can hold arbitrary text; if later resolved, a
       relative link is interpreted in relation to its parent directory.

       -s, --symbolic
              make symbolic links instead of hard links

$ man chmod
SYNOPSIS
       chmod [OPTION]... MODE[,MODE]... FILE...
       chmod [OPTION]... OCTAL-MODE FILE...

       A  numeric  mode  is  from one to four octal digits (0-7), derived by
       adding up the bits with values 4, 2, and 1.  Omitted digits  are  as‐
       sumed  to  be leading zeros. [...] The second digit selects permissions
       for the user who owns the  file:  read  (4),  write (2), and execute (1);
       the third selects permissions for other users in the file's group, with
       the same values; and the fourth for other users not in the file's group,
       with the same values.
```

  - Pour voir les permissions : `ls -l` affiche le format `-rwxrwxrwx`
  - Syntaxe lien : `commande -s chemin_cible nom_du_lien`
  - Astuce : un chemin cible relatif est interprété depuis le dossier du **lien** (`workspace/data/`), pas depuis votre répertoire courant : c'est le même raisonnement qu'à l'étape 2. Un chemin absolu (qui commence par `/`) fonctionne aussi
  - **Commandes utilisées** : `ln`, `chmod`, `cp`

**Validation** : `python3 verify.py 8`

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
- **Processus enfant** : chaque commande lancée depuis le shell (par exemple `python3 verify.py`) est un processus enfant, qui reçoit une copie des variables **exportées** seulement. Les alias, eux, ne sont jamais transmis

**À réaliser (résultat attendu)** :
  1) Créer une variable `MYVAR` avec une valeur de votre choix (sans l'exporter), et l'afficher avec `echo $MYVAR`
  2) Lancer `bash -c 'echo "MYVAR vaut : $MYVAR"'` : cette commande démarre un nouveau shell, enfant du vôtre. Que constatez-vous ?
  3) Exporter `MYVAR`, puis relancer la commande de la tâche 2
  4) Créer un alias `verif` qui lance `python3 verify.py --step`, puis l'utiliser : `verif 9`
  5) Enregistrer la liste de vos alias dans `workspace/preuves/alias.txt`

Bonus (non obligatoire) : rendre l'alias permanent en ajoutant sa définition à la fin de `~/.bashrc`, puis ouvrir un nouveau terminal pour vérifier. Attention : `>>` ajoute à la fin du fichier, `>` effacerait toute votre configuration !

**Extraits de la documentation** :

```text
$ help export
export: export [-fn] [nom[=valeur] ...] ou export -p
    Définit l'attribut « export » pour des variables du shell.

    Marque chaque NOM pour exportation automatique vers l'environnement des
    commandes exécutées ultérieurement.  Si VALEUR est fournie, affecte la VALEUR
    avant l'exportation.

$ help alias
alias: alias [-p] [nom[=valeur] ... ]
    Définit ou affiche des alias.

    Sans argument, « alias » affiche la liste des alias dans le format réutilisable
    « alias NOM=VALEUR » sur la sortie standard.

    Sinon, un alias est défini pour chaque NOM dont la VALEUR est donnée.
```

  - Pour voir toutes les variables exportées : `env` ou `printenv`
  - Pour voir tous les alias : `alias` sans argument
  - **Commandes utilisées** : `export`, `alias`, `echo`, `bash -c`

**Validation** : `python3 verify.py 9`, lancé depuis le terminal où vous avez exporté `MYVAR`. Le script est un processus enfant de votre shell : il ne voit `MYVAR` que si elle est exportée, c'est exactement ce qu'il vérifie.

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
  1) Afficher la liste de vos processus en cours, et repérer le PID du shell (bash) de votre terminal
  2) Lancer un processus simple en arrière-plan : `sleep 1000 &` (notez le numéro de tâche et le PID affichés), puis afficher les tâches du shell avec `jobs`
  3) Trouver le PID de ce processus `sleep` et l'enregistrer dans `workspace/preuves/sleep.pid`
  4) Terminer ce processus en utilisant son nom ou son PID
  5) Enregistrer l'espace disque disponible, en format lisible (humain), dans `workspace/preuves/disque.txt`

**Extraits de la documentation** :

```text
$ man ps
DESCRIPTION
       ps displays information about a selection of the active processes.

       -u userlist
              Select  by effective user ID (EUID) or name.  This selects the
              processes whose effective user name or ID is in userlist.

$ man pgrep
SYNOPSIS
       pgrep [options] pattern
       pkill [options] pattern
DESCRIPTION
       pgrep looks through the currently running  processes  and  lists  the
       process  IDs  which  match the selection criteria to stdout.

       -u, --euid euid,...
              Only  match  processes  whose effective user ID is listed.

$ help kill
kill: kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... ou kill -l [sigspec]
    Envoie un signal à une tâche.

    Envoie le signal nommé par SIGSPEC ou SIGNUM au processus identifié par
    PID ou JOBSPEC. Si SIGSPEC et SIGNUM ne sont pas donnés, alors SIGTERM est
    envoyé.

$ man df
       -h, --human-readable
              print sizes in powers of 1024 (e.g., 1023M)
```

  - Pour lister vos processus : `ps -u $(whoami)` ou `ps -u $USER`
  - `$(whoami)` est une substitution de commande : exécute `whoami` et utilise le résultat
  - Sur une machine partagée, `pgrep sleep` trouve aussi les `sleep` des autres utilisateurs : limitez la recherche aux vôtres
  - **Commandes utilisées** : `ps`, `jobs`, `pgrep`, `pkill`, `kill`, `df`

**Validation** : `python3 verify.py 10` (le script vous demande le PID de votre shell et vérifie que le `sleep` enregistré est bien terminé)

---

### Mode d'emploi rapide

- Préparer: bash setup.sh
- Travailler: lisez l'intro de l'étape, trouvez les commandes via les extraits de documentation et man, réalisez l'objectif observable (résultat concret dans les fichiers).
- Vérifier: python3 verify.py N, corrigez les points ✘ en suivant les explications, puis relancez.
- Consolider: python3 verify.py pour voir votre progression, python3 verify.py --all pour tout rejouer en détail.

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

Lorsque les extraits de documentation ne suffisent pas :
1. Ouvrez la page avec `man <commande>`
2. Utilisez `/` suivi d'un mot-clé (le nom d'une option, un mot de la tâche)
3. Parcourez les occurrences avec `n` jusqu'à trouver l'option pertinente
4. Lisez la section DESCRIPTION pour comprendre le contexte
5. Vérifiez les EXAMPLES si disponibles

**Exemple pour trouver une commande dont on ignore le nom** :
- Vous cherchez la commande qui "copy files and directories"
- `man -k copy` ou `man -k "copy.*files"`
- Trouvez `cp` dans les résultats
- `man cp` pour confirmer

Bon TP, et bonne exploration de la ligne de commande !