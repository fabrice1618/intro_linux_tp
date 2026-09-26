[Sommaire](../readme.md) · [← Étape 7](07-archiver.md) · **Étape 8 / 10** · [Étape 9 →](09-variables-alias.md)

# Étape 8 — Liens symboliques et permissions

- **Objectif** : créer un raccourci vers un fichier, lire et modifier les droits d'accès, rendre un script exécutable
- **Commandes** : `ln` · `chmod` · `cp`
- **À produire** : le lien `workspace/data/link_fruits.txt`, les droits de deux fichiers
- **Prérequis** : étape 6 validée (elle crée `workspace/data/fruits_uniques.txt`)
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Sous Linux, les **liens symboliques** permettent de créer des raccourcis, et les **permissions** contrôlent qui peut lire, écrire ou exécuter chaque fichier.

### Lien symbolique (symlink)

Un "pointeur" vers un autre fichier ou dossier.

- Comme un raccourci Windows, mais plus puissant
- Si on supprime la cible, le lien devient "cassé"
- Utile pour : accès rapide, compatibilité, organisation

### Permissions Linux

Système rwx (read, write, execute) pour 3 catégories :

- **Propriétaire (user)** : le créateur du fichier
- **Groupe (group)** : les utilisateurs du même groupe
- **Autres (others)** : tout le reste du monde

Pour voir les permissions, `ls -l` affiche le format `-rwxrwxrwx` :

```text
-rw-r--r-- 1 fab fab 65 sept. 26 20:39 fruits.txt
│└┬┘└┬┘└┬┘
│ │  │  └── autres (others)
│ │  └───── groupe (group)
│ └──────── propriétaire (user)
└────────── type : - fichier, d dossier, l lien symbolique
```

### Notation octale

Représentation numérique des permissions : r (read) = 4, w (write) = 2, x (execute) = 1. Chaque chiffre additionne ces valeurs : le 1er pour le propriétaire, le 2e pour le groupe, le 3e pour les autres.

| Octal | Symbolique | Propriétaire (user) | Groupe (group) | Autres (others) |
|---|---|---|---|---|
| `640` | `rw-r-----` | lecture+écriture | lecture | rien |
| `755` | `rwxr-xr-x` | tout | lecture+exécution | lecture+exécution |
| `644` | `rw-r--r--` | lecture+écriture | lecture seule | lecture seule |

### Exécuter un script

Un fichier ne peut être lancé comme une commande que s'il a le droit `x`, sinon le shell répond « Permission non accordée ». Le shell ne cherche les commandes que dans les dossiers du `PATH` : pour lancer un script du dossier courant, on précise son chemin (`./salut.sh`).

---

## À réaliser

### Tâche 1 — Créer un lien symbolique

Créer un lien symbolique `workspace/data/link_fruits.txt` qui pointe vers le fichier `data/fruits.txt` (utilisez le chemin absolu ou relatif approprié).

- **Résultat** : le lien `workspace/data/link_fruits.txt`, qui affiche le contenu de `data/fruits.txt`
- **Documentation** : [`man ln`](#man-ln)

Pour contrôler (la flèche `->` indique la cible du lien, et `cat` doit afficher les fruits) :

```bash
ls -l workspace/data/link_fruits.txt
cat workspace/data/link_fruits.txt
```

<details>
<summary>💡 Indice</summary>

Syntaxe lien : `commande -s chemin_cible nom_du_lien`. Un chemin cible relatif est interprété depuis le dossier du **lien** (`workspace/data/`), pas depuis votre répertoire courant : c'est le même raisonnement qu'à l'[étape 2](02-arborescence.md). Un chemin absolu (qui commence par `/`) fonctionne aussi. Si le lien est cassé, supprimez-le avec `rm` avant de le recréer.

</details>

### Tâche 2 — Modifier des permissions

Changer les permissions de `workspace/data/fruits_uniques.txt` en `640` (rw-r-----).

- **Résultat** : `ls -l` affiche `-rw-r-----` pour ce fichier
- **Documentation** : [`man chmod`](#man-chmod)

Pour contrôler :

```bash
ls -l workspace/data/fruits_uniques.txt
```

### Tâche 3 — Rendre un script exécutable

Copier le script `data/salut.sh` dans `workspace/`, essayer de le lancer, lui donner les permissions `755` (rwxr-xr-x), puis le relancer.

Pour le lancer, depuis le dossier du TP :

```bash
./workspace/salut.sh
```

- **Résultat** : `workspace/salut.sh`, copie de `data/salut.sh`, avec les droits `755` ; le second lancement affiche un message de bienvenue
- **Documentation** : [`man chmod`](#man-chmod) · [`man cp`](04-copier-deplacer-supprimer.md#man-cp) (étape 4)

<details>
<summary>💡 Indice</summary>

Le premier lancement doit échouer avec « Permission non accordée » : c'est normal, le fichier n'a pas le droit `x`. 7 = 4+2+1 (rwx), 5 = 4+1 (r-x).

</details>

---

## Documentation

### `man ln`

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
```

- Syntaxe lien : `commande -s chemin_cible nom_du_lien`
- Un chemin cible relatif est interprété depuis le dossier du **lien** (`workspace/data/`), pas depuis votre répertoire courant

### `man chmod`

```text
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

Avec trois chiffres, le premier concerne le propriétaire, le deuxième le groupe, le troisième les autres (les chiffres omis à gauche valent 0).

---

## Valider

```bash
python3 verify.py 8
```

Quand tout est juste :

```text
  → Étape 8 validée (3/3). Étape suivante : 9 (etapes/09-variables-alias.md).
```

---

[Sommaire](../readme.md) · [← Étape 7](07-archiver.md) · **Étape 8 / 10** · [Étape 9 →](09-variables-alias.md)
