# Vérification de cohérence énoncé (etapes/) ↔ verify.py

Pour chaque étape : les tâches de l'énoncé (`etapes/NN-*.md`), ce que `verify.py` contrôle, et les erreurs courantes qu'il reconnaît et explique. Une tâche = une ligne ✔/✘ dans le script (38 tâches au total).

Les tâches notées *(question)* sont vérifiées par une question posée lors de `python3 verify.py N` ; la réponse s'obtient en exécutant les commandes, et les bonnes réponses sont mémorisées dans `workspace/.verify/reponses.json`.

---

## Étape 1 — Trouver de l'aide, historique, horloge

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| Option de `ls` qui trie par taille *(question)* | `-S` | `-s` (casse), `-t` (tri par date) |
| Jour du 1er janvier 2030 *(question)* | calculé (mardi / Tuesday) | — |
| Commande trouvée avec `man -k` *(question)* | `pwd` | `cd` |
| `workspace/preuves/historique.txt` | lignes numérotées de `history` | fichier vide, contenu qui n'est pas une sortie de `history` |

## Étape 2 — Se repérer dans l'arborescence

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| Chemin absolu du TP *(question)* | égal au dossier de `verify.py` | chemin relatif, dossier parent du TP |
| Mot secret de `data/.bienvenue` *(question)* | lu dans le fichier | — |
| Taille de `data/sample.csv` *(question)* | taille réelle en octets | taille arrondie par `-h`, taille d'un dossier (4096) |
| Chemin relatif depuis `workspace/preuves` *(question)* | résolu vers `data/fruits.txt` | chemin absolu, chemin qui mène ailleurs (affiché) |

## Étape 3 — Créer dossiers et fichiers

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `workspace/docs`, `data`, `tmp` | dossiers présents | fichier au lieu de dossier, dossier créé à la racine du TP, `workspace/workspace` |
| `workspace/projets/2026/janvier` | présent (ou supprimé à l'étape 4) | `mkdir` sans `-p` |
| `workspace/data/todo.txt` | fichier présent (remarque s'il n'est pas vide) | dossier au lieu de fichier |
| `workspace/tmp/.cache` | présent | nom sans point |
| `workspace/docs/bonjour.txt` | ≥ 2 lignes (ou déplacé à l'étape 4) | une seule ligne : `>` au lieu de `>>` |

## Étape 4 — Copier, déplacer, renommer, supprimer

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `workspace/backup_data` | tous les fichiers de `data/` identiques, y compris `.bienvenue` | copie imbriquée `backup_data/data` (commande lancée deux fois), fichiers manquants ou différents |
| Renommer `bonjour.txt` | `bonjour.renomme.txt` existe, `docs/bonjour.txt` n'existe plus | copie au lieu de renommage, déplacé sans être renommé |
| Déplacer à la racine de `workspace/` | `workspace/bonjour.renomme.txt`, contenu conservé | encore dans `docs/`, présent aux deux endroits |
| Supprimer `janvier` | absent, `projets/2026` présent | dossier non vide, trop supprimé |
| Supprimer `backup_data/logs` | absent de la sauvegarde, `data/logs` intact | original `data/logs` supprimé |

## Étape 5 — Rechercher des fichiers et du texte

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `workspace/preuves/find_fruits.txt` | contient `fruits.txt` et `Fruits_exotiques.txt` | `-name` au lieu de `-iname`, motif sans jokers, `find` sans critère |
| `workspace/preuves/grep_poire.txt` | exactement `3:poire` et `9:POIRE` | sans `-n`, sans `-i` |
| `workspace/preuves/which_python3.txt` | même exécutable que le `python3` du PATH | sortie de `type` (acceptée avec remarque) |
| `type cd`, `type ls`, `type python3` | non vérifié | — |

## Étape 6 — Filtres et redirections (pipes)

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `lorem_extrait.txt` | lignes 2 à 4 de `lorem.txt` | autres lignes (numéros affichés), `head` seul |
| `fruits_uniques.txt` | trié, sans doublon, complet | `uniq` sans `sort`, `uniq -c`, lignes non triées ; `sort -f`/`uniq -i` accepté |
| `lorem_wc.txt` | nombre de mots | `wc` sans option, lignes (`-l`), octets (`-c`), caractères (`-m`) |
| `fruits_upper.txt` | `fruits.txt` en majuscules, même ordre | minuscules restantes, lignes triées ; `PêCHE` accepté (limite de `tr`) |
| `col2.txt` | 2e colonne, avec ou sans en-tête | `cut` sans `-d`, mauvais numéro de champ |
| `nb_info.txt` | nombre de lignes `INFO` | lignes au lieu du nombre, total des lignes du journal |

## Étape 7 — Archiver et compresser

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `workspace/data_archive.tgz` | tar compressé gzip, chemins `data/...`, tous les fichiers | sans `-z`, archive illisible, chemin absolu, contenu de `data/` sans le dossier |
| `workspace/preuves/contenu_archive.txt` | mentionne `data/fruits.txt` | — |
| Extraction dans `workspace/tmp` | `workspace/tmp/data/fruits.txt` identique à l'original | extraction sans `data/`, chemins absolus, sans `-C` |

## Étape 8 — Liens symboliques et permissions

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `workspace/data/link_fruits.txt` | lien symbolique vers `data/fruits.txt` | lien cassé (chemin relatif lu depuis le dossier du lien), lien physique, copie, mauvaise cible |
| `fruits_uniques.txt` en 640 | mode exact | mode affiché en octal et en rwx |
| `workspace/salut.sh` en 755 | copie identique de `data/salut.sh`, mode exact | lien au lieu de copie, non exécutable, écriture pour les autres (777) |

## Étape 9 — Variables d'environnement et alias

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| `MYVAR` exportée | visible dans l'environnement de `verify.py` (processus enfant du shell) | variable non exportée, script lancé depuis un autre terminal, valeur vide |
| `workspace/preuves/alias.txt` | contient `alias verif=...verify.py...` | alias absent, mauvaise valeur ; remarque bonus si l'alias est dans `~/.bashrc` |

## Étape 10 — Processus et ressources

| Tâche | Contrôle | Erreurs reconnues |
|---|---|---|
| PID du shell *(question)* | processus existant, shell, appartenant à l'étudiant | pas un nombre, processus inexistant, pas un shell, autre utilisateur |
| `workspace/preuves/sleep.pid` | les `sleep` enregistrés sont terminés | processus encore actif, PID d'un autre utilisateur, autres `sleep` restants |
| `workspace/preuves/disque.txt` | sortie de `df` avec tailles lisibles | `df` sans `-h` |

---

## Contrôles transversaux

- `setup.sh` non lancé : message et code de retour 1.
- `data/` modifié ou supprimé par erreur : avertissement en tête (empreintes SHA-256 écrites par `setup.sh`).
- Fichier attendu absent mais présent ailleurs (dossier du TP ou `~`) : le script indique où, en pensant à une erreur de répertoire courant.
- Les étapes suivantes ne font pas échouer les précédentes : un parcours complet donne 38/38.
