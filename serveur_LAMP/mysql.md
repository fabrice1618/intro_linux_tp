# MySQL et mysqladmin - Base de données

## Description

**MySQL** est un système de gestion de bases de données relationnelles (SGBDR) très populaire. Il permet de stocker, organiser et récupérer des données de manière structurée.

**mysqladmin** est l'outil en ligne de commande pour les tâches d'administration du serveur MySQL.

### Qu'est-ce qu'une base de données ?

Une base de données est un système organisé pour stocker des données :

```
┌─────────────────────────────────────────────────────────────┐
│                      SERVEUR MySQL                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐     ┌─────────────────┐                │
│  │  Base: ecole    │     │ Base: boutique  │                │
│  ├─────────────────┤     ├─────────────────┤                │
│  │ Table: etudiants│     │ Table: produits │                │
│  │ Table: notes    │     │ Table: commandes│                │
│  │ Table: cours    │     │ Table: clients  │                │
│  └─────────────────┘     └─────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Vocabulaire important

| Terme | Explication |
|-------|-------------|
| **Base de données** | Conteneur qui stocke des tables |
| **Table** | Structure de données avec lignes et colonnes |
| **Ligne/Enregistrement** | Une entrée dans la table |
| **Colonne/Champ** | Un attribut des données |
| **Clé primaire** | Identifiant unique pour chaque ligne |
| **SQL** | Langage de requête structuré |

## Installation

### Installation de MySQL Server

```bash
sudo apt update
sudo apt install mysql-server
```

### Démarrer et activer MySQL

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Vérifier le statut

```bash
sudo systemctl status mysql
```

### Connexion initiale

```bash
sudo mysql
```

Sur Ubuntu, MySQL peut être accessible sans mot de passe root.

## Commandes mysqladmin

`mysqladmin` est utilisé pour les opérations d'administration depuis le terminal.

### Vérifier si MySQL fonctionne

```bash
mysqladmin -u root -p ping
```

Si MySQL fonctionne, affiche : `mysqld is alive`

### Afficher le statut du serveur

```bash
mysqladmin -u root -p status
```

Affiche :
- Temps d'activité (Uptime)
- Nombre de threads
- Requêtes par seconde

### Afficher les variables du serveur

```bash
mysqladmin -u root -p variables
```

Affiche toutes les variables de configuration de MySQL.

### Afficher les variables étendues

```bash
mysqladmin -u root -p extended-status
```

### Créer une base de données

```bash
mysqladmin -u root -p create ma_base
```

Crée une nouvelle base de données vide.

### Supprimer une base de données

```bash
mysqladmin -u root -p drop ma_base
```

**⚠️ ATTENTION :** Cette opération est irréversible !

### Définir le mot de passe root

```bash
mysqladmin -u root password 'nouveau_mot_de_passe'
```

### Changer le mot de passe root

```bash
mysqladmin -u root -p password 'ancien_mot_de_passe' 'nouveau_mot_de_passe'
```

### Arrêter le serveur MySQL

```bash
mysqladmin -u root -p shutdown
```

### Recharger les privilèges

```bash
mysqladmin -u root -p reload
```

Force MySQL à relire les tables de privilèges.

### Rafraîchir les tables

```bash
mysqladmin -u root -p refresh
```

Ferme et réouvre les fichiers de logs.

### Afficher les processus

```bash
mysqladmin -u root -p processlist
```

Affiche toutes les connexions actives et leurs requêtes.

### Voir l'aide

```bash
mysqladmin --help
```

## Commandes MySQL interactives

Pour utiliser MySQL de manière interactive, on utilise la commande `mysql`.

### Se connecter à MySQL

```bash
mysql -u root -p
```

Affiche le prompt MySQL :
```
Welcome to MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.32 MySQL Community Server

