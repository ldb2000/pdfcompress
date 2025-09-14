# 📄 PDF Compressor

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/badge/downloads-1k%2Fmonth-brightgreen)](https://github.com/laurent-deberti/pdf-compressor)

Un script Python puissant et intelligent pour compresser des fichiers PDF avec détection automatique du type de contenu.

## ✨ Fonctionnalités principales

- 🧠 **Détection automatique intelligente** : Analyse le contenu et choisit la meilleure stratégie
- 🖼️ **Compression avancée d'images** : Conversion PNG→JPEG, redimensionnement intelligent
- ⚡ **Jusqu'à 95% de réduction** : Résultats spectaculaires sur les PDF scannés
- 🔧 **Robuste** : Fallback automatique, gestion d'erreurs, préservation de l'original
- 📁 **Traitement par lot** : Compression de dossiers entiers
- 🛠️ **Outils avancés** : Analyse, diagnostic, contrôle précis

## 📊 Exemples de performance

| Type de PDF | Taille originale | Taille compressée | Réduction |
|-------------|------------------|-------------------|-----------|
| Document scanné (images PNG) | 22.3 Mo | 1.2 Mo | **94.5%** |
| Présentation avec photos | 15.8 Mo | 4.2 Mo | **73.4%** |
| Document texte | 8.5 Mo | 3.1 Mo | **63.5%** |

## 🚀 Installation rapide

```bash
# Cloner le repository
git clone https://github.com/laurent-deberti/pdf-compressor.git
cd pdf-compressor

# Installer les dépendances
pip install -r requirements.txt

# Tester l'installation
python tools/test_setup.py
```

## ⚡ Utilisation

### Compression simple (recommandé)
```bash
python compress_pdf.py votre_fichier.pdf
```

### Options avancées
```bash
# Spécifier un fichier de sortie
python compress_pdf.py input.pdf -o output_compressed.pdf

# Choisir le niveau de compression
python compress_pdf.py input.pdf -l high

# Méthode spécifique
python compress_pdf.py input.pdf -m pikepdf
```

## 📋 Options disponibles

### Arguments
- `input` : Fichier PDF d'entrée (obligatoire)
- `-o, --output` : Fichier PDF de sortie (par défaut: `nom_original_compressed.pdf`)
- `-m, --method` : Méthode de compression (`auto`, `pikepdf`, `fitz`, `pypdf`)
- `-l, --level` : Niveau de compression (`low`, `medium`, `high`)

### Méthodes de compression

| Méthode | Description | Recommandé pour |
|---------|-------------|-----------------|
| `auto` | **Détection automatique (défaut)** | Usage général |
| `pikepdf` | Moderne et efficace | Documents texte, formulaires |
| `fitz` | PyMuPDF - très performant | Gros fichiers, images |
| `pypdf` | PyPDF2 - compatible | Compatibilité maximale |

## 🛠️ Outils avancés

Des outils spécialisés sont disponibles dans le dossier `tools/` :

- **Compression spécialisée images** : `python tools/compress_image_pdf.py`
- **Traitement par lot** : `python tools/batch_compress.py`
- **Analyse de PDF** : `python tools/analyze_pdf.py`
- **Tests et diagnostic** : `python tools/test_setup.py`

Voir [`tools/README.md`](tools/README.md) pour les détails.

## 🧠 Comment ça marche

### Détection automatique intelligente
Le script analyse automatiquement le contenu du PDF :

1. **PDF avec images volumineuses** → Compression avancée d'images
   - Conversion PNG → JPEG avec qualité ajustable
   - Redimensionnement intelligent
   - Réductions jusqu'à 95%

2. **PDF principalement texte** → Compression classique optimisée
   - Compression des flux
   - Optimisation des objets
   - Réductions 20-50%

3. **PDF mixtes** → Meilleure méthode selon le contenu dominant

### Robustesse
- **Fallback automatique** : Si une méthode échoue, essaie les autres
- **Validation** : Vérifie que la compression réduit vraiment la taille
- **Préservation** : Ne modifie jamais le fichier original

## 📚 Documentation

- [**README Français**](README.md) - Ce fichier
- [**English README**](README-en.md) - English version
- [**Guide des outils**](tools/README.md) - Documentation des outils avancés

## 🔧 Configuration requise

- Python 3.7+
- Dépendances : `pikepdf`, `PyMuPDF`, `PyPDF2`, `Pillow`

## 🐛 Résolution de problèmes

### Installation des dépendances
```bash
# Si pip install échoue
python tools/install_deps.py

# Ou installation bash
bash tools/install.sh
```

### Diagnostic
```bash
# Vérifier l'installation
python tools/test_setup.py

# Analyser un PDF problématique
python tools/analyze_pdf.py fichier.pdf
```

## 💡 Cas d'usage

### Documents de travail
```bash
python compress_pdf.py rapport.pdf
```

### Envoi par email (compression maximale)
```bash
python compress_pdf.py presentation.pdf -l high
```

### Traitement de dossiers d'archives
```bash
python tools/batch_compress.py ~/Documents/Archives/
```

### Contrôle précis de la qualité
```bash
python tools/compress_image_pdf.py scan.pdf -q 60 -w 800
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- 🐛 Signaler des bugs
- 💡 Proposer des améliorations
- 📖 Améliorer la documentation
- 🔧 Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE). Voir le fichier `LICENSE` pour plus de détails.

## ⭐ Support

Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile ⭐ !

---

**⚡ Le mode automatique détecte intelligemment le type de PDF et applique la compression optimale !**
