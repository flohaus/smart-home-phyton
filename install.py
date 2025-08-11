#!/usr/bin/env python3
"""
Smart Home System Installer for Raspberry Pi
============================================

Ein CLI-Installationstool für die automatische Einrichtung eines 
Smart Home Systems auf einem Raspberry Pi.

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
║               🏠 SMART HOME SYSTEM INSTALLER 🏠               ║
║                                                               ║
║                  Raspberry Pi Installation                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
"""
    print(banner)

def print_components():
    """Zeigt die zu installierenden Komponenten an"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}Folgende Komponenten werden installiert:{Colors.ENDC}\n")
    
    components = [
        "📋 System-Update (apt update & upgrade)",
        "🐳 Docker & Docker Compose",
        "🏡 OpenHAB 5 (geplant)",
        "📡 Zigbee2MQTT (geplant)", 
        "🦟 Mosquitto MQTT Broker (geplant)"
    ]
    
    for i, component in enumerate(components, 1):
        if "geplant" in component:
            print(f"   {i}. {Colors.WARNING}{component}{Colors.ENDC}")
        else:
            print(f"   {i}. {Colors.OKGREEN}{component}{Colors.ENDC}")
    
    print()

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

def check_root_privileges():
    """Überprüft ob das Skript mit Root-Rechten ausgeführt wird"""
    return os.geteuid() == 0

def update_system():
    """Aktualisiert das System auf den neuesten Stand"""
    print(f"{Colors.OKBLUE}📋 Aktualisiere System...{Colors.ENDC}")
    
    try:
        # APT Update
        print(f"{Colors.OKCYAN}   → apt update wird ausgeführt...{Colors.ENDC}")
        subprocess.run(['apt', 'update'], check=True, capture_output=True)
        
        # APT Upgrade
        print(f"{Colors.OKCYAN}   → apt upgrade wird ausgeführt...{Colors.ENDC}")
        subprocess.run(['apt', 'upgrade', '-y'], check=True, capture_output=True)
        
        print(f"{Colors.OKGREEN}   ✓ System erfolgreich aktualisiert{Colors.ENDC}\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}   ✗ Fehler beim System-Update: {e}{Colors.ENDC}\n")
        return False

def install_docker():
    """Installiert Docker und Docker Compose"""
    print(f"{Colors.OKBLUE}🐳 Installiere Docker...{Colors.ENDC}")
    
    try:
        # Docker installieren
        print(f"{Colors.OKCYAN}   → Docker wird installiert...{Colors.ENDC}")
        subprocess.run(['apt', 'install', '-y', 'docker.io'], check=True, capture_output=True)
        
        # Docker Service starten und aktivieren
        print(f"{Colors.OKCYAN}   → Docker Service wird gestartet...{Colors.ENDC}")
        subprocess.run(['systemctl', 'start', 'docker'], check=True, capture_output=True)
        subprocess.run(['systemctl', 'enable', 'docker'], check=True, capture_output=True)
        
        # Docker Compose installieren
        print(f"{Colors.OKCYAN}   → Docker Compose wird installiert...{Colors.ENDC}")
        subprocess.run(['apt', 'install', '-y', 'docker-compose'], check=True, capture_output=True)
        
        # Pi User zur Docker Gruppe hinzufügen
        print(f"{Colors.OKCYAN}   → Benutzer wird zur Docker Gruppe hinzugefügt...{Colors.ENDC}")
        subprocess.run(['usermod', '-aG', 'docker', 'pi'], check=True, capture_output=True)
        
        print(f"{Colors.OKGREEN}   ✓ Docker erfolgreich installiert{Colors.ENDC}\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}   ✗ Fehler bei der Docker Installation: {e}{Colors.ENDC}\n")
        return False

def main():
    """Hauptfunktion des Installers"""
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
        print(f"{Colors.FAIL}   ✗ Root-Rechte erforderlich. Bitte mit 'sudo python3 install.py' ausführen{Colors.ENDC}")
        sys.exit(1)
    else:
        print(f"{Colors.OKGREEN}   ✓ Root-Rechte verfügbar{Colors.ENDC}")
    
    print()
    
    # Komponenten anzeigen
    print_components()
    
    # Prüfe ob auto-install läuft
    auto_install = os.environ.get('AUTO_INSTALL', False)
    
    if auto_install:
        print(f"{Colors.OKCYAN}Automatische Installation erkannt - Installation wird fortgesetzt.{Colors.ENDC}")
    else:
        # Benutzerbestätigung nur bei manueller Ausführung
        try:
            response = input(f"{Colors.BOLD}Möchten Sie mit der Installation fortfahren? (j/N): {Colors.ENDC}").lower()
            if response not in ['j', 'ja', 'y', 'yes']:
                print(f"{Colors.WARNING}Installation abgebrochen.{Colors.ENDC}")
                sys.exit(0)
        except EOFError:
            # Non-interaktive Ausführung - automatisch fortfahren
            print(f"{Colors.OKCYAN}Non-interaktive Ausführung erkannt - Installation wird automatisch fortgesetzt.{Colors.ENDC}")
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}🚀 Installation gestartet...{Colors.ENDC}\n")
    
    # Installationsschritte
    success = True
    
    # 1. System Update
    if not update_system():
        success = False
    
    # 2. Docker Installation
    if success and not install_docker():
        success = False
    
    # Installation Summary
    print(f"{Colors.HEADER}{Colors.BOLD}📊 Installations-Zusammenfassung:{Colors.ENDC}")
    
    if success:
        print(f"{Colors.OKGREEN}{Colors.BOLD}   ✓ Installation erfolgreich abgeschlossen!{Colors.ENDC}")
        
        # Prüfe ob auto-install läuft
        auto_install = os.environ.get('AUTO_INSTALL', False)
        
        if auto_install:
            # Bei auto-install.sh wird der Neustart vom Hauptskript übernommen
            print(f"{Colors.OKCYAN}Docker Installation abgeschlossen. Neustart wird vom Auto-Installer verwaltet.{Colors.ENDC}")
        else:
            # Manuelle Installation - Neustart anbieten
            print(f"\n{Colors.WARNING}Nach der Docker-Installation ist ein Neustart erforderlich, damit alle Änderungen wirksam werden.{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Insbesondere die Docker-Gruppenmitgliedschaft wird erst nach dem Neustart aktiv.{Colors.ENDC}\n")
            
            # Neustart-Bestätigung
            try:
                reboot_response = input(f"{Colors.BOLD}Möchten Sie das System jetzt neu starten? (J/n): {Colors.ENDC}").lower()
            except EOFError:
                # Non-interaktive Ausführung - automatisch neustarten
                print(f"{Colors.OKCYAN}Non-interaktive Ausführung - System wird automatisch neu gestartet.{Colors.ENDC}")
                reboot_response = 'j'
                
            if reboot_response in ['', 'j', 'ja', 'y', 'yes']:
                print(f"\n{Colors.OKBLUE}🔄 System wird neu gestartet...{Colors.ENDC}")
                print(f"{Colors.OKCYAN}Nach dem Neustart können Sie Docker ohne sudo verwenden.{Colors.ENDC}")
                print(f"{Colors.OKCYAN}Testen Sie mit: docker --version{Colors.ENDC}")
                
                # 3 Sekunden Countdown
                for i in range(3, 0, -1):
                    print(f"{Colors.WARNING}Neustart in {i} Sekunden...{Colors.ENDC}")
                    time.sleep(1)
                
                try:
                    subprocess.run(['reboot'], check=True)
                except subprocess.CalledProcessError:
                    print(f"{Colors.FAIL}Fehler beim Neustart. Bitte manuell neustarten: sudo reboot{Colors.ENDC}")
            else:
                print(f"\n{Colors.OKCYAN}Manueller Neustart erforderlich:{Colors.ENDC}")
                print(f"   • System neustarten: sudo reboot")
                print(f"   • Docker Funktionalität testen: docker --version")
                print(f"   • Docker Compose testen: docker-compose --version")
        
        print(f"\n{Colors.WARNING}Hinweis: OpenHAB, Zigbee2MQTT und Mosquitto werden in zukünftigen Versionen implementiert.{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}{Colors.BOLD}   ✗ Installation unvollständig - bitte Fehler prüfen{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
