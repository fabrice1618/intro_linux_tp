# Progression pédagogique 1 : initiation à la ligne de commande

Progression en **2 séances** pour découvrir GNU/Linux et la ligne de commande. Elle alterne les apports de la [présentation](presentation.md) et la pratique guidée du [TP « Commandes de base Linux »](tp_start/readme.md), avec le mémento des [commandes de base](linux_commandes_base.md) comme référence. Les expressions régulières et les scripts shell (parties 8 et 9 de la présentation) ne sont pas au programme : ils sont traités dans la [progression 2](progression_pedagogique2.md).

**Sommaire** : [En bref](#en-bref) · [Objectifs](#objectifs) · [Vue d'ensemble](#vue-densemble) · [Séance 1](#séance-1--premiers-pas-dans-le-shell) · [Séance 2](#séance-2--traiter-du-texte-droits-et-processus) · [Correspondances](#correspondances-entre-les-supports) · [Préparer les séances](#préparer-les-séances) · [Suivi de la progression](#suivi-de-la-progression)

---

## En bref

- **Public** : débutants, sans connaissance préalable de Linux
- **Durée** : 2 séances de 4 heures, soit 8 heures ; les durées indiquées sont à ajuster si les séances sont plus courtes
- **Matériel** : pour chaque étudiant, un terminal Linux avec `bash`, `git` et `python3` (Linux live, machine virtuelle, VPS ou WSL : voir [Accéder à un système Linux](README.md#accéder-à-un-système-linux))
- **Supports** :
  - [présentation](presentation.md) ([PDF](presentation.pdf)) : parties 1 à 7 (diapos 1 à 69), plus la diapo 82 pour l'étape 9 du TP
  - [mémento des commandes de base](linux_commandes_base.md) : référence rapide, à garder ouverte pendant le TP
  - [TP « Commandes de base Linux »](tp_start/readme.md) : les 10 étapes, vérifiées par `verify.py`
- **Hors programme** : parties 8 « Caractères spéciaux et filtres » et 9 « Automatiser des tâches » de la présentation

---

## Objectifs

À la fin des deux séances, l'étudiant sait :

- situer GNU/Linux dans l'histoire d'UNIX et en expliquer la philosophie ;
- trouver de l'aide seul avec `man`, `--help` et `help` ;
- se repérer dans l'arborescence et désigner un fichier par un chemin absolu ou relatif ;
- créer, copier, déplacer, renommer, supprimer et rechercher des fichiers ;
- combiner des commandes avec les redirections et les tubes pour extraire, trier et compter ;
- archiver et compresser un dossier avec `tar` ;
- lire et modifier les droits d'accès d'un fichier ;
- distinguer une variable locale d'une variable exportée, et créer un alias ;
- observer un processus, le lancer en arrière-plan et l'arrêter.

---

## Vue d'ensemble

| Séance | Thème | Présentation | TP « Commandes de base Linux » | Mémento |
|---|---|---|---|---|
| 1 | Premiers pas dans le shell | parties 1 à 6 (diapos 1 à 58) | préparation, étapes 1 à 4 | sections 2, 3, 7, 11 |
| 2 | Traiter du texte, droits et processus | partie 7 (diapos 59 à 69), diapo 82 | étapes 5 à 10 | sections 1, 2, 3, 4, 6, 8, 9, 12 |

---

## Séance 1 : premiers pas dans le shell

**Objectif** : utiliser le terminal, trouver de l'aide, se déplacer dans l'arborescence et manipuler des fichiers.

| Durée | Activité | Supports |
|---|---|---|
| 20 min | Accueil et objectifs. Chaque étudiant ouvre un terminal Linux | Présentation, partie 1 « Mise en route » (diapos 1 à 5) |
| 35 min | Culture : GNU/Linux, histoire d'UNIX, philosophie UNIX | Présentation, parties 2 à 4 (diapos 6 à 29) |
| 45 min | La ligne de commande : structure d'une commande, aide, shell, flux, redirections et tubes, historique, processus, paquets | Présentation, partie 5 « Manipuler sous Linux » (diapos 30 à 45) |
| 10 min | Pause | |
| 30 min | Préparer le TP : `git clone`, `bash setup.sh`, `python3 verify.py`. Présenter la méthode de travail et le mémento. Réaliser l'étape 1 (aide, historique, horloge) | [TP, démarrer](tp_start/readme.md#démarrer), [étape 1](tp_start/etapes/01-aide-historique.md), mémento sections 7 et 11 |
| 35 min | Les fichiers : système de fichiers, arborescence, chemins, inodes, fichiers texte et encodage, commandes de manipulation, `vim` | Présentation, partie 6 « Manipuler des fichiers » (diapos 46 à 58) |
| 55 min | Étapes 2 à 4 : se repérer, créer, copier, déplacer, supprimer | [Étapes 2](tp_start/etapes/02-arborescence.md), [3](tp_start/etapes/03-creer.md) et [4](tp_start/etapes/04-copier-deplacer-supprimer.md), mémento sections 2 et 3 |
| 10 min | Bilan : chacun affiche sa progression avec `python3 verify.py` ; retour sur les difficultés rencontrées | |

> **Remarque** : les diapos 53 à 55 sur l'encodage des caractères peuvent être survolées ; le [TP1](tp/tp1-fichiers-texte.md) les approfondit pour qui veut aller plus loin.

---

## Séance 2 : traiter du texte, droits et processus

**Objectif** : rechercher et filtrer du texte, archiver, gérer les droits, les variables et les processus.

| Durée | Activité | Supports |
|---|---|---|
| 10 min | Rappel de la séance 1. Chacun vérifie sa progression avec `python3 verify.py` et termine les étapes 1 à 4 si besoin | |
| 30 min | Étape 5 : rechercher des fichiers et du texte | [Étape 5](tp_start/etapes/05-rechercher.md), diapos 34 et 57, mémento section 2 (`find`) |
| 45 min | Étape 6 : filtres et tubes | [Étape 6](tp_start/etapes/06-filtres-pipes.md), rappel des diapos 37 et 38, mémento section 6 |
| 15 min | Étape 7 : archiver et compresser | [Étape 7](tp_start/etapes/07-archiver.md), mémento section 12 |
| 10 min | Pause | |
| 35 min | Gestion des droits : utilisateurs et groupes, permissions, `chmod`, droits spéciaux, `umask`, `chown` | Présentation, partie 7 « Gestion des droits » (diapos 59 à 69) |
| 25 min | Étape 8 : liens symboliques et permissions | [Étape 8](tp_start/etapes/08-liens-permissions.md), mémento sections 3 (`ln`) et 4 |
| 25 min | Étape 9 : variables d'environnement et alias | [Étape 9](tp_start/etapes/09-variables-alias.md), diapo 82 « Variables locales et d'environnement », diapo 33 (alias) |
| 30 min | Étape 10 : processus et ressources | [Étape 10](tp_start/etapes/10-processus.md), rappel des diapos 42, 43 et 47, mémento sections 1, 8 et 9 |
| 15 min | Bilan final : `python3 verify.py --all`, synthèse des commandes vues, questions | |

> **Remarque** : la diapo 82 appartient à la partie 9 ; on la montre seule, sans aborder les scripts, car l'étape 9 repose sur la notion de variable exportée.

---

## Correspondances entre les supports

Pour chaque étape du TP, les diapos et les sections du mémento à consulter :

| Étape du TP | Commandes | Diapos | Mémento |
|---|---|---|---|
| 1. Aide, historique, horloge | `man` `--help` `help` `history` `date` | 35, 39 | 7 (`date`), 11 |
| 2. Se repérer dans l'arborescence | `pwd` `cd` `ls` `cat` | 49, 50 | 2 (`ls`, `cd`), 3 (`cat`), 7 (`pwd`) |
| 3. Créer dossiers et fichiers | `mkdir` `touch` `echo` `>` `>>` | 38, 56 | 2 (`mkdir`), 3 (`cat`), 5 (`echo`) |
| 4. Copier, déplacer, supprimer | `cp` `mv` `rm` `rmdir` | 57 | 2 (`rmdir`), 3 |
| 5. Rechercher | `find` `grep` `which` `type` | 33, 34, 57 | 2 (`find`) |
| 6. Filtres et tubes | `head` `tail` `sort` `uniq` `wc` `tr` `cut` `\|` | 37, 38 | 6 |
| 7. Archiver et compresser | `tar` | — | 12 |
| 8. Liens et permissions | `ln` `chmod` | 51, 61 à 65 | 3 (`ln`), 4 |
| 9. Variables et alias | `export` `alias` | 33, 82 | — |
| 10. Processus et ressources | `ps` `jobs` `pgrep` `kill` `df` `&` | 42, 43, 47 | 1, 8, 9 (`df`) |

---

## Préparer les séances

- Vérifier que chaque étudiant dispose d'un terminal Linux avec `bash`, `git` et `python3`, et d'un accès à GitHub pour cloner le dépôt.
- Projeter la présentation depuis le [PDF](presentation.pdf).
- Garder à portée de main le corrigé du TP (`tp_start/readme_correction.md`, hors dépôt).
- Lire la page [Dépannage](tp_start/aide/depannage.md) du TP : elle répond aux blocages les plus courants.

---

## Suivi de la progression

- `python3 verify.py` affiche l'état des 10 étapes : c'est l'indicateur de fin de séance. Objectif : les étapes 1 à 4 validées en fin de séance 1, les 10 étapes en fin de séance 2.
- Le script vérifie le résultat, pas la manière : plusieurs commandes peuvent convenir.
- Pour les étudiants les plus rapides : les sections du mémento qui ne sont pas utilisées dans le TP (5 `more` et `less`, 9 `du` et `mount`, 10 `at` et `crontab`).
- Pour les étudiants en retard : les étapes 9 et 10 sont indépendantes l'une de l'autre et peuvent être terminées en autonomie.
