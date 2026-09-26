[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · [Guide de man](man.md) · **Script de vérification** · [Dépannage](depannage.md)

# Le script de vérification

Un script Python vérifie à chaque étape l'état final (résultat concret) et, en cas d'erreur, explique ce qu'il a trouvé et donne une piste pour corriger. Il ne donne pas la commande : c'est à vous de la trouver.

Le script fonctionne quel que soit votre répertoire courant.

---

## Les commandes

| Commande | Effet |
|---|---|
| `python3 verify.py` | Tableau de progression : étapes validées (✔), commencées (◐), à faire (·), et prochaine étape |
| `python3 verify.py 3` | Vérification détaillée de l'étape 3 (ou `python3 verify.py --step 3`) |
| `python3 verify.py --all` | Vérification détaillée de toutes les étapes |

---

## Le tableau de progression

```bash
python3 verify.py
```

```text
TP « Commandes de base Linux » — progression
  ✔  1  Trouver de l'aide, historique, horloge   4/4
  ✔  2  Se repérer dans l'arborescence           4/4
  ◐  3  Créer dossiers et fichiers               2/5
  ·  4  Copier, déplacer, renommer, supprimer    0/5
  ·  5  Rechercher des fichiers et du texte      0/3
  ·  6  Filtres et redirections (pipes)          0/6
  ·  7  Archiver et compresser                   0/3
  ·  8  Liens symboliques et permissions         0/3
  ·  9  Variables d'environnement et alias       0/2
  · 10  Processus et ressources                  0/3

  10/38 tâches réussies.
  Prochaine étape : 3  →  python3 verify.py 3
  Énoncé          : etapes/03-creer.md
```

| Symbole | Signification |
|---|---|
| ✔ | étape validée |
| ◐ | étape commencée |
| · | étape à faire |

---

## La vérification détaillée d'une étape

```bash
python3 verify.py 3
```

```text
Étape 3 — Créer dossiers et fichiers
  ✔ Dossiers workspace/docs, workspace/data et workspace/tmp présents
  ✘ workspace/projets/2026/janvier introuvable
      ↳ Sans option, mkdir refuse de créer janvier tant que projets/2026 n'existe pas :
        cherchez dans l'extrait de man mkdir l'option qui crée aussi les dossiers parents
        manquants.
  ✔ workspace/data/todo.txt créé
  ✘ workspace/tmp/.cache introuvable
  ✘ workspace/docs/bonjour.txt ne contient qu'une ligne
      ↳ La redirection > remplace tout le contenu du fichier : pour ajouter une ligne à la
        fin, utilisez >>.
  → 2/5 : corrigez les points ✘ puis relancez python3 verify.py 3
```

Pour chaque tâche, le script affiche ✔ (réussie) ou ✘ (à corriger), suivi d'explications ↳ : ce qu'il a trouvé, pourquoi ce n'est pas le résultat attendu, et une piste. Corrigez un point à la fois, puis relancez.

---

## Les preuves

Le script ne voit pas votre écran. Quand une tâche ne laisse pas de trace, l'énoncé demande d'enregistrer ce qu'elle affiche dans `workspace/preuves/` avec une redirection :

```bash
commande > workspace/preuves/fichier.txt
```

---

## Les questions

Certaines tâches se vérifient par une question (un mot secret, une taille, un chemin...) dont la réponse s'obtient en exécutant les commandes. Le script la pose lors de `python3 verify.py N` et retient les bonnes réponses.

```text
  ? D'après la commande date, quel jour de la semaine sera le 1er janvier 2030 ?
    > 
```

- Tapez votre réponse puis Entrée
- Entrée seule passe la question : elle sera reposée au prochain lancement
- Une mauvaise réponse est expliquée, puis reposée au prochain lancement
- Une bonne réponse est mémorisée et n'est plus demandée

Le tableau de progression (`python3 verify.py` sans numéro) ne pose jamais de questions.

---

## Les données sources

`data/` ne doit jamais être modifié. Si c'est arrivé par erreur, le script le signale :

```text
⚠ Données sources altérées : data/fruits.txt (modifié)
```

Relancez `bash setup.sh` pour restaurer `data/`, votre travail dans `workspace/` est conservé.

Pour recommencer le TP de zéro (efface tout `workspace/`) :

```bash
bash setup.sh --reset
```

---

[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · [Guide de man](man.md) · **Script de vérification** · [Dépannage](depannage.md)
