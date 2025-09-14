#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation et le fonctionnement
du compresseur PDF
"""

import sys
import os
import importlib

def test_python_version():
    """Teste la version de Python"""
    print("🐍 Test de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 6:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Version trop ancienne")
        print("   💡 Python 3.6+ requis")
        return False

def test_dependencies():
    """Teste les dépendances"""
    print("\n📦 Test des dépendances...")
    
    dependencies = {
        'pikepdf': 'pikepdf',
        'PyMuPDF': 'fitz', 
        'PyPDF2': 'PyPDF2'
    }
    
    results = {}
    
    for name, module in dependencies.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {name} - Installé")
            results[name] = True
        except ImportError:
            print(f"   ❌ {name} - Non installé")
            results[name] = False
    
    return results

def test_files_present():
    """Teste la présence des fichiers nécessaires"""
    print("\n📄 Test des fichiers du projet...")
    
    # Chemin vers le répertoire racine du projet
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Fichiers essentiels à la racine
    root_files = [
        'compress_pdf.py',
        'requirements.txt',
        'README.md',
        'README-en.md'
    ]
    
    # Fichiers outils dans tools/
    tool_files = [
        'batch_compress.py', 
        'install.sh',
        'analyze_pdf.py',
        'compress_image_pdf.py'
    ]
    
    all_present = True
    
    print("   Fichiers principaux:")
    for filename in root_files:
        full_path = os.path.join(project_root, filename)
        if os.path.exists(full_path):
            print(f"   ✅ {filename} - Présent")
        else:
            print(f"   ❌ {filename} - Manquant")
            all_present = False
    
    print("   Outils avancés:")
    for filename in tool_files:
        full_path = os.path.join(current_dir, filename)
        if os.path.exists(full_path):
            print(f"   ✅ tools/{filename} - Présent")
        else:
            print(f"   ❌ tools/{filename} - Manquant")
            all_present = False
    
    return all_present

def test_permissions():
    """Teste les permissions des fichiers"""
    print("\n🔐 Test des permissions...")
    
    # Chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Fichiers exécutables
    root_executables = ['compress_pdf.py']
    tool_executables = ['batch_compress.py', 'install.sh', 'test_setup.py']
    
    all_executable = True
    
    print("   Scripts principaux:")
    for filename in root_executables:
        full_path = os.path.join(project_root, filename)
        if os.path.exists(full_path):
            if os.access(full_path, os.X_OK):
                print(f"   ✅ {filename} - Exécutable")
            else:
                print(f"   ⚠️  {filename} - Non exécutable")
                print(f"      💡 Exécutez: chmod +x {filename}")
                all_executable = False
        else:
            print(f"   ❌ {filename} - Fichier manquant")
            all_executable = False
    
    print("   Outils:")
    for filename in tool_executables:
        full_path = os.path.join(current_dir, filename)
        if os.path.exists(full_path):
            if os.access(full_path, os.X_OK):
                print(f"   ✅ tools/{filename} - Exécutable")
            else:
                print(f"   ⚠️  tools/{filename} - Non exécutable")
                print(f"      💡 Exécutez: chmod +x tools/{filename}")
                all_executable = False
        else:
            print(f"   ❌ tools/{filename} - Fichier manquant")
            all_executable = False
    
    return all_executable

def test_import_compress():
    """Teste l'import du module de compression"""
    print("\n🔧 Test d'import du module...")
    
    try:
        # Ajouter le répertoire parent au path pour importer compress_pdf
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        sys.path.insert(0, project_root)
        
        from compress_pdf import compress_pdf
        print("   ✅ Module compress_pdf - Import réussi")
        
        # Test des fonctions principales
        functions = ['compress_with_pikepdf', 'compress_with_fitz', 'compress_with_pypdf']
        for func_name in functions:
            if hasattr(sys.modules['compress_pdf'], func_name):
                print(f"   ✅ {func_name} - Fonction disponible")
            else:
                print(f"   ❌ {func_name} - Fonction manquante")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False

