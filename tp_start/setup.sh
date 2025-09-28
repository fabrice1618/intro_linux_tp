#!/usr/bin/env bash
set -euo pipefail

# Données initiales
mkdir -p data/logs
cat > data/lorem.txt <<'EOF'
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.
Excepteur sint occaecat cupidatat non proident, sunt in culpa.
EOF

cat > data/fruits.txt <<'EOF'
pomme
banane
poire
pomme
abricot
Banane
kiwi
pêche
POIRE
fraise
EOF

cat > data/sample.csv <<'EOF'
id,prenom,ville
1,Aline,Lyon
2,Béa,Nantes
3,Camille,Paris
4,Dan,Marseille
5,Emma,Bordeaux
EOF

cat > data/logs/app.log <<'EOF'
[INFO] app démarrée
[DEBUG] initialisation modules
[INFO] utilisateur=demo action=login
[WARN] latence élevée
[ERROR] tentative invalide
[INFO] arrêt normal
EOF

# Espace de travail
mkdir -p workspace/{docs,data,tmp}
touch workspace/tmp/.keep

chmod +x verify.py || true
echo "Préparation terminée. Exemples:"
echo "  python3 verify.py --step 1 --no-quiz"
echo "  python3 verify.py --all"