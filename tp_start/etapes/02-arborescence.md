[Sommaire](../readme.md) · [← Étape 1](01-aide-historique.md) · **Étape 2 / 10** · [Étape 3 →](03-creer.md)

# Étape 2 — Se repérer dans l'arborescence

- **Objectif** : savoir où l'on est, lister le contenu d'un dossier, se déplacer, et désigner un fichier par un chemin absolu ou relatif
- **Commandes** : `pwd` · `cd` · `ls` · `cat`
- **À produire** : 4 réponses (le script vous les demandera)
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Sous Linux, tout est organisé en arborescence de fichiers et dossiers, à partir de la racine `/`. Lorsque vous travaillez dans un terminal, vous êtes toujours "quelque part" dans cette arborescence : c'est le **répertoire courant** (ou répertoire de travail).

### Chemins absolus et relatifs

- **Chemin absolu** : commence par `/` et décrit le chemin complet depuis la racine (ex: `/home/user/Documents`)
- **Chemin relatif** : décrit le chemin depuis le répertoire courant (ex: `Documents/projet`)
- **Noms spéciaux** : `.` désigne le dossier courant, `..` le dossier parent, `~` votre dossier personnel
- **Variables d'environnement** : `$HOME` contient le chemin de votre dossier personnel, `$PWD` contient le répertoire courant

Le dossier du TP, vu comme une arborescence :

```text
tp_start/                ← le dossier du TP
├── data/
│   └── fruits.txt
└── workspace/
    └── preuves/
```

### Se déplacer

```bash
cd dossier    # entrer dans un dossier
cd ..         # remonter au dossier parent
cd            # revenir au dossier personnel
cd -          # revenir au dossier précédent
```

### Fichiers cachés

Sous Linux, tout fichier dont le nom commence par `.` est considéré comme "caché" (ex: `.bashrc`) : `ls` ne l'affiche pas sans option.

> [!TIP]
> La touche **Tab** complète les noms de fichiers et de dossiers : tapez `cat data/fr` puis Tab. Moins de frappe, moins de fautes.

---

## À réaliser

> [!IMPORTANT]
> Commencez dans le dossier du TP (`tp_start`).

### Tâche 1 — Où suis-je ?

Depuis le dossier du TP, afficher le chemin absolu du répertoire courant (pour savoir où vous êtes).

- **Résultat** : le chemin absolu du dossier du TP, que le script vous demandera
- **Documentation** : [`help pwd`](#help-pwd)

### Tâche 2 — Trouver le fichier caché

Lister toutes les entrées de `data/`, y compris les fichiers cachés, puis afficher le contenu du fichier caché qui s'y trouve.

- **Résultat** : le mot secret écrit dans ce fichier, que le script vous demandera
- **Documentation** : [`man ls`](#man-ls) · [`man cat`](#man-cat)

<details>
<summary>💡 Indice</summary>

`ls` n'affiche pas les fichiers dont le nom commence par un point : cherchez l'option de `ls` qui les montre, puis affichez le fichier avec `cat`.

</details>

### Tâche 3 — Lire un listing détaillé

Afficher un listing détaillé de `data/` montrant les permissions, propriétaires, tailles et dates, et relever la taille de `sample.csv` en octets.

- **Résultat** : la taille en octets, que le script vous demandera
- **Documentation** : [`man ls`](#man-ls)

<details>
<summary>💡 Indice</summary>

Dans un listage détaillé, la taille en octets est la colonne juste avant la date.

</details>

### Tâche 4 — Utiliser un chemin relatif

Se placer dans `workspace/preuves`, afficher le fichier `data/fruits.txt` avec un chemin **relatif** depuis ce dossier, puis revenir au dossier du TP.

- **Résultat** : le chemin relatif utilisé, que le script vous demandera (testez-le avec `cat` avant de répondre)
- **Documentation** : [`help cd`](#help-cd)

<details>
<summary>💡 Indice</summary>

`..` désigne le dossier parent : combien de fois faut-il remonter depuis `workspace/preuves` pour revenir au dossier du TP ? Aidez-vous de l'arborescence de la partie [Comprendre](#chemins-absolus-et-relatifs).

</details>

---

## Documentation

### `help pwd`

```text
$ help pwd
pwd: pwd [-LP]
    Affiche le nom du répertoire de travail courant.
```

### `help cd`

```text
$ help cd
cd: cd [-L|[-P [-e]] [-@]] [rép]
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is the value of the
    HOME shell variable. If DIR is "-", it is converted to $OLDPWD.
```

### `man ls`

```text
$ man ls
SYNOPSIS
       ls [OPTION]... [FILE]...

       -a, --all
              do not ignore entries starting with .

       -l     use a long listing format
```

`ls -a` n'ignore pas les entrées commençant par un point ; `ls -l` utilise le format long (détaillé). Vous pouvez combiner plusieurs options, par exemple `-la` ou `-l -a`.

### `man cat`

```text
$ man cat
SYNOPSIS
       cat [OPTION]... [FILE]...
DESCRIPTION
       Concatenate FILE(s) to standard output.
```

`cat` affiche le contenu des fichiers donnés en argument.

---

## Valider

Depuis le dossier du TP :

```bash
python3 verify.py 2
```

Le script vous demande le chemin absolu, le mot secret, la taille et le chemin relatif.

Quand tout est juste :

```text
  → Étape 2 validée (4/4). Étape suivante : 3 (etapes/03-creer.md).
```

---

[Sommaire](../readme.md) · [← Étape 1](01-aide-historique.md) · **Étape 2 / 10** · [Étape 3 →](03-creer.md)
