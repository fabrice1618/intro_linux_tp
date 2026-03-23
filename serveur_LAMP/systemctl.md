# Systemctl - Gestion des services

## Description

**systemctl** est l'outil principal pour contrôler **systemd**, le système d'initialisation utilisé par la plupart des distributions Linux modernes (Ubuntu, Debian, Fedora, CentOS, etc.).

### Qu'est-ce que systemd ?

**systemd** est le premier processus lancé par le noyau Linux (PID 1). Il :
- Gère le **démarrage** du système
- Contrôle les **services** (daemons)
- Gère les **périphériques**
- Configure le **réseau**
- Gère les **sessions utilisateur**

```
┌─────────────────────────────────────────────────────────────┐
│                      SYSTEMD (PID 1)                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  nginx   │  │   mysql  │  │   sshd   │  │   ufw    │     │
│  │ service  │  │ service  │  │ service  │  │ service  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │   cron   │  │  rsyslog │  │  dbus    │                   │
│  │ service  │  │ service  │  │ service  │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Concepts clés

| Terme | Explication |
|-------|--------------|
| **Unit** | Ressource gérée par systemd (service, socket, timer, mount) |
| **Service** | Un type d'unit qui représente un démon/daemon |
| **Daemon** | Programme qui fonctionne en arrière-plan |
| **Target** | Groupe d'units (similaire aux runlevels SysV) |

### Types d'units

- `.service` : Services (Apache, MySQL, SSH)
- `.socket` : Sockets réseau pour activation à la demande
- `.timer` : Tâches planifiées (comme cron)
- `.mount` : Points de montage
- `.target` : Groupes d'units

## Commandes de base

### Vérifier le statut d'un service

```bash
systemctl status nom_du_service
```

Affiche l'état actuel du service avec les derniers logs. Exemple de sortie :

```
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2024-01-15 10:30:00 UTC; 2h ago
       Docs: https://httpd.apache.org/docs/2.4/
   Main PID: 1234 (apache2)
      Tasks: 8 (limit: 4915)
     Memory: 25.3M
        CPU: 234ms
   CGroup: /system.slice/apache2.service
           └─1234 /usr/sbin/apache2 -k start
```

**Lecture de la sortie :**
- `loaded` : Fichier d'unit chargé
- `enabled` : Démarre au boot
- `active (running)` : Le service fonctionne
- `Main PID` : Numéro du processus principal

### Démarrer un service

```bash
sudo systemctl start nom_du_service
```

Démarre le service **immédiatement**. Le service s'arrêtera au prochain redémarrage.

### Arrêter un service

```bash
sudo systemctl stop nom_du_service
```

Arrête le service en cours d'exécution.

### Redémarrer un service

```bash
sudo systemctl restart nom_du_service
```

**Arrête puis redémarre** le service. Utile après une modification de configuration.

### Recharger la configuration

```bash
sudo systemctl reload nom_du_service
```

Demande au service de **relire ses fichiers de configuration** sans s'arrêter. Tous les services ne supportent pas cette fonctionnalité.

### Recharger ou redémarrer intelligemment

```bash
sudo systemctl reload-or-restart nom_du_service
```

Tente de recharger, sinon redémarre. Commande sécurisée.

## Gestion du démarrage automatique

### Activer au démarrage

```bash
sudo systemctl enable nom_du_service
```

Configure le service pour **démarrer automatiquement** au boot du système.

### Activer et démarrer immédiatement

```bash
sudo systemctl enable --now nom_du_service
```

Combine `enable` et `start`. Pratique et rapide.

### Désactiver au démarrage

```bash
sudo systemctl disable nom_du_service
```

Empêche le service de **démarrer automatiquement** au boot.

### Vérifier l'état au boot

```bash
systemctl is-enabled nom_du_service
```

Retourne `enabled`, `disabled` ou `masked`.

### Masquer un service

```bash
sudo systemctl mask nom_du_service
```

**Désactive complètement** le service (même manuellement). Le fichier est remplacé par un lien vers `/dev/null`.

### Démasquer un service

```bash
sudo systemctl unmask nom_du_service
```

Rétablit le service masqué.

## Vérifications

### Vérifier si actif

```bash
systemctl is-active nom_du_service
```

Retourne `active` (code 0) ou `inactive` (code != 0). Pratique pour les scripts.

### Vérifier si activé au boot

```bash
systemctl is-enabled nom_du_service
```

### Lister les services actifs

```bash
systemctl list-units --type=service
```

Affiche **tous les services actuellement actifs**.

### Lister tous les services installés

```bash
systemctl list-unit-files --type=service
```

Affiche **tous les fichiers de services** installés sur le système.

### Lister les services échoués

```bash
systemctl --failed --type=service
```

Affiche les services qui ont échoué au démarrage. Très utile pour le dépannage.

### Lister les dépendances d'un service

```bash
systemctl list-dependencies nom_du_service
```

Affiche les services dont dépend ce service.

## Exemples pratiques

### Gérer Apache

```bash
# Démarrer Apache
sudo systemctl start apache2

# Activer au démarrage
sudo systemctl enable apache2

# Vérifier le statut
sudo systemctl status apache2

# Redémarrer après modification de config
sudo systemctl restart apache2

# Voir les logs
journalctl -u apache2 -n 50
```

### Gérer MySQL

```bash
# Démarrer MySQL
sudo systemctl start mysql

# Redémarrer MySQL
sudo systemctl restart mysql

# Arrêter MySQL
sudo systemctl stop mysql

