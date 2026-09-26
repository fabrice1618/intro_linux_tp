[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · [Guide de man](man.md) · [Script de vérification](verification.md) · **Dépannage**

# Dépannage

Les problèmes les plus fréquents, classés par symptôme. Le réflexe de base : **lire le message d'erreur**, puis vérifier où vous êtes avec `pwd`.

- [Le terminal ne répond plus](#le-terminal-ne-répond-plus)
- [Messages d'erreur fréquents](#messages-derreur-fréquents)
- [Problèmes avec le script de vérification](#problèmes-avec-le-script-de-vérification)
- [Recommencer](#recommencer)

---

## Le terminal ne répond plus

| Symptôme | Cause probable | Solution |
|---|---|---|
| Une page de texte s'affiche, avec `:` ou `(END)` en bas | vous êtes dans `man` (ou `less`) | `q` pour quitter |
| Le curseur attend, sans invite de commande | la commande attend du texte au clavier (par exemple `cat` ou `tr` sans fichier), ou elle tourne encore | `Ctrl+C` pour l'interrompre |
| L'invite devient `>` | un guillemet `"` ou `'` n'est pas fermé | `Ctrl+C`, puis retapez la commande |
| `sleep 1000` bloque le terminal | lancé sans `&`, il est au premier plan | `Ctrl+C` pour l'arrêter, puis relancez-le avec `&` |
| L'écran est encombré | — | `Ctrl+L` ou `clear` |

---

## Messages d'erreur fréquents

### `Aucun fichier ou dossier de ce nom`

```text
cat: nexiste_pas.txt: Aucun fichier ou dossier de ce nom
```

Le chemin ne mène à rien **depuis le répertoire courant**. Vérifiez :

```bash
pwd       # où suis-je ?
ls        # qu'y a-t-il ici ?
```

Utilisez la touche **Tab** pour compléter les noms : si Tab ne complète rien, le chemin est faux. Attention aussi aux majuscules : `Fruits.txt` et `fruits.txt` sont deux noms différents.

### `commande introuvable`

```text
lss : commande introuvable
```

Faute de frappe dans le nom de la commande, ou mauvaise casse (`LS` au lieu de `ls`).

### `Permission non accordée`

```text
bash: ./data/salut.sh: Permission non accordée
```

Le fichier n'a pas le droit d'exécution `x` : voir l'[étape 8](../etapes/08-liens-permissions.md).

### `-r non spécifié ; omission du répertoire`

```text
cp: -r non spécifié ; omission du répertoire 'data'
```

`cp` ne copie un dossier qu'avec l'option récursive : voir l'[étape 4](../etapes/04-copier-deplacer-supprimer.md).

### `est un dossier` ou `Le dossier n'est pas vide`

```text
rm: impossible de supprimer 'data': est un dossier
rmdir: impossible de supprimer 'workspace': Le dossier n'est pas vide
```

`rm` sans option ne supprime que des fichiers, `rmdir` que des dossiers vides : voir l'[étape 4](../etapes/04-copier-deplacer-supprimer.md).

### `impossible de créer le répertoire`

```text
mkdir: impossible de créer le répertoire «workspace/a/b/c»: Aucun fichier ou dossier de ce nom
mkdir: impossible de créer le répertoire «workspace»: Le fichier existe
```

- `Aucun fichier ou dossier de ce nom` : un dossier parent manque, voir l'option `-p` à l'[étape 3](../etapes/03-creer.md)
- `Le fichier existe` : le dossier existe déjà, il n'y a rien à faire

### Un fichier est devenu vide

Une redirection vers le fichier que l'on lit le vide : `sort f > f` vide `f`, car le shell vide le fichier de destination avant même que `sort` ne commence à le lire. Écrivez toujours le résultat dans un **autre** fichier. Si c'est arrivé dans `data/`, relancez `bash setup.sh`.

---

## Problèmes avec le script de vérification

### `L'environnement du TP n'est pas prêt`

```text
✘ L'environnement du TP n'est pas prêt. Lancez d'abord :  bash setup.sh
```

Lancez `bash setup.sh` depuis le dossier du TP.

### `Données sources altérées`

```text
⚠ Données sources altérées : data/fruits.txt (modifié)
```

Un fichier de `data/` a été modifié ou supprimé par erreur. Relancez `bash setup.sh` : `data/` est restauré, votre travail dans `workspace/` est conservé.

### `introuvable`, alors que le fichier existe

Le fichier a sans doute été créé ailleurs, à cause d'un mauvais répertoire courant. Le script l'indique quand il le trouve :

```text
  ✘ workspace/preuves/find_fruits.txt introuvable
      ↳ Un « find_fruits.txt » existe ailleurs : workspace/find_fruits.txt. Mauvais répertoire
        courant ? Vérifiez avec pwd, puis placez le fichier au bon endroit.
      ↳ Redirigez la sortie de find vers ce fichier.
```

Déplacez-le avec `mv`, ou refaites la tâche depuis le dossier du TP.

### `MYVAR n'est pas visible par ce script` (étape 9)

- La variable n'est pas exportée : `export MYVAR`
- Le script est lancé depuis un autre terminal : chaque terminal a son propre shell, avec ses propres variables

### L'alias `verif` a disparu (étape 9)

Un alias n'existe que dans le shell où il a été défini : un nouveau terminal ne le connaît pas. Redéfinissez-le, ou voyez le bonus de l'[étape 9](../etapes/09-variables-alias.md#pour-aller-plus-loin).

### `Vérification impossible`

Une erreur imprévue dans le script : signalez le message à l'enseignant.

---

## Recommencer

| Besoin | Commande | Effet |
|---|---|---|
| Restaurer les fichiers sources | `bash setup.sh` | recrée `data/`, **conserve** `workspace/` |
| Recommencer tout le TP | `bash setup.sh --reset` | recrée `data/`, **efface** `workspace/` et les réponses mémorisées |
| Refaire une tâche | — | supprimez ou corrigez le fichier concerné dans `workspace/`, puis relancez la vérification |

---

[Sommaire](../readme.md) · Aides : [Aide-mémoire](memo.md) · [Guide de man](man.md) · [Script de vérification](verification.md) · **Dépannage**
