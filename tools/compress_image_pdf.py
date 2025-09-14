#!/usr/bin/env python3
"""
Compresseur spécialisé pour les PDF contenant principalement des images
"""

import os
import sys
import argparse
from pathlib import Path

def compress_image_pdf_advanced(input_path, output_path, quality=75, max_width=1200):
    """
    Compresse un PDF avec des images en recréant le PDF avec des images optimisées
    
    Args:
        input_path (str): Chemin du fichier PDF d'entrée
        output_path (str): Chemin du fichier PDF de sortie
        quality (int): Qualité JPEG (10-95)
        max_width (int): Largeur maximale des images
    """
    try:
        import fitz
        from PIL import Image
        import io
        
        print(f"🔄 Compression avancée des images (qualité: {quality}, largeur max: {max_width})")
        
        # Ouvrir le PDF source
        doc = fitz.open(input_path)
        
        # Créer un nouveau PDF
        new_doc = fitz.open()
        
        for page_num in range(doc.page_count):
            print(f"📄 Traitement page {page_num + 1}/{doc.page_count}")
            
            page = doc[page_num]
            
            # Obtenir les dimensions de la page
            page_rect = page.rect
            
            # Créer une nouvelle page
            new_page = new_doc.new_page(width=page_rect.width, height=page_rect.height)
            
            # Obtenir toutes les images de la page
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    # Extraire l'image
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    print(f"  🖼️  Image {img_index + 1}: {image_ext.upper()}, taille originale: {len(image_bytes)/1024:.1f} KB")
                    
                    # Ouvrir l'image avec Pillow
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    
                    # Convertir en RGB si nécessaire
                    if pil_image.mode in ('RGBA', 'LA', 'P'):
                        # Créer un fond blanc pour les images transparentes
                        background = Image.new('RGB', pil_image.size, (255, 255, 255))
                        if pil_image.mode == 'P':
                            pil_image = pil_image.convert('RGBA')
                        background.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode in ('RGBA', 'LA') else None)
                        pil_image = background
                    elif pil_image.mode != 'RGB':
                        pil_image = pil_image.convert('RGB')
                    
                    # Redimensionner si nécessaire
                    original_size = pil_image.size
                    if pil_image.width > max_width:
                        ratio = max_width / pil_image.width
                        new_height = int(pil_image.height * ratio)
                        pil_image = pil_image.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        print(f"    📏 Redimensionné: {original_size} → {pil_image.size}")
                    
                    # Compresser en JPEG
                    compressed_buffer = io.BytesIO()
                    pil_image.save(compressed_buffer, format='JPEG', quality=quality, optimize=True)
                    compressed_bytes = compressed_buffer.getvalue()
                    
                    print(f"    💾 Compressé: {len(image_bytes)/1024:.1f} KB → {len(compressed_bytes)/1024:.1f} KB")
                    
                    # Obtenir la position de l'image sur la page
                    image_rects = page.get_image_rects(xref)
                    if image_rects:
                        for rect in image_rects:
                            # Insérer l'image compressée
                            new_page.insert_image(rect, stream=compressed_bytes)
                    else:
                        # Si on ne trouve pas la position, insérer sur toute la page
                        new_page.insert_image(page_rect, stream=compressed_bytes)
                    
                except Exception as e:
                    print(f"    ❌ Erreur image {img_index + 1}: {e}")
                    continue
            
            # Copier le texte et autres éléments si présents
            try:
                # Récupérer le texte et les annotations
                text_dict = page.get_text("dict")
                if text_dict.get("blocks"):
                    # Il y a du contenu textuel, on le recrée
                    for block in text_dict["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    text = span["text"]
                                    if text.strip():
                                        bbox = span["bbox"]
                                        font_size = span["size"]
                                        # Insérer le texte (simplifié)
                                        new_page.insert_text(
                                            (bbox[0], bbox[1]), 
                                            text, 
                                            fontsize=font_size,
                                            color=(0, 0, 0)
                                        )
            except:
                # Ignore les erreurs de texte
                pass
        
        # Sauvegarder le nouveau PDF
        new_doc.save(output_path, garbage=4, clean=True, deflate=True)
        new_doc.close()
        doc.close()
        
        return True
        
    except ImportError as e:
        if "PIL" in str(e):
            print("❌ Pillow requis pour cette méthode: pip install Pillow")
        else:
            print("❌ PyMuPDF requis: pip install PyMuPDF")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def compress_with_ghostscript(input_path, output_path, quality='screen'):
    """
    Compression avec Ghostscript (si disponible)
    """
    try:
        import subprocess
        
        quality_settings = {
            'screen': '/screen',      # 72 dpi, très petite taille
            'ebook': '/ebook',       # 150 dpi, bonne pour lecture
            'printer': '/printer',   # 300 dpi, bonne qualité
            'prepress': '/prepress'  # Haute qualité
        }
        
        gs_command = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={quality_settings.get(quality, "/screen")}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        print(f"🔄 Tentative avec Ghostscript (qualité: {quality})")
        result = subprocess.run(gs_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
        else:
            print(f"❌ Erreur Ghostscript: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Ghostscript non installé (brew install ghostscript)")
        return False
    except Exception as e:
        print(f"❌ Erreur Ghostscript: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Compresseur spécialisé pour PDF avec images")
    parser.add_argument("input", help="Fichier PDF d'entrée")
    parser.add_argument("-o", "--output", help="Fichier PDF de sortie")
    parser.add_argument("-q", "--quality", type=int, default=75, 
                       help="Qualité JPEG (10-95, défaut: 75)")
    parser.add_argument("-w", "--width", type=int, default=1200, 
                       help="Largeur max des images (défaut: 1200)")
    parser.add_argument("-m", "--method", choices=['advanced', 'ghostscript'], 
                       default='advanced', help="Méthode de compression")
    parser.add_argument("--gs-quality", choices=['screen', 'ebook', 'printer'], 
                       default='ebook', help="Qualité Ghostscript")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Fichier non trouvé: {args.input}")
        sys.exit(1)
    
    # Générer le nom de sortie si non spécifié
    if args.output is None:
        input_file = Path(args.input)
        args.output = str(input_file.parent / f"{input_file.stem}_compressed_images{input_file.suffix}")
    
    # Obtenir les tailles
    original_size = os.path.getsize(args.input) / (1024 * 1024)
    
    print("🖼️  COMPRESSEUR SPÉCIALISÉ IMAGES")
    print("=" * 40)
    print(f"📄 Fichier: {args.input}")
    print(f"📏 Taille originale: {original_size:.2f} Mo")
    print(f"🎯 Fichier de sortie: {args.output}")
    
    success = False
    
    if args.method == 'advanced':
        success = compress_image_pdf_advanced(args.input, args.output, args.quality, args.width)
    elif args.method == 'ghostscript':
        success = compress_with_ghostscript(args.input, args.output, args.gs_quality)
    
    if success and os.path.exists(args.output):
        compressed_size = os.path.getsize(args.output) / (1024 * 1024)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        print("\n✅ Compression terminée!")
        print(f"📏 Taille compressée: {compressed_size:.2f} Mo")
        print(f"💾 Réduction: {reduction:.1f}%")
        print(f"💾 Espace économisé: {original_size - compressed_size:.2f} Mo")
    else:
        print("\n❌ Échec de la compression")

if __name__ == "__main__":
    main()