# Activer au démarrage
sudo systemctl enable mysql
```

### Gérer UFW (le pare-feu)

```bash
# Démarrer UFW
sudo systemctl start ufw

# Activer UFW au démarrage
sudo systemctl enable ufw

# Vérifier le statut
sudo systemctl status ufw
```

### Gérer plusieurs services

```bash
# Redémarrer plusieurs services
sudo systemctl restart apache2 mysql php-fpm

# Arrêter tous les services web
sudo systemctl stop apache2 php-fpm
```

## Consultation des logs

systemd enregistre les logs dans le **journal** (stocké dans `/var/log/journal/`).

### Logs d'un service

```bash
journalctl -u nom_du_service
```

Affiche tous les logs du service.

### Logs récents

```bash
journalctl -u nom_du_service -n 50
```

Affiche les 50 dernières lignes.

### Logs en temps réel

```bash
journalctl -u nom_du_service -f
```

**Suivi en direct** des logs (comme `tail -f`).

### Logs depuis le dernier démarrage

```bash
journalctl -u nom_du_service --since today
```

### Logs entre deux dates

```bash
journalctl -u nom_du_service --since "2024-01-01" --until "2024-01-02"
```

### Logs du démarrage système

```bash
journalctl -b
```

Affiche les logs du dernier démarrage.

### Logs du démarrage précédent

```bash
journalctl -b -1
```

### Voir les logs kernel

```bash
journalctl -k
```

## Cibles systemd (targets)

Les **targets** sont des groupes d'units, similaires aux **runlevels** de l'ancien système SysVinit.

### Targets courants

| Target | Description | Équivalent SysV |
|--------|-------------|------------------|
| `graphical.target` | Mode graphique complet | runlevel 5 |
| `multi-user.target` | Mode multi-utilisateur (texte) | runlevel 3 |
| `rescue.target` | Mode rescue (single user) | runlevel 1 |
| `emergency.target` | Shell d'urgence | - |

### Afficher la cible par défaut

```bash
systemctl get-default
```

### Définir la cible par défaut

```bash
# Mode graphique
sudo systemctl set-default graphical.target

# Mode texte (sans GUI)
sudo systemctl set-default multi-user.target
```

### Changer de cible immédiatement

```bash
# Passer en mode texte
sudo systemctl isolate multi-user.target

# Passer en mode graphique
sudo systemctl isolate graphical.target
```

### Arrêter le système

```bash
sudo systemctl poweroff
```

### Redémarrer le système

```bash
sudo systemctl reboot
```

### Arrêt d'urgence

```bash
sudo systemctl halt
```

## Fichiers d'units

### Emplacement des fichiers

```
/lib/systemd/system/   # Fichiers installés par les paquets
/etc/systemd/system/   # Fichiers créés par l'administrateur
/run/systemd/system/   # Fichiers temporaires (runtime)
```

### Structure d'un fichier .service

```ini
[Unit]
Description=Apache HTTP Server
After=network.target remote-fs.target
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/sbin/apache2 -k start
ExecReload=/usr/sbin/apache2 -k graceful
ExecStop=/usr/sbin/apache2 -k stop
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

**Explication des sections :**

- `[Unit]` : Métadonnées et dépendances
- `[Service]` : Comment exécuter le service
- `[Install]` : Comment activer le service

### Créer un service personnalisé

1. Créer le fichier :
   ```bash
   sudo nano /etc/systemd/system/mon-service.service
   ```

2. Recharger systemd :
   ```bash
   sudo systemctl daemon-reload
   ```

3. Activer et démarrer :
   ```bash
   sudo systemctl enable --now mon-service
   ```

## Astuces et bonnes pratiques

### Commandes utiles

```bash
# Éviter la pagination dans les scripts
systemctl status nom_du_service --no-pager

# Voir les dépendances inversées
systemctl list-dependencies --reverse nom_du_service

# Vérifier si une unit existe
systemctl list-unit-files | grep nom_du_service
```

### Bonnes pratiques

1. **Toujours vérifier le statut** après un redémarrage de service
2. **Lire les logs** (`journalctl -u service`) en cas de problème
3. **Utiliser `daemon-reload`** après modification d'un fichier .service
4. **Tester la configuration** avant de redémarrer
5. **Comprendre les dépendances** (After=, Requires=, Wants=)

### Commandes équivalentes anciennes

| Ancienne commande | Commande systemd |
|-------------------|------------------|
| `service apache2 start` | `systemctl start apache2` |
| `service apache2 stop` | `systemctl stop apache2` |
| `service apache2 restart` | `systemctl restart apache2` |
| `service apache2 status` | `systemctl status apache2` |
| `chkconfig on` | `systemctl enable` |
| `runlevel` | `systemctl get-default` |

## Dépannage

### Service qui ne démarre pas

```bash
# 1. Vérifier le statut
systemctl status nom_du_service

# 2. Voir les logs
journalctl -u nom_du_service -n 100

# 3. Vérifier la configuration
systemctl cat nom_du_service

# 4. Relancer systemd
sudo systemctl daemon-reload
```

### Service en état "failed"

```bash
# Voir pourquoi il a échoué
systemctl status nom_du_service

# Essayer de le démarrer manuellement
sudo systemctl start nom_du_service

# Voir les logs
journalctl -u nom_du_service -xe
```

### Service masked

```bash
# Vérifier
systemctl is-enabled nom_du_service

# Démasquer si nécessaire
sudo systemctl unmask nom_du_service
```
