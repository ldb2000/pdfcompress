#!/usr/bin/env python3
"""
Script de compression par lot pour PDF
Compresse tous les fichiers PDF d'un répertoire
"""

import os
import sys
import argparse
import glob
from pathlib import Path
from compress_pdf import compress_pdf

def batch_compress(directory_path, output_dir=None, method='auto', compression_level='medium', pattern='*.pdf'):
    """
    Compresse tous les PDFs d'un répertoire
    
    Args:
        directory_path (str): Répertoire contenant les PDFs
        output_dir (str): Répertoire de sortie (optionnel)
        method (str): Méthode de compression
        compression_level (str): Niveau de compression
        pattern (str): Pattern de fichiers à traiter
    """
    
    if not os.path.exists(directory_path):
        print(f"❌ Le répertoire {directory_path} n'existe pas.")
        return False
    
    # Créer le répertoire de sortie si spécifié
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Trouver tous les fichiers PDF
    search_pattern = os.path.join(directory_path, pattern)
    pdf_files = glob.glob(search_pattern)
    
    if not pdf_files:
        print(f"❌ Aucun fichier PDF trouvé dans {directory_path}")
        return False
    
    print(f"📁 Répertoire: {directory_path}")
    print(f"📄 {len(pdf_files)} fichier(s) PDF trouvé(s)")
    print(f"🔧 Méthode: {method}, Niveau: {compression_level}")
    print("=" * 50)
    
    total_original = 0
    total_compressed = 0
    success_count = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] {os.path.basename(pdf_file)}")
        print("-" * 30)
        
        # Déterminer le fichier de sortie
        if output_dir:
            output_file = os.path.join(output_dir, os.path.basename(pdf_file))
        else:
            input_path = Path(pdf_file)
            output_file = str(input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}")
        
        # Obtenir la taille originale
        original_size = os.path.getsize(pdf_file) / (1024 * 1024)
        total_original += original_size
        
        # Comprimer le fichier
        if compress_pdf(pdf_file, output_file, method, compression_level):
            if os.path.exists(output_file):
                compressed_size = os.path.getsize(output_file) / (1024 * 1024)
                total_compressed += compressed_size
                success_count += 1
            else:
                total_compressed += original_size
        else:
            total_compressed += original_size
    
    # Statistiques finales
    print("\n" + "=" * 50)
    print("📊 STATISTIQUES FINALES")
    print("=" * 50)
    print(f"✅ Fichiers traités avec succès: {success_count}/{len(pdf_files)}")
    print(f"📏 Taille totale originale: {total_original:.2f} Mo")
    print(f"📏 Taille totale compressée: {total_compressed:.2f} Mo")
    
    if total_original > 0:
        total_reduction = ((total_original - total_compressed) / total_original) * 100
        print(f"💾 Réduction totale: {total_reduction:.1f}%")
        print(f"💾 Espace économisé: {total_original - total_compressed:.2f} Mo")
    
    return success_count > 0

def main():
    parser = argparse.ArgumentParser(description="Compression par lot de fichiers PDF")
    parser.add_argument("directory", help="Répertoire contenant les fichiers PDF")
    parser.add_argument("-o", "--output", help="Répertoire de sortie (optionnel)")
    parser.add_argument("-m", "--method", choices=['auto', 'pikepdf', 'fitz', 'pypdf'], 
                       default='auto', help="Méthode de compression (défaut: auto)")
    parser.add_argument("-l", "--level", choices=['low', 'medium', 'high'], 
                       default='medium', help="Niveau de compression (défaut: medium)")
    parser.add_argument("-p", "--pattern", default='*.pdf', 
                       help="Pattern de fichiers à traiter (défaut: *.pdf)")
    
    args = parser.parse_args()
    
    print("🔄 COMPRESSION PAR LOT - PDF COMPRESSOR")
    print("=" * 50)
    
    success = batch_compress(
        args.directory, 
        args.output, 
        args.method, 
        args.level, 
        args.pattern
    )
    
    if not success:
        print("\n💡 Conseils:")
        print("   - Vérifiez que le répertoire contient des fichiers PDF")
        print("   - Assurez-vous que les dépendances sont installées")
        print("   pip install pikepdf PyMuPDF PyPDF2")
        sys.exit(1)

if __name__ == "__main__":
    main()