mysql>
```

### Afficher les bases de données

```sql
SHOW DATABASES;
```

Affiche toutes les bases de données.

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

### Créer une base de données

```sql
CREATE DATABASE ecole;
```

Crée une base de données nommée "ecole".

### Utiliser une base

```sql
USE ecole;
```

Sélectionne la base de données "ecole" pour les opérations suivantes.

### Afficher les tables

```sql
SHOW TABLES;
```

Affiche les tables de la base de données active.

### Créer une table

```sql
CREATE TABLE etudiants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE,
    date_naissance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Explication des types :**
| Type | Description |
|------|-------------|
| `INT` | Nombre entier |
| `VARCHAR(n)` | Texte variable (max n caractères) |
| `DATE` | Date (AAAA-MM-JJ) |
| `TIMESTAMP` | Date et heure |
| `AUTO_INCREMENT` | Numéro automatique |
| `PRIMARY KEY` | Clé primaire (identifiant unique) |
| `NOT NULL` | Champ obligatoire |
| `UNIQUE` | Valeur unique dans la colonne |

### Types de données courants

| Type | Usage | Exemple |
|------|-------|---------|
| `INT` | Nombres entiers | 1, 42, -5 |
| `BIGINT` | Grands nombres | 9999999999 |
| `VARCHAR(n)` | Texte court | "Jean", "email@test.com" |
| `TEXT` | Texte long | Articles, descriptions |
| `DATE` | Date | 2024-01-15 |
| `DATETIME` | Date et heure | 2024-01-15 14:30:00 |
| `DECIMAL(10,2)` | Nombre décimal | 19.99 |
| `BOOLEAN` | Vrai/Faux | TRUE, FALSE |

### Insérer des données

```sql
INSERT INTO etudiants (nom, prenom, email, date_naissance)
VALUES ('Dupont', 'Marie', 'marie.dupont@email.com', '2003-05-12');
```

Insérer plusieurs lignes :

```sql
INSERT INTO etudiants (nom, prenom, email) VALUES
('Martin', 'Pierre', 'pierre@email.com'),
('Bernard', 'Sophie', 'sophie@email.com'),
('Petit', 'Lucas', 'lucas@email.com');
```

### Lire les données (SELECT)

```sql
-- Tous les étudiants
SELECT * FROM etudiants;

-- Colonnes spécifiques
SELECT nom, prenom FROM etudiants;

-- Avec condition
SELECT * FROM etudiants WHERE id = 1;

-- Avec filtrage
SELECT * FROM etudiants WHERE nom = 'Dupont';

-- Tri
SELECT * FROM etudiants ORDER BY nom ASC;
SELECT * FROM etudiants ORDER BY date_naissance DESC;

-- Limiter les résultats
SELECT * FROM etudiants LIMIT 10;

-- Compter
SELECT COUNT(*) FROM etudiants;
```

### Mettre à jour des données

```sql
UPDATE etudiants 
SET email = 'nouveau@email.com' 
WHERE id = 1;
```

**⚠️ IMPORTANT :** Toujours préciser `WHERE` sinon TOUTES les lignes seront modifiées !

### Supprimer des données

```sql
DELETE FROM etudiants WHERE id = 3;
```

**⚠️ IMPORTANT :** Toujours préciser `WHERE` sinon TOUTES les lignes seront supprimées !

### Supprimer une table

```sql
DROP TABLE etudiants;
```

### Supprimer une base de données

```sql
DROP DATABASE ecole;
```

## Gestion des utilisateurs

### Créer un utilisateur

```sql
CREATE USER 'utilisateur'@'localhost' IDENTIFIED BY 'mot_de_passe';
```

- `'localhost'` : Se connecte uniquement depuis la machine locale
- `'%'` : Se connecte depuis n'importe où

### Accorder des privilèges

```sql
-- Tous les privilèges sur une base
GRANT ALL PRIVILEGES ON ma_base.* TO 'utilisateur'@'localhost';

-- Privilèges spécifiques
GRANT SELECT, INSERT, UPDATE ON ma_base.* TO 'utilisateur'@'localhost';

-- Accès lecture seule
GRANT SELECT ON ma_base.* TO 'lecteur'@'localhost';
```

