#!/bin/bash

# Smart Home System - Komplette Installation
# ==========================================
# 
# Dieses Skript führt die komplette Installation durch:
# 1. Basis-Tools (falls benötigt)
# 2. Smart Home System
#
# Autor: Smart Home Setup
# Version: 1.0.0

set -e  # Bei Fehlern abbrechen

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Banner anzeigen
print_banner() {
    echo -e "${PURPLE}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║           🏠 SMART HOME KOMPLETTINSTALLATION 🏠               ║"
    echo "║                                                               ║"
    echo "║                  Raspberry Pi Setup                          ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Prüfung ob Root-Rechte vorhanden
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ Dieses Skript muss mit Root-Rechten ausgeführt werden!${NC}"
        echo -e "${YELLOW}Verwendung: sudo $0${NC}"
        exit 1
    fi
}

# Git-Installation prüfen
check_git() {
    if ! command -v git &> /dev/null; then
        echo -e "${YELLOW}⚠️  Git ist nicht installiert${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Git ist bereits installiert$(NC)"
        return 0
    fi
}

# Python3-Installation prüfen
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  Python3 ist nicht installiert${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Python3 ist bereits installiert${NC}"
        return 0
    fi
}

# Basis-Tools installieren
install_basics() {
    echo -e "${BLUE}${BOLD}📦 Installiere Basis-Tools...${NC}"
    
    if [ -f "setup-basics.py" ]; then
        python3 setup-basics.py
    else
        echo -e "${YELLOW}⚠️  setup-basics.py nicht gefunden, lade es herunter...${NC}"
        curl -O https://raw.githubusercontent.com/flohaus/smart-home-phyton/master/setup-basics.py
        python3 setup-basics.py
    fi
}

# Smart Home System installieren
install_smart_home() {
    echo -e "${BLUE}${BOLD}🏠 Installiere Smart Home System...${NC}"
    
    if [ -f "install.py" ]; then
        python3 install.py
    else
        echo -e "${RED}❌ install.py nicht gefunden!${NC}"
        echo -e "${YELLOW}Stelle sicher, dass du im richtigen Verzeichnis bist.${NC}"
        exit 1
    fi
}

# Repository klonen (falls nicht lokal)
clone_repo() {
    if [ ! -d ".git" ]; then
        echo -e "${BLUE}📥 Klone Repository...${NC}"
        cd /tmp
        git clone https://github.com/flohaus/smart-home-phyton.git
        cd smart-home-phyton
        echo -e "${GREEN}✓ Repository geklont${NC}"
    else
        echo -e "${GREEN}✓ Repository bereits vorhanden${NC}"
    fi
}

main() {
    print_banner
    
    echo -e "${CYAN}${BOLD}Systemprüfungen:${NC}"
    check_root
    
    # Prüfe verfügbare Tools
    need_basics=false
    
    if ! check_git; then
        need_basics=true
    fi
    
    if ! check_python; then
        need_basics=true
    fi
    
    echo ""
    
    # Installationsschritte
    if [ "$need_basics" = true ]; then
        echo -e "${YELLOW}${BOLD}🔧 Basis-Tools werden benötigt${NC}"
        read -p "Basis-Tools jetzt installieren? (J/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            echo -e "${RED}Installation abgebrochen${NC}"
            exit 1
        fi
        install_basics
        echo -e "${GREEN}✓ Basis-Tools Installation abgeschlossen${NC}"
        echo ""
    fi
    
    # Repository klonen falls nötig
    clone_repo
    
    # Smart Home System installieren
    echo -e "${BLUE}${BOLD}🏠 Starte Smart Home Installation...${NC}"
    install_smart_home
    
    echo ""
    echo -e "${GREEN}${BOLD}🎉 Installation abgeschlossen!${NC}"
    echo -e "${CYAN}Das Smart Home System ist jetzt bereit.${NC}"
}

# Skript ausführen
main "$@"
