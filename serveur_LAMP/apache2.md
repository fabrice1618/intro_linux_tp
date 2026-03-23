# Apache2 - Serveur Web et VirtualHosts

## Description

**Apache2** (httpd) est le serveur HTTP le plus populaire au monde. Il permet d'héberger des sites web et prend en charge les virtualhosts pour gérer plusieurs sites sur un même serveur.

### Comment fonctionne un serveur web ?

```
┌──────────────┐         INTERNET         ┌──────────────────┐
│              │ ◄──────────────────────► │                  │
│  Navigateur  │     Requête HTTP         │    SERVEUR       │
│   (Chrome)   │ ──────────────────────►  │    Apache2       │
│              │ ◄─────────────────────── │                  │
│              │     Réponse HTML         │  /var/www/html/  │
└──────────────┘                          └──────────────────┘

Requête:  GET /index.html HTTP/1.1
          Host: www.example.com

Réponse:  HTTP/1.1 200 OK
          Content-Type: text/html
          
          <html>...</html>
```

### Apache vs Nginx

| Caractéristique | Apache | Nginx |
|-----------------|--------|-------|
| Maturité | Plus ancien | Plus récent |
| Performance | Bonne | Excellente |
| Connexions simultanées | Moyenne | Très haute |
| Configuration | Directives | Configuration monolithique |
| .htaccess | Oui | Non |

## Installation

### Installation basique

```bash
sudo apt update
sudo apt install apache2
sudo systemctl start apache2
sudo systemctl enable apache2
```

### Vérification

Ouvrez votre navigateur et accédez à :
```
http://adresse_ip_serveur
```

Vous devriez voir la page par défaut d'Apache (It works!).

## Commandes de base

### Démarrer Apache

```bash
sudo systemctl start apache2
```

### Arrêter Apache

```bash
sudo systemctl stop apache2
```

### Redémarrer Apache

```bash
sudo systemctl restart apache2
```

Arrête puis démarre le serveur. Utilisé après modification de configuration.

### Recharger la configuration

```bash
sudo systemctl reload apache2
```

Demande à Apache de relire ses fichiers de configuration sans redémarrer.

### Vérifier le statut

```bash
sudo systemctl status apache2
```

Affiche si Apache fonctionne et le nombre de requêtes.

## Structure des fichiers

```
/etc/apache2/
├── apache2.conf          # Configuration principale
├── envvars               # Variables d'environnement
├── ports.conf             # Ports d'écoute (défaut: 80, 443)
├── mods-available/       # Modules disponibles
├── mods-enabled/         # Modules activés
├── sites-available/      # Configurations de sites disponibles
├── sites-enabled/        # Configurations de sites actifs
├── conf-available/       # Configurations additionnelles disponibles
├── conf-enabled/         # Configurations additionnelles actives
└── logs/
    ├── access.log        # Journal d'accès
    └── error.log         # Journal d'erreurs
```

### Fichier de configuration principal

```bash
cat /etc/apache2/apache2.conf
```

Contient les directives globales et inclut les autres fichiers de configuration.

### Ports d'écoute

```bash
cat /etc/apache2/ports.conf
```

```
Listen 80
<IfModule ssl_module>
    Listen 443
</IfModule>
<IfModule mod_gnutls.c>
    Listen 443
</IfModule>
```

## VirtualHosts

Les **VirtualHosts** permettent d'héberger **plusieurs sites** sur un seul serveur avec une seule adresse IP.

### Types de VirtualHosts

1. **Name-based (par nom)** : Utilise l'en-tête Host de la requête HTTP
2. **IP-based (par IP)** : Chaque site a sa propre adresse IP

Le **name-based** est le plus courant et recommandé.

### Principe du VirtualHost par nom

```
                    ┌─────────────────────────────────┐
                    │         SERVEUR                 │
                    │         192.168.1.100           │
                    └─────────────┬───────────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
         Host: site1.com     Host: site2.com      Host: site3.com
              │                   │                   │
              ▼                   ▼                   ▼
        ┌───────────┐      ┌───────────┐      ┌───────────┐
        │/var/www/  │      │/var/www/  │      │/var/www/  │
        │ site1.com │      │ site2.com │      │ site3.com │
        │   /html   │      │   /html   │      │   /html   │
        └───────────┘      └───────────┘      └───────────┘
```

