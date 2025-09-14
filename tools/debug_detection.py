#!/usr/bin/env python3
"""
Script de debug pour la détection d'images
"""

import sys

def debug_pdf_images(pdf_path):
    try:
        import fitz
        
        doc = fitz.open(pdf_path)
        total_images = 0
        large_images = 0
        
        print(f"📄 Analyse: {pdf_path}")
        print(f"📑 Pages: {doc.page_count}")
        
        for page_num in range(min(3, doc.page_count)):
            print(f"\n--- Page {page_num + 1} ---")
            images = doc[page_num].get_images()
            total_images += len(images)
            print(f"Images trouvées: {len(images)}")
            
            for img_index, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_size = len(base_image["image"])
                    print(f"  Image {img_index + 1}: {image_size/1024:.1f} KB")
                    
                    if image_size > 1024 * 1024:  # > 1MB
                        large_images += 1
                        print(f"    ✅ Grande image détectée!")
                except Exception as e:
                    print(f"    ❌ Erreur: {e}")
        
        page_count = doc.page_count
        doc.close()
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"Total images: {total_images}")
        print(f"Grandes images (>1MB): {large_images}")
        print(f"Seuil détection: {page_count * 0.5}")
        print(f"Condition 1 (large_images >= 1): {large_images >= 1}")
        print(f"Condition 2 (total_images >= seuil): {total_images >= page_count * 0.5}")
        print(f"Détection activée: {large_images >= 1 and total_images >= page_count * 0.5}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python debug_detection.py fichier.pdf")
        sys.exit(1)
    
    debug_pdf_images(sys.argv[1])
