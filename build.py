import json, sys
sys.path.insert(0, 'C:/Users/furlo/flota-municipal')
from normalizar import aplicar_normalizacion
from render_html import generar_html

with open('C:/Users/furlo/flota-municipal/data.json', encoding='utf-8') as f:
    vehiculos = json.load(f)

vehiculos = aplicar_normalizacion(vehiculos)

SERIES = {
    'A': {'label': 'Autos',        'emoji': '\U0001f697', 'color': '#2563eb'},
    'B': {'label': 'Ambulancias',  'emoji': '\U0001f691', 'color': '#dc2626'},
    'C': {'label': 'Camiones',     'emoji': '\U0001f69b', 'color': '#7c3aed'},
    'E': {'label': 'Equipos',      'emoji': '⚙️', 'color': '#0891b2'},
    'K': {'label': 'Furgones K',   'emoji': '\U0001f4e6', 'color': '#64748b'},
    'M': {'label': 'Eq. Menores',  'emoji': '\U0001f33f', 'color': '#16a34a'},
    'N': {'label': 'Motos',        'emoji': '\U0001f3cd️', 'color': '#d97706'},
    'O': {'label': 'Omnibus',      'emoji': '\U0001f68c', 'color': '#9333ea'},
    'T': {'label': 'Camionetas',   'emoji': '\U0001f6fb', 'color': '#ea580c'},
    'V': {'label': 'Maq. Vial',    'emoji': '\U0001f3d7️', 'color': '#854d0e'},
    'W': {'label': 'Autos W',      'emoji': '\U0001f697', 'color': '#475569'},
}

series_activas = [s for s in SERIES if any(v['serie'] == s for v in vehiculos)]

html = generar_html(vehiculos, SERIES, series_activas)

with open('C:/Users/furlo/flota-municipal/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'OK — {len(html)//1024} KB — {len(vehiculos)} vehiculos')
