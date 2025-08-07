# Smart Home System - Raspberry Pi Installation

Ein automatisiertes CLI-Installationstool für die Einrichtung eines umfassenden Smart Home Systems auf einem Raspberry Pi.

## 🎯 Zielbild

Dieses Projekt hat zum Ziel, ein vollständig automatisiertes Smart Home System auf einem Raspberry Pi zu installieren und zu konfigurieren. Das finale System wird folgende Komponenten umfassen:

### 🏠 Smart Home Komponenten

#### ✅ Bereits implementiert:
- **System-Update**: Automatische Aktualisierung des Raspberry Pi Systems
- **Docker & Docker Compose**: Container-Plattform für alle Services

#### 🔄 In Entwicklung / Geplant:
- **OpenHAB 5**: Open Source Home Automation Platform
  - Web-basierte Benutzeroberfläche
  - Regel-Engine für Automatisierungen
  - Unterstützung für hunderte von Smart Home Geräten
  
- **Zigbee2MQTT**: Zigbee zu MQTT Bridge
  - Unterstützung für Zigbee-Geräte ohne proprietäre Hubs
  - Direkte Integration in das MQTT-Netzwerk
  - Große Geräte-Kompatibilität
  
- **Mosquitto MQTT Broker**: Zentraler Nachrichtenvermittler
  - Lightweight Message Broker
  - Verbindung zwischen allen Smart Home Komponenten
  - Sichere Kommunikation mit TLS-Unterstützung

## 🚀 Installation

### Voraussetzungen

- Raspberry Pi (3B+ oder neuer empfohlen)
- Raspberry Pi OS (Bullseye oder neuer)
- Internetverbindung
- Root-Zugriff (sudo)

### Schnellinstallation

```bash
# Repository klonen
git clone https://github.com/flohaus/smart-home-phyton.git
cd smart-home-phyton

# Installationsskript ausführen
sudo python3 install.py
```

### Manuelle Installation

Falls Sie die Installation Schritt für Schritt durchführen möchten:

```bash
# 1. System aktualisieren
sudo apt update && sudo apt upgrade -y

# 2. Docker installieren
sudo apt install -y docker.io docker-compose

# 3. Docker Service starten
sudo systemctl start docker
sudo systemctl enable docker

# 4. Benutzer zur Docker-Gruppe hinzufügen
sudo usermod -aG docker pi
```

## 📁 Projektstruktur

```
smart-home-phyton/
├── install.py          # Hauptinstallationsskript
├── README.md          # Diese Datei
├── docker/            # Docker Compose Dateien (geplant)
│   ├── openhab/
│   ├── zigbee2mqtt/
│   └── mosquitto/
├── configs/           # Konfigurationsdateien (geplant)
└── scripts/           # Hilfsskripte (geplant)
```

## 🔧 Konfiguration

### Nach der Installation

1. **Neustart des Systems**:
   ```bash
   sudo reboot
   ```

2. **Docker Funktionalität testen**:
   ```bash
   docker --version
   docker-compose --version
   ```

3. **Docker ohne sudo verwenden**:
   Nach dem Neustart sollte Docker ohne sudo-Rechte funktionieren.

## 📋 Geplante Features

### Version 2.0
- [ ] OpenHAB 5 Installation via Docker
- [ ] Automatische OpenHAB Basiskonfiguration
- [ ] Web-Interface Setup

### Version 3.0
- [ ] Mosquitto MQTT Broker Setup
- [ ] SSL/TLS Zertifikat-Management
- [ ] MQTT Benutzer- und Rechteverwaltung

### Version 4.0
- [ ] Zigbee2MQTT Installation
- [ ] Automatische Zigbee-Adapter Erkennung
- [ ] Integration mit OpenHAB

### Version 5.0
- [ ] Backup und Restore Funktionalität
- [ ] Update-Management für alle Komponenten
- [ ] Monitoring und Logging
- [ ] Web-basiertes Setup-Interface

## 🛠️ Entwicklung

### Lokale Entwicklung

```bash
# Repository forken und klonen
git clone https://github.com/IHR_USERNAME/smart-home-phyton.git
cd smart-home-phyton

# Virtual Environment erstellen (optional)
python3 -m venv venv
source venv/bin/activate

# Entwicklung...
```

### Beitragen

1. Fork des Repositories erstellen
2. Feature Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

## 📊 System-Anforderungen

### Minimum
- Raspberry Pi 3B+
- 1GB RAM
- 8GB SD-Karte
- Raspberry Pi OS Lite

### Empfohlen
- Raspberry Pi 4B (4GB RAM)
- 32GB SD-Karte (Class 10)
- Raspberry Pi OS Desktop
- Ethernet-Verbindung

## 🔒 Sicherheit

- Alle Services laufen in Docker-Containern
- Regelmäßige Updates der Base Images
- Sichere Standardkonfigurationen
- Optional: SSL/TLS Verschlüsselung

## 📞 Support

Bei Fragen oder Problemen:

1. Prüfen Sie die [Issues](https://github.com/flohaus/smart-home-phyton/issues)
2. Erstellen Sie ein neues Issue mit detaillierter Beschreibung
3. Fügen Sie Log-Ausgaben bei

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe `LICENSE` Datei für Details.

## 🙏 Danksagungen

- OpenHAB Community für die großartige Smart Home Platform
- Zigbee2MQTT Entwickler für die Zigbee-Integration
- Eclipse Mosquitto für den zuverlässigen MQTT Broker

---

**Status**: 🔄 In aktiver Entwicklung  
**Version**: 1.0.0  
**Letztes Update**: August 2025
