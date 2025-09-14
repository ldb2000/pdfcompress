#!/usr/bin/env python3
"""
Script d'analyse de PDF pour comprendre pourquoi un PDF ne se compresse pas
"""

import sys
import os

def analyze_with_fitz(pdf_path):
    """Analyse un PDF avec PyMuPDF"""
    try:
        import fitz
        
        doc = fitz.open(pdf_path)
        
        print(f"📄 Analyse de: {os.path.basename(pdf_path)}")
        print(f"📏 Taille: {os.path.getsize(pdf_path) / (1024*1024):.2f} Mo")
        print(f"📑 Pages: {doc.page_count}")
        print(f"🔒 Chiffré: {'Oui' if doc.needs_pass else 'Non'}")
        print(f"📝 Métadonnées: {doc.metadata}")
        
        total_images = 0
        total_image_size = 0
        image_formats = {}
        
        print("\n🖼️  ANALYSE DES IMAGES")
        print("=" * 30)
        
        for page_num in range(min(5, doc.page_count)):  # Analyser seulement les 5 premières pages
            page = doc[page_num]
            images = page.get_images()
            
            if images:
                print(f"\nPage {page_num + 1}: {len(images)} image(s)")
                
                for img_index, img in enumerate(images):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        
                        width = base_image["width"]
                        height = base_image["height"]
                        image_ext = base_image["ext"]
                        image_size = len(base_image["image"])
                        
                        total_images += 1
                        total_image_size += image_size
                        
                        if image_ext in image_formats:
                            image_formats[image_ext] += 1
                        else:
                            image_formats[image_ext] = 1
                        
                        print(f"  Image {img_index + 1}: {width}x{height} {image_ext.upper()} ({image_size/1024:.1f} KB)")
                        
                    except Exception as e:
                        print(f"  Erreur analyse image {img_index + 1}: {e}")
        
        print(f"\n📊 RÉSUMÉ DES IMAGES")
        print(f"Total images analysées: {total_images}")
        print(f"Taille totale images: {total_image_size / (1024*1024):.2f} Mo")
        print(f"Formats: {image_formats}")
        
        # Analyse des objets
        print(f"\n🔧 ANALYSE DES OBJETS")
        print("=" * 25)
        print(f"Nombre d'objets: {doc.xref_length()}")
        
        doc.close()
        
        return True
        
    except ImportError:
        print("❌ PyMuPDF non disponible")
        return False
    except Exception as e:
        print(f"❌ Erreur d'analyse: {e}")
        return False

def analyze_with_pikepdf(pdf_path):
    """Analyse un PDF avec pikepdf"""
    try:
        import pikepdf
        
        pdf = pikepdf.open(pdf_path)
        
        print(f"\n📊 ANALYSE PIKEPDF")
        print("=" * 20)
        
        # Informations générales
        print(f"Version PDF: {pdf.pdf_version}")
        print(f"Nombre d'objets: {len(pdf.objects)}")
        
        # Vérifier la compression des flux
        compressed_streams = 0
        uncompressed_streams = 0
        
        for obj_id in range(1, min(100, len(pdf.objects))):  # Analyser les 100 premiers objets
            try:
                obj = pdf.get_object(obj_id, 0)
                if hasattr(obj, 'get') and obj.get('/Type') == '/ObjStm':
                    if obj.get('/Filter'):
                        compressed_streams += 1
                    else:
                        uncompressed_streams += 1
            except:
                continue
        
        print(f"Flux compressés: {compressed_streams}")
        print(f"Flux non compressés: {uncompressed_streams}")
        
        pdf.close()
        
        return True
        
    except ImportError:
        print("❌ pikepdf non disponible")
        return False
    except Exception as e:
        print(f"❌ Erreur pikepdf: {e}")
        return False

def suggest_optimization(pdf_path):
    """Suggère des optimisations basées sur l'analyse"""
    
    file_size_mb = os.path.getsize(pdf_path) / (1024*1024)
    
    print(f"\n💡 SUGGESTIONS D'OPTIMISATION")
    print("=" * 35)
    
    if file_size_mb > 50:
        print("📄 Gros fichier détecté (>50 Mo)")
        print("   → Essayez une compression par lot des images")
        print("   → Vérifiez si certaines pages peuvent être supprimées")
    
    print("🔧 Tentatives de compression alternatives:")
    print("   → Ghostscript: gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen")
    print("   → Adobe Acrobat: fonction 'Réduire la taille du fichier'")
    print("   → Convertir en images puis recréer le PDF avec une qualité réduite")
    
    print("\n🔍 Si le PDF ne se compresse pas:")
    print("   → Le fichier est peut-être déjà optimisé")
    print("   → Les images sont peut-être déjà en basse résolution")
    print("   → Le contenu est principalement textuel (difficile à compresser)")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_pdf.py fichier.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"❌ Fichier non trouvé: {pdf_path}")
        sys.exit(1)
    
    print("🔍 ANALYSE DÉTAILLÉE DU PDF")
    print("=" * 50)
    
    # Analyser avec différentes méthodes
    fitz_ok = analyze_with_fitz(pdf_path)
    pikepdf_ok = analyze_with_pikepdf(pdf_path)
    
    if not fitz_ok and not pikepdf_ok:
        print("❌ Impossible d'analyser le PDF - vérifiez les dépendances")
        sys.exit(1)
    
    suggest_optimization(pdf_path)

if __name__ == "__main__":
    main()
