# PHP - Langage de script serveur

## Description

**PHP** (PHP: Hypertext Preprocessor) est un langage de script côté serveur principalement utilisé pour le développement web. Il permet de créer des pages web dynamiques qui peuvent afficher différents contenus selon les utilisateurs, les heures, ou les données stockées.

### Comment fonctionne PHP ?

```
┌──────────────┐         INTERNET        ┌──────────────────┐
│              │                         │                  │
│   Navigateur │  1. Requête PHP         │    SERVEUR       │
│              │ ──────────────────────► │                  │
│              │ ◄────────────────────── │  Apache + PHP    │
│              │  2. Réponse HTML        │                  │
└──────────────┘                         │  1. Lit le code  │
                                         │  2. L'exécute    │
┌──────────────┐                         │  3. Génère HTML  │
│ Page affichée│◄────────────────────────└────────┬─────────┘
│ (résultat)   │                                  │
└──────────────┘                                  ▼
                                          ┌──────────────┐
                                          │   MySQL      │
                                          │ (données)    │
                                          └──────────────┘

Séquence：
1. Navigateur → Serveur : "Voici ma requête pour page.php"
2. Apache lit page.php
3. PHP exécute le code (peut lire/écrire dans MySQL)
4. PHP génère du HTML
5. Apache envoie le HTML au navigateur
6. Navigateur affiche la page
```

### PHP vs HTML statique

| HTML | PHP |
|------|-----|
| Même contenu pour tous | Contenu dynamique |
| Fichiers `.html` | Fichiers `.php` |
| Affiché tel quel | Exécuté côté serveur |
| Pas d'interaction avec BD | Peut accéder aux bases de données |

### PHP et MySQL : Le stack LAMP

**LAMP** est un acronyme pour l'ensemble des logiciels open-source utilisés ensemble :

| Lettre | Logiciel | Rôle |
|--------|----------|------|
| **L** | Linux | Système d'exploitation |
| **A** | Apache | Serveur web |
| **M** | MySQL | Base de données |
| **P** | PHP | Langage de script |

## Installation

### Installer PHP avec Apache

```bash
sudo apt update
sudo apt install php libapache2-mod-php
```

Le module `libapache2-mod-php` permet à Apache d'exécuter PHP.

### Installer PHP-FPM

PHP-FPM (FastCGI Process Manager) est une alternative plus performante :

```bash
sudo apt install php-fpm
sudo a2enmod proxy_fcgi setenvif
sudo a2enconf php*-fpm
```

### Installer des extensions courantes

```bash
sudo apt install php-mysql php-curl php-gd php-mbstring php-xml php-zip
```

### Extensions importantes

| Extension | Commande d'installation | Usage |
|-----------|------------------------|-------|
| php-mysql | php-mysql | Connexion MySQL/MariaDB |
| php-pdo | php-mysql | Interface d'accès aux bases (PDO) |
| php-curl | php-curl | Requêtes HTTP (API) |
| php-gd | php-gd | Création/manipulation d'images |
| php-mbstring | php-mbstring | Gestion texte UTF-8 |
| php-xml | php-xml | Parsing XML |
| php-zip | php-zip | Lecture/écriture fichiers ZIP |
| php-intl | php-intl | Internationalisation |

### Redémarrer Apache

```bash
sudo systemctl restart apache2
```

## Vérification de l'installation

### Vérifier la version de PHP

```bash
php -v
```

Affiche quelque chose comme :
```
PHP 8.1.2 (cli)
Copyright (c) 1997-2022 The PHP Group
```

### Vérifier les modules PHP chargés

```bash
php -m
```

Liste tous les modules PHP disponibles.

### Page phpinfo()

Créez le fichier `/var/www/html/info.php` :

```php
<?php
phpinfo();
?>
```

Accédez-y via : `http://adresse_ip/info.php`

Cette page affiche toutes les informations de configuration PHP.

**⚠️ IMPORTANT :** Supprimez ce fichier après utilisation en production !

## Configuration PHP

### Emplacement des fichiers de configuration

```
/etc/php/*/apache2/php.ini    # Configuration pour Apache
/etc/php/*/cli/php.ini        # Configuration en ligne de commande
/etc/php/*/fpm/php.ini        # Configuration PHP-FPM
```

L'astérisque `*` représente la version de PHP (ex: `8.1`).

### Trouver la version exacte

```bash
php -i | grep "Loaded Configuration File"
```

### Modifier la configuration

```bash
sudo nano /etc/php/8.1/apache2/php.ini
```

Puis recherchez et modifiez les paramètres souhaités.

### Paramètres importants

