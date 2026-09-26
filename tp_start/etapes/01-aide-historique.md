[Sommaire](../readme.md) · **Étape 1 / 10** · [Étape 2 →](02-arborescence.md)

# Étape 1 — Trouver de l'aide, historique, horloge

- **Objectif** : savoir s'auto-documenter, c'est-à-dire trouver de l'aide rapidement et réutiliser ses commandes précédentes
- **Commandes** : `man` · `--help` · `help` · `history` · `date`
- **À produire** : 3 réponses (le script vous les demandera) et le fichier `workspace/preuves/historique.txt`
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

Un bon développeur Linux sait **s'auto-documenter** : trouver de l'aide rapidement, réutiliser des commandes précédentes, et utiliser les outils système.

### Les pages de manuel : `man`

Documentation complète de toutes les commandes.

```bash
man ls        # ouvrir la page de manuel de ls
man -k mot    # lister les commandes dont la description contient « mot »
```

- Structure standard : NAME, SYNOPSIS, DESCRIPTION, OPTIONS, EXAMPLES...
- Navigation : espace (page suivante), `/mot` (rechercher), `n` (occurrence suivante), `q` (quitter)
- Sections : man 1 (commandes), man 3 (fonctions C), man 5 (formats de fichiers)...
- Recherche par mot-clé : `man -k mot` liste les commandes dont la description contient ce mot, utile quand on ne connaît pas encore le nom de la commande

Tout le détail est dans le [guide de man](../aide/man.md).

### L'aide rapide : `--help`

Résumé court, affiché directement dans le terminal : plus rapide que man pour une référence rapide.

```bash
ls --help     # affiche les options de ls
```

### L'aide des commandes intégrées : `help`

Certaines commandes, comme `history` ou `cd`, sont intégrées à Bash (*builtin*) : elles n'ont pas de page man, leur aide s'obtient avec `help` (en français si le système est en français).

```bash
help history
```

### L'historique des commandes

Bash garde en mémoire vos commandes précédentes.

| Commande ou touche | Effet |
|---|---|
| `history` | affiche l'historique complet |
| `↑` / `↓` | naviguer dans l'historique |
| `!n` | ré-exécuter la commande numéro n |
| `!!` | ré-exécuter la dernière commande |
| `!grep` | ré-exécuter la dernière commande commençant par "grep" |
| `Ctrl+R` | recherche interactive dans l'historique |

### La date : `date`

`date` affiche (ou configure) la date et l'heure.

### Enregistrer un résultat : la redirection `>`

Aperçu, détaillée à l'étape 3 : `commande > fichier` enregistre dans un fichier ce que la commande aurait affiché à l'écran. C'est ainsi que vous transmettez un résultat au script de vérification.

```text
commande > fichier
```

---

## À réaliser

> [!IMPORTANT]
> Placez-vous dans le dossier du TP (`tp_start`) : toutes les commandes du TP s'y tapent, sauf indication contraire.

### Tâche 1 — Chercher une option dans le manuel

Ouvrir la page de manuel de `ls`, y chercher le mot "size", trouver l'option courte qui trie les fichiers par taille (du plus gros au plus petit), puis quitter.

```bash
man ls
```

- **Résultat** : le nom de l'option, que le script vous demandera
- **Documentation** : [navigation et recherche dans man](../aide/man.md#navigation-dans-man)

<details>
<summary>💡 Indice</summary>

Dans la page, tapez `/size` puis Entrée : `n` passe à l'occurrence suivante, `q` quitte. Attention, les options sont sensibles à la casse : `-s` et `-S` sont deux options différentes.

</details>

### Tâche 2 — Afficher une autre date

Avec l'aide rapide `date --help`, trouver comment afficher une autre date que celle du jour, puis afficher le jour de la semaine du 1er janvier 2030.

```bash
date --help
```

- **Résultat** : le jour de la semaine, que le script vous demandera

<details>
<summary>💡 Indice</summary>

Cherchez l'option qui affiche une date décrite par une chaîne (« not 'now' »), puis donnez-lui `2030-01-01`.

</details>

### Tâche 3 — Trouver une commande par mot-clé

Avec `man -k`, trouver la commande dont la description est "print name of current/working directory".

- **Résultat** : le nom de la commande, que le script vous demandera
- **Documentation** : [`man man`](#man-man)

<details>
<summary>💡 Indice</summary>

`man -k directory` liste toutes les commandes dont la description contient « directory » ; un mot plus précis (working) réduit la liste.

</details>

### Tâche 4 — Enregistrer l'historique

Enregistrer vos 10 dernières commandes dans un fichier :

```bash
history 10 > workspace/preuves/historique.txt
```

- **Résultat** : le fichier `workspace/preuves/historique.txt`
- **Documentation** : [`help history`](#help-history)

Pour contrôler :

```bash
cat workspace/preuves/historique.txt
```

---

## Documentation

Extraits réels des pages de manuel (en anglais) et de l'aide `help` (en français). Pour la page complète : `man <commande>` ou `help <commande>`.

### `man man`

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
```

`man -k mot` cherche dans les descriptions courtes (la ligne NAME de chaque page) : rapide. `man -K mot` cherche dans le texte complet de toutes les pages : lent.

### `help history`

```text
$ help history
history: history [-c] [-d décalage] [n] ou history -anrw [nomfichier] ou history -ps arg [arg...]
    Affiche ou manipule l'historique.

    Affiche l'historique avec les numéros de lignes en préfixant chaque élément
    modifié d'un « * ».  Un argument égal à N limite la liste aux N derniers éléments.
```

`history` est une commande intégrée (builtin) de Bash : elle n'a pas de page man, son aide s'obtient avec `help history` (en français si le système est en français).

---

## Valider

```bash
python3 verify.py 1
```

Le script vous pose les questions des tâches 1 à 3 : tapez votre réponse puis Entrée (Entrée seule pour passer une question). Les bonnes réponses sont mémorisées et ne sont plus redemandées. Pour chaque ligne ✘, lisez les explications ↳, corrigez, puis relancez.

Quand tout est juste :

```text
  → Étape 1 validée (4/4). Étape suivante : 2 (etapes/02-arborescence.md).
```

---

[Sommaire](../readme.md) · **Étape 1 / 10** · [Étape 2 →](02-arborescence.md)
