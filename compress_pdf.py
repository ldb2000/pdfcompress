#!/usr/bin/env python3
"""
Script de compression PDF
Compresse les fichiers PDF en utilisant différentes méthodes
"""

import os
import sys
import argparse
from pathlib import Path

def compress_with_pikepdf(input_path, output_path, compression_level='medium'):
    """
    Compresse un PDF avec pikepdf (recommandé)
    
    Args:
        input_path (str): Chemin du fichier PDF d'entrée
        output_path (str): Chemin du fichier PDF de sortie
        compression_level (str): Niveau de compression ('low', 'medium', 'high')
    """
    try:
        import pikepdf
        
        # Paramètres de compression selon le niveau
        compression_params = {
            'low': {
                'compress_streams': True,
                'preserve_pdfa': True,
                'object_stream_mode': pikepdf.ObjectStreamMode.preserve
            },
            'medium': {
                'compress_streams': True,
                'preserve_pdfa': False,
                'object_stream_mode': pikepdf.ObjectStreamMode.generate
            },
            'high': {
                'compress_streams': True,
                'preserve_pdfa': False,
                'object_stream_mode': pikepdf.ObjectStreamMode.generate,
                'normalize_content': True
            }
        }
        
        with pikepdf.open(input_path) as pdf:
            params = compression_params.get(compression_level, compression_params['medium'])
            pdf.save(output_path, **params)
            
        return True
        
    except ImportError:
        print("❌ pikepdf n'est pas installé. Installez-le avec: pip install pikepdf")
        return False
    except Exception as e:
        print(f"❌ Erreur avec pikepdf: {e}")
        return False

