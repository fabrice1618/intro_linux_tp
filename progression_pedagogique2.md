# Progression pédagogique 2 : de la ligne de commande au serveur LAMP

Progression en **5 séances** : les deux premières reprennent la [progression 1](progression_pedagogique1.md) (présentation, mémento des commandes de base et [TP « Commandes de base Linux »](tp_start/readme.md)), les suivantes ajoutent les expressions régulières, les scripts shell et l'installation d'un [serveur LAMP](serveur_LAMP/README.md) de développement. Le serveur LAMP réinvestit tout ce qui précède : paquets, services, droits, fichiers de configuration, journaux et scripts.

**Sommaire** : [En bref](#en-bref) · [Objectifs](#objectifs) · [Vue d'ensemble](#vue-densemble) · [Séance 1](#séance-1--premiers-pas-dans-le-shell) · [Séance 2](#séance-2--traiter-du-texte-droits-et-processus) · [Séance 3](#séance-3--expressions-régulières-et-premiers-scripts) · [Séance 4](#séance-4--scripts-et-installation-du-serveur) · [Séance 5](#séance-5--mysql-apache-et-php) · [Préparer les séances](#préparer-les-séances) · [Suivi de la progression](#suivi-de-la-progression)

---

## En bref

- **Public** : débutants, sans connaissance préalable de Linux
- **Durée** : 5 séances de 4 heures, soit 20 heures ; les durées indiquées sont à ajuster si les séances sont plus courtes
- **Matériel** :
  - séances 1 à 3 : pour chaque étudiant, un terminal Linux avec `bash`, `git` et `python3` (voir [Accéder à un système Linux](README.md#accéder-à-un-système-linux))
  - séances 4 et 5 : un poste sur lequel l'étudiant peut installer un hyperviseur et créer une machine virtuelle (2 Go de RAM et 25 Go de disque pour la VM)
- **Supports** :
  - [présentation](presentation.md) ([PDF](presentation.pdf)) : les 9 parties (diapos 1 à 92)
  - [cours complet](README.md) : le texte détaillé de la présentation et ses exemples, en particulier pour les expressions régulières et les scripts
  - [mémento des commandes de base](linux_commandes_base.md) : référence rapide, à garder ouverte pendant les TP
  - [TP « Commandes de base Linux »](tp_start/readme.md) : les 10 étapes, vérifiées par `verify.py`
  - [TP « Serveur LAMP »](serveur_LAMP/README.md) : parties A à F et ses fiches de ressources

---

## Objectifs

À la fin des cinq séances, l'étudiant sait, en plus des [objectifs de la progression 1](progression_pedagogique1.md#objectifs) :

- distinguer les caractères génériques du shell et les expressions régulières ;
- écrire une expression régulière (BRE ou ERE) et l'utiliser avec `grep`, `sed` et `awk` ;
- écrire, rendre exécutable et lancer un script shell ;
- utiliser dans un script les variables, les paramètres, les tests, les structures conditionnelles, les boucles et les fonctions ;
- créer une machine virtuelle et y installer Ubuntu Server ;
- administrer un serveur à distance avec `ssh` : paquets (`apt`), services (`systemctl`), pare-feu (`ufw`) ;
- installer et configurer MySQL, Apache 2 et PHP pour le développement ;
- consulter les journaux d'un service et proposer des mesures de sécurisation pour la production.

---

## Vue d'ensemble

| Séance | Thème | Présentation | Travaux pratiques |
|---|---|---|---|
| 1 | Premiers pas dans le shell | parties 1 à 6 (diapos 1 à 58) | TP « Commandes de base Linux » : préparation, étapes 1 à 4 |
| 2 | Traiter du texte, droits et processus | partie 7 (diapos 59 à 69), diapo 82 | TP « Commandes de base Linux » : étapes 5 à 10 |
| 3 | Expressions régulières et premiers scripts | partie 8 (diapos 70 à 76), partie 9 (diapos 77 à 85) | exercices sur les filtres et premiers scripts |
| 4 | Scripts et installation du serveur | partie 9 (diapos 86 à 92) | scripts ; TP LAMP parties A et B |
| 5 | MySQL, Apache et PHP | — | TP LAMP parties C à F |

---

## Séance 1 : premiers pas dans le shell

Identique à la [séance 1 de la progression 1](progression_pedagogique1.md#séance-1--premiers-pas-dans-le-shell).

| Durée | Activité | Supports |
|---|---|---|
| 20 min | Accueil et objectifs. Chaque étudiant ouvre un terminal Linux | Présentation, partie 1 « Mise en route » (diapos 1 à 5) |
| 35 min | Culture : GNU/Linux, histoire d'UNIX, philosophie UNIX | Présentation, parties 2 à 4 (diapos 6 à 29) |
| 45 min | La ligne de commande : structure d'une commande, aide, shell, flux, redirections et tubes, historique, processus, paquets | Présentation, partie 5 « Manipuler sous Linux » (diapos 30 à 45) |
| 10 min | Pause | |
| 30 min | Préparer le TP : `git clone`, `bash setup.sh`, `python3 verify.py`. Présenter la méthode de travail et le mémento. Réaliser l'étape 1 | [TP, démarrer](tp_start/readme.md#démarrer), [étape 1](tp_start/etapes/01-aide-historique.md), mémento sections 7 et 11 |
| 35 min | Les fichiers : système de fichiers, arborescence, chemins, inodes, fichiers texte et encodage, commandes de manipulation, `vim` | Présentation, partie 6 « Manipuler des fichiers » (diapos 46 à 58) |
| 55 min | Étapes 2 à 4 : se repérer, créer, copier, déplacer, supprimer | [Étapes 2](tp_start/etapes/02-arborescence.md), [3](tp_start/etapes/03-creer.md) et [4](tp_start/etapes/04-copier-deplacer-supprimer.md), mémento sections 2 et 3 |
| 10 min | Bilan : `python3 verify.py` ; retour sur les difficultés rencontrées | |

---

## Séance 2 : traiter du texte, droits et processus

Identique à la [séance 2 de la progression 1](progression_pedagogique1.md#séance-2--traiter-du-texte-droits-et-processus).

| Durée | Activité | Supports |
|---|---|---|
| 10 min | Rappel de la séance 1. Chacun termine les étapes 1 à 4 si besoin | `python3 verify.py` |
| 30 min | Étape 5 : rechercher des fichiers et du texte | [Étape 5](tp_start/etapes/05-rechercher.md), diapos 34 et 57, mémento section 2 |
| 45 min | Étape 6 : filtres et tubes | [Étape 6](tp_start/etapes/06-filtres-pipes.md), diapos 37 et 38, mémento section 6 |
| 15 min | Étape 7 : archiver et compresser | [Étape 7](tp_start/etapes/07-archiver.md), mémento section 12 |
| 10 min | Pause | |
| 35 min | Gestion des droits : utilisateurs et groupes, permissions, `chmod`, droits spéciaux, `umask`, `chown` | Présentation, partie 7 « Gestion des droits » (diapos 59 à 69) |
| 25 min | Étape 8 : liens symboliques et permissions | [Étape 8](tp_start/etapes/08-liens-permissions.md), mémento sections 3 et 4 |
| 25 min | Étape 9 : variables d'environnement et alias | [Étape 9](tp_start/etapes/09-variables-alias.md), diapos 33 et 82 |
| 30 min | Étape 10 : processus et ressources | [Étape 10](tp_start/etapes/10-processus.md), diapos 42, 43 et 47, mémento sections 1, 8 et 9 |
| 15 min | Bilan : `python3 verify.py --all`, synthèse des commandes vues | |

> **Remarque** : la [correspondance entre les étapes du TP, les diapos et le mémento](progression_pedagogique1.md#correspondances-entre-les-supports) est détaillée dans la progression 1.

---

## Séance 3 : expressions régulières et premiers scripts

**Objectif** : rechercher et transformer du texte avec des expressions régulières, puis écrire ses premiers scripts.

| Durée | Activité | Supports |
|---|---|---|
| 10 min | Rappel de la séance 2 ; terminer le TP « Commandes de base Linux » si besoin | `python3 verify.py` |
| 45 min | Caractères génériques du shell, expressions régulières (opérateurs, quantificateurs), BRE, ERE et PCRE, protection des caractères spéciaux, `grep`, `sed` et `awk` | Présentation, partie 8 « Caractères spéciaux et filtres » (diapos 70 à 76) ; cours, [Caractères spéciaux et filtres](README.md#caractères-spéciaux-et-filtres) |
| 55 min | Exercices sur les filtres : refaire les exemples du cours sur `/etc/passwd`, puis les pistes ci-dessous sur les fichiers du TP | Cours, [Les filtres grep, sed et awk](README.md#les-filtres-grep-sed-et-awk) |
| 10 min | Pause | |
| 45 min | Scripts shell : intérêt, premier script, exécution, variables, substitutions, paramètres et variables internes, affichage et saisie | Présentation, partie 9 « Automatiser des tâches » (diapos 77 à 85) ; cours, [Automatiser des tâches](README.md#automatiser-des-tâches) |
| 65 min | Exercices : écrire, rendre exécutables et lancer ses premiers scripts, en reprenant les exemples du cours (variables internes, `echo`, `read`) puis en les modifiant | Cours, de [Les shell scripts](README.md#les-shell-scripts) à [La saisie de données](README.md#la-saisie-de-données) |
| 10 min | Bilan | |

**Pistes d'exercices sur les filtres**, avec les fichiers de `tp_start/data/` (en lecture seule : on n'utilise pas `sed -i` sur ces fichiers, `verify.py` signalerait la modification) :

- dans `logs/app.log`, afficher les lignes de niveau `WARN` ou `ERROR`, puis les compter ;
- dans `fruits.txt`, afficher les fruits de cinq lettres exactement, puis ceux qui sont écrits entièrement en majuscules ;
- dans `sample.csv`, remplacer les virgules par des points-virgules avec `sed` ;
- avec `awk`, afficher « prénom habite ville » pour chaque ligne de `sample.csv`, sans la ligne d'en-tête ;
- dans `lorem.txt`, afficher les lignes qui contiennent le mot `dolor` seul, sans celles qui ne contiennent que `dolore`.

---

## Séance 4 : scripts et installation du serveur

**Objectif** : écrire des scripts avec des tests, des boucles et des fonctions, puis installer et administrer à distance un serveur Ubuntu.

| Durée | Activité | Supports |
|---|---|---|
| 10 min | Rappel de la séance 3 | |
| 40 min | Tests et conditions, `if`, `case` et `select`, boucles `for`, `while` et `until`, fonctions | Présentation, partie 9 (diapos 86 à 92) ; cours, de [Les tests et conditions](README.md#les-tests-et-conditions) à [Les fonctions](README.md#les-fonctions) |
| 70 min | Exercices : reproduire, exécuter puis modifier les scripts du cours (`if1.sh`, `case1.sh`, `for1a.sh`, `while.sh`, `rootCheck.sh`...) | Cours, [Les structures conditionnelles](README.md#les-structures-conditionnelles), [Les contrôles itératifs](README.md#les-contrôles-itératifs-les-boucles-for-while-et-until), [Les fonctions](README.md#les-fonctions) |
| 10 min | Pause | |
| 20 min | Présentation du TP LAMP : architecture, serveur de développement et de production, rôle de chaque composant | [TP Serveur LAMP](serveur_LAMP/README.md), rappel de la diapo 5 (hyperviseurs) |
| 20 min | Partie A : installer l'hyperviseur et créer la machine virtuelle (1 cœur, 2 Go de RAM, 25 Go de disque, réseau en pont) | TP LAMP, A1 et A2 |
| 60 min | Partie B : installer Ubuntu Server 24.04, mettre à jour le système, installer OpenSSH, se connecter en SSH depuis l'hôte, configurer le pare-feu | TP LAMP, B1 à B5 ; fiches [APT](serveur_LAMP/apt.md), [Systemctl](serveur_LAMP/systemctl.md), [UFW](serveur_LAMP/ufw.md), [Configuration réseau](serveur_LAMP/configuration_reseau.md) |
| 10 min | Bilan : chaque étudiant se connecte en SSH à sa VM et affiche l'état du pare-feu | `ssh`, `sudo ufw status` |

> **Remarque** : pendant la copie des paquets de l'installation d'Ubuntu Server, les étudiants lisent les fiches APT et Systemctl.

---

## Séance 5 : MySQL, Apache et PHP

**Objectif** : installer et configurer MySQL, Apache 2 et PHP, travailler sur le serveur depuis VS Code, et réfléchir à la sécurisation d'un serveur de production.

| Durée | Activité | Supports |
|---|---|---|
| 10 min | Connexion SSH à la VM, mise à jour du système | TP LAMP, B2 et B4 |
| 75 min | Partie C : installer MySQL, le configurer (journaux, accès distant), créer les utilisateurs `root` et `dba`, la base et l'utilisateur applicatifs, tester, installer MySQL Workbench sur l'hôte | TP LAMP, C1 à C8 ; fiches [MySQL](serveur_LAMP/mysql.md) et [Systemctl](serveur_LAMP/systemctl.md) |
| 10 min | Pause | |
| 55 min | Partie D : installer Apache 2 et PHP 8, configurer PHP pour le développement, vérifier la configuration, consulter les journaux | TP LAMP, D1 à D4 ; fiches [Apache2](serveur_LAMP/apache2.md) et [PHP](serveur_LAMP/php.md) |
| 25 min | Partie E : installer Git sur le serveur, s'y connecter avec l'extension Remote-SSH de VS Code | TP LAMP, E1 et E2 |
| 20 min | Réinvestir les séances 3 et 4 : filtrer les journaux d'Apache avec `grep -E` ; écrire un script de sauvegarde de la base avec `mysqldump`, dont le nom de fichier contient la date | Fiche MySQL, [Sauvegarde et restauration](serveur_LAMP/mysql.md#sauvegarde-et-restauration) |
| 30 min | Partie F : sécuriser un serveur de production. Recherche par groupes (une question F1 à F7 par groupe), puis mise en commun | TP LAMP, F1 à F7 |
| 15 min | Bilan final : chaque étudiant affiche la page `phpinfo()` de son serveur et se connecte à sa base ; synthèse du cours | |

> **Remarque** : si le temps manque, l'installation de MySQL Workbench (C8) est facultative et la partie F peut être donnée en travail personnel.

---

## Préparer les séances

Séances 1 à 3 :

- Vérifier que chaque étudiant dispose d'un terminal Linux avec `bash`, `git` et `python3`, et d'un accès à GitHub pour cloner le dépôt.
- Projeter la présentation depuis le [PDF](presentation.pdf).
- Garder à portée de main le corrigé du TP (`tp_start/readme_correction.md`, hors dépôt) et la page [Dépannage](tp_start/aide/depannage.md).

Séances 4 et 5 :

- Vérifier que les postes permettent d'installer un hyperviseur (droits d'administration, virtualisation activée dans l'UEFI, Hyper-V disponible seulement sous Windows Pro).
- Faire télécharger l'image `ubuntu-24.04-live-server-amd64.iso` avant la séance 4 : le téléchargement simultané par tout le groupe est long.
- Vérifier que le réseau accepte les machines virtuelles en mode pont ; à défaut, prévoir le mode NAT avec redirection du port 22.
- Pour la connexion SSH depuis Windows, prévoir Git Bash, PowerShell ou `cmd.exe`, et VS Code avec l'extension Remote-SSH.

---

## Suivi de la progression

| Fin de séance | Indicateur |
|---|---|
| 1 | `python3 verify.py` : étapes 1 à 4 validées |
| 2 | `python3 verify.py --all` : les 10 étapes validées |
| 3 | les exercices sur les filtres résolus ; un script qui lit un nom et affiche un message s'exécute avec `./script.sh` |
| 4 | un script avec une boucle et une fonction s'exécute ; connexion SSH à la VM, pare-feu actif |
| 5 | la page `phpinfo()` s'affiche depuis l'hôte, connexion à la base applicative, script de sauvegarde fonctionnel |
