#!/bin/bash

# Smart Home System - Vollautomatische Installation
# =================================================
# 
# Dieses Skript installiert automatisch alle benötigten Tools und
# das komplette Smart Home System ohne Benutzerinteraktion
#
# Autor: Smart Home Setup
# Version: 2.0.0

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Logging
LOG_FILE="/tmp/smart-home-install.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

# Banner anzeigen
print_banner() {
    echo -e "${PURPLE}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║        🏠 SMART HOME VOLLAUTOMATIK-INSTALLATION 🏠           ║"
    echo "║                                                               ║"
    echo "║              Raspberry Pi Setup - Hands-Free                 ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}Log-Datei: ${LOG_FILE}${NC}"
    echo ""
}

# Fehlerbehandlung
handle_error() {
    echo -e "${RED}❌ Fehler in Zeile $1${NC}"
    echo -e "${YELLOW}Siehe Log-Datei: ${LOG_FILE}${NC}"
    exit 1
}

trap 'handle_error $LINENO' ERR

# Root-Rechte prüfen
check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ Dieses Skript muss mit Root-Rechten ausgeführt werden!${NC}"
        echo -e "${YELLOW}Verwendung: curl -sSL https://raw.githubusercontent.com/flohaus/smart-home-phyton/master/auto-install.sh | sudo bash${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Root-Rechte verfügbar${NC}"
}

# System-Update
update_system() {
    echo -e "${BLUE}${BOLD}📋 System wird aktualisiert...${NC}"
    
    echo -e "${CYAN}→ apt-get update${NC}"
    apt-get update -qq > /dev/null 2>&1
    
    echo -e "${CYAN}→ apt-get upgrade${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq > /dev/null 2>&1
    
    echo -e "${GREEN}✓ System aktualisiert${NC}"
}

# Python3 installieren
install_python() {
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓ Python3 bereits installiert: $(python3 --version)${NC}"
        return 0
    fi
    
    echo -e "${BLUE}🐍 Python3 wird installiert...${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 python3-pip python3-venv python3-dev > /dev/null 2>&1
    echo -e "${GREEN}✓ Python3 installiert: $(python3 --version)${NC}"
}

# Curl installieren (falls nicht vorhanden)
install_curl() {
    if command -v curl &> /dev/null; then
        echo -e "${GREEN}✓ curl bereits installiert${NC}"
        return 0
    fi
    
    echo -e "${BLUE}📦 curl wird installiert...${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq curl > /dev/null 2>&1
    echo -e "${GREEN}✓ curl installiert${NC}"
}

# Git installieren
install_git() {
    if command -v git &> /dev/null; then
        echo -e "${GREEN}✓ Git bereits installiert: $(git --version | head -1)${NC}"
        return 0
    fi
    
    echo -e "${BLUE}🔧 Git wird installiert...${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git > /dev/null 2>&1
    echo -e "${GREEN}✓ Git installiert: $(git --version | head -1)${NC}"
}

# Basis-Tools installieren
install_essential_tools() {
    echo -e "${BLUE}${BOLD}🔧 Essenzielle Tools werden installiert...${NC}"
    
    local tools=(
        "wget"
        "vim" 
        "nano"
        "unzip"
        "ca-certificates"
        "gnupg"
        "software-properties-common"
        "apt-transport-https"
        "lsb-release"
    )
    
    echo -e "${CYAN}→ Installiere: ${tools[*]}${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "${tools[@]}" > /dev/null 2>&1
    
    echo -e "${GREEN}✓ Essenzielle Tools installiert${NC}"
}

# Docker installieren
install_docker() {
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓ Docker bereits installiert: $(docker --version)${NC}"
        return 0
    fi
    
    echo -e "${BLUE}${BOLD}🐳 Docker wird installiert...${NC}"
    
    # Docker über apt-get installieren (einfacher für Raspberry Pi)
    echo -e "${CYAN}→ Docker installieren${NC}"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker.io docker-compose > /dev/null 2>&1
    
    # Docker Service starten und aktivieren
    echo -e "${CYAN}→ Docker Service starten${NC}"
    systemctl start docker > /dev/null 2>&1
    systemctl enable docker > /dev/null 2>&1
    
    # Pi User zur Docker-Gruppe hinzufügen
    echo -e "${CYAN}→ Benutzer 'pi' zur Docker-Gruppe hinzufügen${NC}"
    usermod -aG docker pi > /dev/null 2>&1 || echo "   Benutzer 'pi' nicht gefunden - übersprungen"
    
    # Aktuellen Benutzer zur Docker-Gruppe hinzufügen (falls nicht root)
    if [ "$SUDO_USER" ]; then
        echo -e "${CYAN}→ Benutzer '$SUDO_USER' zur Docker-Gruppe hinzufügen${NC}"
        usermod -aG docker "$SUDO_USER" > /dev/null 2>&1
    fi
    
    echo -e "${GREEN}✓ Docker installiert: $(docker --version)${NC}"
}

