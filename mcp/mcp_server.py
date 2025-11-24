from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Union, Optional
import json
import os
import re

# --- KONFIGURATION & DATENBANK-SETUP ---

DB_KEYS = [
    "HERO_UI_COMPONENTS", "GETTING_STARTED", "DESIGN_PRINCIPLES", "INSTALLATION",
    "CLI", "ROUTING", "FORMS", "TAILWIND_V4", "NEXTJS_GUIDE", "VITE_GUIDE",
    "CUSTOMIZATION_THEME", "CUSTOMIZATION_LAYOUT", "CUSTOMIZATION_COLORS",
    "CUSTOMIZATION_CUSTOMIZE_THEME", "CUSTOMIZATION_CREATE_THEME", "CUSTOMIZATION_DARK_MODE",
    "CUSTOMIZATION_OVERRIDE_STYLES", "CUSTOMIZATION_CUSTOM_VARIANTS", "PROVIDER",
    "COMPONENTS_ACCORDION", "COMPONENTS_AUTOCOMPLETE", "COMPONENTS_ALERT", "COMPONENTS_AVATAR",
    "COMPONENTS_BADGE", "COMPONENTS_BREADCRUMBS", "COMPONENTS_BUTTON", "COMPONENTS_CARD",
    "COMPONENTS_CHECKBOX", "COMPONENTS_CHECKBOX_GROUP", "COMPONENTS_CHIP", "COMPONENTS_CODE",
    "COMPONENTS_DATE_INPUT", "COMPONENTS_DATE_PICKER", "COMPONENTS_DATE_RANGE_PICKER",
    "COMPONENTS_DIVIDER", "COMPONENTS_DROPDOWN", "COMPONENTS_DRAWER", "COMPONENTS_FORM",
    "COMPONENTS_IMAGE", "COMPONENTS_INPUT", "COMPONENTS_INPUT_OTP", "COMPONENTS_KBD",
    "COMPONENTS_LINK", "COMPONENTS_LISTBOX", "COMPONENTS_MODAL", "COMPONENTS_NAVBAR",
    "COMPONENTS_NUMBER_INPUT", "COMPONENTS_PAGINATION", "COMPONENTS_POPOVER",
    "COMPONENTS_PROGRESS", "COMPONENTS_RADIO_GROUP", "COMPONENTS_RANGE_CALENDAR",
    "COMPONENTS_SCROLL_SHADOW", "COMPONENTS_SELECT", "COMPONENTS_SKELETON", "COMPONENTS_SLIDER",
    "COMPONENTS_SNIPPET", "COMPONENTS_SPACER", "COMPONENTS_SPINNER", "COMPONENTS_SWITCH",
    "COMPONENTS_TABLE", "COMPONENTS_TABS", "COMPONENTS_TEXTAREA", "COMPONENTS_TIME_INPUT",
    "COMPONENTS_TOOLTIP", "COMPONENTS_USER"
]

FILENAME_MAPPING = {
    "HERO_UI_COMPONENTS": "hero_ui_db.json",
    **{key: f"{key.lower()}_db.json" for key in DB_KEYS if key != "HERO_UI_COMPONENTS"}
}

# Zentraler Speicher für alle geladenen JSON-Daten
DATABASES: Dict[str, List[Dict[str, Any]]] = {key: [] for key in DB_KEYS}

# --- Pydantic Models for JSON-RPC 2.0 ---

class McpRequest(BaseModel):
    jsonrpc: str = Field(..., pattern="2.0")
    id: Optional[Union[str, int]] = None
    method: str
    params: Optional[Dict[str, Any]] = None

# --- Helper Functions ---

def load_dbs():
    """Lädt alle Datenbanken neu ein."""
    base_path = "."
    loaded_count = 0
    for db_key, filename in FILENAME_MAPPING.items():
        file_path = os.path.join(base_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                if isinstance(content, list):
                    DATABASES[db_key] = content
                else:
                    print(f"Warning: {filename} content is not a list. Skipping.")
                loaded_count += 1
        except FileNotFoundError:
            pass # Silent fail for missing optional DBs
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{file_path}'.")
    print(f"Reloaded {loaded_count} database files.")

def find_best_matches(query: str, items: List[Dict[str, Any]], fields: List[str], limit: int = 5) -> List[Dict[str, Any]]:
    """
    Eine einfache Suchfunktion, die Keywords gewichtet.
    """
    query_terms = set(query.lower().split())
    scored_items = []

    for item in items:
        score = 0
        for field in fields:
            value = item.get(field)
            if isinstance(value, str):
                value_lower = value.lower()
                # Exakte Matches im Text boosten
                if query.lower() in value_lower:
                    score += 3
                # Einzelne Term-Matches
                for term in query_terms:
                    if term in value_lower:
                        score += 1
            elif isinstance(value, list): # z.B. keywords
                for list_item in value:
                    if isinstance(list_item, str):
                        if query.lower() in list_item.lower():
                            score += 2
                        for term in query_terms:
                            if term in list_item.lower():
                                score += 1
        
        if score > 0:
            scored_items.append((score, item))

    # Sortieren nach Score (absteigend)
    scored_items.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored_items[:limit]]

# --- Tool Definitions ---

