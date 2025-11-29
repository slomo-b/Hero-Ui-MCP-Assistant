# Hero UI MCP Assistant 🚀

Ein leistungsstarker Model Context Protocol (MCP) Server, der umfassendes Wissen über Hero UI bereitstellt. Dieser Server ermöglicht es KI-Assistenten, auf die gesamte Hero UI Dokumentation, Komponenten und Design-Prinzipien zuzugreifen.

## 📋 Inhaltsverzeichnis

- [Features](#-features)
- [Voraussetzungen](#-voraussetzungen)
- [Installation](#-installation)
- [Server Starten](#-server-starten)
- [MCP Integration](#-mcp-integration)
- [Verfügbare Tools](#-verfügbare-tools)
- [Verwendungsbeispiele](#-verwendungsbeispiele)
- [Projektstruktur](#-projektstruktur)
- [Entwicklung](#-entwicklung)

## ✨ Features

- **Umfassende Hero UI Dokumentation**: Zugriff auf alle Komponenten, Guides und Best Practices
- **Intelligente Suche**: Durchsucht automatisch alle Dokumentationen nach relevanten Informationen
- **60+ UI Komponenten**: Detaillierte Informationen zu allen Hero UI Komponenten
- **Design Principles**: Zugriff auf Hero UI Design-Richtlinien
- **Code Snippets**: Sofort verwendbare Code-Beispiele für jede Komponente
- **Hot-Reload**: Automatisches Neuladen der Datenbanken während der Entwicklung

## 📦 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

## 🔧 Installation

1. **Repository klonen oder herunterladen:**
```bash
git clone https://github.com/slomo-b/Hero-Ui-MCP-Assistant.git
cd Hero-Ui-MCP-Assistant
```

2. **Python-Abhängigkeiten installieren:**
```bash
pip install fastapi uvicorn pydantic
```

Alternativ mit einer requirements.txt (erstellen Sie diese bei Bedarf):
```bash
pip install -r requirements.txt
```

## 🚀 Server Starten

### Standard Start

```bash
cd mcp
uvicorn mcp_server:app --reload
```

Der Server läuft standardmäßig auf `http://127.0.0.1:8000`

### Mit spezifischem Port

```bash
uvicorn mcp_server:app --reload --port 8001
```

### Mit spezifischem Host (für Netzwerkzugriff)

```bash
uvicorn mcp_server:app --reload --host 0.0.0.0 --port 8000
```

### Produktionsmodus (ohne Auto-Reload)

```bash
uvicorn mcp_server:app --host 0.0.0.0 --port 8000
```

### Server-Status überprüfen

Öffnen Sie im Browser: `http://127.0.0.1:8000`

Sie sollten sehen:
```json
{
  "status": "Hero UI MCP Server Active",
  "version": "0.3.0"
}
```

## 🔌 MCP Integration

### Claude Desktop Integration

1. **Claude Desktop Konfigurationsdatei öffnen:**

   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Server-Konfiguration hinzufügen:**

```json
{
  "mcpServers": {
    "hero-ui-assistant": {
      "command": "uvicorn",
      "args": [
        "mcp_server:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
      ],
      "cwd": "C:/Users/LENOVO/Documents/Hero-Ui-MCP-Assistant/mcp",
      "env": {}
    }
  }
}
```

**Wichtig:** Passen Sie den `cwd` Pfad an Ihren lokalen Pfad an!

3. **Claude Desktop neu starten**

### Cline (VS Code Extension) Integration

1. **Cline MCP Settings öffnen** (in VS Code)

2. **Server hinzufügen:**

```json
{
  "mcpServers": {
    "hero-ui-assistant": {
      "command": "uvicorn",
      "args": [
        "mcp_server:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
      ],
      "cwd": "C:/Users/LENOVO/Documents/Hero-Ui-MCP-Assistant/mcp"
    }
  }
}
```

3. **VS Code neu laden** oder Cline Extension neu starten

### Manuelle HTTP Integration

Wenn Sie den Server manuell einbinden möchten:

```bash
# Server starten
cd mcp
uvicorn mcp_server:app --host 127.0.0.1 --port 8000

# MCP-Anfragen an
# http://127.0.0.1:8000/mcp
```

## 🛠️ Verfügbare Tools

### 1. `hero_ui.search_all`

Durchsucht die gesamte Hero UI Dokumentation.

**Parameter:**
- `query` (string, erforderlich): Suchbegriff

**Beispiel:**
```json
{
  "query": "button color variants"
}
```

### 2. `hero_ui.get_component_details`

Holt detaillierte Informationen zu einer spezifischen Komponente.

**Parameter:**
- `component_name` (string, erforderlich): Komponenten-Name (z.B. "Button", "Modal")

**Beispiel:**
```json
{
  "component_name": "Button"
}
```

### 3. `hero_ui.list_available_components`

Listet alle verfügbaren Hero UI Komponenten auf.

**Keine Parameter erforderlich**

### 4. `hero_ui.get_design_principles`

Ruft die Hero UI Design-Prinzipien ab.

**Keine Parameter erforderlich**

## 💡 Verwendungsbeispiele

### Beispiel 1: Komponente suchen
```
"Zeige mir wie ich einen Button mit Hero UI erstelle"
→ Der Assistent nutzt hero_ui.get_component_details("Button")
```

### Beispiel 2: Design-Guidance
```
"Was sind die Design-Prinzipien von Hero UI?"
→ Der Assistent nutzt hero_ui.get_design_principles()
```

### Beispiel 3: Breite Suche
```
"Wie implementiere ich Dark Mode in Hero UI?"
→ Der Assistent nutzt hero_ui.search_all("dark mode")
```

### Beispiel 4: Komponenten-Übersicht
```
"Welche Formular-Komponenten bietet Hero UI?"
→ Der Assistent nutzt hero_ui.list_available_components() und filtert
```

## 📁 Projektstruktur

```
Hero-Ui-MCP-Assistant/
├── README.md                           # Diese Datei
├── LICENSE                             # MIT Lizenz
├── mcp/
│   ├── mcp_server.py                   # FastAPI MCP Server
│   ├── hero_ui_db.json                 # Komponenten-Übersicht
│   ├── getting_started_db.json         # Getting Started Guide
│   ├── installation_db.json            # Installation Guide
│   ├── design_principles_db.json       # Design Principles
│   ├── components_*_db.json            # Komponenten-Details (60+ Dateien)
│   ├── customization_*_db.json         # Customization Guides
│   └── *_guide_db.json                 # Framework-spezifische Guides
└── .gitattributes
```

## 🔨 Entwicklung

### Hot-Reload während der Entwicklung

Der Server lädt automatisch alle JSON-Datenbanken bei jedem Tool-Aufruf neu (nur im `--reload` Modus):

```bash
uvicorn mcp_server:app --reload
```

### Neue Datenbank hinzufügen

1. Erstellen Sie eine neue `.json` Datei im `mcp/` Verzeichnis
2. Fügen Sie den Schlüssel zu `DB_KEYS` in `mcp_server.py` hinzu
3. Fügen Sie das Mapping zu `FILENAME_MAPPING` hinzu
4. Server neu starten

### Datenbank-Format

Alle Datenbanken verwenden folgendes JSON-Format:

```json
[
  {
    "topic": "Titel des Eintrags",
    "content": "Detaillierter Inhalt...",
    "keywords": ["keyword1", "keyword2"],
    "code_snippet": "// Optional: Code-Beispiel"
  }
]
```

### Server testen

```bash
# Server starten
uvicorn mcp_server:app --reload

# In einem anderen Terminal/Browser
curl http://127.0.0.1:8000
```

## 📝 Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei

## 🤝 Beitragen

Contributions sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue.

## 📧 Support

Bei Fragen oder Problemen öffnen Sie bitte ein Issue im GitHub Repository.

---

**Erstellt mit ❤️ für die Hero UI Community**
