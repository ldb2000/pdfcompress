#!/usr/bin/env python3
"""
Script d'installation des dépendances PDF
"""

import subprocess
import sys

def install_package(package_name):
    """Installe un package en contournant les restrictions si nécessaire"""
    try:
        # Essayer d'abord l'installation normale
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print(f"✅ {package_name} installé avec succès")
        return True
    except subprocess.CalledProcessError:
        try:
            # Si échec, essayer avec --break-system-packages
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', package_name])
            print(f"✅ {package_name} installé avec succès (système)")
            return True
        except subprocess.CalledProcessError:
            try:
                # Dernière tentative avec --user
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '--break-system-packages', package_name])
                print(f"✅ {package_name} installé avec succès (utilisateur)")
                return True
            except subprocess.CalledProcessError:
                print(f"❌ Impossible d'installer {package_name}")
                return False

def main():
    print("🔧 Installation des dépendances PDF...")
    print("=" * 40)
    
    packages = ['pikepdf', 'PyMuPDF', 'PyPDF2', 'Pillow']
    
    success_count = 0
    for package in packages:
        print(f"\n📦 Installation de {package}...")
        if install_package(package):
            success_count += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Résultats: {success_count}/{len(packages)} packages installés")
    
    if success_count > 0:
        print("🎉 Installation terminée! Vous pouvez maintenant utiliser le compresseur PDF.")
    else:
        print("❌ Aucun package installé. Vérifiez vos permissions.")

if __name__ == "__main__":
    main()
