# UFW - Firewall

## Description

**UFW** signifie *Uncomplicated Firewall*. C'est l'outil de configuration de pare-feu par défaut pour Ubuntu. Il fournit une interface simplifiée pour gérer **iptables**, qui est l'outil de pare-feu de plus bas niveau sous Linux.

### Qu'est-ce qu'un pare-feu ?

Un **pare-feu** (firewall) est un système de sécurité qui :
- **Autorise** ou **bloque** le trafic réseau
- Filtre les connexions entrantes et sortantes
- Protège votre serveur des attaques extérieures

```
┌─────────────────────────────────────────────────────────────┐
│                     INTERNET                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
              ┌───────┴───────┐
              │   PARE-FEU    │  ← UFW/iptables
              │  - Port 80 ✓  │     Filtre le trafic
              │  - Port 443 ✓ │
              │  - Port 22 ✓  │
              │  - Port 23 ✗  │
              └───────┬───────┘
                      │
              ┌───────┴───────┐
              │   SERVEUR     │
              │   (Apache)    │
              └───────────────┘
```

### Pourquoi utiliser UFW ?

| iptables (complexe) | UFW (simple) |
|---------------------|--------------|
| `iptables -A INPUT -p tcp --dport 80 -j ACCEPT` | `ufw allow 80` |
| Syntaxe complexe | Syntaxe intuitive |
| Difficile à apprendre | Facile à utiliser |

### Principes fondamentaux

1. **Tout est bloqué par défaut** sauf si explicitement autorisé
2. **Les règles sont évaluées dans l'ordre** (de haut en bas)
3. **deny = DROP** (ignorer silencieusement)
4. **reject = REFUSE** (signaler au client que la connexion est refusée)

## Commandes essentielles

### Vérifier le statut

```bash
sudo ufw status
```

Affiche l'état du pare-feu et les règles actives. Exemple de sortie :
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
```

### Activer le pare-feu

```bash
sudo ufw enable
```

Active UFW. Le pare-feu démarrera automatiquement après chaque redémarrage.

**⚠️ ATTENTION :** Avant d'activer UFW sur un serveur distant, **assurez-vous d'avoir autorisé SSH** ! Sinon vous perdrez l'accès à votre serveur.

### Désactiver le pare-feu

```bash
sudo ufw disable
```

Désactive temporairement le pare-feu. Les règles sont conservées.

### Autoriser une connexion SSH

```bash
sudo ufw allow ssh
```

Cette commande est **indispensable** avant d'activer le pare-feu sur un serveur distant. Elle ouvre le port 22 (SSH).

## Règles par port

### Autoriser un port (TCP et UDP)

```bash
sudo ufw allow 80
```

Ouvre le port 80 pour le trafic HTTP. Autorise à la fois TCP et UDP sur ce port.

### Autoriser un port TCP spécifique

```bash
sudo ufw allow 443/tcp
```

Ouvre uniquement le port 443 en TCP (protocole utilisé par HTTPS).

**Pourquoi spécifier le protocole ?**
- HTTP/HTTPS = TCP (fiables, avec confirmation)
- DNS = TCP et UDP (les deux protocoles)
- Minecraft = UDP (temps réel, sans confirmation)

### Autoriser un port UDP spécifique

```bash
sudo ufw allow 53/udp
```

Ouvre le port 53 uniquement en UDP (DNS).

### Autoriser une plage de ports

```bash
sudo ufw allow 8000:8100/tcp
```

Ouvre les ports 8000, 8001, 8002... jusqu'à 8100 en TCP.

**Cas d'usage :** Applications web de développement, serveurs de jeux.

### Bloquer un port

```bash
sudo ufw deny 23/tcp
```

Bloque le port 23 (Telnet - protocole non sécurisé).

### Limiter le nombre de connexions

```bash
sudo ufw limit 22/tcp
```

Autorise SSH mais **limite les tentatives de connexion** à 6 par 30 secondes. Protection contre les attaques par force brute.

## Règles par service

UFW reconnaît les services courants par leur nom (défini dans `/etc/services`) :

```bash
sudo ufw allow ssh       # Port 22
sudo ufw allow http      # Port 80
sudo ufw allow https     # Port 443
sudo ufw allow ftp       # Port 21
sudo ufw allow smtp      # Port 25
sudo ufw allow imaps     # Port 993
```

**Avantage :** Plus lisible que les numéros de port.

## Règles par IP

### Autoriser une IP spécifique

```bash
sudo ufw allow from 192.168.1.100
```

Autorise **tout le trafic** depuis cette adresse IP.

### Autoriser une IP sur un port spécifique

```bash
sudo ufw allow from 192.168.1.100 to any port 22
```

Autorise uniquement les connexions **SSH** depuis cette IP. Toutes les autres connexions depuis cette IP sont bloquées.

**Cas d'usage :** Accès SSH limité à votre réseau local ou à une IP spécifique.

### Bloquer une IP spécifique

```bash
sudo ufw deny from 198.51.100.23
```

Bloque **tout le trafic** depuis cette adresse IP.

### Bloquer un sous-réseau

```bash
sudo ufw deny from 198.51.100.0/24
```

Bloque toutes les IPs de 198.51.100.0 à 198.51.100.255.

### Autoriser un sous-réseau sur un port

```bash
sudo ufw allow from 192.168.1.0/24 to any port 3306
```

Autorise les connexions MySQL uniquement depuis le réseau local 192.168.1.x.

## Politique par défaut

### Configurer les règles par défaut

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Explication :**
- `deny incoming` : Tout le trafic entrant est bloqué par défaut
- `allow outgoing` : Tout le trafic sortant est autorisé

Cette configuration est recommandée pour la plupart des serveurs.

### Configurer pour un poste de travail

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80
sudo ufw allow 443
```

