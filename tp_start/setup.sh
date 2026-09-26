#!/usr/bin/env bash
# Prépare le TP : données sources (data/) et espace de travail (workspace/).
#   bash setup.sh           recrée data/ à l'identique ; workspace/ est conservé
#   bash setup.sh --reset   efface aussi workspace/ pour recommencer le TP de zéro
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--reset" ]]; then
    rm -rf workspace
    echo "workspace/ effacé : le TP repart de zéro."
fi

# Données initiales (recréées à chaque lancement : data/ ne doit jamais être modifié)
rm -rf data
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

# Nom avec majuscule : la recherche de l'étape 5 doit ignorer la casse
cat > data/Fruits_exotiques.txt <<'EOF'
mangue
ananas
litchi
papaye
EOF

# Fichier caché à découvrir à l'étape 2
cat > data/.bienvenue <<'EOF'
Bravo, vous avez trouvé le fichier caché !
Son nom commence par un point : ls ne l'affiche qu'avec l'option -a.

Mot secret : manchot
EOF

# Script livré sans droit d'exécution : il faut le rendre exécutable à l'étape 8
cat > data/salut.sh <<'EOF'
#!/usr/bin/env bash
echo "Bonjour $USER ! Le script $0 s'exécute."
echo "Ses permissions : $(stat -c '%a (%A)' "$0")"
EOF
chmod 644 data/salut.sh

# Espace de travail : les autres dossiers sont créés par l'étudiant à l'étape 3
mkdir -p workspace/preuves workspace/.verify
# Empreintes des données : verify.py signale si data/ a été modifié par erreur
(cd data && find . -type f -print0 | sort -z | xargs -0 sha256sum) > workspace/.verify/data.sha256

chmod +x verify.py || true
echo "Préparation terminée."
echo "  Progression du TP   : python3 verify.py"
echo "  Vérifier l'étape 1  : python3 verify.py 1"