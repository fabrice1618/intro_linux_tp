# Vérification de cohérence readme.md ↔ verify.py

## ✅ Étape 1 — Se repérer dans l'arborescence
- **README** : Découverte de `pwd` et `ls` (pas de création de fichiers)
- **VERIFY** : Vérifie l'existence des outils (pwd, ls, wc, whoami, uname)
- **Statut** : ✅ Cohérent (étape purement exploratoire)

---

## ✅ Étape 2 — Créer dossiers et fichiers
- **README demande** :
  1. Fichier vide `workspace/data/todo.txt`
  2. Fichier caché `workspace/tmp/.cache`
  3. Fichier `workspace/docs/bonjour.txt` avec ≥2 lignes

- **VERIFY contrôle** :
  - `workspace/docs/`, `workspace/data/`, `workspace/tmp/` existent
  - `workspace/data/todo.txt` existe
  - `workspace/tmp/.cache` existe
  - `workspace/docs/bonjour.txt` existe et contient ≥2 lignes

- **Statut** : ✅ Parfaitement cohérent

---

## ✅ Étape 3 — Copier, déplacer, renommer, supprimer
- **README demande** :
  1. Copier `data/` vers `workspace/backup_data/` (récursif)
  2. Renommer `backup_data/bonjour.txt` → `bonjour.renomme.txt` et déplacer vers `workspace/`
  3. Supprimer `workspace/docs/bonjour.txt`

- **VERIFY contrôle** :
  - `workspace/backup_data/` existe (dossier)
  - `workspace/bonjour.renomme.txt` existe
  - `workspace/docs/bonjour.txt` n'existe plus

- **Statut** : ✅ Cohérent (tâche 4 optionnelle supprimée du README)

---

## ✅ Étape 4 — Rechercher des fichiers et du texte
- **README demande** :
  1. Rechercher fichiers contenant "fruits" sous `workspace/` (insensible casse)
  2. Trouver lignes avec "pomme" dans `data/fruits.txt` avec numéros de ligne
  3. Trouver chemin de `python3`

- **VERIFY contrôle** :
  - `find workspace/ -iname "*fruits*"` retourne un résultat
  - `grep -n "pomme" data/fruits.txt` retourne un résultat
  - `which python3` fonctionne

- **Statut** : ✅ Parfaitement cohérent

---

## ✅ Étape 5 — Filtres et redirections (pipes)
- **README demande** :
  1. Afficher 5 premières et 3 dernières lignes de `lorem.txt` (visualisation)
  2. Créer `workspace/data/fruits_uniques.txt` (tri + dédupliquer)
  3. Créer `workspace/data/lorem_wc.txt` (nombre de mots)
  4. Créer `workspace/data/fruits_upper.txt` (majuscules)
  5. Créer `workspace/data/col2.txt` (2e colonne du CSV)

- **VERIFY contrôle** :
  - `workspace/data/fruits_uniques.txt` existe
  - `workspace/data/lorem_wc.txt` existe et contient un nombre (`\b\d+\b`)
  - `workspace/data/fruits_upper.txt` existe
  - `workspace/data/col2.txt` existe

- **Statut** : ✅ Cohérent (tâche 1 est purement visuelle, non vérifiable)

---

## ✅ Étape 6 — Archiver et compresser
- **README demande** :
  1. Créer archive `workspace/data_archive.tgz` du dossier `data/`
  2. Lister le contenu (visualisation)
  3. Extraire dans `workspace/tmp/`

- **VERIFY contrôle** :
  - `workspace/data_archive.tgz` existe
  - `workspace/tmp/data/fruits.txt` existe (preuve d'extraction)

- **Statut** : ✅ Cohérent (listage est visuel, extraction vérifiée)

---

## ✅ Étape 7 — Liens symboliques et permissions
- **README demande** :
  1. Créer symlink `workspace/data/link_fruits.txt` → `data/fruits.txt`
  2. Permissions `640` sur `workspace/data/fruits_uniques.txt`

- **VERIFY contrôle** :
  - `workspace/data/link_fruits.txt` est un symlink
  - Le symlink pointe vers `BASE/data/fruits.txt` (chemin absolu résolu)
  - `workspace/data/fruits_uniques.txt` a les permissions `0o640`

- **Statut** : ✅ Cohérent (README clarifié : chemin absolu ou relatif accepté, verify.py résout le lien)

---

## ✅ Étape 8 — Variables d'environnement et alias
- **README demande** :
  1. Créer et exporter `MYVAR`
  2. Créer alias `ll`
  3. Utiliser `ll`
  4. Afficher `$MYVAR`

- **VERIFY contrôle** :
  - Tente de lire `MYVAR` (avec message tolérant)
  - Informe que les alias ne sont pas visibles (processus séparé)
  - Retourne toujours `True` (validation tolérante)

- **Statut** : ✅ Cohérent et bien expliqué (limitation technique documentée)

---

## ✅ Étape 9 — Processus et ressources
- **README demande** :
  1. Lister processus de l'utilisateur
  2. Lancer `sleep 300 &`
  3. Trouver PID de sleep
  4. Terminer le processus
  5. Afficher espace disque (`df -h`)

- **VERIFY contrôle** :
  - `ps -u $(whoami)` fonctionne (code retour 0)
  - `df -h` fonctionne
  - Détecte si `sleep` est encore présent (avertissement, non bloquant)

- **Statut** : ✅ Cohérent (vérification souple)

---

## ✅ Étape 10 — Trouver de l'aide, historique, horloge
- **README demande** :
  1. Ouvrir `man ls`, chercher "hidden", quitter
  2. Afficher aide avec `--help`
  3. Afficher 10 dernières commandes historique
  4. Afficher date/heure
  5. (Optionnel) calendrier

- **VERIFY contrôle** :
  - `man` est disponible (which)
  - `date` est disponible (which)

- **Statut** : ✅ Cohérent (tâches exploratoires, vérification minimale)

---

## Résumé global

| Étape | Cohérence | Notes |
|-------|-----------|-------|
| 1 | ✅ | Exploratoire |
| 2 | ✅ | Parfaite correspondance |
| 3 | ✅ | Tâche optionnelle supprimée |
| 4 | ✅ | Parfaite correspondance |
| 5 | ✅ | Tâche 1 visuelle non vérifiée |
| 6 | ✅ | Listage visuel, extraction vérifiée |
| 7 | ✅ | README clarifié (chemin relatif/absolu) |
| 8 | ✅ | Limitation technique documentée |
| 9 | ✅ | Vérification souple |
| 10 | ✅ | Tâches exploratoires |

**Conclusion** : Le readme.md et verify.py sont maintenant **parfaitement cohérents**. Les corrections apportées :
1. Suppression de la tâche 4 de l'étape 3 (suppression dossier vide optionnel)
2. Clarification de l'étape 7 sur les chemins absolus/relatifs pour les symlinks