```ini
; Taille maximale des fichiers uploadés
upload_max_filesize = 20M

; Taille maximale des données POST
post_max_size = 25M

; Mémoire maximale pour un script
memory_limit = 256M

; Affichage des erreurs (development = On, production = Off)
display_errors = On
error_reporting = E_ALL

; Timezone
date.timezone = Europe/Paris

; Durée d'exécution maximale (secondes)
max_execution_time = 300

; Taille maximale des données entrantes
max_input_vars = 1000
```

### Recharger la configuration Apache

```bash
sudo systemctl reload apache2
```

## Configuration PHP-FPM

### Démarrer PHP-FPM

```bash
sudo systemctl start php*-fpm
sudo systemctl enable php*-fpm
```

### Vérifier le statut

```bash
sudo systemctl status php*-fpm
```

### Redémarrer PHP-FPM

```bash
sudo systemctl restart php*-fpm
```

### Changer de version PHP-FPM

```bash
# Voir les versions disponibles
ls /etc/php/

# Activer une version
sudo a2enconf php8.1-fpm
sudo a2disconf php7.4-fpm
```

## Les bases du PHP

### Syntaxe de base

```php
<?php
// Code PHP ici
?>
```

Tout code PHP doit être entre les balises `<?php` et `?>`.

### Commentaires

```php
<?php
// Commentaire sur une ligne

# Autre style de commentaire sur une ligne

/*
   Commentaire
   multi-lignes
*/
?>
```

### Afficher du texte

```php
<?php
echo "Bonjour le monde !";
echo "<h1>Titre en HTML</h1>";
?>
```

## Variables

### Déclaration et types

```php
<?php
// Types de base
$nom = "Linux";          // Chaîne de caractères (string)
$version = 2;            // Nombre entier (integer)
$prix = 19.99;           // Nombre décimal (float)
$actif = true;           // Booléen (boolean)

// Affichage
echo $nom;               // Affiche: Linux
echo $version;           // Affiche: 2
?>
```

### Concaténation

```php
<?php
$prenom = "Jean";
$nom = "Dupont";

// Avec points
echo $prenom . " " . $nom;  // Jean Dupont

// Dans une chaîne avec guillemets doubles
echo "$prenom $nom";         // Jean Dupont
?>
```

### Types de données

| Type | Exemple | Description |
|------|---------|-------------|
| `string` | `"Bonjour"` | Texte |
| `int` | `42`, `-17` | Nombre entier |
| `float` | `3.14`, `-0.5` | Nombre décimal |
| `bool` | `true`, `false` | Booléen |
| `array` | `[1, 2, 3]` | Tableau |
| `NULL` | `NULL` | Valeur nulle |

## Tableaux

### Tableaux numérotés

```php
<?php
// Ancienne syntaxe
$couleurs = array("rouge", "vert", "bleu");

// Syntaxe moderne
$fruits = ["pomme", "banane", "orange"];

// Accéder aux éléments
echo $fruits[0];  // pomme
echo $fruits[1];  // banane

// Nombre d'éléments
echo count($fruits);  // 3
?>
```

### Tableaux associatifs

```php
<?php
$utilisateur = [
    "nom" => "Dupont",
    "prenom" => "Marie",
    "email" => "marie@email.com",
    "age" => 25
];

// Accéder aux éléments
echo $utilisateur["nom"];     // Dupont
echo $utilisateur["email"];   // marie@email.com

// Modifier une valeur
$utilisateur["age"] = 26;

// Ajouter un élément
$utilisateur["ville"] = "Paris";
?>
```

### Boucle sur un tableau

```php
<?php
$fruits = ["pomme", "banane", "orange"];

// foreach - syntaxe recommandée
foreach ($fruits as $fruit) {
    echo $fruit . "<br>";
}

// foreach avec clé et valeur
$capitales = [
    "France" => "Paris",
    "Allemagne" => "Berlin",
    "Espagne" => "Madrid"
];

foreach ($capitales as $pays => $capitale) {
    echo "$capitale est la capitale de $pays<br>";
}
?>
```

## Conditions

### If / elseif / else

```php
<?php
$age = 18;

if ($age >= 18) {
    echo "Majeur";
} elseif ($age >= 12) {
    echo "Adolescent";
} else {
    echo "Enfant";
}

// Opérateur ternaire (raccourci)
echo $age >= 18 ? "Majeur" : "Mineur";
?>
```

### Opérateurs de comparaison

| Opérateur | Signification |
|-----------|---------------|
| `==` | Égal (valeur) |
| `===` | Égal (valeur ET type) |
| `!=` | Différent |
| `<>` | Différent |
| `<` | Inférieur |
| `>` | Supérieur |
| `<=` | Inférieur ou égal |
| `>=` | Supérieur ou égal |

### Switch