### Appliquer les privilèges

```sql
FLUSH PRIVILEGES;
```

**Obligatoire** après modification des privilèges !

### Révoquer des privilèges

```sql
REVOKE ALL PRIVILEGES ON ma_base.* FROM 'utilisateur'@'localhost';
FLUSH PRIVILEGES;
```

### Supprimer un utilisateur

```sql
DROP USER 'utilisateur'@'localhost';
```

### Afficher les privilèges d'un utilisateur

```sql
SHOW GRANTS FOR 'utilisateur'@'localhost';
```

### Privilèges courants

| Privilège | Description |
|-----------|-------------|
| `SELECT` | Lire les données |
| `INSERT` | Ajouter des données |
| `UPDATE` | Modifier des données |
| `DELETE` | Supprimer des données |
| `CREATE` | Créer des tables/bases |
| `DROP` | Supprimer des tables/bases |
| `ALL PRIVILEGES` | Tous les privilèges |

## Sauvegarde et restauration

### Sauvegarder une base

```bash
mysqldump -u root -p ma_base > sauvegarde.sql
```

Crée un fichier SQL contenant toutes les données.

### Sauvegarder avec compression

```bash
mysqldump -u root -p ma_base | gzip > sauvegarde.sql.gz
```

### Sauvegarder toutes les bases

```bash
mysqldump -u root -p --all-databases > sauvegarde_totale.sql
```

### Sauvegarder uniquement la structure

```bash
mysqldump -u root -p --no-data ma_base > structure.sql
```

### Restaurer une base

```bash
mysql -u root -p ma_base < sauvegarde.sql
```

### Restaurer dans une base existante

```bash
mysql -u root -p ma_base < sauvegarde.sql
```

La base doit exister (CREATE DATABASE si nécessaire).

## Sécurisation

### Script de sécurisation

```bash
sudo mysql_secure_installation
```

Ce script propose de :
1. Définir un mot de passe root
2. Supprimer les utilisateurs anonymes
3. Désactiver la connexion root distante
4. Supprimer la base de test

### Bonnes pratiques de sécurité

1. **Utiliser des mots de passe forts**
2. **Limiter les accès** (localhost plutôt que %)
3. **Appliquer le principe du moindre privilège**
4. **Sauvegarder régulièrement**
5. **Mettre à jour MySQL**

## MariaDB

**MariaDB** est un fork de MySQL créé après l'acquisition de MySQL par Oracle. Il est :
- 100% compatible avec MySQL
- Installé par défaut sur certaines distributions
- Utilise les mêmes commandes et outils

### Installation de MariaDB

```bash
sudo apt install mariadb-server
sudo systemctl start mariadb
```

### Se connecter

```bash
sudo mysql
# ou
mysql -u root -p
```

Les commandes MySQL fonctionnent identiques.

## Exemples pratiques

### Requêtes JOIN

```sql
-- INNER JOIN : uniquement les articles avec commentaires
SELECT articles.titre, commentaires.message
FROM articles
INNER JOIN commentaires ON articles.id = commentaires.article_id;

-- LEFT JOIN : tous les articles, avec leurs commentaires (si existants)
SELECT a.titre, c.message
FROM articles a
LEFT JOIN commentaires c ON a.id = c.article_id;
```

## Commandes utiles dans MySQL

| Commande | Description |
|----------|-------------|
| `SHOW DATABASES;` | Liste des bases |
| `USE db_name;` | Sélectionner une base |
| `SHOW TABLES;` | Liste des tables |
| `DESCRIBE table;` | Structure d'une table |
| `SHOW CREATE TABLE table;` | SQL de création |
| `EXIT;` ou `QUIT;` | Quitter MySQL |
| `Ctrl+C` | Annuler la commande en cours |