### Configuration d'un VirtualHost

#### Étape 1 : Créer le répertoire du site

```bash
sudo mkdir -p /var/www/monsite.com/public_html
```

Convention de nommage : `/var/www/[nom_domaine]/public_html`

#### Étape 2 : Définir les permissions

```bash
# Définir le propriétaire
sudo chown -R $USER:$USER /var/www/monsite.com

# Définir les permissions
sudo chmod -R 755 /var/www
```

- `$USER` : variable contenant le nom de l'utilisateur courant
- `755` : Propriétaire peut tout faire, autres peuvent lire/exécuter

#### Étape 3 : Créer une page de test

```bash
echo "<h1>Bienvenue sur monsite.com</h1>
<p>C'est le site de monsite.com</p>" | sudo tee /var/www/monsite.com/public_html/index.html
```

#### Étape 4 : Créer le fichier de configuration

```bash
sudo nano /etc/apache2/sites-available/monsite.com.conf
```

Contenu du fichier :

```apache
<VirtualHost *:80>
    # Informations administrateur
    ServerAdmin admin@monsite.com
    
    # Nom de domaine principal
    ServerName monsite.com
    
    # Alias (domaines additionnels)
    ServerAlias www.monsite.com
    
    # Répertoire des fichiers web
    DocumentRoot /var/www/monsite.com/public_html
    
    # Journal des erreurs (chemin abrégé)
    ErrorLog ${APACHE_LOG_DIR}/monsite.com_error.log
    
    # Journal des accès
    CustomLog ${APACHE_LOG_DIR}/monsite.com_access.log combined
</VirtualHost>
```

**Explication des directives :**

| Directive | Description |
|-----------|-------------|
| `ServerAdmin` | Email de l'administrateur (affiché dans les pages d'erreur) |
| `ServerName` | Nom de domaine principal |
| `ServerAlias` | Autres noms de domaine pointant vers ce site |
| `DocumentRoot` | Répertoire contenant les fichiers du site |
| `ErrorLog` | Fichier journal des erreurs |
| `CustomLog` | Fichier journal des accès |
| `combined` | Format de log complet (avec referer, user-agent) |

#### Étape 5 : Activer le site

```bash
sudo a2ensite monsite.com.conf
```

Crée un lien symbolique dans `sites-enabled/`.

#### Étape 6 : Désactiver le site par défaut (optionnel)

```bash
sudo a2dissite 000-default.conf
```

Recommandé si vous n'avez qu'un seul site.

#### Étape 7 : Tester la configuration

```bash
sudo apache2ctl configtest
```

Affiche `Syntax OK` si la configuration est valide, sinon affiche les erreurs.

#### Étape 8 : Recharger Apache

```bash
sudo systemctl reload apache2
```

## Commandes a2

Apache fournit des scripts pour faciliter la gestion :

| Commande | Description |
|----------|-------------|
| `a2ensite` | Activer un site (create symlink) |
| `a2dissite` | Désactiver un site |
| `a2enmod` | Activer un module |
| `a2dismod` | Désactiver un module |
| `a2enconf` | Activer une configuration |
| `a2disconf` | Désactiver une configuration |

### Activer/désactiver des sites

```bash
sudo a2ensite monsite.com.conf   # Activer
sudo a2dissite monsite.com.conf  # Désactiver
```

### Lister les sites actifs

```bash
ls /etc/apache2/sites-enabled/
```

### Activer/désactiver des modules

```bash
sudo a2enmod rewrite      # Activer mod_rewrite
sudo a2dismod autoindex  # Désactiver le listing de répertoire
```

## Configuration HTTPS (SSL/TLS)

### Qu'est-ce que SSL/TLS ?

SSL (Secure Sockets Layer) et son successeur TLS (Transport Layer Security) permettent de **chiffrer** les communications entre le navigateur et le serveur.

