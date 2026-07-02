"""
Normalización de modelos de vehículos para clasificación mecánica.
Extrae marca y modelo base, eliminando specs de motor y trim levels.
"""
import re

# Marcas de dos palabras
MARCAS_DOS_PALABRAS = [
    'JOHN DEERE', 'MERCEDES BENZ', 'MASSEY FERGUSON', 'NEW HOLLAND',
    'DEUTZ AGRALE', 'LAND ROVER', 'ALFA ROMEO',
]

# Alias de marcas (normalizar nombre)
ALIAS_MARCA = {
    r'^VW\b': 'VOLKSWAGEN',
    r'^MB\b': 'MERCEDES BENZ',
}

# Palabras de trim/versión que se eliminan del modelo
TRIM = {
    'GL', 'GLS', 'GLD', 'LS', 'LT', 'LTZ', 'SL', 'SE', 'RL', 'TL',
    'EX', 'ELX', 'LX', 'DLX', 'GTL', 'GTX', 'SER', 'MOD',
    'DRIVE', 'ACTIVE', 'JOY', 'WIND', 'PACK', 'COMFORT', 'CONFORT',
    'AUTHENTIQUE', 'EXPRESSION', 'PRIVILEGE', 'PRESTIGE', 'STEPWAY',
    'HIGHLINE', 'COMFORTLINE', 'TRENDLINE', 'SPORT', 'LUXURY',
    'MT', 'AT', 'CVT', 'MAN', 'AUT',
    'SD', 'MPI', 'TN', 'FSI', 'TSI', 'TDI', 'HDI', 'JTD', 'CRDI',
    'RLD', 'RLD.', 'MSI', 'GLE',       # engine codes
    'N', 'C', 'L', 'S', 'T',           # single-letter trim codes
    'BREAK', 'MULTISPACE', 'PATAGONICA', 'CONFORT', 'MY23',
}


def _aplicar_alias(m):
    """Normaliza alias de marca (ej: VW → VOLKSWAGEN)."""
    for pat, real in ALIAS_MARCA.items():
        m = re.sub(pat, real, m, count=1)
    return m.strip()


def normalizar_marca(modelo_raw):
    m = _aplicar_alias(modelo_raw.strip().upper())
    for b in MARCAS_DOS_PALABRAS:
        if m.startswith(b):
            return b
    partes = m.split()
    return partes[0] if partes else 'SIN MARCA'


def _limpiar_specs(m):
    """Elimina specs de motor, trim codes y códigos de chasis."""
    # "I.9L" OCR → "1.9L" — el I puede ser 1 mal escaneado
    m = re.sub(r'\bI\.(\d+)', r'1.\1', m)
    # Engine displacement: 1.4, 1,4, 2.0, 1.9L, 1.3 GSE, etc.
    m = re.sub(r'\s+\d+[,\.]\d+\s*(?:[A-Z]{0,5})?\s*(?:\d+V)?\s*(?:MT|AT|CVT)?\b', ' ', m)
    # "8V", "16V" sueltos
    m = re.sub(r'\s+\d+V\b', ' ', m)
    # Códigos: L813, C3L, J8S, 557T y similares (letra+dígitos o dígitos+letra)
    m = re.sub(r'\s+[A-Z]\d+[A-Z0-9]*\b', ' ', m)
    m = re.sub(r'\s+\d+[A-Z]\b', ' ', m)
    # MOT., SER.
    m = re.sub(r'\s+(?:MOT\.?|SER\.?)\b', ' ', m)
    # /42, /35 (variantes de chasis)
    m = re.sub(r'/\w+', '', m)
    # Puntos y comas sueltos al final
    m = re.sub(r'[\.,\s]+$', '', m)
    return re.sub(r'\s{2,}', ' ', m).strip()


def normalizar_modelo_nombre(modelo_raw, marca):
    m = _aplicar_alias(modelo_raw.strip().upper())
    m = m.replace('"', '').replace("'", '').strip()

    # Quitar la marca del inicio
    if m.startswith(marca.upper()):
        m = m[len(marca.upper()):].strip()

    # Limpiar specs técnicas
    m = _limpiar_specs(m)

    # Quitar trim words del final (múltiples pasadas)
    for _ in range(8):
        words = m.strip().split()
        if not words:
            break
        last = words[-1].rstrip('.,')
        if last in TRIM:
            words.pop()
            m = ' '.join(words)
        else:
            break

    # Limpiar y limitar a 3 palabras significativas
    words = [w for w in m.strip().split() if w and w not in {'.', ',', '-'}]
    result = ' '.join(words[:3]).strip()

    return result or '(base)'


def aplicar_normalizacion(vehiculos):
    """Agrega campos marca y modelo_norm a cada vehículo."""
    for v in vehiculos:
        modelo_raw = v.get('modelo', '') or v.get('tipo', '') or ''
        tipo_raw   = v.get('tipo', '') or ''

        marca = normalizar_marca(modelo_raw) if modelo_raw else 'SIN MARCA'
        mod_n = normalizar_modelo_nombre(modelo_raw, marca)

        # Para tipos cortos sin modelo específico, usar el tipo como descripción
        if not v.get('modelo') and tipo_raw:
            marca = tipo_raw.split()[0].upper() if tipo_raw else 'SIN MARCA'
            mod_n = tipo_raw

        v['marca']      = marca
        v['modelo_norm'] = f"{marca} {mod_n}".strip() if mod_n and mod_n != '(base)' else marca

    return vehiculos


# ── Test rápido ──────────────────────────────────────────────────
if __name__ == '__main__':
    casos = [
        'FIAT UNO 1,4 8V',
        'VOLKSWAGEN POLO CLASSIC I.9L SD',
        'VW POLO MSI MT',
        'CHEVROLET CORSA CLASSIC 1,4 N LT',
        'CHEVROLET CORSA CLASSIC 1,4 N LS',
        'CHEVROLET CORSA GL 1.4',
        'CHEVROLET CORSA II 1,8 GL',
        'CHEVROLET PRISMA 1.4 N LT',
        'RENAULT 12 TL',
        'RENAULT KANGOO BREAK RLD.',
        'RENAULT CLIO RL 557T MOT. C3L',
        'VOLKSWAGEN VOYAGE 1,6',
        'VOLKSWAGEN GOL 1.6 L',
        'JOHN DEERE 670 G',
        'CATERPILLAR 120H',
        'MASSEY FERGUSON 265 S',
        'MERCEDES BENZ L1215/42',
        'Peugeot MX 408 Active 1,6',
        'FIAT CRONOS DRIVE 1.3 GSE MY23',
        'HUSQVARNA 450',
        'STIHL MS 250',
    ]
    print(f'{"ORIGINAL":<40} {"MARCA":<20} {"NORM":<30}')
    print('-' * 95)
    for c in casos:
        m = normalizar_marca(c)
        n = normalizar_modelo_nombre(c, m)
        full = f"{m} {n}".strip()
        print(f'{c:<40} {m:<20} {full:<30}')