```php
<?php
$jour = date("l");  // Nom anglais du jour

switch ($jour) {
    case "Monday":
        echo "Lundi";
        break;
    case "Tuesday":
        echo "Mardi";
        break;
    case "Wednesday":
        echo "Mercredi";
        break;
    default:
        echo "Autre jour";
}
?>
```

## Boucles

### Boucle for

```php
<?php
// Compter de 1 à 10
for ($i = 1; $i <= 10; $i++) {
    echo "Numéro: $i<br>";
}

// Boucle inversée
for ($i = 10; $i >= 0; $i--) {
    echo "$i<br>";
}
?>
```

### Boucle while

```php
<?php
$compteur = 0;

while ($compteur < 5) {
    echo "Compteur: $compteur<br>";
    $compteur++;
}
?>
```

### Boucle do...while

```php
<?php
$compteur = 0;

do {
    echo "Exécuté au moins une fois<br>";
    $compteur++;
} while ($compteur < 0);
?>
```

## Fonctions

### Définir et appeler une fonction

```php
<?php
// Fonction simple
function direBonjour() {
    echo "Bonjour !<br>";
}

direBonjour();  // Appeler la fonction

// Fonction avec paramètre
function saluer($nom) {
    echo "Bonjour $nom !<br>";
}

saluer("Marie");  // Affiche: Bonjour Marie !

// Fonction avec valeur par défaut
function presenter($nom = "inconnu") {
    echo "Je suis $nom<br>";
}

presenter();         // Je suis inconnu
presenter("Pierre"); // Je suis Pierre

// Fonction qui retourne une valeur
function additionner($a, $b) {
    return $a + $b;
}

$resultat = additionner(5, 3);
echo $resultat;  // 8
?>
```

### Fonctions utiles

```php
<?php
// Mathématiques
echo abs(-5);        // 5 (valeur absolue)
echo ceil(4.3);     // 5 (arrondi supérieur)
echo floor(4.8);    // 4 (arrondi inférieur)
echo round(4.5);    // 5 (arrondi)
echo rand(1, 10);   // Nombre aléatoire 1-10

// Chaînes
$texte = "Bonjour le monde";
echo strlen($texte);           // 17 (longueur)
echo strtoupper($texte);      // BONJOUR LE MONDE
echo strtolower($texte);      // bonjour le monde
echo substr($texte, 0, 7);    // Bonjour (extrait)
echo str_replace("monde", "PHP", $texte); // Bonjour le PHP

// Tableaux
$nombres = [3, 1, 4, 1, 5];
echo count($nombres);           // 5 (nombre d'éléments)
sort($nombres);                 // Trie le tableau
print_r($nombres);              // Affiche le tableau

// Dates
echo date("d/m/Y");             // 22/03/2024
echo date("H:i:s");             // 14:30:00
?>
```

## Connexion MySQL avec PDO

**PDO** (PHP Data Objects) est une interface pour accéder aux bases de données.

### Connexion basique

```php
<?php
try {
    // Paramètres de connexion
    $host = 'localhost';
    $dbname = 'ma_base';
    $user = 'utilisateur';
    $password = 'mot_de_passe';
    
    // Créer la connexion
    $pdo = new PDO(
        "mysql:host=$host;dbname=$dbname;charset=utf8mb4",
        $user,
        $password
    );
    
    // Configurer les erreurs
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    echo "Connexion réussie !";
    
} catch (PDOException $e) {
    echo "Erreur de connexion: " . $e->getMessage();
}
?>
```

### Requêtes SELECT

```php
<?php
// Requête simple
$stmt = $pdo->query("SELECT * FROM utilisateurs");
$utilisateurs = $stmt->fetchAll(PDO::FETCH_ASSOC);

foreach ($utilisateurs as $utilisateur) {
    echo $utilisateur['nom'] . "<br>";
}

// Requête préparée (sécurisée)
$stmt = $pdo->prepare("SELECT * FROM utilisateurs WHERE id = ?");
$stmt->execute([1]);
$utilisateur = $stmt->fetch(PDO::FETCH_ASSOC);

// Requête avec paramètres nommés
$stmt = $pdo->prepare("SELECT * FROM utilisateurs WHERE nom = :nom");
$stmt->execute(['nom' => 'Dupont']);
?>
```

### Requêtes INSERT

```php
<?php
// Méthode préparée (recommandée)
$stmt = $pdo->prepare("INSERT INTO utilisateurs (nom, email) VALUES (:nom, :email)");
$stmt->execute([
    'nom' => 'Martin',
    'email' => 'martin@email.com'
]);

// Vérifier le succès
if ($stmt->rowCount() > 0) {
    echo "Utilisateur ajouté !";
    echo "ID: " . $pdo->lastInsertId();
}
?>
```

### Requêtes UPDATE