```
HTTP (non sécurisé)     HTTPS (sécurisé)
┌──────────────┐        ┌──────────────┐
│   Navigateur │        │   Navigateur │
└──────┬───────┘        └──────┬───────┘
       │                       │
       │  Données visibles     │  Données chiffrées
       │                       │
       ▼                       ▼
┌──────────────────────────────────┐
│  Intercepteur : VOIT LES DONNÉES │
└──────────────────────────────────┘
              vs
┌──────────────────────────────────┐
│  Intercepteur : ###!@#$%^&*      │
└──────────────────────────────────┘
```

### Activation de SSL

#### Étape 1 : Activer le module SSL

```bash
sudo a2enmod ssl
```

#### Étape 2 : Obtenir un certificat SSL

**Option A : Certificat auto-signé (pour tests)**
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/apache.key \
    -out /etc/ssl/certs/apache.crt
```

**Option B : Let's Encrypt (production, gratuit)**
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d monsite.com -d www.monsite.com
```

#### Étape 3 : Créer le VirtualHost HTTPS

```bash
sudo nano /etc/apache2/sites-available/monsite.com-ssl.conf
```

```apache
<VirtualHost *:443>
    ServerAdmin admin@monsite.com
    ServerName monsite.com
    ServerAlias www.monsite.com
    DocumentRoot /var/www/monsite.com/public_html
    
    # Configuration SSL
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/apache.crt
    SSLCertificateKeyFile /etc/ssl/private/apache.key
    
    # Journal
    ErrorLog ${APACHE_LOG_DIR}/monsite.com_error.log
    CustomLog ${APACHE_LOG_DIR}/monsite.com_access.log combined
</VirtualHost>
```

#### Étape 4 : Activer et redémarrer

```bash
sudo a2ensite monsite.com-ssl.conf
sudo systemctl restart apache2
```

### Redirection HTTP vers HTTPS

Ajoutez dans le VirtualHost HTTP (*:80) :

```apache
<VirtualHost *:80>
    ServerName monsite.com
    ServerAlias www.monsite.com
    
    # Redirection vers HTTPS
    Redirect permanent / https://monsite.com/
</VirtualHost>
```

## Modules Apache utiles

### Module rewrite (URLs conviviales)

Permet de réécrire les URLs (essentiel pour WordPress, Laravel, etc.)

```bash
sudo a2enmod rewrite
```

Dans le VirtualHost, ajoutez :

```apache
<Directory /var/www/monsite.com/public_html>
    AllowOverride All
</Directory>
```

### Module headers

Permet de modifier les en-têtes HTTP.

```bash
sudo a2enmod headers
```

### Module expires

Contrôle le cache navigateur.

```bash
sudo a2enmod expires
```

### Module compression (mod_deflate)

Compresse les fichiers pour réduire la bande passante.

```bash
sudo a2enmod deflate
```

## Tests locaux (sans DNS)

Pour tester un VirtualHost sans nom de domaine, modifiez le fichier hosts :

```bash
sudo nano /etc/hosts
```

Ajoutez :

```
127.0.0.1    monsite.com
127.0.0.1    www.monsite.com
127.0.0.1    site2.com
```

Maintenant, accédez à `http://monsite.com` dans votre navigateur.

## Débogage

### Voir les erreurs Apache

```bash
sudo tail -f /var/log/apache2/error.log
```

### Voir les accès

```bash
sudo tail -f /var/log/apache2/access.log
```

### Tester la configuration

```bash
sudo apache2ctl configtest
```

### Vérifier les modules actifs

```bash
apache2ctl -M
```

### Test de charge

```bash
ab -n 1000 -c 10 http://localhost/
```

Apache Bench (ab) simule 1000 requêtes avec 10 connexions simultanées.

## Configuration recommandée pour un serveur de production

```apache
# Limites de sécurité
<Directory /var/www/>
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>

# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Cache des fichiers statiques
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Headers de sécurité
<IfModule mod_headers.c>
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-Content-Type-Options "nosniff"
    Header set X-XSS-Protection "1; mode=block"
</IfModule>
```
