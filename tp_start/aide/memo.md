[Sommaire](../readme.md) · Aides : **Aide-mémoire** · [Guide de man](man.md) · [Script de vérification](verification.md) · [Dépannage](depannage.md)

# Aide-mémoire

Tout ce qui sert souvent pendant le TP, sur une seule page. Pour le détail d'une commande : le lien vers son étape, ou `man <commande>`.

- [Raccourcis clavier](#raccourcis-clavier)
- [Chemins](#chemins)
- [Redirections, pipe et arrière-plan](#redirections-pipe-et-arrière-plan)
- [Jokers et guillemets](#jokers-et-guillemets)
- [Variables utiles](#variables-utiles)
- [Commandes du TP](#commandes-du-tp)

---

## Raccourcis clavier

| Touche | Effet |
|---|---|
| `Tab` | compléter un nom de commande, de fichier ou de dossier (deux fois : afficher les possibilités) |
| `↑` / `↓` | rappeler les commandes précédentes |
| `Ctrl+R` | rechercher dans l'historique |
| `Ctrl+C` | interrompre la commande en cours |
| `Ctrl+L` | effacer l'écran |
| `q` | quitter `man` (ou `less`) |

---

## Chemins

| Notation | Signification | Exemple |
|---|---|---|
| `/` | la racine de l'arborescence | `cd /` |
| `~` | votre dossier personnel | `cd ~` |
| `.` | le dossier courant | `./salut.sh` |
| `..` | le dossier parent | `cd ..` |
| commence par `/` | chemin **absolu**, depuis la racine | `/home/fab/intro_linux_tp` |
| ne commence pas par `/` | chemin **relatif**, depuis le répertoire courant | `data/fruits.txt` |

```bash
pwd       # où suis-je ?
ls        # qu'y a-t-il ici ?
cd -      # revenir au dossier précédent
```

---

## Redirections, pipe et arrière-plan

```text
commande > fichier      écrit la sortie dans fichier (écrase son contenu)
commande >> fichier     ajoute la sortie à la fin de fichier
commande < fichier      fournit le contenu de fichier comme entrée de la commande
cmd1 | cmd2             envoie la sortie de cmd1 à l'entrée de cmd2 (pipe)
commande &              lance la commande en arrière-plan
```

> [!CAUTION]
> Ne redirigez jamais vers le fichier que vous lisez : `sort f > f` vide `f`.

Détails : [étape 3](../etapes/03-creer.md) (`>` et `>>`), [étape 6](../etapes/06-filtres-pipes.md) (`|` et `<`), [étape 10](../etapes/10-processus.md) (`&`).

---

## Jokers et guillemets

| Joker | Remplace | Exemple |
|---|---|---|
| `*` | n'importe quelle séquence de caractères | `*fruits*` : tout nom contenant « fruits » |
| `?` | un seul caractère | `F??` : `Foo`, `FOO`... |

Le shell remplace lui-même les jokers par les noms de fichiers du dossier courant. Pour transmettre un motif tel quel à une commande (`find`), écrivez-le entre guillemets : `"*fruits*"`.

---

## Variables utiles

| Variable | Contenu |
|---|---|
| `$HOME` | votre dossier personnel |
| `$PWD` | le répertoire courant |
| `$USER` | votre nom d'utilisateur |
| `$PATH` | les dossiers où le shell cherche les commandes |

```bash
echo $HOME
```

---

## Commandes du TP

| Commande | Rôle | Options vues | Étape |
|---|---|---|---|
| `man` | page de manuel | `-k` | [1](../etapes/01-aide-historique.md) |
| `--help` | aide rapide d'un programme | | [1](../etapes/01-aide-historique.md) |
| `help` | aide d'une commande intégrée à Bash | | [1](../etapes/01-aide-historique.md) |
| `history` | historique des commandes | `N` (les N dernières) | [1](../etapes/01-aide-historique.md) |
| `date` | date et heure | | [1](../etapes/01-aide-historique.md) |
| `pwd` | afficher le répertoire courant | | [2](../etapes/02-arborescence.md) |
| `cd` | changer de répertoire courant | `..` `-` | [2](../etapes/02-arborescence.md) |
| `ls` | lister le contenu d'un dossier | `-a` `-l` | [2](../etapes/02-arborescence.md) |
| `cat` | afficher le contenu d'un fichier | `-n` | [2](../etapes/02-arborescence.md), [3](../etapes/03-creer.md) |
| `mkdir` | créer des dossiers | `-p` | [3](../etapes/03-creer.md) |
| `touch` | créer un fichier vide | | [3](../etapes/03-creer.md) |
| `echo` | afficher un texte | | [3](../etapes/03-creer.md) |
| `cp` | copier | `-R` `-i` `-v` | [4](../etapes/04-copier-deplacer-supprimer.md) |
| `mv` | déplacer ou renommer | | [4](../etapes/04-copier-deplacer-supprimer.md) |
| `rm` | supprimer | `-r` `-i` | [4](../etapes/04-copier-deplacer-supprimer.md) |
| `rmdir` | supprimer un dossier vide | | [4](../etapes/04-copier-deplacer-supprimer.md) |
| `find` | chercher des fichiers | `-name` `-iname` | [5](../etapes/05-rechercher.md) |
| `grep` | chercher du texte dans des fichiers | `-i` `-n` | [5](../etapes/05-rechercher.md) |
| `which` | chemin complet d'un exécutable | | [5](../etapes/05-rechercher.md) |
| `type` | type d'une commande (alias, primitive, fichier) | | [5](../etapes/05-rechercher.md) |
| `head` / `tail` | premières / dernières lignes | `-n` | [6](../etapes/06-filtres-pipes.md) |
| `sort` | trier des lignes | `-f` `-r` | [6](../etapes/06-filtres-pipes.md) |
| `uniq` | supprimer les lignes identiques consécutives | `-c` | [6](../etapes/06-filtres-pipes.md) |
| `wc` | compter lignes, mots, octets | `-l` `-w` `-c` | [6](../etapes/06-filtres-pipes.md) |
| `tr` | remplacer des caractères | `[:lower:]` `[:upper:]` | [6](../etapes/06-filtres-pipes.md) |
| `cut` | extraire des colonnes | `-d` `-f` | [6](../etapes/06-filtres-pipes.md) |
| `tar` | archiver | `-c` `-t` `-x` `-z` `-f` `-C` | [7](../etapes/07-archiver.md) |
| `ln` | créer un lien | `-s` | [8](../etapes/08-liens-permissions.md) |
| `chmod` | modifier les permissions | notation octale | [8](../etapes/08-liens-permissions.md) |
| `export` | exporter une variable vers les processus enfants | | [9](../etapes/09-variables-alias.md) |
| `alias` | créer ou lister des alias | | [9](../etapes/09-variables-alias.md) |
| `env` / `printenv` | afficher les variables exportées | | [9](../etapes/09-variables-alias.md) |
| `ps` | lister des processus | `-u` | [10](../etapes/10-processus.md) |
| `jobs` | lister les tâches du shell | | [10](../etapes/10-processus.md) |
| `pgrep` / `pkill` | trouver / terminer des processus par leur nom | `-u` | [10](../etapes/10-processus.md) |
| `kill` | envoyer un signal à un processus | | [10](../etapes/10-processus.md) |
| `df` | espace disque | `-h` | [10](../etapes/10-processus.md) |

---

[Sommaire](../readme.md) · Aides : **Aide-mémoire** · [Guide de man](man.md) · [Script de vérification](verification.md) · [Dépannage](depannage.md)
