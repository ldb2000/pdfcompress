# 🛠️ Outils avancés - PDF Compressor

Ce dossier contient des outils spécialisés pour des cas d'usage avancés de compression PDF.

## 📋 Liste des outils

### 🖼️ compress_image_pdf.py
**Compresseur spécialisé pour PDF contenant principalement des images**

```bash
python tools/compress_image_pdf.py fichier.pdf [options]
```

**Options:**
- `-o, --output` : Fichier de sortie
- `-q, --quality` : Qualité JPEG (10-95, défaut: 75)
- `-w, --width` : Largeur max des images (défaut: 1200)
- `-m, --method` : Méthode (`advanced`, `ghostscript`)

**Cas d'usage:**
- PDF scannés avec images PNG volumineuses
- Menus, flyers, documents graphiques
- Contrôle précis de la qualité de compression
- Réduction drastique de taille (jusqu'à 95%)

**Exemple:**
```bash
# Compression agressive pour email
python tools/compress_image_pdf.py scan.pdf -q 60 -w 800 -o scan_mini.pdf
```

---

### 📁 batch_compress.py
**Traitement par lot de dossiers entiers**

```bash
python tools/batch_compress.py dossier/ [options]
```

**Options:**
- `-o, --output` : Dossier de sortie
- `-m, --method` : Méthode de compression
- `-l, --level` : Niveau de compression
- `-p, --pattern` : Pattern de fichiers (défaut: `*.pdf`)

**Cas d'usage:**
- Compression de dossiers d'archives
- Traitement de lots de documents
- Automatisation de compression
- Statistiques de compression globales

**Exemples:**
```bash
# Comprimer tous les PDFs d'un dossier
python tools/batch_compress.py ~/Documents/PDFs/

# Avec dossier de sortie séparé
python tools/batch_compress.py ~/Archives/ -o ~/Archives_compressed/

# Seulement les rapports de 2024
python tools/batch_compress.py ~/Docs/ -p "*2024*.pdf"
```

---

### 🔍 analyze_pdf.py
**Analyse détaillée de structure et contenu PDF**

```bash
python tools/analyze_pdf.py fichier.pdf
```

**Informations fournies:**
- Nombre de pages et objets
- Analyse détaillée des images (taille, format, résolution)
- Métadonnées du document
- État de compression des flux
- Suggestions d'optimisation

**Cas d'usage:**
- Diagnostic avant compression
- Comprendre pourquoi un PDF ne se compresse pas
- Analyser la composition d'un document
- Évaluer le potentiel de compression

**Exemple de sortie:**
```
📄 Analyse de: document.pdf
📏 Taille: 22.23 Mo
📑 Pages: 5
🖼️ Images analysées: 5
- Image 1: 1708x2460 PNG (4281.3 KB)
- Image 2: 1770x2539 PNG (4715.7 KB)
💡 Suggestions: Compression d'images recommandée
```

---

### 🐛 debug_detection.py
**Diagnostic de la détection automatique d'images**

```bash
python tools/debug_detection.py fichier.pdf
```

**Informations fournies:**
- Nombre d'images par page
- Taille de chaque image
- Seuils de détection
- Logique de décision pour la compression automatique

**Cas d'usage:**
- Comprendre pourquoi la détection automatique ne fonctionne pas
- Déboguer les problèmes de classification
- Ajuster les seuils de détection

---

### ✅ test_setup.py
**Vérification complète de l'installation**

```bash
python tools/test_setup.py
```

**Tests effectués:**
- Version Python compatible
- Présence de toutes les dépendances
- Permissions des fichiers
- Fonctionnalité des modules d'import
- Création et compression d'un PDF de test

**Cas d'usage:**
- Vérifier l'installation après setup
- Diagnostiquer les problèmes de dépendances
- Valider le fonctionnement avant utilisation
- Obtenir des recommandations d'installation

---

### 📦 install_deps.py
**Installation automatique des dépendances**

```bash
python tools/install_deps.py
```

**Fonctionnalités:**
- Installation avec contournement des restrictions système
- Tentatives multiples (pip, --user, --break-system-packages)
- Rapport de succès/échec par package
- Compatible avec les environnements restrictifs

**Cas d'usage:**
- Installation dans des environnements protégés
- Automatisation du setup
- Résolution des problèmes de permissions pip

---

### 🎭 demo_complete.py
**Démonstration complète des fonctionnalités**

```bash
python tools/demo_complete.py
```

**Démonstrations:**
- Tests de configuration
- Aide de tous les scripts
- Exemples d'utilisation
- Statistiques de performance
- Résumé des fonctionnalités

**Cas d'usage:**
- Découverte des capacités du système
- Formation et présentation
- Validation du fonctionnement global

---

### ⚙️ install.sh
**Script d'installation bash**

```bash
bash tools/install.sh
```

**Fonctionnalités:**
- Vérification de Python et pip
- Installation des dépendances
- Configuration des permissions
- Messages de succès/erreur

**Cas d'usage:**
- Installation rapide en une commande
- Automatisation de déploiement
- Setup sur serveurs

## 🎯 Scénarios d'utilisation

### 📊 Analyse avant compression
```bash
# 1. Analyser le PDF
python tools/analyze_pdf.py document.pdf

# 2. Si beaucoup d'images, utiliser la compression spécialisée
python tools/compress_image_pdf.py document.pdf -q 70

# 3. Sinon, utiliser le compresseur principal
python compress_pdf.py document.pdf
```

### 📁 Traitement de masse
```bash
# 1. Analyser quelques fichiers représentatifs
python tools/analyze_pdf.py ~/Archives/sample.pdf

# 2. Traitement par lot avec la méthode appropriée
python tools/batch_compress.py ~/Archives/ -m auto -l medium
```

### 🔧 Diagnostic de problème
```bash
# 1. Vérifier l'installation
python tools/test_setup.py

# 2. Analyser le fichier problématique
python tools/analyze_pdf.py problematic.pdf

# 3. Déboguer la détection
python tools/debug_detection.py problematic.pdf

# 4. Essayer la compression spécialisée
python tools/compress_image_pdf.py problematic.pdf -q 80
```

### 🚀 Installation et setup
```bash
# Option 1: Script bash
bash tools/install.sh

# Option 2: Script Python
python tools/install_deps.py

# Vérification
python tools/test_setup.py
```

## 💡 Conseils d'utilisation

- **Commencez toujours par `analyze_pdf.py`** pour comprendre le contenu
- **Utilisez `batch_compress.py`** pour traiter des dossiers entiers
- **`compress_image_pdf.py`** donne un contrôle précis sur la qualité
- **`test_setup.py`** aide à diagnostiquer les problèmes d'installation
- **Le script principal `compress_pdf.py`** reste le meilleur choix pour 95% des cas

Ces outils permettent un contrôle fin et des diagnostics avancés pour les cas complexes ou spécialisés.
