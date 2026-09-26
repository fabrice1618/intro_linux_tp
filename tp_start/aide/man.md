[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · **Guide de man** · [Script de vérification](verification.md) · [Dépannage](depannage.md)

# Guide d'utilisation de man (pages de manuel)

Le système `man` (manual) est votre référence principale pour comprendre les commandes Linux. Chaque page de manuel suit une structure standardisée et offre des fonctions de navigation et de recherche puissantes.

- [man, --help ou help ?](#man---help-ou-help-)
- [Utilisation de base](#utilisation-de-base)
- [Structure d'une page de manuel](#structure-dune-page-de-manuel)
- [Navigation dans man](#navigation-dans-man)
- [Fonctions de recherche](#fonctions-de-recherche)
- [Sections du manuel](#sections-du-manuel)
- [Astuces pour ce TP](#astuces-pour-ce-tp)

---

## man, --help ou help ?

Trois sources d'aide, selon le type de commande :

| Source | Pour quelles commandes | Exemple |
|---|---|---|
| `man commande` | les programmes installés (fichiers exécutables) : documentation complète | `man ls` |
| `commande --help` | la plupart des programmes : résumé court des options, affiché dans le terminal | `ls --help` |
| `help commande` | les commandes intégrées à Bash (*builtin*), qui n'ont pas de page man | `help cd` |

`type` indique à quelle catégorie appartient une commande :

```bash
type cd    # cd est une primitive du shell   → help cd
type ls    # ls est /usr/bin/ls              → man ls
```

---

## Utilisation de base

```bash
man <commande>        # Ouvrir la page de manuel d'une commande
man man              # Afficher l'aide sur man lui-même
man -k <mot-clé>     # Chercher des commandes par mot-clé (apropos)
whatis <commande>    # Description courte d'une commande
```

---

## Structure d'une page de manuel

Les pages man sont organisées en sections standardisées :

- **NAME** : Nom de la commande et brève description
- **SYNOPSIS** : Syntaxe d'utilisation (entre [] = optionnel, <> = obligatoire)
- **DESCRIPTION** : Description détaillée de la commande et de ses fonctionnalités
- **OPTIONS** : Liste et explication de toutes les options disponibles (-a, --verbose, etc.)
- **EXAMPLES** : Exemples d'utilisation concrets (pas toujours présent)
- **SEE ALSO** : Commandes et pages de manuel connexes
- **AUTHOR** : Auteur(s) de la commande
- **BUGS** : Bugs connus et limitations

---

## Navigation dans man

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

---

## Fonctions de recherche

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

---

## Sections du manuel

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

---

## Astuces pour ce TP

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

```bash
man -k copy
man cp
```

---

[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · **Guide de man** · [Script de vérification](verification.md) · [Dépannage](depannage.md)
