# APT - Gestion des paquets

## Description

**APT** signifie *Advanced Package Tool*. C'est le système de gestion de paquets principal pour les distributions Linux basées sur **Debian** (Ubuntu, Linux Mint, etc.).

### Qu'est-ce qu'un paquet ?

Un **paquet** est un fichier compressé contenant :
- Les fichiers du logiciel (programmes, bibliothèques)
- Des métadonnées (version, dépendances, description)
- Des scripts d'installation et de désinstallation

### Comment fonctionne APT ?

APT utilise des **dépôts** (repositories) qui sont des serveurs contenant des milliers de paquets. Lorsque vous utilisez `apt update`, votre système télécharge la liste des paquets disponibles depuis ces dépôts.

```
┌──────────────┐     apt update     ┌───────────────────────┐
│   Votre PC   │ ─────────────────► │   Dépôt Ubuntu        │
│              │ ◄───────────────── │ (packages.ubuntu.com) │
└──────────────┘    liste paquets   └───────────────────────┘
```

### Différence entre apt et apt-get

| Commande | Usage |
|----------|-------|
| `apt` | Interface utilisateur moderne (recommandée) |
| `apt-get` | Outil de bas niveau pour les scripts |

## Commandes essentielles

### Mettre à jour la liste des paquets

```bash
sudo apt update
```

**Explication :** Cette commande ne télécharge pas de mises à jour. Elle met uniquement à jour la **liste locale des paquets disponibles** en contactant les serveurs de dépôts. Après cette commande, votre système sait quels paquets peuvent être mis à jour.

**Pourquoi c'est nécessaire ?** Sans `apt update`, votre système ne connaît pas les nouvelles versions disponibles.

### Mettre à jour le système

```bash
sudo apt upgrade
```

**Explication :** Cette commande installe les nouvelles versions de tous les paquets déjà installés. Elle **ne supprime jamais** de paquets existants et **n'installe jamais** de nouveaux paquets.

### Mise à jour complète

```bash
sudo apt full-upgrade
```

**Explication :** Similaire à `upgrade`, mais peut **supprimer des paquets** si nécessaire pour résoudre des dépendances complexes. Utile quand une mise à jour nécessite de retirer des paquets obsolètes.

### Installer un paquet

```bash
sudo apt install nom_du_paquet
```

**Explication :** Installe le paquet spécifié et **automatiquement toutes ses dépendances** (les autres paquets dont il a besoin pour fonctionner).

**Exemple :**
```bash
sudo apt install nginx
# Télécharge et installe nginx + toutes ses dépendances
```

### Mettre à jour un seul paquet

```bash
sudo apt install --only-upgrade nom_du_paquet
```

### Supprimer un paquet

```bash
sudo apt remove nom_du_paquet
```

**Explication :** Supprime le paquet mais **conserve les fichiers de configuration**. Pratique si vous voulez réinstaller le logiciel plus tard.

### Supprimer complètement un paquet

```bash
sudo apt purge nom_du_paquet
```

**Explication :** Supprime le paquet **ET ses fichiers de configuration**. Utilisez cette commande pour un nettoyage complet.

### Nettoyer les paquets inutilisés

```bash
sudo apt autoremove
```

**Explication :** Quand vous installez un paquet, ses dépendances restent parfois sur le système. Cette commande supprime les dépendances **qui ne sont plus utilisées par aucun paquet**.

### Lister les paquets installés

```bash
apt list --installed
```

Affiche la liste de tous les paquets installés sur votre système.

### Lister les paquets pouvant être mis à jour

```bash
apt list --upgradable
```

### Rechercher un paquet

```bash
apt search nom_du_paquet
```

Recherche dans les descriptions des paquets disponibles.

### Afficher les informations d'un paquet

```bash
apt show nom_du_paquet
```

Affiche les détails : version, taille, description, dépendances.

## Workflow classique de mise à jour

```bash
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
```

| Étape | Commande | Rôle |
|-------|----------|------|
| 1 | `apt update` | Met à jour la liste des paquets |
| 2 | `apt upgrade` | Installe les mises à jour |
| 3 | `autoremove` | Nettoie les dépendances inutiles |
| 4 | `-y` | Répond "oui" automatiquement aux questions |

## Fichiers de configuration

### Sources des dépôts

```bash
sudo nano /etc/apt/sources.list
```

Ce fichier contient les adresses des dépôts utilisés par votre système.

Exemple de ligne :
```
deb http://fr.archive.ubuntu.com/ubuntu/ jammy main restricted
```

### Signification des lignes

- `deb` : paquets binaires précompilés
- `deb-src` : код source des paquets
- `jammy` : nom de code de la version Ubuntu
- `main`, `restricted`, `universe` : sections du dépôt

## Dépôts tiers (PPA)

### Ajouter un PPA (Personal Package Archive)

```bash
sudo add-apt-repository ppa:nom_du_ppa
sudo apt update
sudo apt install nom_du_paquet
```

### Supprimer un dépôt

```bash
sudo add-apt-repository --remove ppa:nom_du_ppa
```

## Nettoyage

### Vider le cache des paquets

```bash
sudo apt clean
```

Supprime tous les fichiers `.deb` téléchargés du cache.

### Supprimer uniquement les paquets obsolètes du cache

```bash
sudo apt autoclean
```

## Bonnes pratiques

1. **Toujours faire `apt update` avant `apt install` ou `apt upgrade`**
2. **Lire les messages d'APT** : il indique souvent ce qui va être installé ou supprimé
3. **Utiliser `apt` plutôt que `apt-get`** pour les commandes interactives
4. **Faire des sauvegardes** avant les mises à jour majeures du système
5. **Vérifier l'espace disque** avec `df -h` avant les mises à jour
