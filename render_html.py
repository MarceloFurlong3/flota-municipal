"""
Genera index.html — Flota Municipal Bahía Blanca
Estados por RI individual guardados en Supabase.
"""
import json

PIN_ADMIN   = 'admin'
SUPA_URL    = 'https://sugkmcdngvtvwzglodkh.supabase.co'
SUPA_KEY    = 'sb_publishable_ZtJOsrwumSdUOPonai0m0A_LhojWgXm'

def generar_html(vehiculos, SERIES, series_activas):
    data_js  = json.dumps(vehiculos, ensure_ascii=False)
    total    = len(vehiculos)
    SCFG_JS  = json.dumps({k: v for k, v in SERIES.items() if k in series_activas}, ensure_ascii=False)
    SACT_JS  = json.dumps(series_activas, ensure_ascii=False)
    PIN_JS   = json.dumps(PIN_ADMIN)

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#0f172a">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>Flota Municipal — Bahía Blanca</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700;800&family=Barlow+Condensed:wght@700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
:root{{--dark:#0f172a;--border:#e4eaf5;--bg:#f1f5f9;--text:#0f172a;--muted:#64748b}}
body{{font-family:'Barlow',sans-serif;background:var(--bg);color:var(--text);overscroll-behavior:none}}

/* HEADER */
.hdr{{background:var(--dark);padding:14px 16px 12px;position:sticky;top:0;z-index:200}}
.hdr-row{{display:flex;align-items:center;gap:8px;margin-bottom:10px}}
.hdr-titulo{{font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:800;color:#fff;letter-spacing:1px;line-height:1;flex:1}}
.hdr-sub{{font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;text-transform:uppercase;margin-top:2px}}
.hdr-badge{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:5px 12px;color:rgba(255,255,255,.8);font-size:12px;font-weight:700;white-space:nowrap}}
.admin-btn{{background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.2);border-radius:8px;color:#fff;padding:6px 10px;font-family:'Barlow',sans-serif;font-size:11px;font-weight:700;cursor:pointer;white-space:nowrap;-webkit-appearance:none;transition:all .2s;flex-shrink:0}}
.sbox{{position:relative}}
.sico{{position:absolute;left:12px;top:50%;transform:translateY(-50%);font-size:15px;pointer-events:none;opacity:.5;color:#fff}}
.sinp{{width:100%;padding:11px 14px 11px 38px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.14);border-radius:12px;color:#fff;font-family:'Barlow',sans-serif;font-size:15px;outline:none;-webkit-appearance:none}}
.sinp::placeholder{{color:rgba(255,255,255,.3);font-size:14px}}
.sinp:focus{{border-color:rgba(255,255,255,.35);background:rgba(255,255,255,.12)}}

/* PILLS */
.pills{{display:flex;gap:7px;overflow-x:auto;padding:10px 16px;scrollbar-width:none;background:#fff;border-bottom:1px solid var(--border);position:sticky;top:90px;z-index:100}}
.pills::-webkit-scrollbar{{display:none}}
.pill{{display:inline-flex;align-items:center;gap:5px;white-space:nowrap;padding:8px 14px;border-radius:99px;border:1.5px solid var(--border);background:#f8fafc;color:var(--muted);font-size:11px;font-weight:700;cursor:pointer;transition:all .15s;flex-shrink:0;min-height:36px;-webkit-appearance:none}}
.pill.sel{{color:#fff;border-color:transparent}}
.cnt{{background:rgba(0,0,0,.12);border-radius:99px;padding:1px 6px;font-size:10px}}
.pill:not(.sel) .cnt{{background:#f0f4f9;color:var(--muted)}}

/* CONTENT */
.content{{padding:12px 14px 110px}}

/* SERIE GRID */
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px}}
.scard{{background:#fff;border-radius:14px;padding:12px;text-align:center;cursor:pointer;border:1px solid var(--border);border-top:3px solid;transition:transform .12s}}
.scard:active{{transform:scale(.96)}}
.scard-ico{{font-size:22px;margin-bottom:4px}}
.scard-n{{font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;line-height:1}}
.scard-lbl{{font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-top:2px}}

/* BUSQUEDA */
.busq-info{{background:#eff6ff;border:1.5px solid #bfdbfe;border-radius:10px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:#1d4ed8;font-weight:700}}

/* SERIE HEADER */
.sec-hdr{{display:flex;align-items:center;gap:10px;margin-bottom:12px;padding:12px 14px;background:#fff;border-radius:12px;border:1px solid var(--border)}}
.sec-ico{{font-size:26px}}
.sec-tit{{font-size:15px;font-weight:800}}
.sec-sub{{font-size:11px;color:var(--muted);margin-top:2px}}

/* MARCA SECTION */
.marca-wrap{{margin-bottom:10px}}
.marca-hdr{{display:flex;align-items:center;gap:10px;padding:11px 14px;border-radius:12px;cursor:pointer;user-select:none;background:var(--dark);color:#fff;transition:opacity .12s}}
.marca-hdr:active{{opacity:.85}}
.marca-logo{{width:34px;height:34px;border-radius:8px;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff;flex-shrink:0}}
.marca-nombre{{flex:1;font-size:13px;font-weight:800;letter-spacing:.3px}}
.marca-n{{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;background:rgba(255,255,255,.15);border-radius:8px;padding:3px 10px;min-width:36px;text-align:center}}
.marca-arrow{{font-size:14px;opacity:.6;transition:transform .2s}}
.marca-wrap.closed .marca-arrow{{transform:rotate(-90deg)}}
.marca-wrap.closed .marca-body{{display:none}}
.marca-body{{padding:6px 0 0 8px}}

/* MODELO ROW */
.mod-row{{display:flex;align-items:center;gap:10px;padding:10px 12px;background:#fff;border-radius:10px;margin-bottom:5px;border:1px solid var(--border);cursor:pointer;box-shadow:0 1px 3px rgba(15,23,42,.04);transition:box-shadow .12s}}
.mod-row:active{{background:#f8fafc}}
.mod-row.open{{border-bottom-left-radius:0;border-bottom-right-radius:0;border-bottom-color:transparent}}
.mod-color{{width:5px;height:32px;border-radius:3px;flex-shrink:0}}
.mod-info{{flex:1;min-width:0}}
.mod-nombre{{font-size:12px;font-weight:800;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.mod-tipo{{font-size:10px;color:var(--muted);margin-top:1px}}
.mod-right{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.mod-n{{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;background:var(--bg);border-radius:7px;padding:3px 9px;min-width:30px;text-align:center}}
.mod-agg{{display:flex;gap:4px;font-size:11px;font-weight:700}}
.mod-agg span{{padding:2px 6px;border-radius:6px}}
.mod-agg .agg-ok{{background:#dcfce7;color:#16a34a}}
.mod-agg .agg-rev{{background:#fef9c3;color:#d97706}}
.mod-agg .agg-baja{{background:#fee2e2;color:#dc2626}}
.mod-arrow{{color:var(--muted);font-size:13px;transition:transform .2s}}
.mod-row.open .mod-arrow{{transform:rotate(90deg)}}

/* VEHÍCULOS LISTA */
.vlista{{display:none;background:#fff;border:1px solid var(--border);border-top:1px solid #f0f4f9;border-bottom-left-radius:10px;border-bottom-right-radius:10px;margin-bottom:5px;margin-top:-5px;overflow:hidden}}
.mod-row.open + .vlista{{display:block}}
.vrow{{display:flex;align-items:center;gap:10px;padding:9px 12px;border-bottom:1px solid #f8fafc}}
.vrow:last-child{{border-bottom:none}}
.vrow.v-baja{{opacity:.5;border-left:3px solid #dc2626}}
.vri-box{{display:flex;flex-direction:column;align-items:center;background:#f0f4f9;border-radius:7px;padding:3px 8px;min-width:44px;text-align:center;flex-shrink:0}}
.vrow.v-baja .vri-box{{background:#fee2e2}}
.vri-s{{font-size:9px;font-weight:700;color:var(--muted);line-height:1}}
.vri-n{{font-family:'Barlow Condensed',sans-serif;font-size:17px;font-weight:800;color:var(--dark);line-height:1.1}}
.vdata{{flex:1;min-width:0}}
.vpat{{font-size:12px;font-weight:700}}
.vrow.v-baja .vpat{{text-decoration:line-through;color:var(--muted)}}
.vtipo{{font-size:9px;color:var(--muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.vdep{{font-size:10px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px}}
.vanio{{font-size:11px;font-weight:700;color:var(--muted);flex-shrink:0}}

/* BOTONES DE ESTADO POR RI (solo admin) */
.vest{{display:none;gap:4px;flex-shrink:0}}
.admin-mode .vest{{display:flex}}
.vebtn{{border:1.5px solid var(--border);border-radius:7px;background:#f8fafc;padding:5px 7px;font-size:13px;cursor:pointer;-webkit-appearance:none;transition:all .12s;line-height:1}}
.vebtn:active{{transform:scale(.9)}}
.vebtn.e-ok.on{{background:#16a34a;border-color:#16a34a}}
.vebtn.e-rev.on{{background:#d97706;border-color:#d97706}}
.vebtn.e-baja.on{{background:#dc2626;border-color:#dc2626}}

/* LOADING */
.loading{{text-align:center;padding:60px 20px;color:var(--muted);font-size:14px;font-weight:700}}
.loading-dot{{display:inline-block;animation:blink 1s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}

/* EMPTY */
.empty{{text-align:center;padding:50px 20px}}
.empty-ico{{font-size:44px;margin-bottom:12px}}
.empty-txt{{font-size:14px;font-weight:700;color:var(--muted)}}

/* BOTTOM BAR */
.btm{{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid var(--border);padding:10px 16px;display:flex;align-items:center;gap:8px;box-shadow:0 -4px 20px rgba(0,0,0,.07);z-index:150}}
.sblk{{text-align:center;flex:1}}
.sn{{font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:800;line-height:1}}
.sn.ok{{color:#16a34a}}.sn.rev{{color:#d97706}}.sn.baja{{color:#dc2626}}
.slbl{{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-top:2px}}
.dvd{{width:1px;height:36px;background:var(--border)}}
.xbtn{{background:var(--dark);color:#fff;border:none;border-radius:10px;padding:10px 14px;font-family:'Barlow',sans-serif;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap;-webkit-appearance:none}}

@media(max-width:380px){{
  .grid{{grid-template-columns:repeat(2,1fr)}}
  .hdr-titulo{{font-size:18px}}
}}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-row">
    <div style="flex:1">
      <div class="hdr-titulo">\U0001f3db️ Flota Municipal</div>
      <div class="hdr-sub">Bahía Blanca — Parque Automotor</div>
    </div>
    <div class="hdr-badge">{total} vehículos</div>
    <button id="admin-btn" class="admin-btn" onclick="toggleAdmin()">\U0001f512</button>
  </div>
  <div class="sbox">
    <span class="sico">\U0001f50d</span>
    <input id="buscar" class="sinp" type="search" autocomplete="off" autocorrect="off"
      spellcheck="false" placeholder="RI, patente, modelo, dependencia...">
  </div>
</div>

<div class="pills" id="pills"></div>
<div class="content" id="content"><div class="loading">Cargando estados<span class="loading-dot">...</span></div></div>

<div class="btm">
  <div class="sblk"><div class="sn ok" id="s-ok">—</div><div class="slbl">✅ Activos</div></div>
  <div class="dvd"></div>
  <div class="sblk"><div class="sn rev" id="s-rev">—</div><div class="slbl">⚠️ Revisar</div></div>
  <div class="dvd"></div>
  <div class="sblk"><div class="sn baja" id="s-baja">—</div><div class="slbl">❌ De baja</div></div>
  <div class="dvd"></div>
  <button class="xbtn" onclick="exportar()">\U0001f4cb CSV</button>
</div>

<script>
const VEH={data_js};
const SCFG={SCFG_JS};
const SACT={SACT_JS};
const PIN={PIN_JS};
const SUPA_URL='{SUPA_URL}';
const SUPA_KEY='{SUPA_KEY}';

let EST={{}};  // {{ ri: {{e:'ok'|'rev'|'baja'|'', fb:timestamp|null}} }}
let isAdmin=sessionStorage.getItem('fleet_admin')==='1';
let serie='TODAS', q='';

// ── Supabase ─────────────────────────────────────────────────
async function cargarEstados(){{
  try{{
    const res=await fetch(SUPA_URL+'/rest/v1/flota_estados?select=*&limit=10000',{{
      headers:{{'apikey':SUPA_KEY,'Authorization':'Bearer '+SUPA_KEY}}
    }});
    const rows=await res.json();
    EST={{}};
    if(Array.isArray(rows))rows.forEach(r=>{{
      EST[r.ri]={{e:r.estado||'',fb:r.fecha_baja?new Date(r.fecha_baja).getTime():null}};
    }});
  }}catch(err){{EST={{}};}}
}}

async function guardarEstado(ri,estado,fb){{
  const body={{
    ri,
    estado:estado||null,
    fecha_baja:fb?new Date(fb).toISOString():null,
    updated_at:new Date().toISOString()
  }};
  try{{
    await fetch(SUPA_URL+'/rest/v1/flota_estados',{{
      method:'POST',
      headers:{{
        'apikey':SUPA_KEY,
        'Authorization':'Bearer '+SUPA_KEY,
        'Content-Type':'application/json',
        'Prefer':'resolution=merge-duplicates'
      }},
      body:JSON.stringify(body)
    }});
  }}catch(err){{}}
}}

// ── Estado helpers ───────────────────────────────────────────
function getEst(ri){{
  const v=EST[ri];
  if(!v)return {{e:'',fb:null}};
  return {{e:v.e||'',fb:v.fb||null}};
}}

function isBaja(ri){{return getEst(ri).e==='baja';}}

function diasBaja(ri){{
  const fb=getEst(ri).fb;
  if(!fb)return null;
  return Math.floor((Date.now()-fb)/(24*60*60*1000));
}}

// ── Admin ────────────────────────────────────────────────────
function toggleAdmin(){{
  if(isAdmin){{
    if(!confirm('¿Salir del modo administrador?'))return;
    isAdmin=false;
    sessionStorage.removeItem('fleet_admin');
  }}else{{
    const pin=prompt('\U0001f512 PIN de administrador:');
    if(pin===null)return;
    if(pin!==PIN){{alert('PIN incorrecto');return;}}
    isAdmin=true;
    sessionStorage.setItem('fleet_admin','1');
  }}
  updAdminUI();
  render();
}}

function updAdminUI(){{
  const btn=document.getElementById('admin-btn');
  if(!btn)return;
  if(isAdmin){{
    btn.textContent='\U0001f513 ADMIN';
    btn.style.background='rgba(22,163,74,.8)';
    btn.style.borderColor='#16a34a';
    document.body.classList.add('admin-mode');
  }}else{{
    btn.textContent='\U0001f512';
    btn.style.background='rgba(255,255,255,.1)';
    btn.style.borderColor='rgba(255,255,255,.2)';
    document.body.classList.remove('admin-mode');
  }}
}}

// ── Filtrado ─────────────────────────────────────────────────
function kmod(v){{return v.serie+'|'+(v.marca||'SIN MARCA')+'|'+(v.modelo_norm||'Sin modelo');}}

function visibles(lista){{
  return lista.filter(v=>isAdmin||!isBaja(v.ri));
}}

// ── Pills ────────────────────────────────────────────────────
const pillsEl=document.getElementById('pills');

function mkPill(s,lbl,n,col){{
  const b=document.createElement('button');
  b.className='pill'+(s===serie?' sel':'');
  b.id='pill-'+s;
  if(s===serie)b.style.background=col||'#0f172a';
  b.innerHTML=lbl+(n!==undefined?` <span class="cnt">${{n}}</span>`:'');
  b.onclick=()=>selS(s,col);
  pillsEl.appendChild(b);
}}

function updPills(){{
  const vis=visibles(VEH);
  pillsEl.innerHTML='';
  mkPill('TODAS','\U0001f697 Todas',vis.length,'#0f172a');
  SACT.forEach(s=>{{
    const c=SCFG[s];if(!c)return;
    mkPill(s,c.emoji+' '+c.label,vis.filter(v=>v.serie===s).length,c.color);
  }});
}}

function selS(s){{
  serie=s;q='';document.getElementById('buscar').value='';
  render();
}}

document.getElementById('buscar').addEventListener('input',e=>{{
  q=e.target.value.toLowerCase().trim();
  if(q)serie='TODAS';
  render();
}});

// ── Render ────────────────────────────────────────────────────
function render(){{
  updPills();
  let lista=visibles(VEH);
  if(serie!=='TODAS')lista=lista.filter(v=>v.serie===serie);
  if(q)lista=lista.filter(v=>(v.ri+' '+v.modelo+' '+v.patente+' '+v.dep+' '+v.tipo+' '+(v.modelo_norm||'')).toLowerCase().includes(q));
  const el=document.getElementById('content');
  if(!lista.length){{
    el.innerHTML='<div class="empty"><div class="empty-ico">\U0001f50d</div><div class="empty-txt">Sin resultados'+(q?' para "'+q+'"':'')+'</div></div>';
    return;
  }}
  let html='';
  if(q){{
    html+='<div class="busq-info">\U0001f50d '+lista.length+' resultado'+(lista.length!==1?'s':'')+' para "'+q+'"</div>';
    html+=renderMM(lista);
  }}else if(serie==='TODAS'){{
    html+='<div class="grid">';
    SACT.forEach(s=>{{
      const c=SCFG[s];if(!c)return;
      const n=visibles(VEH).filter(v=>v.serie===s).length;
      html+=`<div class="scard" style="border-top-color:${{c.color}}" onclick="selS('${{s}}')">
        <div class="scard-ico">${{c.emoji}}</div>
        <div class="scard-n" style="color:${{c.color}}">${{n}}</div>
        <div class="scard-lbl">${{c.label}}</div>
      </div>`;
    }});
    html+='</div>';
    html+=renderMM(lista);
  }}else{{
    const c=SCFG[serie];
    const marcas=new Set(lista.map(v=>v.marca));
    if(c)html+=`<div class="sec-hdr"><span class="sec-ico">${{c.emoji}}</span><div>
      <div class="sec-tit">${{c.label}}</div>
      <div class="sec-sub">${{lista.length}} vehículos · ${{marcas.size}} marcas</div>
    </div></div>`;
    html+=renderMM(lista);
  }}
  el.innerHTML=html;
}}

function renderMM(lista){{
  const gMarca={{}};
  lista.forEach(v=>{{
    const km=v.serie+'|'+(v.marca||'SIN MARCA');
    if(!gMarca[km])gMarca[km]={{serie:v.serie,marca:v.marca||'SIN MARCA',veh:[]}};
    gMarca[km].veh.push(v);
  }});
  const marcasOrd=Object.entries(gMarca).sort((a,b)=>b[1].veh.length-a[1].veh.length);

  return marcasOrd.map(([km,gm])=>{{
    const c=SCFG[gm.serie]||{{color:'#64748b',emoji:'\U0001f697'}};
    const gMod={{}};
    gm.veh.forEach(v=>{{
      const k=kmod(v);
      if(!gMod[k])gMod[k]={{mod:v.modelo_norm||'Sin modelo',tipo:v.tipo,veh:[]}};
      gMod[k].veh.push(v);
    }});
    const modsOrd=Object.entries(gMod).sort((a,b)=>b[1].veh.length-a[1].veh.length);

    const modCards=modsOrd.map(([k,gmod])=>{{
      // Contadores por RI dentro del modelo
      let nOk=0,nRev=0,nBaja=0;
      gmod.veh.forEach(v=>{{
        const e=getEst(v.ri).e;
        if(e==='ok')nOk++;
        else if(e==='rev')nRev++;
        else if(e==='baja')nBaja++;
      }});

      const aggHtml=[
        nOk?`<span class="agg-ok">✅${{nOk}}</span>`:'',
        nRev?`<span class="agg-rev">⚠️${{nRev}}</span>`:'',
        nBaja?`<span class="agg-baja">❌${{nBaja}}</span>`:''
      ].join('');

      const anios=gmod.veh.map(v=>parseInt(v.anio)).filter(Boolean);
      const aMin=anios.length?Math.min(...anios):null;
      const aMax=anios.length?Math.max(...anios):null;
      const anioStr=aMin?(aMin===aMax?String(aMin):aMin+'-'+aMax):'';
      const subtitulo=(gmod.tipo||'')+(anioStr?' · '+anioStr:'');

      const vrows=gmod.veh.sort((a,b)=>a.ri.localeCompare(b.ri)).map(v=>{{
        const est=getEst(v.ri);
        const esBaja=est.e==='baja';
        const dias=esBaja?diasBaja(v.ri):null;
        const diasTxt=isAdmin&&esBaja&&dias!==null?` <span style="font-size:9px;color:#dc2626">(${{dias}}d)</span>`:'';
        const riEsc=v.ri.replace(/'/g,"\\'");
        return `<div class="vrow${{esBaja?' v-baja':''}}" data-ri="${{v.ri}}">
  <div class="vri-box"><span class="vri-s">${{v.ri[0]}}</span><span class="vri-n">${{v.ri.slice(1)}}</span></div>
  <div class="vdata">
    <div class="vpat">${{v.patente||'Sin patente'}}${{diasTxt}}</div>
    <div class="vtipo">${{v.tipo||''}}</div>
    <div class="vdep">${{v.dep||'—'}}</div>
  </div>
  <div class="vest">
    <button class="vebtn e-ok${{est.e==='ok'?' on':''}}" onclick="setVehE(event,'${{riEsc}}','ok')" title="Activo">✅</button>
    <button class="vebtn e-rev${{est.e==='rev'?' on':''}}" onclick="setVehE(event,'${{riEsc}}','rev')" title="Revisar">⚠️</button>
    <button class="vebtn e-baja${{est.e==='baja'?' on':''}}" onclick="setVehE(event,'${{riEsc}}','baja')" title="De baja">❌</button>
  </div>
  <span class="vanio">${{v.anio||'—'}}</span>
</div>`;
      }}).join('');

      return `<div class="mod-row" onclick="togMod(this)">
  <div class="mod-color" style="background:${{c.color}}"></div>
  <div class="mod-info">
    <div class="mod-nombre">${{gmod.mod}}</div>
    <div class="mod-tipo">${{subtitulo}}</div>
  </div>
  <div class="mod-right">
    <div class="mod-agg">${{aggHtml}}</div>
    <span class="mod-n">${{gmod.veh.length}}</span>
    <span class="mod-arrow">›</span>
  </div>
</div>
<div class="vlista" style="display:none">${{vrows}}</div>`;
    }}).join('');

    const initials=gm.marca.split(' ').map(w=>w[0]||'').join('').substring(0,3);
    return `<div class="marca-wrap closed" data-km="${{km.replace(/"/g,'&quot;')}}">
  <div class="marca-hdr" style="background:${{c.color}}" onclick="togMarca('${{km.replace(/'/g,"\\\\'")}}')" >
    <div class="marca-logo">${{initials}}</div>
    <div class="marca-nombre">${{gm.marca}}</div>
    <div class="marca-n">${{gm.veh.length}}</div>
    <span class="marca-arrow">›</span>
  </div>
  <div class="marca-body">${{modCards}}</div>
</div>`;
  }}).join('');
}}

// ── Interacciones ────────────────────────────────────────────
function togMarca(km){{
  document.querySelectorAll('.marca-wrap').forEach(el=>{{
    if(el.dataset.km===km)el.classList.toggle('closed');
  }});
}}

function togMod(row){{
  const wasOpen=row.classList.contains('open');
  row.classList.toggle('open');
  const next=row.nextElementSibling;
  if(next&&next.classList.contains('vlista')){{
    next.style.display=wasOpen?'none':'block';
  }}
}}

async function setVehE(e,ri,val){{
  e.stopPropagation();
  if(!isAdmin)return;
  const curr=getEst(ri);
  const newE=curr.e===val?'':val;
  const fb=newE==='baja'?Date.now():(newE?curr.fb:null);

  // Optimistic update
  EST[ri]={{e:newE,fb}};

  // Guardar en Supabase
  guardarEstado(ri,newE,fb);

  // Actualizar UI del vrow
  const vrow=e.target.closest('.vrow');
  if(vrow){{
    vrow.querySelectorAll('.vebtn').forEach(b=>b.classList.remove('on'));
    if(newE)vrow.querySelector('.e-'+newE)?.classList.add('on');
    vrow.classList.toggle('v-baja',newE==='baja');
  }}

  // Actualizar aggregate del mod-row
  const vlista=e.target.closest('.vlista');
  if(vlista){{
    const modRow=vlista.previousElementSibling;
    if(modRow){{
      const ris=[...vlista.querySelectorAll('.vrow')].map(r=>r.dataset.ri);
      let nOk=0,nRev=0,nBaja=0;
      ris.forEach(r=>{{
        const ev=getEst(r).e;
        if(ev==='ok')nOk++;
        else if(ev==='rev')nRev++;
        else if(ev==='baja')nBaja++;
      }});
      const agg=modRow.querySelector('.mod-agg');
      if(agg)agg.innerHTML=[
        nOk?`<span class="agg-ok">✅${{nOk}}</span>`:'',
        nRev?`<span class="agg-rev">⚠️${{nRev}}</span>`:'',
        nBaja?`<span class="agg-baja">❌${{nBaja}}</span>`:''
      ].join('');
    }}
  }}

  updSum();

  // Si se marcó como baja y no es admin, esconder al hacer re-render
  if(newE==='baja'&&!isAdmin)render();
}}

function updSum(){{
  let ok=0,rev=0,baja=0;
  VEH.forEach(v=>{{
    const e=getEst(v.ri).e;
    if(e==='ok')ok++;
    else if(e==='rev')rev++;
    else if(e==='baja')baja++;
  }});
  document.getElementById('s-ok').textContent=ok;
  document.getElementById('s-rev').textContent=rev;
  document.getElementById('s-baja').textContent=isAdmin?baja:0;
}}

// ── Export CSV ───────────────────────────────────────────────
function exportar(){{
  const esc=x=>'"'+(x||'').toString().replace(/"/g,'""')+'"';
  let csv='RI,Serie,Tipo,Modelo,Marca,Año,Patente,Dependencia,Estado,Dias_de_baja\\n';
  const sorted=[...VEH].sort((a,b)=>a.serie.localeCompare(b.serie)||a.ri.localeCompare(b.ri));
  sorted.forEach(v=>{{
    const est=getEst(v.ri);
    const estado=est.e==='ok'?'Activo':est.e==='rev'?'Revisar':est.e==='baja'?'De baja':'Sin clasificar';
    const dias=est.e==='baja'&&est.fb?Math.floor((Date.now()-est.fb)/(24*60*60*1000)):'';
    csv+=esc(v.ri)+','+esc(v.serie)+','+esc(v.tipo)+','+esc(v.modelo_norm)+','+esc(v.marca)+','+esc(v.anio)+','+esc(v.patente)+','+esc(v.dep)+','+esc(estado)+','+esc(dias)+'\\n';
  }});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv;charset=utf-8'}}));
  a.download='flota-'+new Date().toISOString().slice(0,10)+'.csv';
  a.click();
}}

// ── Init ─────────────────────────────────────────────────────
async function init(){{
  updAdminUI();
  await cargarEstados();
  render();
  updSum();
}}
init();
</script>
</body>
</html>'''