def compress_with_pypdf(input_path, output_path):
    """
    Compresse un PDF avec PyPDF2 (alternative)
    
    Args:
        input_path (str): Chemin du fichier PDF d'entrée
        output_path (str): Chemin du fichier PDF de sortie
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Copier toutes les pages
        for page in reader.pages:
            # Compresser le contenu de la page
            page.compress_content_streams()
            writer.add_page(page)
        
        # Écrire le PDF compressé
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
            
        return True
        
    except ImportError:
        print("❌ PyPDF2 n'est pas installé. Installez-le avec: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ Erreur avec PyPDF2: {e}")
        return False

def compress_with_fitz(input_path, output_path, compression_level='medium'):
    """
    Compresse un PDF avec PyMuPDF (fitz) - très efficace pour les images
    
    Args:
        input_path (str): Chemin du fichier PDF d'entrée
        output_path (str): Chemin du fichier PDF de sortie
        compression_level (str): Niveau de compression ('low', 'medium', 'high')
    """
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(input_path)
        
        # Compression des images selon le niveau
        if compression_level == 'low':
            # Compression légère des images
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        if image_ext in ["png", "jpg", "jpeg"]:
                            # Recompresser en JPEG avec qualité 85
                            import io
                            from PIL import Image
                            image = Image.open(io.BytesIO(image_bytes))
                            if image.mode == 'RGBA':
                                image = image.convert('RGB')
                            
                            output_buffer = io.BytesIO()
                            image.save(output_buffer, format='JPEG', quality=85, optimize=True)
                            new_image_bytes = output_buffer.getvalue()
                            
                            # Remplacer l'image dans le PDF
                            doc._update_stream(xref, new_image_bytes)
                    except:
                        continue
                        
        elif compression_level == 'medium':
            # Compression modérée des images
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        if image_ext in ["png", "jpg", "jpeg"]:
                            import io
                            from PIL import Image
                            image = Image.open(io.BytesIO(image_bytes))
                            if image.mode == 'RGBA':
                                image = image.convert('RGB')
                            
                            # Réduire la résolution si trop élevée
                            max_width, max_height = 1500, 1500
                            if image.width > max_width or image.height > max_height:
                                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                            
                            output_buffer = io.BytesIO()
                            image.save(output_buffer, format='JPEG', quality=75, optimize=True)
                            new_image_bytes = output_buffer.getvalue()
                            
                            doc._update_stream(xref, new_image_bytes)
                    except:
                        continue
                        
        elif compression_level == 'high':
            # Compression maximale des images
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        if image_ext in ["png", "jpg", "jpeg"]:
                            import io
                            from PIL import Image
                            image = Image.open(io.BytesIO(image_bytes))
                            if image.mode == 'RGBA':
                                image = image.convert('RGB')
                            
                            # Réduire significativement la résolution
                            max_width, max_height = 1000, 1000
                            if image.width > max_width or image.height > max_height:
                                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                            
                            output_buffer = io.BytesIO()
                            image.save(output_buffer, format='JPEG', quality=60, optimize=True)
                            new_image_bytes = output_buffer.getvalue()
                            
                            doc._update_stream(xref, new_image_bytes)
                    except:
                        continue
        
        # Sauvegarder avec compression de base
        doc.save(output_path, garbage=4, clean=True, deflate=True)
        doc.close()
        
        return True
        
    except ImportError as ie:
        if "PIL" in str(ie) or "Pillow" in str(ie):
            print("⚠️  Pillow non disponible, tentative sans compression d'images...")
            return compress_with_fitz_basic(input_path, output_path, compression_level)
        else:
            print("❌ PyMuPDF n'est pas installé. Installez-le avec: pip install PyMuPDF")
            return False
    except Exception as e:
        print(f"❌ Erreur avec PyMuPDF: {e}")
        return False

def compress_with_fitz_basic(input_path, output_path, compression_level='medium'):
    """
    Version basique de compression PyMuPDF sans Pillow
    """
    try:
        import fitz
        
        doc = fitz.open(input_path)
        
        # Paramètres selon le niveau
        if compression_level == 'high':
            params = {'garbage': 4, 'clean': True, 'deflate': True, 'ascii': True}
        elif compression_level == 'medium':
            params = {'garbage': 3, 'clean': True, 'deflate': True}
        else:  # low
            params = {'garbage': 1, 'clean': True, 'deflate': True}
        
        doc.save(output_path, **params)
        doc.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur avec PyMuPDF basique: {e}")
        return False

def compress_image_pdf_advanced(input_path, output_path, quality=75, max_width=1200):
    """
    Compression avancée pour PDF contenant principalement des images
    """
    try:
        import fitz
        from PIL import Image
        import io
        
        doc = fitz.open(input_path)
        new_doc = fitz.open()
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_rect = page.rect
            new_page = new_doc.new_page(width=page_rect.width, height=page_rect.height)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Compression avec Pillow
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    
                    if pil_image.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', pil_image.size, (255, 255, 255))
                        if pil_image.mode == 'P':
                            pil_image = pil_image.convert('RGBA')
                        background.paste(pil_image, mask=pil_image.split()[-1] if pil_image.mode in ('RGBA', 'LA') else None)
                        pil_image = background
                    elif pil_image.mode != 'RGB':
                        pil_image = pil_image.convert('RGB')
                    
                    # Redimensionner si nécessaire
                    if pil_image.width > max_width:
                        ratio = max_width / pil_image.width
                        new_height = int(pil_image.height * ratio)
                        pil_image = pil_image.resize((max_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Compresser en JPEG
                    compressed_buffer = io.BytesIO()
                    pil_image.save(compressed_buffer, format='JPEG', quality=quality, optimize=True)
                    compressed_bytes = compressed_buffer.getvalue()
                    
                    # Insérer l'image compressée
                    image_rects = page.get_image_rects(xref)
                    if image_rects:
                        for rect in image_rects:
                            new_page.insert_image(rect, stream=compressed_bytes)
                    else:
                        new_page.insert_image(page_rect, stream=compressed_bytes)
                        
                except:
                    continue
        
        new_doc.save(output_path, garbage=4, clean=True, deflate=True)
        new_doc.close()
        doc.close()
        
        return True
        
    except ImportError:
        return False
    except:
        return False

def get_file_size(file_path):
    """Retourne la taille du fichier en Mo"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_pdf(input_path, output_path=None, method='auto', compression_level='medium'):
    """
    Fonction principale de compression PDF
    
    Args:
        input_path (str): Chemin du fichier PDF d'entrée
        output_path (str): Chemin du fichier PDF de sortie (optionnel)
        method (str): Méthode de compression ('pikepdf', 'pypdf', 'fitz', 'auto')
        compression_level (str): Niveau de compression ('low', 'medium', 'high')
    """
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(input_path):
        print(f"❌ Le fichier {input_path} n'existe pas.")
        return False
    
    # Générer le nom de sortie si non spécifié
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_compressed{input_file.suffix}")
    
    # Taille du fichier original
    original_size = get_file_size(input_path)
    print(f"📄 Fichier original: {input_path}")
    print(f"📏 Taille originale: {original_size:.2f} Mo")
    print(f"🔧 Méthode: {method}, Niveau: {compression_level}")
    print("🔄 Compression en cours...")
    
    success = False
    
    # Essayer différentes méthodes selon le paramètre
    if method == 'auto':
        # Détecter si c'est un PDF principalement composé d'images
        advanced_tried = False
        try:
            import fitz
            doc = fitz.open(input_path)
            total_images = 0
            large_images = 0
            page_count = doc.page_count
            
            for page_num in range(min(3, doc.page_count)):  # Vérifier les 3 premières pages
                images = doc[page_num].get_images()
                total_images += len(images)
                for img in images:
                    try:
                        base_image = doc.extract_image(img[0])
                        if len(base_image["image"]) > 1024 * 1024:  # Images > 1MB
                            large_images += 1
                    except:
                        continue
            
            doc.close()
            
            # Si beaucoup d'images volumineuses, utiliser la compression avancée
            if large_images >= 1 and total_images >= page_count * 0.5:
                print(f"🖼️  PDF avec images volumineuses détecté ({large_images} grandes images)")
                print("🔄 Utilisation de la compression avancée d'images...")
                advanced_tried = True
                success = compress_image_pdf_advanced(input_path, output_path, 75, 1200)
                if success:
                    print("✅ Compression avancée d'images réussie")
                else:
                    print("⚠️  Compression avancée échouée, tentative méthodes classiques...")
        except Exception as e:
            print(f"🐛 Erreur détection: {e}")
        
        # Si pas de compression avancée ou si elle a échoué, essayer les méthodes classiques
        if not advanced_tried or not success:
            methods_to_try = [
                ('pikepdf', lambda: compress_with_pikepdf(input_path, output_path, compression_level)),
                ('fitz', lambda: compress_with_fitz(input_path, output_path, compression_level)),
                ('pypdf', lambda: compress_with_pypdf(input_path, output_path))
            ]
            
            for method_name, compress_func in methods_to_try:
                print(f"🔄 Tentative avec {method_name}...")
                if compress_func():
                    # Vérifier si la compression est efficace
                    if os.path.exists(output_path):
                        compressed_size = get_file_size(output_path)
                        reduction = ((original_size - compressed_size) / original_size) * 100
                        if reduction > 5:  # Au moins 5% de réduction
                            success = True
                            print(f"✅ Compression réussie avec {method_name}")
                            break
                        else:
                            print(f"⚠️  {method_name} - compression inefficace ({reduction:.1f}%)")
                    else:
                        success = True
                        print(f"✅ Compression réussie avec {method_name}")
                        break
    else:
        # Utiliser la méthode spécifiée
        if method == 'pikepdf':
            success = compress_with_pikepdf(input_path, output_path, compression_level)
        elif method == 'fitz':
            success = compress_with_fitz(input_path, output_path, compression_level)
        elif method == 'pypdf':
            success = compress_with_pypdf(input_path, output_path)
        else:
            print(f"❌ Méthode inconnue: {method}")
            return False
    
    if success and os.path.exists(output_path):
        compressed_size = get_file_size(output_path)
        reduction = ((original_size - compressed_size) / original_size) * 100
        
        print(f"✅ Compression terminée!")
        print(f"📄 Fichier compressé: {output_path}")
        print(f"📏 Taille compressée: {compressed_size:.2f} Mo")
        print(f"💾 Réduction: {reduction:.1f}%")
        
        return True
    else:
        print("❌ Échec de la compression avec toutes les méthodes.")
        return False

def main():
    parser = argparse.ArgumentParser(description="Compresser des fichiers PDF")
    parser.add_argument("input", help="Fichier PDF d'entrée")
    parser.add_argument("-o", "--output", help="Fichier PDF de sortie (optionnel)")
    parser.add_argument("-m", "--method", choices=['auto', 'pikepdf', 'fitz', 'pypdf'], 
                       default='auto', help="Méthode de compression (défaut: auto)")
    parser.add_argument("-l", "--level", choices=['low', 'medium', 'high'], 
                       default='medium', help="Niveau de compression (défaut: medium)")
    
    args = parser.parse_args()
    
    # Compression du PDF
    success = compress_pdf(args.input, args.output, args.method, args.level)
    
    if not success:
        print("\n💡 Conseils d'installation:")
        print("   pip install pikepdf PyMuPDF PyPDF2")
        sys.exit(1)

if __name__ == "__main__":
    main()