def create_test_pdf():
    """Crée un PDF de test simple si possible"""
    print("\n📄 Création d'un PDF de test...")
    
    try:
        # Essayer avec reportlab si disponible
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        test_file = "test_document.pdf"
        c = canvas.Canvas(test_file, pagesize=letter)
        c.drawString(100, 750, "Document de test pour PDF Compressor")
        c.drawString(100, 730, "Ce fichier peut être utilisé pour tester la compression.")
        c.drawString(100, 710, "Créé automatiquement par test_setup.py")
        
        # Ajouter du contenu pour avoir une taille significative
        for i in range(50):
            c.drawString(100, 650 - i*10, f"Ligne de test numéro {i+1} " + "x" * 50)
        
        c.save()
        
        if os.path.exists(test_file):
            size = os.path.getsize(test_file) / 1024
            print(f"   ✅ PDF de test créé: {test_file} ({size:.1f} KB)")
            return test_file
        else:
            print("   ❌ Échec de création du PDF de test")
            return None
            
    except ImportError:
        print("   ⚠️  reportlab non disponible - pas de PDF de test créé")
        print("   💡 Pour créer un PDF de test: pip install reportlab")
        return None
    except Exception as e:
        print(f"   ❌ Erreur lors de la création: {e}")
        return None

def run_compression_test(test_pdf):
    """Teste la compression sur un fichier"""
    print(f"\n🔄 Test de compression sur {test_pdf}...")
    
    try:
        from compress_pdf import compress_pdf
        
        output_file = "test_document_compressed.pdf"
        
        # Supprimer le fichier de sortie s'il existe
        if os.path.exists(output_file):
            os.remove(output_file)
        
        # Tester la compression
        success = compress_pdf(test_pdf, output_file, method='auto', compression_level='medium')
        
        if success and os.path.exists(output_file):
            original_size = os.path.getsize(test_pdf)
            compressed_size = os.path.getsize(output_file)
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            print(f"   ✅ Compression réussie!")
            print(f"   📏 Taille originale: {original_size/1024:.1f} KB")
            print(f"   📏 Taille compressée: {compressed_size/1024:.1f} KB") 
            print(f"   💾 Réduction: {reduction:.1f}%")
            
            # Nettoyer les fichiers de test
            os.remove(test_pdf)
            os.remove(output_file)
            
            return True
        else:
            print("   ❌ Échec de la compression")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST DE CONFIGURATION - PDF COMPRESSOR")
    print("=" * 50)
    
    tests_results = {}
    
    # Tests de base
    tests_results['python'] = test_python_version()
    tests_results['dependencies'] = test_dependencies()
    tests_results['files'] = test_files_present()
    tests_results['permissions'] = test_permissions()
    tests_results['import'] = test_import_compress()
    
    # Test de compression si possible
    test_pdf = create_test_pdf()
    if test_pdf:
        tests_results['compression'] = run_compression_test(test_pdf)
    else:
        tests_results['compression'] = None
    
    # Résumé final
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    for test_name, result in tests_results.items():
        if result is True:
            print(f"✅ {test_name.capitalize()} - OK")
        elif result is False:
            print(f"❌ {test_name.capitalize()} - ÉCHEC")
        elif result is None:
            print(f"⚠️  {test_name.capitalize()} - NON TESTÉ")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS")
    print("=" * 20)
    
    failed_deps = [name for name, installed in test_dependencies().items() if not installed]
    if failed_deps:
        print("📦 Installer les dépendances manquantes:")
        print(f"   pip install {' '.join(failed_deps)}")
    
    if not tests_results['permissions']:
        print("🔐 Corriger les permissions:")
        print("   chmod +x *.py *.sh")
    
    if all(v for v in tests_results.values() if v is not None):
        print("🎉 Tous les tests passent! Le compresseur PDF est prêt à utiliser.")
        print("\n🚀 Pour commencer:")
        print("   ./compress_pdf.py --help")
        print("   ./batch_compress.py --help")
    else:
        print("⚠️  Certains tests ont échoué. Consultez les recommandations ci-dessus.")

if __name__ == "__main__":
    main()
