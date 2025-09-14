#!/bin/bash

# Script d'installation pour PDF Compressor
# Usage: ./install.sh

echo "🚀 Installation de PDF Compressor"
echo "=================================="

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python3 détecté: $(python3 --version)"

# Vérifier que pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ pip3 détecté"

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
echo "================================="

echo "🔄 Installation de pikepdf..."
pip3 install pikepdf

echo "🔄 Installation de PyMuPDF..."
pip3 install PyMuPDF

echo "🔄 Installation de PyPDF2..."
pip3 install PyPDF2

# Rendre le script exécutable
echo ""
echo "🔧 Configuration des permissions..."
chmod +x compress_pdf.py

echo ""
echo "✅ Installation terminée!"
echo "========================"
echo ""
echo "💡 Pour utiliser le script:"
echo "   python3 compress_pdf.py mon_fichier.pdf"
echo ""
echo "📚 Pour plus d'informations:"
echo "   python3 compress_pdf.py --help"
echo "   cat README.md"
