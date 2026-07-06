# 🏛️ Flota Municipal — Bahía Blanca

Sistema de gestión del parque automotor municipal de Bahía Blanca.
App web estática, mobile-first, sin backend — funciona desde GitHub Pages.

🔗 **Live:** https://marcelofurlong3.github.io/flota-municipal/

---

## Qué hace

- Visualiza todos los vehículos municipales organizados por **serie**, **marca** y **modelo**
- Búsqueda en tiempo real por RI, patente, modelo o dependencia
- **Modo admin** (PIN protegido) para clasificar modelos como Activo / Revisar / De baja
- Estados guardados en `localStorage` del navegador — sin servidor
- Export a **CSV** con estado actual de toda la flota
- Funciona en celular igual que en escritorio

---

## Series del parque automotor

| Serie | Tipo | Color |
|-------|------|-------|
| A | Autos | Azul |
| B | Ambulancias | Rojo |
| C | Camiones | Violeta |
| E | Equipos | Celeste |
| K | Furgones | Gris |
| M | Eq. Menores | Verde |
| N | Motos | Ámbar |
| O | Omnibus | Púrpura |
| T | Camionetas | Naranja |
| V | Maq. Vial | Marrón |
| W | Autos W | Pizarra |

---

## Estructura del repo

```
flota-municipal/
├── data.json          ← Base de datos de vehículos (generada externamente)
├── normalizar.py      ← Limpieza y normalización de datos
├── render_html.py     ← Genera index.html completo desde data.json
├── build.py           ← Script principal: normaliza → renderiza → guarda
└── index.html         ← App final (generada, no editar a mano)
```

---

## Cómo generar el sitio

```bash
# Desde C:\Users\furlo\flota-municipal\
python build.py
```

Eso normaliza los datos, genera `index.html` y lo deja listo para publicar.

Para deployar:
```bash
git add -A
git commit -m "update: nueva versión de flota"
git push origin master
```
GitHub Pages publica automáticamente desde `master`.

---

## Cómo funciona el modo admin

- El botón 🔒 en el header abre el login
- PIN actual: `admin` (cambiar en `render_html.py` → `PIN_ADMIN`)
- En modo admin se puede marcar cada modelo como:
  - ✅ Activo — operativo
  - ⚠️ Revisar — requiere atención
  - ❌ De baja — fuera de servicio
- Los modelos "de baja" se ocultan en la vista pública
- Después de 30 días de baja aparece el botón 🗑️ para borrar definitivamente

---

## Scripts auxiliares (locales, no en repo)

| Script | Qué hace |
|--------|----------|
| `generar_word.py` | Genera orden de service en Word (.docx) con kits sugeridos |
| `buscar_ris.py` | Consulta rápida en terminal por lista de RIs |

Ubicación local: `C:\Users\furlo\flota-municipal\`

---

## Roadmap — Módulo de Service (próximo)

El depósito recibe RIs a service y necesita saber qué filtros/kits comprar por modelo
para hacer una sola compra en lugar de pedir de a uno.

### Qué se va a construir

- [ ] Pestaña "Service" por RI — historial de intervenciones (fecha, km/hs, tipo)
- [ ] Tabla de filtros por modelo:
  - Filtro de aceite (N° de parte)
  - Filtro de aire primario / secundario
  - Filtro de combustible
  - Aceite (tipo + capacidad en litros)
  - Filtro de transmisión (si aplica)
- [ ] Frecuencia de service recomendada (km o meses)
- [ ] Alerta de service próximo
- [ ] Cruce automático: RIs que entran → modelos → kits necesarios → cantidad total a comprar

### Estructura de datos planeada

```json
// service.json
{
  "TECTOR 240": {
    "aceite": { "tipo": "15W40", "litros": 12, "parte": "HF6" },
    "filtro_aire": { "primario": "AF25557", "secundario": "AF25558" },
    "filtro_combustible": "FF5613",
    "intervalo_km": 10000
  }
}
```

### Fuentes de datos de repuestos
- TecDoc (API paga, referencia europea)
- Portales de fabricante: IVECO, Caterpillar, New Holland, Mercedes Benz
- Proveedores locales: Dieselgas, Champion, Purolator, Mann-Filter
- Equivalencias: RockAuto (US)

---

## Stack

- **Frontend:** HTML + CSS + JS vanilla (sin frameworks)
- **Generador:** Python 3
- **Deploy:** GitHub Pages (estático, gratis)
- **Persistencia:** `localStorage` del navegador
- **Sin backend, sin base de datos, sin dependencias externas**

---

## Contexto

Proyecto para el taller mecánico municipal de Bahía Blanca.
Desarrollado por Marcelo Furlong — 2026.
