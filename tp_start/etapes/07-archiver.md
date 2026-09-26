[Sommaire](../readme.md) · [← Étape 6](06-filtres-pipes.md) · **Étape 7 / 10** · [Étape 8 →](08-liens-permissions.md)

# Étape 7 — Archiver et compresser

- **Objectif** : regrouper un dossier dans une archive compressée, en lister le contenu, puis l'extraire
- **Commandes** : `tar`
- **À produire** : l'archive `workspace/data_archive.tgz`, sa liste et son extraction dans `workspace/tmp/`
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Pour partager ou sauvegarder plusieurs fichiers/dossiers, on les regroupe dans une **archive** unique, souvent **compressée** pour économiser de l'espace.

- **Archive** : regroupe plusieurs fichiers et dossiers en un seul fichier (comme un "sac"). Le format `tar` (Tape ARchive) est le standard sous Linux
- **Compression** : réduit la taille des données. `gzip` est un algorithme de compression courant (extension `.gz`) ; une archive tar compressée = `.tar.gz` ou `.tgz`
- **Opérations sur les archives** :
  - **Créer** : rassembler des fichiers dans une archive
  - **Lister** : voir le contenu sans extraire
  - **Extraire** : récupérer les fichiers originaux

### Les options de `tar`

Elles sont souvent combinées (ex: `-czf` = create + gzip + file).

| Option | Signification | Rôle |
|---|---|---|
| `-c` | create | créer |
| `-x` | extract | extraire |
| `-t` | test/list | lister |
| `-z` | gzip | compresser/décompresser |
| `-f` | file | spécifier le nom de l'archive |
| `-C` | change directory | extraire vers un répertoire spécifique |

Une commande `tar` choisit toujours **une** opération (`-c`, `-t` ou `-x`) ; `-f` doit être suivi du nom de l'archive.

---

## À réaliser

### Tâche 1 — Créer une archive compressée

Depuis le dossier du TP, créer une archive compressée `workspace/data_archive.tgz` contenant tout le dossier `data/`.

- **Résultat** : le fichier `workspace/data_archive.tgz`
- **Documentation** : [`man tar`](#man-tar)

Pour contrôler :

```bash
ls -l workspace/data_archive.tgz
```

<details>
<summary>💡 Indice</summary>

Cherchez dans l'extrait de `man tar` les options create, gzip et file. `-f` doit être immédiatement suivi du nom de l'archive ; viennent ensuite les fichiers à archiver. L'archive garde les chemins tels qu'ils ont été donnés à la création : archivez `data` depuis le dossier du TP pour que les chemins commencent par `data/`.

</details>

### Tâche 2 — Lister le contenu de l'archive

Lister le contenu de l'archive et enregistrer cette liste dans `workspace/preuves/contenu_archive.txt`.

- **Résultat** : le fichier `workspace/preuves/contenu_archive.txt`, où chaque chemin commence par `data/`
- **Documentation** : [`man tar`](#man-tar)

Pour contrôler :

```bash
cat workspace/preuves/contenu_archive.txt
```

<details>
<summary>💡 Indice</summary>

`tar` doit savoir quoi faire (lister), avec quel filtre (gzip) et sur quelle archive (`-f`). Affichez la liste à l'écran, puis ajoutez la redirection.

</details>

### Tâche 3 — Extraire l'archive

Extraire l'archive dans `workspace/tmp/`.

- **Résultat** : le dossier `workspace/tmp/data/`, identique à `data/`
- **Documentation** : [`man tar`](#man-tar)

Pour contrôler :

```bash
ls -a workspace/tmp/data
```

<details>
<summary>💡 Indice</summary>

Sans `-C`, `tar` extrait dans le répertoire courant : `-C` indique le dossier de destination.

</details>

---

## Documentation

### `man tar`

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

---

## Valider

```bash
python3 verify.py 7
```

Quand tout est juste :

```text
  → Étape 7 validée (3/3). Étape suivante : 8 (etapes/08-liens-permissions.md).
```

---

[Sommaire](../readme.md) · [← Étape 6](06-filtres-pipes.md) · **Étape 7 / 10** · [Étape 8 →](08-liens-permissions.md)
