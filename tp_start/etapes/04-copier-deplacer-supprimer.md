[Sommaire](../readme.md) · [← Étape 3](03-creer.md) · **Étape 4 / 10** · [Étape 5 →](05-rechercher.md)

# Étape 4 — Copier, déplacer, renommer, supprimer

- **Objectif** : réorganiser ses fichiers : sauvegarder, renommer, déplacer, nettoyer
- **Commandes** : `cp` · `mv` · `rm` · `rmdir`
- **À produire** : la sauvegarde `workspace/backup_data/` et le fichier `workspace/bonjour.renomme.txt`
- **Prérequis** : étape 3 validée (elle crée `bonjour.txt` et `janvier/`)
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Une fois vos fichiers créés, vous devez pouvoir les réorganiser : faire des copies de sauvegarde, déplacer des fichiers entre dossiers, renommer, ou nettoyer ce qui ne sert plus.

### Copier

Crée un duplicata du fichier/dossier source, l'original reste intact. La copie récursive (`-R` ou `-r`) est nécessaire pour copier un dossier avec tout son contenu.

### Déplacer et renommer

Sous Linux, c'est la même opération ! Déplacer un fichier dans le même dossier = le renommer.

> [!NOTE]
> **Destination existante** : si la destination est un dossier qui existe déjà, `cp` et `mv` placent la source **à l'intérieur** de ce dossier.

### Supprimer

- Fichiers : avec la commande de suppression classique
- Dossiers vides : commande spécifique dédiée aux répertoires vides
- Dossiers non vides : nécessite l'option récursive (`-r`)

Le **mode verbeux** (`-v`) affiche ce qui est fait, utile pour suivre les opérations.

> [!CAUTION]
> Il n'y a pas de "corbeille" en ligne de commande, la suppression est définitive ! Relisez le chemin avant d'appuyer sur Entrée.

---

## À réaliser

À la fin de l'étape, `workspace/` doit ressembler à ceci (extrait) :

```text
workspace/
├── backup_data/            (tâche 1 : copie de data/, sans logs/ à la tâche 5)
├── bonjour.renomme.txt     (tâches 2 et 3 : l'ancien docs/bonjour.txt)
├── docs/                   (vide)
└── projets/
    └── 2026/               (janvier/ supprimé à la tâche 4)
```

### Tâche 1 — Sauvegarder un dossier

Sauvegarder le dossier `data` : le copier, avec tout son contenu, vers `workspace/backup_data`.

- **Résultat** : le dossier `workspace/backup_data/`, avec les mêmes fichiers que `data/` (y compris le fichier caché)
- **Documentation** : [`man cp`](#man-cp)

Pour contrôler :

```bash
ls -a workspace/backup_data
```

<details>
<summary>💡 Indice</summary>

Sans option, `cp` refuse de copier un dossier (« -r non spécifié ») : cherchez l'option de copie récursive dans l'extrait de `man cp`. Lancez la copie **une seule fois** : si `workspace/backup_data` existe déjà, `cp` copie `data` à l'intérieur.

</details>

### Tâche 2 — Renommer un fichier

Renommer `workspace/docs/bonjour.txt` en `bonjour.renomme.txt` (dans le même dossier).

- **Résultat** : `workspace/docs/bonjour.renomme.txt` existe, `workspace/docs/bonjour.txt` n'existe plus
- **Documentation** : [`man mv`](#man-mv)

Pour contrôler :

```bash
ls workspace/docs
```

<details>
<summary>💡 Indice</summary>

Relisez la DESCRIPTION de `man mv` dans l'extrait : « Rename SOURCE to DEST ».

</details>

### Tâche 3 — Déplacer un fichier

Déplacer `workspace/docs/bonjour.renomme.txt` à la racine de `workspace/`.

- **Résultat** : le fichier `workspace/bonjour.renomme.txt`, avec son contenu
- **Documentation** : [`man mv`](#man-mv)

Pour contrôler :

```bash
ls workspace workspace/docs
```

<details>
<summary>💡 Indice</summary>

Quand la destination de `mv` est un dossier existant, le fichier y est déplacé en gardant son nom.

</details>

### Tâche 4 — Supprimer un dossier vide

Supprimer le dossier vide `workspace/projets/2026/janvier` (créé à l'étape 3).

- **Résultat** : `janvier/` a disparu, `workspace/projets/2026/` est toujours là
- **Documentation** : [`man rmdir`](#man-rmdir)

Pour contrôler :

```bash
ls workspace/projets/2026
```

### Tâche 5 — Supprimer un dossier et son contenu

La sauvegarde n'a pas besoin des journaux : supprimer le dossier `workspace/backup_data/logs` et son contenu.

- **Résultat** : `workspace/backup_data/logs` a disparu, l'original `data/logs` est intact
- **Documentation** : [`man rm`](#man-rm)

Pour contrôler :

```bash
ls workspace/backup_data data
```

<details>
<summary>💡 Indice</summary>

Un dossier non vide ne se supprime pas avec `rmdir` : cherchez l'option récursive de `rm`. Vérifiez deux fois le chemin : c'est la copie `workspace/backup_data/logs` qu'il faut supprimer, pas l'original `data/logs`.

</details>

---

## Pour aller plus loin

Une fois l'étape validée, cherchez comment faire les tâches 2 et 3 en une seule commande.

---

## Documentation

### `man cp`

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
```

`cp -R` copie un dossier et tout son contenu ; `-i` demande confirmation avant d'écraser ; `-v` affiche ce qui est fait.

### `man mv`

```text
$ man mv
SYNOPSIS
       mv [OPTION]... [-T] SOURCE DEST
       mv [OPTION]... SOURCE... DIRECTORY
DESCRIPTION
       Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
```

`mv` renomme SOURCE en DEST, ou déplace les SOURCEs dans DIRECTORY.

### `man rm`

```text
$ man rm
SYNOPSIS
       rm [OPTION]... [FILE]...

       -i     prompt before every removal

       -r, -R, --recursive
              remove directories and their contents recursively
```

`rm -r` supprime un dossier et son contenu.

### `man rmdir`

```text
$ man rmdir
SYNOPSIS
       rmdir [OPTION]... DIRECTORY...
DESCRIPTION
       Remove the DIRECTORY(ies), if they are empty.
```

`rmdir` ne supprime que les dossiers vides.

---

## Valider

```bash
python3 verify.py 4
```

Quand tout est juste :

```text
  → Étape 4 validée (5/5). Étape suivante : 5 (etapes/05-rechercher.md).
```

---

[Sommaire](../readme.md) · [← Étape 3](03-creer.md) · **Étape 4 / 10** · [Étape 5 →](05-rechercher.md)
