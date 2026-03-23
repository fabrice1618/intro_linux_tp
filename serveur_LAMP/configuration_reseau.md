# Configuration Réseau

## Description

Linux propose un ensemble d'outils puissants pour configurer et diagnostiquer le réseau. Ces commandes sont essentielles pour les administrateurs système et les développeurs.

### Comment fonctionne le réseau sur Linux ?

```
┌─────────────────────────────────────────────────────────────┐
│                     STACK RÉSEAU LINUX                      │
├─────────────────────────────────────────────────────────────┤
│  Couche Application    │  Navigateur, cURL, SSH client      │
├─────────────────────────────────────────────────────────────┤
│  Couche Transport      │  TCP, UDP (ports)                  │
├─────────────────────────────────────────────────────────────┤
│  Couche Internet       │  IP (adresses, routage)            │
├─────────────────────────────────────────────────────────────┤
│  Couche Liaison        │  Ethernet (MAC addresses)          │
├─────────────────────────────────────────────────────────────┤
│  Couche Physique       │  Câble réseau, WiFi                │
└─────────────────────────────────────────────────────────────┘
```

## Commandes de diagnostic

### Afficher les interfaces réseau

```bash
ip addr
```

Affiche toutes les adresses IP et informations des interfaces. Exemple de sortie :

```
1: lo: <LOOPBACK,UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo

2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state UP
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::1/64 scope link
```

**Explication des éléments :**
- `lo` : Interface loopback (127.0.0.1) - pour les communications locales
- `eth0` : Première interface Ethernet (carte réseau filaire)
- `wlan0` : Interface WiFi
- `inet` : Adresse IPv4
- `inet6` : Adresse IPv6

### Afficher les informations des interfaces

```bash
ip link show
```