# Repository klonen
clone_repository() {
    echo -e "${BLUE}${BOLD}📥 Repository wird geklont...${NC}"
    
    local work_dir="/opt/smart-home-system"
    echo -e "${CYAN}→ Arbeitsverzeichnis: ${work_dir}${NC}"
    
    # Altes Verzeichnis entfernen falls vorhanden
    if [ -d "$work_dir" ]; then
        echo -e "${YELLOW}⚠️  Entferne altes Verzeichnis${NC}"
        rm -rf "$work_dir"
    fi
    
    # Verzeichnis erstellen und Repository klonen
    mkdir -p "$work_dir"
    cd "$work_dir"
    
    echo -e "${CYAN}→ Klone Repository...${NC}"
    git clone https://github.com/flohaus/smart-home-phyton.git .
    
    echo -e "${GREEN}✓ Repository geklont nach: ${work_dir}${NC}"
    
    # Verzeichnis-Rechte für normalen Benutzer setzen
    if [ "$SUDO_USER" ]; then
        chown -R "$SUDO_USER:$SUDO_USER" "$work_dir"
    fi
}

# Smart Home System installieren
install_smart_home() {
    echo -e "${BLUE}${BOLD}🏠 Smart Home System wird installiert...${NC}"
    
    if [ ! -f "install.py" ]; then
        echo -e "${RED}❌ install.py nicht gefunden!${NC}"
        return 1
    fi
    
    echo -e "${CYAN}→ Führe install.py aus...${NC}"
    # Setze Umgebungsvariable für non-interaktive Ausführung
    export AUTO_INSTALL=1
    python3 install.py
    
    echo -e "${GREEN}✓ Smart Home System installiert${NC}"
}

# Neustart anbieten
offer_reboot() {
    echo -e "${YELLOW}${BOLD}🔄 Ein Neustart wird empfohlen${NC}"
    echo -e "${CYAN}Dies aktiviert die Docker-Gruppenmitgliedschaft vollständig.${NC}"
    echo -e "${CYAN}Das System startet automatisch in 10 Sekunden neu...${NC}"
    echo -e "${YELLOW}Drücke Ctrl+C zum Abbrechen${NC}"
    
    # 10 Sekunden Countdown
    for i in {10..1}; do
        echo -e "${YELLOW}Neustart in ${i} Sekunden...${NC}"
        sleep 1
    done
    
    echo -e "${BLUE}🔄 System wird neu gestartet...${NC}"
    reboot
}

# Hauptfunktion
main() {
    print_banner
    
    echo -e "${CYAN}${BOLD}🔍 Systemprüfungen und automatische Installation${NC}"
    echo -e "${CYAN}Alle fehlenden Komponenten werden automatisch installiert.${NC}"
    echo ""
    
    # Root-Rechte prüfen
    check_root
    
    # System aktualisieren
    update_system
    
    # Basis-Tools installieren
    install_curl
    install_python
    install_git
    install_essential_tools
    
    # Docker installieren
    install_docker
    
    # Repository klonen
    clone_repository
    
    # Smart Home System installieren
    install_smart_home
    
    echo ""
    echo -e "${GREEN}${BOLD}🎉 INSTALLATION ERFOLGREICH ABGESCHLOSSEN! 🎉${NC}"
    echo ""
    echo -e "${CYAN}${BOLD}📋 Zusammenfassung:${NC}"
    echo -e "${GREEN}✓ System aktualisiert${NC}"
    echo -e "${GREEN}✓ Python3 installiert: $(python3 --version 2>/dev/null || echo 'N/A')${NC}"
    echo -e "${GREEN}✓ Git installiert: $(git --version 2>/dev/null | head -1 || echo 'N/A')${NC}"
    echo -e "${GREEN}✓ Docker installiert: $(docker --version 2>/dev/null || echo 'N/A')${NC}"
    echo -e "${GREEN}✓ Smart Home System installiert${NC}"
    echo ""
    echo -e "${CYAN}📁 Installation befindet sich in: /opt/smart-home-system${NC}"
    echo -e "${CYAN}📄 Log-Datei: ${LOG_FILE}${NC}"
    echo ""
    
    # Neustart anbieten
    offer_reboot
}

# Skript ausführen
main "$@"