```php
<?php
$stmt = $pdo->prepare("UPDATE utilisateurs SET email = :email WHERE id = :id");
$stmt->execute([
    'email' => 'nouveau@email.com',
    'id' => 1
]);

if ($stmt->rowCount() > 0) {
    echo "Utilisateur modifié !";
}
?>
```

### Requêtes DELETE

```php
<?php
$stmt = $pdo->prepare("DELETE FROM utilisateurs WHERE id = :id");
$stmt->execute(['id' => 3]);

if ($stmt->rowCount() > 0) {
    echo "Utilisateur supprimé !";
}
?>
```

## Traitement de formulaires

### Formulaire HTML

```html
<form action="traitement.php" method="POST">
    <label>Nom:</label>
    <input type="text" name="nom" required>
    
    <label>Email:</label>
    <input type="email" name="email" required>
    
    <label>Message:</label>
    <textarea name="message"></textarea>
    
    <button type="submit">Envoyer</button>
</form>
```

### Traitement en PHP

```php
<?php
// Vérifier que le formulaire a été soumis
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Récupérer et nettoyer les données
    $nom = trim($_POST['nom']);
    $email = trim($_POST['email']);
    $message = trim($_POST['message']);
    
    // Validation simple
    $erreurs = [];
    
    if (empty($nom)) {
        $erreurs[] = "Le nom est requis";
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erreurs[] = "Email invalide";
    }
    
    // Si pas d'erreurs, traiter
    if (empty($erreurs)) {
        // Échapper pour éviter les injections SQL et XSS
        $nom = htmlspecialchars($nom);
        $email = htmlspecialchars($email);
        $message = htmlspecialchars($message);
        
        echo "Merci $nom pour votre message !";
        
        // Ou enregistrer en base de données...
    } else {
        // Afficher les erreurs
        foreach ($erreurs as $erreur) {
            echo "<p style='color:red;'>$erreur</p>";
        }
    }
}
?>
```

### Sécurité des formulaires

| Menace | Protection |
|--------|------------|
| **XSS** (Cross-Site Scripting) | `htmlspecialchars()` |
| **SQL Injection** | Requêtes préparées (PDO) |
| **CSRF** | Token de sécurité |
| **Validation** | filter_var(), regex |

## Variables superglobales

| Variable | Description |
|----------|-------------|
| `$_GET` | Paramètres URL (ex: `page.php?id=5`) |
| `$_POST` | Données de formulaire POST |
| `$_SESSION` | Variables de session |
| `$_COOKIE` | Cookies |
| `$_SERVER` | Informations serveur |
| `$_FILES` | Fichiers uploadés |
| `$_REQUEST` | GET + POST combinés |

### Exemple avec GET

```php
<?php
// URL: page.php?id=5
if (isset($_GET['id'])) {
    $id = (int)$_GET['id'];  // Conversion en entier
    echo "ID: " . $id;
}
?>
```

### Sessions

```php
<?php
// Démarrer la session
session_start();

// Stocker des données
$_SESSION['utilisateur'] = 'Marie';
$_SESSION['role'] = 'admin';

// Lire des données
if (isset($_SESSION['utilisateur'])) {
    echo "Bienvenue " . $_SESSION['utilisateur'];
}

// Détruire la session
session_destroy();
?>
```

## Inclusions de fichiers

### include et require

```php
<?php
// Inclusion simple (avertissement si non trouvé)
include 'header.php';

// Inclusion requise (erreur fatale si non trouvé)
require 'config.php';

// Inclusion une seule fois
include_once 'fonctions.php';
require_once 'config.php';
?>
```

### Structure typique d'un site

```
/var/www/monsite/
├── index.php           # Page d'accueil
├── config.php          # Configuration base de données
├── header.php         # En-tête commun
├── footer.php         # Pied de page commun
├── styles.css         # Feuille de style
├── fonctions.php       # Fonctions personnalisées
└──/
    ├── connexion.php  # Page de connexion
    └── inscription.php # Page d'inscription
```

## Commandes utiles

### Recharger la configuration PHP

```bash
sudo systemctl reload apache2
```

### Tester un script en CLI

```bash
php script.php
```

### Vérifier la syntaxe

```bash
php -l script.php
```

### Mode interactif

```bash
php -a
```

Ouvre un interpréteur PHP en ligne de commande.

## Bonnes pratiques

1. **Toujours fermer les balises PHP** à la fin si seul du code
2. **Utiliser les short tags** (`<?= $var ?>`) pour l'affichage
3. **Déclarer les types** pour les fonctions
4. **Valider et nettoyer** toutes les entrées utilisateur
5. **Utiliser les requêtes préparées** pour SQL
6. **Ne jamais stocker de secrets** dans le code source
7. **Activer error reporting** en développement, le désactiver en production