Affiche les informations de niveau liaison (MAC address, état de l'interface).

### Afficher la table de routage

```bash
ip route
```

Affiche comment les paquets sont routés. Exemple :

```
default via 192.168.1.1 dev eth0 proto dhcp
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

**Explication :**
- `default via 192.168.1.1` : Route par défaut (passerelle)
- `192.168.1.0/24 dev eth0` : Réseau local accessible directement

### Tester la connectivité

```bash
ping -c 4 google.com
```

Envoie 4 paquets ICMP (ping) pour tester la connexion. Exemple de sortie :

```
PING google.com (142.250.185.46) 56(84) bytes of data.
64 bytes from par10s34-in-f14.1e100.net: icmp_seq=1 ttl=118 time=14.2 ms
64 bytes from par10s34-in-f14.1e100.net: icmp_seq=2 ttl=118 time=14.1 ms
```

**Interprétation :**
- `time=14.2 ms` : Temps de réponse (latence)
- Si "Destination Host Unreachable" → problème de réseau
- Si "Request timeout" → pare-feu qui bloque ICMP

### Afficher les connexions actives

```bash
ss -tuln
```

| Option | Signification |
|--------|---------------|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Ports en écoute (listening) |
| `-n` | Numéro de port (pas de résolution de nom) |

Exemple de sortie :
```
Netid  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port
tcp    LISTEN  0       128     0.0.0.0:22          0.0.0.0:*
tcp    LISTEN  0       128     0.0.0.0:80          0.0.0.0:*
tcp    LISTEN  0       80      127.0.0.1:3306       0.0.0.0:*
```

### Anciennes commandes (toujours utilisées)

```bash
ifconfig        # Deprecated mais encore présent sur certains systèmes
netstat -tuln   # Équivalent de ss
```

## Configuration IP

### Assigner une adresse IP

```bash
sudo ip addr add 192.168.1.100/24 dev eth0
```

**Attention :** Cette modification est **temporaire** et sera perdue au redémarrage.

**Notation CIDR :**
- `/24` = masque 255.255.255.0
- `/16` = masque 255.255.0.0
- `/8` = masque 255.0.0.0

### Supprimer une adresse IP

```bash
sudo ip addr del 192.168.1.100/24 dev eth0
```

### Activer une interface

```bash
sudo ip link set eth0 up
```

Active l'interface réseau (comme la brancher).

### Désactiver une interface

```bash
sudo ip link set eth0 down
```

Désactive l'interface réseau (comme la débrancher).

### Ajouter une route

```bash
sudo ip route add 192.168.2.0/24 via 192.168.1.1
```

Ajoute une route vers le réseau 192.168.2.x via la passerelle 192.168.1.1.

### Supprimer une route

```bash
sudo ip route del 192.168.2.0/24
```

## Configuration DNS

### Qu'est-ce que DNS ?

DNS (Domain Name System) traduit les noms de domaine en adresses IP :

```
www.google.com ──────► DNS ──────► 142.250.185.46
```

### Fichier de résolution DNS

```bash
sudo nano /etc/resolv.conf
```

Contient les serveurs DNS utilisés par votre système :

```
nameserver 8.8.8.8          # DNS Google
nameserver 8.8.4.4          # DNS Google secondaire
nameserver 1.1.1.1          # DNS Cloudflare
```

**Serveurs DNS publics courants :**
| Provider | DNS Primaire | DNS Secondaire |
|----------|---------------|----------------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |

### Fichier hosts

```bash
sudo nano /etc/hosts
```

Permet de mapper des noms d'hôte à des IPs **localement** (sans DNS).

```
127.0.0.1    localhost
127.0.1.1    mon-serveur

# Exemple: redirection locale
192.168.1.100    monsite.local
```

**Cas d'usage :**
- Tests de sites web sans nom de domaine
- Développement local
- Surcharger des entrées DNS

## Configuration réseau persistante (Netplan)

### Présentation de Netplan

Sur Ubuntu moderne (18.04+), la configuration réseau se fait via **Netplan**, qui génère la configuration pour systemd-networkd ou NetworkManager.

### Emplacement des fichiers

```bash
ls /etc/netplan/
```

Typiquement : `01-netcfg.yaml` ou `50-cloud-init.yaml`

### Exemple : Configuration DHCP

Le DHCP (Dynamic Host Configuration Protocol) obtenir automatiquement une IP :

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```

### Exemple : Configuration IP statique

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
        search:
          - mon-domaine.local
```

**Explication :**
- `addresses` : Adresse IP avec son masque (CIDR)
- `gateway4` : Adresse de la passerelle (routeur)
- `nameservers` : Serveurs DNS
- `search` : Domaine de recherche par défaut

### Appliquer la configuration

```bash
sudo netplan apply
```

Applique les modifications. Pour débugger :
```bash
sudo netplan --debug apply
```

### Générer la configuration

```bash
sudo netplan generate
```

Génère les fichiers de configuration pour le renderer (networkd/NetworkManager).

## Commandes utiles

### Afficher le hostname

```bash
hostname
```

Affiche le nom de la machine (ex: `mon-serveur`).

```bash
hostname -I
```

Affiche uniquement les adresses IP de la machine.

### Tracer une route

```bash
traceroute google.com
```

Affiche le chemin parcouru par les paquets jusqu'à la destination. Permet d'identifier où un problème de réseau survient.

```
traceroute to google.com (142.250.185.46), 30 hops max
 1   192.168.1.1        1.2 ms
 2   10.0.0.1           5.4 ms
 3   72.14.215.85       12.1 ms
```

### Afficher les informations DNS

```bash
dig google.com
```

Affiche les informations DNS détaillées (record A, TTL, serveur utilisé).

```bash
dig +short google.com
```

Affiche uniquement l'adresse IP.

### Résoudre un nom d'hôte

```bash
nslookup google.com
```

Ancienne commande mais toujours fonctionnelle.

### Voir le cache ARP

```bash
arp -a
```

Affiche la table ARP (adresses MAC des machines locales).

### Tester un port spécifique

```bash
nc -zv google.com 80
```

Teste si le port 80 est accessible sur google.com.

```bash
nc -zv 192.168.1.1 22-25
```

Teste les ports 22 à 25 sur une machine locale.

## Diagnostic de problèmes réseau

### Liste de vérification

1. **Vérifier que l'interface est active :**
   ```bash
   ip link show eth0
   ```

2. **Vérifier l'adresse IP :**
   ```bash
   ip addr show eth0
   ```

3. **Vérifier la passerelle :**
   ```bash
   ip route show
   ```

4. **Tester la connectivité locale :**
   ```bash
   ping 192.168.1.1
   ```

5. **Tester la connectivité Internet :**
   ```bash
   ping 8.8.8.8
   ```

6. **Tester DNS :**
   ```bash
   ping google.com
   ```

### Commandes de diagnostic avancées

```bash
# Voir les statistiques réseau
ip -s link

# Monitorer le trafic en temps réel
sudo tcpdump -i eth0

# Voir les connexions établies
ss -tunap

# Afficher les règles de routage
ip rule show
```

## Bonnes pratiques

1. **Toujours vérifier la configuration actuelle** avant de modifier
2. **Faire des sauvegardes** des fichiers de configuration
3. **Tester les modifications** avant de les appliquer en production
4. **Utiliser IP statique** pour les serveurs (DHCP peut changer l'IP)
5. **Documenter** vos configurations réseau
