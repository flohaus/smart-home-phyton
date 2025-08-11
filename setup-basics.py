#!/usr/bin/env python3
"""
Basis Tools Setup für Raspberry Pi
==================================

Installiert essenzielle Tools, die für das Smart Home System benötigt werden.
Dieses Skript sollte vor dem eigentlichen Smart Home Installer ausgeführt werden.

Autor: Smart Home Setup
Version: 1.0.0
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class Colors:
    """ANSI Color codes für farbige Terminal-Ausgabe"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Zeigt das Welcome Banner an"""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                🔧 BASIS TOOLS INSTALLER 🔧                    ║
║                                                               ║
║              Raspberry Pi Grundausstattung                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

def print_tools():
    """Zeigt die zu installierenden Tools an"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}Folgende Basis-Tools werden installiert:{Colors.ENDC}\n")
    
    tools = [
        "📋 System-Update (apt update & upgrade)",
        "🔧 Git - Versionskontrolle",
        "🐍 Python3 & pip - Python Entwicklung",
        "📦 curl & wget - Download-Tools",
        "📝 vim & nano - Text-Editoren",
        "🗜️ unzip - Archiv-Tool",
        "🌐 ca-certificates - SSL-Zertifikate",
        "🔒 gnupg - Verschlüsselung",
        "🔗 software-properties-common - Repository-Management"
    ]
    
    for i, tool in enumerate(tools, 1):
        print(f"   {i}. {Colors.OKGREEN}{tool}{Colors.ENDC}")
    
    print()

def check_root_privileges():
    """Überprüft ob das Skript mit Root-Rechten ausgeführt wird"""
    return os.geteuid() == 0

def check_raspberry_pi():
    """Überprüft ob das System auf einem Raspberry Pi läuft"""
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            if 'Raspberry Pi' in cpuinfo or 'BCM' in cpuinfo:
                return True
    except FileNotFoundError:
        pass
    return False

def run_command(command, description, show_output=False):
    """Führt einen Befehl aus und gibt Erfolg/Fehler zurück"""
    print(f"{Colors.OKCYAN}   → {description}...{Colors.ENDC}")
    
    try:
        if show_output:
            result = subprocess.run(command, check=True, shell=True, text=True, 
                                  capture_output=True)
            if result.stdout:
                print(f"{Colors.OKCYAN}     {result.stdout.strip()}{Colors.ENDC}")
        else:
            subprocess.run(command, check=True, shell=True, 
                         capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}     ✗ Fehler: {e}{Colors.ENDC}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"{Colors.FAIL}     Stderr: {e.stderr.strip()}{Colors.ENDC}")
        return False

def update_system():
    """Aktualisiert das System auf den neuesten Stand"""
    print(f"{Colors.OKBLUE}📋 Aktualisiere System...{Colors.ENDC}")
    
    success = True
    
    # APT Update
    if not run_command('apt update', 'Paketlisten werden aktualisiert'):
        success = False
    
    # APT Upgrade
    if success and not run_command('apt upgrade -y', 'System wird aktualisiert'):
        success = False
    
    if success:
        print(f"{Colors.OKGREEN}   ✓ System erfolgreich aktualisiert{Colors.ENDC}\n")
    else:
        print(f"{Colors.FAIL}   ✗ Fehler beim System-Update{Colors.ENDC}\n")
    
    return success

def install_git():
    """Installiert Git"""
    print(f"{Colors.OKBLUE}🔧 Installiere Git...{Colors.ENDC}")
    
    success = True
    
    # Git installieren
    if not run_command('apt install -y git', 'Git wird installiert'):
        success = False
    
    # Git Version prüfen
    if success:
        run_command('git --version', 'Git Version', show_output=True)
    
    if success:
        print(f"{Colors.OKGREEN}   ✓ Git erfolgreich installiert{Colors.ENDC}\n")
    else:
        print(f"{Colors.FAIL}   ✗ Fehler bei der Git Installation{Colors.ENDC}\n")
    
    return success

def install_python_tools():
    """Installiert Python3 und pip"""
    print(f"{Colors.OKBLUE}🐍 Installiere Python3 Tools...{Colors.ENDC}")
    
    success = True
    
    # Python3 und pip installieren
    packages = ['python3', 'python3-pip', 'python3-venv', 'python3-dev']
    for package in packages:
        if not run_command(f'apt install -y {package}', f'{package} wird installiert'):
            success = False
            break
    
    # Python Version prüfen
    if success:
        run_command('python3 --version', 'Python3 Version', show_output=True)
        run_command('pip3 --version', 'pip3 Version', show_output=True)
    
    if success:
        print(f"{Colors.OKGREEN}   ✓ Python3 Tools erfolgreich installiert{Colors.ENDC}\n")
    else:
        print(f"{Colors.FAIL}   ✗ Fehler bei der Python3 Installation{Colors.ENDC}\n")
    
    return success

def install_essential_tools():
    """Installiert weitere essenzielle Tools"""
    print(f"{Colors.OKBLUE}📦 Installiere essenzielle Tools...{Colors.ENDC}")
    
    tools = [
        'curl',
        'wget', 
        'vim',
        'nano',
        'unzip',
        'ca-certificates',
        'gnupg',
        'software-properties-common',
        'apt-transport-https'
    ]
    
    success = True
    
    # Alle Tools in einem Befehl installieren
    tools_str = ' '.join(tools)
    if not run_command(f'apt install -y {tools_str}', 'Essenzielle Tools werden installiert'):
        success = False
    
    # Versionen einiger wichtiger Tools prüfen
    if success:
        run_command('curl --version | head -1', 'curl Version', show_output=True)
        run_command('wget --version | head -1', 'wget Version', show_output=True)
    
    if success:
        print(f"{Colors.OKGREEN}   ✓ Essenzielle Tools erfolgreich installiert{Colors.ENDC}\n")
    else:
        print(f"{Colors.FAIL}   ✗ Fehler bei der Installation der essenziellen Tools{Colors.ENDC}\n")
    
    return success

def setup_git_config():
    """Fragt nach Git-Konfiguration"""
    print(f"{Colors.OKBLUE}⚙️ Git Konfiguration (optional)...{Colors.ENDC}")
    
    response = input(f"{Colors.BOLD}Möchten Sie Git jetzt konfigurieren? (j/N): {Colors.ENDC}").lower()
    if response in ['j', 'ja', 'y', 'yes']:
        print()
        name = input(f"{Colors.OKCYAN}Git Benutzername: {Colors.ENDC}")
        email = input(f"{Colors.OKCYAN}Git E-Mail: {Colors.ENDC}")
        
        if name and email:
            run_command(f'git config --global user.name "{name}"', 'Benutzername wird gesetzt')
            run_command(f'git config --global user.email "{email}"', 'E-Mail wird gesetzt')
            run_command('git config --global init.defaultBranch main', 'Standard Branch wird gesetzt')
            print(f"{Colors.OKGREEN}   ✓ Git erfolgreich konfiguriert{Colors.ENDC}\n")
        else:
            print(f"{Colors.WARNING}   ⚠ Git Konfiguration übersprungen{Colors.ENDC}\n")
    else:
        print(f"{Colors.OKCYAN}   → Git Konfiguration übersprungen{Colors.ENDC}\n")

def main():
    """Hauptfunktion des Basis-Installers"""
    print_banner()
    
    # Systemprüfungen
    print(f"{Colors.OKBLUE}{Colors.BOLD}Systemprüfungen:{Colors.ENDC}")
    
    # Raspberry Pi Check
    if check_raspberry_pi():
        print(f"{Colors.OKGREEN}   ✓ Raspberry Pi erkannt{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}   ⚠ Kein Raspberry Pi erkannt - Installation kann trotzdem fortgesetzt werden{Colors.ENDC}")
    
    # Root Rechte Check  
    if not check_root_privileges():
        print(f"{Colors.FAIL}   ✗ Root-Rechte erforderlich. Bitte mit 'sudo python3 setup-basics.py' ausführen{Colors.ENDC}")
        sys.exit(1)
    else:
        print(f"{Colors.OKGREEN}   ✓ Root-Rechte verfügbar{Colors.ENDC}")
    
    print()
    
    # Tools anzeigen
    print_tools()
    
    # Benutzerbestätigung
    response = input(f"{Colors.BOLD}Möchten Sie mit der Installation der Basis-Tools fortfahren? (j/N): {Colors.ENDC}").lower()
    if response not in ['j', 'ja', 'y', 'yes']:
        print(f"{Colors.WARNING}Installation abgebrochen.{Colors.ENDC}")
        sys.exit(0)
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}🚀 Basis-Installation gestartet...{Colors.ENDC}\n")
    
    # Installationsschritte
    steps = [
        ("System-Update", update_system),
        ("Git", install_git),
        ("Python3 Tools", install_python_tools),
        ("Essenzielle Tools", install_essential_tools)
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_function in steps:
        if step_function():
            success_count += 1
        else:
            print(f"{Colors.FAIL}Kritischer Fehler bei: {step_name}{Colors.ENDC}")
            break
    
    # Git Konfiguration (optional)
    setup_git_config()
    
    # Installation Summary
    print(f"{Colors.HEADER}{Colors.BOLD}📊 Installations-Zusammenfassung:{Colors.ENDC}")
    
    if success_count == total_steps:
        print(f"{Colors.OKGREEN}{Colors.BOLD}   ✓ Alle Basis-Tools erfolgreich installiert! ({success_count}/{total_steps}){Colors.ENDC}")
        print(f"\n{Colors.OKCYAN}System ist bereit für die Smart Home Installation:{Colors.ENDC}")
        print(f"   • Führen Sie nun aus: sudo python3 install.py")
        print(f"   • Oder klonen Sie das Repository: git clone https://github.com/flohaus/smart-home-phyton.git")
        print(f"\n{Colors.OKGREEN}Nächste Schritte:{Colors.ENDC}")
        print(f"   1. cd smart-home-phyton")
        print(f"   2. sudo python3 install.py")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}   ✗ Installation unvollständig ({success_count}/{total_steps} erfolgreich){Colors.ENDC}")
        print(f"{Colors.WARNING}Bitte Fehler beheben und erneut versuchen.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
