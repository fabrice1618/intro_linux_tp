[Cours GNU/Linux](../README.md#travaux-pratiques) · **TP 1 / 5** · [TP 2 →](tp2-fichiers-executables.md)

# TP 1 — Les fichiers texte

- **Objectifs** : créer, afficher, examiner et modifier des fichiers « texte » avec les commandes de base ; comprendre qu’un fichier texte n’est qu’une suite d’octets qui codent des caractères ; repérer les deux pièges des échanges de fichiers : les fins de ligne et l’encodage des caractères
- **Prérequis** : savoir ouvrir un terminal et taper une commande
- **Durée indicative** : 2 h
- **Commandes** : `touch` · `echo` · `cat` · `less` · `head` · `tail` · `wc` · `file` · `hexdump` · `hexedit` · `tr` · `md5sum` · `iconv`
- **Cours** : [Shell Bash](../README.md#shell-bash) · [Les Fichiers « texte »](../README.md#les-fichiers--texte-) · [L’encodage des caractères](../README.md#lencodage-des-caractères)

_Remarque : les tp ont pour but d’établir ou de renforcer vos compétences pratiques. Vous pouvez penser que vous comprenez tout ce que vous lisez ou tout ce que vous a dit votre enseignant mais la répétition et la pratique sont nécessaires pour développer des compétences en informatique. Ceci est comparable au sport ou à la musique ou à tout autre métier demandant un long entraînement pour acquérir l’habileté nécessaire. Imaginez quelqu’un qui voudrait disputer une compétition dans l’un de ces domaines sans pratique régulière. Vous savez bien quel serait le résultat._

---

## Avant de commencer

### Espace de travail

Créez un répertoire pour ce TP et placez-vous dedans : tous les fichiers du TP y seront créés.

```bash
$ mkdir -p ~/tpos/tpos1
$ cd ~/tpos/tpos1
```

### Conventions

- `$` représente l’invite (_prompt_) du shell : ne la tapez pas.
- Les lignes qui ne commencent pas par `$` montrent ce qu’affiche la commande. Votre affichage peut différer (date, taille, nom d’utilisateur) : c’est normal.
- Les **questions** sont numérotées. Notez vos réponses dans un compte rendu : sur papier, ou dans le fichier texte `~/tpos/reponses_tp1.txt` avec l’éditeur `nano` (`Ctrl+O` pour enregistrer, `Ctrl+X` pour quitter).

### Méthode : prédire, exécuter, expliquer

Avant de taper une commande, essayez de **prédire** ce qu’elle va afficher. Exécutez-la, puis **expliquez** ce que vous observez, surtout quand le résultat vous surprend : c’est là que l’on apprend.

### Astuce : l’historique des commandes

Le _shell_ garde la liste des commandes déjà tapées. Inutile de retaper une longue commande :

| Touche ou commande | Effet |
|---|---|
| flèches **HAUT** et **BAS** | parcourent les commandes précédentes |
| `Ctrl+R` puis un mot | recherche la dernière commande contenant ce mot |
| `history` | affiche tout l’historique, numéroté |
| `!!` | réexécute la dernière commande |
| `!100` | réexécute la commande n° 100 |
| `!ls` | réexécute la dernière commande commençant par `ls` |
| `!$` | remplacé par le dernier argument de la commande précédente |

L’aide des commandes internes du shell s’obtient avec `help` : `help history`, `help echo`.

---

## Rappels

### Le shell et les flux standard

**Bash** (_Bourne-again shell_) est le shell du projet GNU et l’interpréteur de commandes par défaut de la plupart des distributions GNU/Linux. L’utilisateur tape une commande sous forme de texte ; le shell l’interprète et demande au noyau de l’exécuter. Il existe d’autres shells : sh, dash, ksh, zsh (le shell par défaut de macOS depuis 2019)…

Tout processus (programme en cours d’exécution) démarre avec **3 flux** déjà ouverts :

| N° | Nom | Rôle | Par défaut |
|---|---|---|---|
| 0 | _stdin_ (_standard input_) | entrée des données | le clavier |
| 1 | _stdout_ (_standard output_) | sortie des données | l’écran |
| 2 | _stderr_ (_standard error_) | messages d’erreur | l’écran |

![Les trois flux standard d’un processus](../img/flux-standard.svg)

Le shell permet de **rediriger** ces flux vers (ou depuis) un fichier, ou de les relier entre deux commandes :

| Syntaxe | Effet |
|---|---|
| `cmd > fichier` | écrit la sortie standard dans `fichier` (le fichier est **vidé** s’il existait, créé sinon) |
| `cmd >> fichier` | **ajoute** la sortie standard à la fin de `fichier` |
| `cmd < fichier` | la commande lit son entrée standard dans `fichier` au lieu du clavier |
| `cmd 2> fichier` | écrit les messages d’erreur dans `fichier` |
| `cmd1 \| cmd2` | tube (_pipe_) : la sortie standard de `cmd1` devient l’entrée standard de `cmd2` |

### Fichiers texte et fichiers binaires

On distingue en général deux types de fichiers : **texte** et **binaire**.

- Un fichier **texte** ne contient que des octets qui codent des caractères selon un codage standard (ASCII, UTF-8…) : il est lisible directement. Exemples : code source d’un programme, fichiers de configuration (`/etc`), pages web, scripts, journaux (_logs_).
- Un fichier **binaire** est un fichier informatique qui n’est pas assimilable à un fichier texte : image, programme compilé, archive, document Word ou LibreOffice.

On manipule un fichier texte avec un **éditeur de texte** (nano, vim, emacs, VS Code…), à ne pas confondre avec un **traitement de texte** (Word, LibreOffice Writer), dont les documents sont des fichiers binaires.

_Remarque : L’éditeur de texte est le programme le plus important et le plus utilisé par un informaticien dans l’exercice de son métier (administration, programmation)._

---

## Manipulations

### Étape 1 — Créer un fichier texte

Créer un fichier vide :

```bash
$ touch vide
$ ls -l vide
-rw-rw-r-- 1 fab fab 0 sept. 26 23:32 vide
$ file vide
vide: empty
```

Créer un fichier avec un contenu, grâce à la redirection `>` :

```bash
$ echo "Hello world" > bonjour.txt
$ ls -l bonjour.txt
-rw-rw-r-- 1 fab fab 12 sept. 26 23:32 bonjour.txt
$ file bonjour.txt
bonjour.txt: ASCII text
```

> **Question 1** — Quelle est la taille du fichier `vide` ? Et celle de `bonjour.txt` ? Comptez les caractères de « Hello world » : que remarquez-vous ? (l’explication viendra à l’étape 3)

La commande `file` ne se fie pas au nom du fichier : elle examine son **contenu**.

```bash
$ cp bonjour.txt bonjour.jpg
$ file bonjour.jpg
```

> **Question 2** — Que répond `file` ? Que signifie l’extension `.txt` (ou `.jpg`) pour le système Linux ?

L’entrée standard peut, elle aussi, venir d’un fichier :

```bash
$ wc -l bonjour.txt
1 bonjour.txt
$ wc -l < bonjour.txt
1
```

> **Question 3** — Pourquoi le nom du fichier n’apparaît-il pas dans le second cas ? Qui ouvre le fichier `bonjour.txt` : la commande `wc` ou le shell ?

Les messages d’erreur empruntent un flux séparé :

```bash
$ ls bonjour.txt absent.txt > resultat.txt
ls: impossible d'accéder à 'absent.txt': Aucun fichier ou dossier de ce nom
$ cat resultat.txt
bonjour.txt
$ ls bonjour.txt absent.txt > resultat.txt 2> erreurs.txt
$ cat erreurs.txt
```

> **Question 4** — Pourquoi le message d’erreur de la première commande s’affiche-t-il à l’écran alors que la sortie est redirigée vers `resultat.txt` ? Que fait `2>` ?

### Étape 2 — Afficher le contenu d’un fichier texte

Il existe de nombreuses possibilités pour afficher le contenu d’un fichier texte. Essayez-les sur le fichier `/etc/passwd`, qui contient la liste des comptes de la machine :

| Commande | Affiche |
|---|---|
| `cat /etc/passwd` | tout le fichier d’un coup |
| `cat -n /etc/passwd` ou `nl /etc/passwd` | tout le fichier, avec les numéros de ligne |
| `less /etc/passwd` | page par page : `Espace` page suivante, `b` page précédente, `/mot` recherche, `q` quitte |
| `head -n 3 /etc/passwd` | les 3 premières lignes |
| `tail -n 3 /etc/passwd` | les 3 dernières lignes |

**Utilisation d’un tube (_pipe_) pour « relier » des commandes**

Le mécanisme de **tube** (symbole `|`) chaîne des processus de sorte que la sortie d’un processus (stdout) alimente directement l’entrée (stdin) du suivant. C’est un mécanisme de communication inter-processus (IPC), très utilisé pour enchaîner des traitements avec des commandes simples.

```bash
$ ls /usr/bin | wc -l
$ history | tail -5
```

> **Question 5** — Que calcule `ls /usr/bin | wc -l` ? Décrivez le rôle de chacune des deux commandes, puis celui du tube.

### Étape 3 — Examiner les octets d’un fichier texte

Un fichier texte contient fondamentalement une suite d’octets. Sa particularité est que l’ensemble du fichier respecte un **codage de caractères** standard.

La norme **ASCII** (_American Standard Code for Information Interchange_) est la plus ancienne et la plus connue. Elle définit 128 caractères numérotés de 0 à 127 : sept bits suffisent donc pour coder un caractère, et chaque caractère est stocké dans un octet dont le 8e bit est 0. Les caractères 0 à 31 et le 127 ne sont pas affichables : ce sont des caractères de contrôle (fin de ligne, tabulation, bip…). La table complète s’affiche avec `man ascii`.

Pour afficher le contenu brut d’un fichier (texte ou binaire) :

```bash
$ hexdump -C bonjour.txt
00000000  48 65 6c 6c 6f 20 77 6f  72 6c 64 0a              |Hello world.|
0000000c
$ od -c bonjour.txt
0000000   H   e   l   l   o       w   o   r   l   d  \n
0000014
```

Chaque ligne de `hexdump -C` donne : la position du premier octet (en hexadécimal), jusqu’à 16 octets en hexadécimal, puis les mêmes octets en caractères (un `.` remplace les caractères non affichables).

> **Question 6** — Combien d’octets contient le fichier ? Quel est le code hexadécimal du dernier octet, et à quel caractère correspond-il (`man ascii`) ? Expliquez maintenant la taille observée à la question 1.

> **Question 7** — Quel est le code hexadécimal de l’espace ? De la lettre `H` ? De la lettre `h` (cherchez dans `man ascii`) ? Quel écart y a-t-il entre une majuscule et sa minuscule ?

```bash
$ wc -c bonjour.txt
12 bonjour.txt
$ echo -n "Hello world" | wc -c
11
```

> **Question 8** — D’après `help echo`, que fait l’option `-n` ? Expliquez la différence entre les deux résultats.

### Étape 4 — Modifier le contenu d’un fichier

Le système d’exploitation ne permet que de très simples modifications d’un fichier : on peut soit modifier un (ou plusieurs) octet, soit ajouter des octets en fin de fichier.

**Remplacer un octet** : avec l’éditeur hexadécimal `hexedit`, remplacez le `w` de `bonjour.txt` par un `W`, puis affichez le fichier.

```bash
$ hexedit bonjour.txt
$ cat bonjour.txt
Hello World
```

> **Mode d’emploi de `hexedit`** : les flèches déplacent le curseur ; `Tab` passe de la colonne hexadécimale à la colonne texte ; tapez le nouveau caractère (ou sa valeur hexadécimale) ; `Ctrl+X` enregistre et quitte, `Ctrl+C` quitte sans enregistrer. Si la commande est absente : `sudo apt install hexedit`.

<details>
<summary>Sans <code>hexedit</code></summary>

La commande `dd` sait écrire un octet à une position donnée, sans tronquer le fichier (`conv=notrunc`) :

```bash
$ printf 'W' | dd of=bonjour.txt bs=1 seek=6 conv=notrunc
```

</details>

> **Question 9** — À quelle position (en comptant à partir de 0) se trouve le `w` ? Quelle valeur hexadécimale avez-vous écrite à sa place ?

Remarque : il est impossible en utilisant les services de l’OS de supprimer ou d’insérer du texte dans un fichier (sauf à la fin). Ce sont des opérations bien trop complexes car elles nécessiteraient un décalage d’un ensemble d’octets dans le fichier. Pour réaliser cela, il faut soit utiliser un éditeur de texte soit écrire soi-même un programme équivalent.

**Ajouter du texte à la fin du fichier** avec la redirection `>>` :

```bash
$ date +"le %A %d %B %Y à %T" >> bonjour.txt
$ echo "by $USER" >> bonjour.txt
$ cat bonjour.txt
```

> **Question 10** — Quelle est la différence entre `>` et `>>` ? Donnez une ligne de commande qui **vide** le fichier `bonjour.txt` sans le supprimer.

### Étape 5 — Les fins de ligne : Unix ou Windows ?

Les fichiers texte n’ont pas de structure : ce ne sont qu’une suite d’octets encodant des caractères. La notion de « fin de ligne » est pourtant ambiguë. Historiquement, les premiers terminaux (des imprimantes) avaient besoin de deux actions pour passer à la ligne : ramener le chariot à gauche (_Carriage Return_, CR) et faire avancer le papier d’une ligne (_Line Feed_, LF). Plusieurs conventions coexistent :

| Système | Fin de ligne | Octets |
|---|---|---|
| Unix, GNU/Linux, macOS | LF | `0a` |
| Mac OS jusqu’à la version 9 | CR | `0d` |
| MS-DOS, Microsoft Windows | CR+LF | `0d 0a` |

Ainsi, lorsque l’on ouvre sur un système un fichier texte créé sur un autre, il faut parfois refaire les fins de ligne. Les éditeurs de texte modernes détectent le type de fin de ligne et s’y adaptent, mais certains programmes (et les scripts shell !) le supportent mal.

```bash
$ echo -e -n "Hello World\nBienvenue le monde\n" > bonjour_unix.txt
$ echo -e -n "Hello World\r\nBienvenue le monde\r\n" > bonjour_dos.txt
$ file bonjour_unix.txt bonjour_dos.txt
bonjour_unix.txt: ASCII text
bonjour_dos.txt:  ASCII text, with CRLF line terminators
$ ls -l bonjour_unix.txt bonjour_dos.txt
$ cat -A bonjour_dos.txt
Hello World^M$
Bienvenue le monde^M$
```

> **Question 11** — D’après `help echo`, que permet l’option `-e` ? Quelle est la différence de taille entre les deux fichiers ? Pourquoi ?

> **Question 12** — Que représentent `^M` et `$` dans l’affichage de `cat -A` (`man cat`) ? Retrouvez les octets correspondants avec `hexdump -C bonjour_dos.txt`.

Pour convertir un fichier Windows au format Unix, il suffit de supprimer les CR :

```bash
$ tr -d '\r' < bonjour_dos.txt > bonjour_converti.txt
$ file bonjour_converti.txt
```

> **Question 13** — Expliquez cette commande. Que contiendrait le fichier si l’on écrivait `tr -d '\r' < bonjour_dos.txt > bonjour_dos.txt` ? Pourquoi ? (faites l’essai sur une copie)

_Remarque : les commandes `dos2unix` et `unix2dos` (paquet `dos2unix`) réalisent ces conversions ; l’éditeur `vim` affiche `[dos]` en bas de l’écran quand il ouvre un fichier au format Windows._

### Étape 6 — L’encodage des caractères

Un codage de caractères définit une manière de représenter les caractères (lettres, chiffres, symboles) par des octets.

- **ASCII** ne code que 128 caractères : pas de lettres accentuées, de cédilles, etc. utilisées par des langues comme le français.
- Les normes **ISO 8859** étendent l’ASCII à 256 caractères, toujours sur **un octet** : ISO 8859-1 (_latin1_) pour les langues occidentales, puis ISO 8859-15 (_latin9_), qui ajoute notamment « œ » et « € ». Chaque région a sa propre variante : un même octet ne désigne pas le même caractère d’une norme à l’autre.
- **Unicode** (ISO/CEI 10646) a pour ambition de représenter sans ambiguïté tous les signes écrits de toutes les langues : plus de 150 000 caractères, numérotés sur 21 bits (de U+0000 à U+10FFFF).
- **UTF-8** (RFC 3629) est la façon la plus répandue d’enregistrer de l’Unicode, sur Linux comme sur Internet. C’est un **codage à longueur variable**, compatible avec l’ASCII :

| Caractères | Octets | Exemple |
|---|---|---|
| ASCII (U+0000 à U+007F) | 1 | `A` → `41` (identique à l’ASCII) |
| lettres accentuées, grec, cyrillique… | 2 | `à` → `c3 a0` |
| reste des langues vivantes, symboles | 3 | `€` → `e2 82 ac` |
| emojis, écritures anciennes… | 4 | `😀` → `f0 9f 98 80` |

Le premier octet d’un caractère codé sur plusieurs octets indique la longueur de la séquence ; les octets suivants sont toujours compris entre `80` et `bf`.

Quel est l’encodage utilisé par votre session ? Il est défini par la variable d’environnement `LANG` :

```bash
$ env | grep LANG
LANG=fr_FR.UTF-8
```

> **Question 14** — Quel est l’encodage de votre session ? Que signifie la partie `fr_FR` ?

Encodons en UTF-8 une chaîne de caractères contenant le caractère `à` :

```bash
$ date +"le %A %d %B %Y à %T" > date.txt
$ cat date.txt
le samedi 26 septembre 2026 à 23:32:56
$ file date.txt
date.txt: Unicode text, UTF-8 text
$ hexdump -C date.txt
00000000  6c 65 20 73 61 6d 65 64  69 20 32 36 20 73 65 70  |le samedi 26 sep|
00000010  74 65 6d 62 72 65 20 32  30 32 36 20 c3 a0 20 32  |tembre 2026 .. 2|
00000020  33 3a 33 32 3a 35 36 0a                           |3:32:56.|
00000028
```

> **Question 15** — À partir de l’affichage de `hexdump`, donnez la valeur des octets qui encodent le caractère `à`. Combien d’octets occupent les autres caractères ?

```bash
$ echo -n "été" | wc -c
5
$ echo -n "été" | wc -m
3
```

> **Question 16** — Expliquez la différence entre les options `-c` et `-m` de `wc` (`man wc`). Un octet est-il toujours un caractère ?

Convertissons maintenant le fichier (qui est en UTF-8) en ISO 8859-1 avec `iconv` :

```bash
$ iconv -f UTF-8 -t ISO-8859-1 date.txt -o date_latin1.txt
$ file date_latin1.txt
date_latin1.txt: ISO-8859 text
$ cat date_latin1.txt
$ hexdump -C date_latin1.txt
```

> **Question 17** — Que se passe-t-il lors de l’affichage du fichier avec la commande `cat` ? Pourquoi ?

> **Question 18** — Quelle valeur encode le caractère `à` en ISO 8859-1 ? Correspond-elle à la valeur trouvée en UTF-8 ? Comparez les tailles des deux fichiers.

Pour en savoir plus : `man ascii`, `man iso_8859-1`, `man iso_8859-15`, `man utf-8`, `man unicode`, `man charsets`.

---

## Exercices

### Exercice 1 — Les commandes de base

L’objectif de cet exercice est de manipuler des fichiers texte avec les commandes de base d’un système Unix/Linux. Créez d’abord un fichier de plusieurs lignes :

```bash
$ printf 'Linux  est   un noyau\nGNU est un projet\nbash  est un shell\n' > phrases.txt
```

> **Question 19** — Pour chaque commande, prédisez ce qu’elle affiche, puis vérifiez (aidez-vous de `man`) :
>
> ```bash
> a) $ wc -l phrases.txt
> b) $ sort phrases.txt
> c) $ tac phrases.txt
> d) $ head -1 phrases.txt
> e) $ tail -2 phrases.txt
> f) $ cat phrases.txt | tr -s " " "."
> ```
>
> Pour `b)`, pourquoi la ligne `bash` apparaît-elle en premier ? Comparez avec `LC_ALL=C sort phrases.txt`.

### Exercice 2 — Vérifier l’intégrité d’un fichier

Une **somme de contrôle** (ou empreinte) est calculée à partir de tous les octets d’un fichier : la moindre modification du contenu la change.

> **Question 20** — Exécutez les commandes suivantes dans l’ordre et expliquez chaque résultat. Pourquoi `touch` ne change-t-il pas l’empreinte ? À quoi sert une empreinte quand on télécharge une image ISO de Linux ?
>
> ```bash
> a) $ md5sum phrases.txt > phrases.md5
> b) $ cat phrases.md5
> c) $ md5sum -c phrases.md5
> d) $ touch phrases.txt
> e) $ md5sum -c phrases.md5
> f) $ echo "fin" >> phrases.txt
> g) $ md5sum -c phrases.md5
> ```

_Remarque : MD5 n’est plus considéré comme sûr face à une falsification volontaire ; les distributions publient aujourd’hui des empreintes SHA-256 (`sha256sum`)._

### Exercice 3 — Deux programmes qui collaborent

L’objectif de cet exercice est d’apprendre à adapter des commandes à ses propres besoins.

> **Question 21** — Sans utiliser `sed` ni `awk`, combinez deux commandes vues dans ce TP pour afficher uniquement la **deuxième** ligne du fichier `phrases.txt`. Comment afficher la ligne n° _n_ ?

### Exercice 4 — Surveiller un fichier

L’administrateur d’un système est souvent amené à surveiller en direct le contenu de certains fichiers, par exemple les fichiers de journalisation (_logs_). Pour cet exercice, ouvrez **deux terminaux** : l’un pour suivre le fichier, l’autre pour le modifier.

> **Question 22** — Trouvez l’option de la commande `tail` qui affiche les nouvelles lignes au fur et à mesure qu’elles sont ajoutées. Créez le fichier avec `touch journal.txt`, puis lancez `tail` avec cette option sur `journal.txt` dans le premier terminal ; dans le second (placé dans le même répertoire), exécutez plusieurs fois `date >> journal.txt`. Qu’observez-vous ? Comment arrêter le suivi ?

### Exercice 5 — Combien d’encodages ?

> **Question 23** — La commande `iconv -l` liste les jeux de caractères connus. Donnez la ligne de commande qui affiche leur nombre. Pourquoi ce nombre n’est-il qu’une approximation du nombre réel d’encodages ?

---

## Questions de révision

Ces questions vous permettent de vérifier que vous avez identifié et compris les points clés du TP. Répondez-y sans refaire les manipulations.

> **Question 24** — Quel est le rôle d’un shell ? Qu’est-ce que bash ?

> **Question 25** — Quels sont les trois flux standard d’un processus, leurs numéros et leur destination par défaut ?

> **Question 26** — Quelle est la différence entre une redirection `>` et un tube `|` ?

> **Question 27** — Quelle est la différence entre un fichier texte et un fichier binaire ? Un document Word est-il un fichier texte ?

> **Question 28** — Que signifie l’extension `.txt` à la fin d’un nom de fichier pour le système ? Comment connaître le type réel d’un fichier ?

> **Question 29** — Est-il possible de supprimer des caractères au milieu d’un fichier texte en utilisant les services de base de l’OS ? Comment fait alors un éditeur de texte ?

> **Question 30** — Pourquoi la chaîne « Hello world », suivie d’un retour à la ligne, occupe-t-elle 12 octets sous Linux ? Combien en occuperait-elle dans un fichier Windows ?

> **Question 31** — Combien d’octets occupe le caractère `é` en UTF-8 ? En ISO 8859-1 ? Et le caractère `e` ?

---

## Bilan

- Un fichier texte n’est qu’une **suite d’octets** ; seul le **codage** (ASCII, ISO 8859-1, UTF-8…) permet de les interpréter comme des caractères. L’extension du nom ne compte pas : `file` examine le contenu.
- Le shell **redirige** les flux standard (`>`, `>>`, `<`, `2>`) et **relie** les commandes par des tubes (`|`).
- L’OS ne sait que remplacer des octets ou en ajouter à la fin : insérer ou supprimer du texte est le travail d’un éditeur.
- Les **fins de ligne** (LF ou CR+LF) et l’**encodage** des caractères sont les deux pièges des échanges de fichiers texte entre systèmes.

UTF-8 est aujourd’hui largement majoritaire, mais on rencontre encore des fichiers dans d’autres encodages : anciens fichiers, exports de logiciels, fichiers Windows. Les risques d’échange entre systèmes hétérogènes concernent :

- l’utilisation des flux de texte dans les programmes
- les échanges sur internet
- les noms de fichiers et de répertoires

Par précaution (et le technicien informatique est prudent !), il est donc conseillé de ne jamais utiliser de caractères étendus ou spéciaux (comme l’espace) dans les noms de fichiers et de répertoires, de privilégier l’encodage Unicode et d’être cohérent avec les fichiers qui permettent de déclarer l’encodage utilisé (cas des fichiers **html** et **xml** par exemple).

## Pour aller plus loin

- `file -i fichier` affiche le type MIME et l’encodage d’un fichier.
- Une boucle `while` lit un fichier ligne par ligne, grâce à la redirection `<` : `while read ligne; do echo "contenu : $ligne"; done < phrases.txt`
- La commande `recode` (paquet `recode`) convertit elle aussi les encodages : `recode -l` liste ceux qu’elle connaît.

---

[Cours GNU/Linux](../README.md#travaux-pratiques) · **TP 1 / 5** · [TP 2 →](tp2-fichiers-executables.md)
