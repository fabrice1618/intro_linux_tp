[Sommaire](../readme.md) · [← Étape 5](05-rechercher.md) · **Étape 6 / 10** · [Étape 7 →](07-archiver.md)

# Étape 6 — Filtres et redirections (pipes)

- **Objectif** : combiner des commandes simples pour extraire, trier, compter et transformer du texte
- **Commandes** : `head` · `tail` · `sort` · `uniq` · `wc` · `tr` · `cut` · `grep`
- **À produire** : 6 fichiers dans `workspace/data/`
- **Aides** : [Aide-mémoire](../aide/memo.md) · [Guide de man](../aide/man.md) · [Dépannage](../aide/depannage.md)

---

## Comprendre

La puissance de Linux réside dans la capacité à **combiner des commandes simples** pour réaliser des traitements complexes. C'est la philosophie Unix : chaque outil fait une chose, mais la fait bien, et on les combine.

### Le pipe `|`

Il connecte la sortie d'une commande à l'entrée de la suivante.

```bash
cat fichier.txt | grep "mot"                   # affiche le fichier puis filtre les lignes contenant "mot"
cat fichier.txt | grep "mot" > resultat.txt    # même chose, résultat enregistré dans un fichier
```

### Les filtres

Commandes qui lisent l'entrée, la transforment, et produisent une sortie. Opérations courantes :

- Extraire des portions : premières/dernières lignes, colonnes spécifiques
- Trier : ordre alphabétique, numérique, inverse
- Dédupliquer : enlever les doublons (nécessite un tri préalable avec `uniq`)
- Compter : lignes, mots, caractères
- Transformer : changer la casse, remplacer des caractères

### Les redirections

- `>` envoie le résultat dans un fichier au lieu de l'écran
- `<` fait l'inverse : il fournit le contenu d'un fichier comme entrée d'une commande (`tr ... < fichier`)

```mermaid
flowchart LR
    F[("fichier.txt")] -->|"#lt; : stdin"| C1["cmd1"]
    C1 -->|"tube : stdout vers stdin"| C2["cmd2"]
    C2 -->|"#gt; : stdout"| S[("resultat.txt")]
```

> [!CAUTION]
> Ne redirigez jamais vers le fichier que vous lisez. `sort f > f` vide `f`, car le shell vide le fichier de destination avant même que `sort` ne commence à le lire.

---

## À réaliser

> [!TIP]
> Construisez chaque commande pas à pas : affichez d'abord le résultat à l'écran, ajoutez un filtre avec `|`, vérifiez, et seulement quand le résultat est bon, rappelez la commande (flèche ↑) pour ajouter la redirection `> fichier`.

### Tâche 1 — Extraire des lignes

Créer `workspace/data/lorem_extrait.txt` contenant les lignes 2 à 4 de `data/lorem.txt` (combinez deux commandes avec un pipe).

