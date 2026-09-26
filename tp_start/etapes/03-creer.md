[Sommaire](../readme.md) · [← Étape 2](02-arborescence.md) · **Étape 3 / 10** · [Étape 4 →](04-copier-deplacer-supprimer.md)

# Étape 3 — Créer dossiers et fichiers

- **Objectif** : organiser son espace de travail en créant des dossiers et des fichiers
- **Commandes** : `mkdir` · `touch` · `echo` · `cat`
- **À produire** : l'arborescence de `workspace/` ci-dessous
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Pour organiser votre travail, vous devez savoir créer des dossiers et des fichiers. Linux distingue plusieurs façons de créer et manipuler des fichiers texte.

### Créer des dossiers

Utile pour organiser vos fichiers en arborescence. L'**option -p** crée les dossiers parents manquants (ex: `docs/rapports/2024` crée les trois niveaux d'un coup).

### Créer des fichiers

- **Fichiers vides** : parfois on a besoin de créer un fichier sans contenu (pour le remplir plus tard)
- **Fichiers cachés** : nommer un fichier `.cache` ou `.config` le rend invisible au listage normal

### Écrire dans un fichier : les redirections

- `>` : écrit dans un fichier (écrase le contenu existant)
- `>>` : ajoute à la fin d'un fichier (sans écraser)

```bash
echo "première ligne" > fichier.txt     # crée fichier.txt, ou remplace son contenu
echo "deuxième ligne" >> fichier.txt    # ajoute une ligne à la fin
```

---

## À réaliser

À la fin de l'étape, `workspace/` doit ressembler à ceci :

```text
workspace/
├── data/
│   └── todo.txt          (tâche 3)
├── docs/
│   └── bonjour.txt       (tâche 5)
├── preuves/
├── projets/
│   └── 2026/
│       └── janvier/      (tâche 2)
└── tmp/
    └── .cache            (tâche 4)
```

### Tâche 1 — Créer trois dossiers

Créer les dossiers `docs`, `data` et `tmp` dans `workspace/` (une seule commande suffit).

- **Résultat** : les dossiers `workspace/docs/`, `workspace/data/` et `workspace/tmp/`
- **Documentation** : [`man mkdir`](#man-mkdir)

Pour contrôler :

```bash
ls workspace
```

<details>
<summary>💡 Indice</summary>

`mkdir` accepte plusieurs dossiers dans une même commande. Les dossiers doivent être créés **dans** `workspace/` : si vous êtes dans le dossier du TP, chaque nom commence donc par `workspace/`.

</details>

### Tâche 2 — Créer une arborescence en une commande

Créer en une seule commande l'arborescence `workspace/projets/2026/janvier`.

- **Résultat** : le dossier `workspace/projets/2026/janvier/`
- **Documentation** : [`man mkdir`](#man-mkdir)

Pour contrôler :

```bash
ls workspace/projets/2026
```

<details>
<summary>💡 Indice</summary>

Sans option, `mkdir` refuse de créer `janvier` tant que `projets/2026` n'existe pas : cherchez dans l'extrait de `man mkdir` l'option qui crée aussi les dossiers parents manquants.

</details>

### Tâche 3 — Créer un fichier vide

Créer un fichier vide nommé `todo.txt` dans `workspace/data`.

- **Résultat** : le fichier `workspace/data/todo.txt`
- **Documentation** : [`man touch`](#man-touch)

Pour contrôler :

```bash
ls -l workspace/data
```

### Tâche 4 — Créer un fichier caché

Créer un fichier caché nommé `.cache` dans `workspace/tmp`.

- **Résultat** : le fichier `workspace/tmp/.cache`
- **Documentation** : [`man touch`](#man-touch)

Pour contrôler (sans `-a`, le fichier n'apparaît pas) :

```bash
ls -a workspace/tmp
```

### Tâche 5 — Écrire un fichier de deux lignes

Créer le fichier `workspace/docs/bonjour.txt` contenant au moins 2 lignes de texte, puis l'afficher avec les numéros de ligne.

- **Résultat** : le fichier `workspace/docs/bonjour.txt`, avec au moins 2 lignes
- **Documentation** : [`help echo`](#help-echo) · [`man cat`](#man-cat)

<details>
<summary>💡 Indice</summary>

`echo` affiche un texte ; la redirection `>` envoie cet affichage dans un fichier. Attention : `>` remplace tout le contenu du fichier, `>>` ajoute à la fin. Relisez l'exemple de la partie [Comprendre](#écrire-dans-un-fichier--les-redirections).

</details>

---

## Documentation

### `man mkdir`

```text
$ man mkdir
SYNOPSIS
       mkdir [OPTION]... DIRECTORY...

       -p, --parents
              no error if existing, make parent directories as needed
```

`mkdir -p` crée aussi les dossiers parents manquants, sans erreur s'ils existent déjà.

### `man touch`

```text
$ man touch
SYNOPSIS
       touch [OPTION]... FILE...

       A FILE argument that does not exist is created empty, unless -c or -h
       is supplied.
```

`touch` crée vide un fichier qui n'existe pas.

### `help echo`

```text
$ help echo
echo: echo [-neE] [arg ...]
    Écrit les arguments sur la sortie standard.

    Affiche les ARGs, séparés par une espace, sur la sortie standard, suivis
    d'un retour à la ligne.
```

Les redirections `>` et `>>` permettent d'écrire la sortie d'une commande dans un fichier.

### `man cat`

```text
$ man cat
       -n, --number
              number all output lines
```

---

## Valider

```bash
python3 verify.py 3
```

Quand tout est juste :

```text
  → Étape 3 validée (5/5). Étape suivante : 4 (etapes/04-copier-deplacer-supprimer.md).
```

---

[Sommaire](../readme.md) · [← Étape 2](02-arborescence.md) · **Étape 3 / 10** · [Étape 4 →](04-copier-deplacer-supprimer.md)