Permet la navigation web tout en bloquant les connexions entrantes non sollicitées.

## Supprimer des règles

### Supprimer par contenu

```bash
sudo ufw delete allow 80
sudo ufw delete deny from 198.51.100.23
```

Supprime la règle qui autorise le port 80 / bloque l'IP.

### Supprimer par numéro

```bash
sudo ufw status numbered
```

Affiche les règles avec des numéros :
```
Status: active

     To                         Action      From
     --                         ------      ----
 [ 1] 22/tcp                     ALLOW       Anywhere
 [ 2] 80/tcp                     ALLOW       Anywhere
```

```bash
sudo ufw delete 2
```

Supprime la règle n°2 (le port 80).

## Interface et direction

### Spécifier la direction

```bash
sudo ufw allow in 80/tcp    # Trafic entrant sur port 80
sudo ufw allow out 53/udp   # Trafic sortant sur port 53 (DNS)
```

### Sur une interface spécifique

```bash
sudo ufw allow in on eth0 to any port 80
```

Autorise le trafic HTTP uniquement sur l'interface eth0 (utile sur un serveur multi-interface).

## Configuration recommandée pour serveur

```bash
# 1. Définir les politiques par défaut
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Autoriser SSH (ESSENTIEL avant d'activer)
sudo ufw allow ssh

# 3. Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 4. (Optionnel) Limiter SSH pour sécurité
sudo ufw limit ssh

# 5. Activer le pare-feu
sudo ufw enable
```

**Ordre recommandé :** Always allow SSH first → then enable firewall.

## Logs UFW

### Activer les logs

```bash
sudo ufw logging on
```

### Voir les logs

```bash
sudo tail -f /var/log/ufw.log
```

Affiche les connexions bloquées en temps réel.

### Niveaux de logging

```bash
sudo ufw logging low      # Minimal logging
sudo ufw logging medium   # Blocage de connexions
sudo ufw logging high    # Logging complet
```

## Réinitialiser UFW

```bash
sudo ufw reset
```

Supprime toutes les règles et remet UFW à zéro. Utile pour recommencer proprement.

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `ufw status` | Voir les règles actives |
| `ufw status numbered` | Voir les règles numérotées |
| `ufw delete <règle>` | Supprimer une règle |
| `ufw reset` | Réinitialiser le pare-feu |
| `ufw reload` | Recharger les règles |
| `ufw version` | Voir la version |

## Tableau récapitulatif des ports courants

| Service | Port | Protocole | Commande UFW |
|---------|------|-----------|--------------|
| SSH | 22 | TCP | `ufw allow ssh` |
| HTTP | 80 | TCP | `ufw allow http` |
| HTTPS | 443 | TCP | `ufw allow https` |
| FTP | 21 | TCP | `ufw allow ftp` |
| MySQL | 3306 | TCP | `ufw allow 3306` |
| PostgreSQL | 5432 | TCP | `ufw allow 5432` |
| SMTP | 25 | TCP | `ufw allow smtp` |
| DNS | 53 | TCP/UDP | `ufw allow 53` |