- **Résultat** : le fichier `workspace/data/lorem_extrait.txt` (3 lignes)
- **Documentation** : [`man head`](#man-head) · [`man tail`](#man-tail)

Pour comparer avec l'original, affichez-le avec les numéros de ligne :

```bash
cat -n data/lorem.txt
```

<details>
<summary>💡 Indice</summary>

`head -n 4` garde les 4 premières lignes ; il reste à ne conserver que les 3 dernières de celles-ci, avec une deuxième commande reliée par un pipe `|`.

</details>

### Tâche 2 — Trier et dédupliquer

Créer `workspace/data/fruits_uniques.txt` : trier `data/fruits.txt` et enlever les doublons.

- **Résultat** : le fichier `workspace/data/fruits_uniques.txt`, trié et sans doublon
- **Documentation** : [`man sort`](#man-sort) · [`man uniq`](#man-uniq)

<details>
<summary>💡 Indice</summary>

`uniq` ne supprime que les doublons **consécutifs** : triez d'abord avec `sort`, puis transmettez le résultat à `uniq` avec un pipe `|`. `uniq -c` ajoute le nombre d'occurrences : ici on veut seulement la liste.

</details>

### Tâche 3 — Compter les mots

Créer `workspace/data/lorem_wc.txt` contenant le nombre de mots du fichier `lorem.txt`.

- **Résultat** : le fichier `workspace/data/lorem_wc.txt`
- **Documentation** : [`man wc`](#man-wc)

<details>
<summary>💡 Indice</summary>

Sans option, `wc` affiche lignes, mots et octets : choisissez l'option qui n'affiche que les mots.

</details>

### Tâche 4 — Passer en majuscules

Créer `workspace/data/fruits_upper.txt` : convertir `data/fruits.txt` en MAJUSCULES, sans changer l'ordre des lignes.

- **Résultat** : le fichier `workspace/data/fruits_upper.txt`
- **Documentation** : [`man tr`](#man-tr)

<details>
<summary>💡 Indice</summary>

`tr` lit uniquement son entrée standard (pipe ou `<`) : il ne prend pas de nom de fichier en argument. Il remplace chaque caractère de la 1re liste par le caractère correspondant de la 2e : voyez les classes `[:lower:]` et `[:upper:]`.

Bon à savoir : `pêche` devient `PêCHE`, car `tr` ne convertit pas les lettres accentuées. C'est une limite connue de `tr`, acceptée par le script.

</details>

### Tâche 5 — Extraire une colonne

Extraire la 2ème colonne de `data/sample.csv` vers `workspace/data/col2.txt`.

- **Résultat** : le fichier `workspace/data/col2.txt`, une valeur par ligne
- **Documentation** : [`man cut`](#man-cut)

Regardez d'abord comment les colonnes sont séparées :

```bash
cat data/sample.csv
```

<details>
<summary>💡 Indice</summary>

Sans `-d`, `cut` découpe sur la tabulation : indiquez la virgule comme délimiteur. Les champs sont numérotés à partir de 1.

</details>

### Tâche 6 — Compter des lignes filtrées

Créer `workspace/data/nb_info.txt` contenant le nombre de lignes `INFO` du journal `data/logs/app.log`.

- **Résultat** : le fichier `workspace/data/nb_info.txt`, qui contient un nombre
- **Documentation** : [`man grep`](05-rechercher.md#man-grep) (étape 5) · [`man wc`](#man-wc)

<details>
<summary>💡 Indice</summary>

Filtrez d'abord les lignes `INFO` avec `grep`, puis transmettez le résultat, avec un pipe `|`, à la commande qui compte les lignes.

</details>

---

## Documentation

### `man head`

```text
$ man head
DESCRIPTION
       Print  the first 10 lines of each FILE to standard output.

       -n, --lines=[-]NUM
              print the first NUM lines instead of the first  10;  with  the
              leading '-', print all but the last NUM lines of each file
```

### `man tail`

```text
$ man tail
       -n, --lines=[+]NUM
              output the last NUM lines, instead of the last 10; or  use  -n
              +NUM to skip NUM-1 lines at the start
```

`head -n N` / `tail -n N` : les N premières / dernières lignes.

### `man sort`

```text
$ man sort
DESCRIPTION
       Write sorted concatenation of all FILE(s) to standard output.

       -f, --ignore-case
              fold lower case to upper case characters

       -r, --reverse
              reverse the result of comparisons
```

### `man uniq`

```text
$ man uniq
DESCRIPTION
       Filter  adjacent matching lines from INPUT (or standard input), writ‐
       ing to OUTPUT (or standard output).

       -c, --count
              prefix lines by the number of occurrences
```

`uniq` ne supprime que les lignes identiques **adjacentes** (consécutives), d'où le tri préalable avec `sort`.

### `man wc`

```text
$ man wc
       -c, --bytes
              print the byte counts

       -l, --lines
              print the newline counts

       -w, --words
              print the word counts
```

`wc` compte les lignes (`-l`), les mots (`-w`) ou les octets (`-c`).

### `man tr`

```text
$ man tr
SYNOPSIS
       tr [OPTION]... STRING1 [STRING2]
DESCRIPTION
       Translate,  squeeze,  and/or  delete  characters from standard input,
       writing to standard output.

       [:lower:]
              all lower case letters

       [:upper:]
              all upper case letters
```

`tr` lit uniquement son entrée standard (pipe ou `<`) : il ne prend pas de nom de fichier en argument.

### `man cut`

```text
$ man cut
       -d, --delimiter=DELIM
              use DELIM instead of TAB for field delimiter

       -f, --fields=LIST
              select only these fields
```

`cut -d` choisit le délimiteur (tabulation par défaut), `-f` le numéro du champ, en commençant à 1.

---

## Valider

```bash
python3 verify.py 6
```

Quand tout est juste :

```text
  → Étape 6 validée (6/6). Étape suivante : 7 (etapes/07-archiver.md).
```

---

[Sommaire](../readme.md) · [← Étape 5](05-rechercher.md) · **Étape 6 / 10** · [Étape 7 →](07-archiver.md)