TOOLS = {
    "hero_ui.search_all": {
        "description": "Die wichtigste Funktion zum Entdecken. Durchsucht ALLE Dokumentationen, Komponenten und Design-Guides nach Stichworten. Nutze dies, wenn du nicht genau weißt, wo du suchen sollst.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Suchbegriff, z.B. 'button color', 'dark mode', 'form validation'."
                }
            },
            "required": ["query"]
        }
    },
    "hero_ui.get_component_details": {
        "description": "Holt umfassende Informationen zu einer spezifischen Komponente. Beinhaltet Code-Snippets, Props, Styling-Varianten und Best Practices. Nutze dies, wenn du eine konkrete Komponente implementieren willst.",
        "parameters": {
            "type": "object",
            "properties": {
                "component_name": {
                    "type": "string",
                    "description": "Der exakte Name der Komponente (z.B. 'Button', 'Table', 'Modal')."
                }
            },
            "required": ["component_name"]
        }
    },
    "hero_ui.list_available_components": {
        "description": "Listet alle verfügbaren Hero UI Komponenten auf. Hilfreich, um einen Überblick zu bekommen.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    "hero_ui.get_design_principles": {
        "description": "Ruft die allgemeinen Design-Prinzipien von Hero UI ab. Wichtig für Konsistenz und UX-Entscheidungen.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

# --- FastAPI App ---

app = FastAPI(
    title="Hero UI MCP Server",
    description="Mächtiger Assistent für Hero UI Design und Implementation.",
    version="0.3.0",
)

@app.on_event("startup")
async def startup_event():
    load_dbs()

@app.get("/")
def read_root():
    return {"status": "Hero UI MCP Server Active", "version": "0.3.0"}

# --- MCP Handler ---

@app.post("/mcp")
async def handle_mcp_request(request: McpRequest):
    if request.id is None:
        # Notifications
        return Response(status_code=204)

    if request.method == 'initialize':
        return create_jsonrpc_response(request.id, {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "hero-ui-assistant", "version": "0.3.0"},
            "capabilities": {"tools": TOOLS}
        })
    
    if request.method == 'tools/list':
        tool_list = []
        for name, data in TOOLS.items():
            tool_list.append({
                "id": name,
                "name": name,
                "description": data["description"],
                "inputSchema": data["parameters"] # "inputSchema" ist der korrekte Key für MCP
            })
        return create_jsonrpc_response(request.id, {"tools": tool_list})

    if request.method == 'tools/call':
        load_dbs() # Hot-Reload für Entwicklung
        
        tool_name = request.params.get("name")
        args = request.params.get("arguments", {})
        
        result_content = []

        try:
            if tool_name == "hero_ui.search_all":
                query = args.get("query", "")
                if not query:
                    raise ValueError("Query parameter required")

                matches = []
                
                # 1. Suche in Komponenten-Liste (Overview)
                comps = DATABASES.get("HERO_UI_COMPONENTS", [])
                found_comps = find_best_matches(query, comps, ["name", "description", "keywords"])
                for c in found_comps:
                    matches.append(f"Component: {c['name']} - {c['description']}")

                # 2. Suche in Detail-Dokumentationen (Guides, Komponenten-Details)
                for key, db in DATABASES.items():
                    if key == "HERO_UI_COMPONENTS": continue
                    found_docs = find_best_matches(query, db, ["topic", "content", "keywords"])
                    for d in found_docs:
                        matches.append(f"Guide ({key.replace('_DB', '')}): {d.get('topic', 'N/A')}\nExcerpt: {d.get('content', '')[:150]}...")

                if matches:
                    result_content.append({"type": "text", "text": "Gefundene Informationen:\n\n" + "\n\n".join(matches[:10])})
                else:
                    result_content.append({"type": "text", "text": f"Keine Ergebnisse für '{query}' gefunden."})

            elif tool_name == "hero_ui.get_component_details":
                c_name = args.get("component_name", "").lower()
                
                # 1. Basis-Info finden
                comps = DATABASES.get("HERO_UI_COMPONENTS", [])
                base_info = next((c for c in comps if c['name'].lower() == c_name), None)
                
                text_output = ""
                
                if base_info:
                    text_output += f"=== {base_info['name']} ===\n"
                    text_output += f"Description: {base_info['description']}\n\n"
                    text_output += f"Usage Example:\n```jsx\n{base_info.get('code_snippet', '')}\n```\n\n"
                
                # 2. Detail-DB finden (z.B. COMPONENTS_BUTTON)
                detail_key = f"COMPONENTS_{c_name.upper()}"
                details = DATABASES.get(detail_key)
                
                if details:
                    text_output += f"--- Detailed Documentation for {c_name} ---\n"
                    for item in details:
                        text_output += f"### {item.get('topic', 'Topic')}\n{item.get('content', '')}\n\n"
                elif not base_info:
                    text_output = f"Komponente '{c_name}' wurde nicht gefunden."
                else:
                    text_output += "\n(Keine tiefergehende Dokumentation verfügbar)"

                result_content.append({"type": "text", "text": text_output})

            elif tool_name == "hero_ui.list_available_components":
                comps = DATABASES.get("HERO_UI_COMPONENTS", [])
                names = sorted([c['name'] for c in comps])
                result_content.append({"type": "text", "text": "Verfügbare Hero UI Komponenten:\n" + ", ".join(names)})

            elif tool_name == "hero_ui.get_design_principles":
                principles = DATABASES.get("DESIGN_PRINCIPLES", [])
                text = "Hero UI Design Principles:\n\n"
                for p in principles:
                    text += f"## {p.get('topic', 'Principle')}\n{p.get('content', '')}\n\n"
                result_content.append({"type": "text", "text": text})

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return create_jsonrpc_response(request.id, {"content": result_content, "isError": False})

        except Exception as e:
             return create_jsonrpc_response(request.id, {"content": [{"type": "text", "text": f"Error executing tool: {str(e)}"}], "isError": True})

    return create_jsonrpc_error(request.id, -32601, f"Method not found: '{request.method}'")

def create_jsonrpc_response(request_id: Union[str, int], result: Any) -> JSONResponse:
    return JSONResponse(content={
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    })

def create_jsonrpc_error(request_id: Union[str, int, None], code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=200, content={ # MCP bevorzugt 200 OK auch bei logischen Fehlern
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message}
    })
