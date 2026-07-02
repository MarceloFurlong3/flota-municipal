"""
Genera index.html con agrupamiento MARCA → MODELO normalizado.
"""
import json

def generar_html(vehiculos, SERIES, series_activas):
    data_js = json.dumps(vehiculos, ensure_ascii=False)
    total = len(vehiculos)
    SCFG_JS = json.dumps({k: v for k, v in SERIES.items() if k in series_activas}, ensure_ascii=False)
    SACT_JS = json.dumps(series_activas, ensure_ascii=False)

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
.hdr-row{{display:flex;align-items:center;margin-bottom:10px}}
.hdr-titulo{{font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:800;color:#fff;letter-spacing:1px;line-height:1;flex:1}}
.hdr-sub{{font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;text-transform:uppercase;margin-top:2px}}
.hdr-badge{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:5px 12px;color:rgba(255,255,255,.8);font-size:12px;font-weight:700;white-space:nowrap}}
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

/* MARCA SECTION — nivel 1 */
.marca-wrap{{margin-bottom:10px}}
.marca-hdr{{
  display:flex;align-items:center;gap:10px;padding:11px 14px;
  border-radius:12px;cursor:pointer;user-select:none;
  background:var(--dark);color:#fff;
  transition:opacity .12s;
}}
.marca-hdr:active{{opacity:.85}}
.marca-logo{{
  width:34px;height:34px;border-radius:8px;
  background:rgba(255,255,255,.15);
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:800;color:#fff;flex-shrink:0;
}}
.marca-nombre{{flex:1;font-size:13px;font-weight:800;letter-spacing:.3px}}
.marca-n{{
  font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;
  background:rgba(255,255,255,.15);border-radius:8px;padding:3px 10px;min-width:36px;text-align:center;
}}
.marca-arrow{{font-size:14px;opacity:.6;transition:transform .2s}}
.marca-wrap.closed .marca-arrow{{transform:rotate(-90deg)}}
.marca-wrap.closed .marca-body{{display:none}}
.marca-body{{padding:6px 0 0 8px}}

/* MODELO ROW — nivel 2 */
.mod-row{{
  display:flex;align-items:center;gap:10px;padding:10px 12px;
  background:#fff;border-radius:10px;margin-bottom:5px;
  border:1px solid var(--border);cursor:pointer;
  box-shadow:0 1px 3px rgba(15,23,42,.04);
  transition:box-shadow .12s;
}}
.mod-row:active{{background:#f8fafc}}
.mod-row.open{{border-bottom-left-radius:0;border-bottom-right-radius:0;border-bottom-color:transparent}}
.mod-color{{width:5px;height:32px;border-radius:3px;flex-shrink:0}}
.mod-info{{flex:1;min-width:0}}
.mod-nombre{{font-size:12px;font-weight:800;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.mod-tipo{{font-size:10px;color:var(--muted);margin-top:1px}}
.mod-right{{display:flex;align-items:center;gap:7px;flex-shrink:0}}
.mod-n{{
  font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;
  background:var(--bg);border-radius:7px;padding:3px 9px;min-width:30px;text-align:center;
}}
.mod-est{{font-size:16px}}
.mod-arrow{{color:var(--muted);font-size:13px;transition:transform .2s}}
.mod-row.open .mod-arrow{{transform:rotate(90deg)}}

/* ESTADO BOTONES */
.est-row{{
  display:flex;gap:5px;padding:7px 10px 9px;
  background:#fff;border:1px solid var(--border);border-top:none;
  border-bottom-left-radius:10px;border-bottom-right-radius:10px;
  margin-bottom:5px;
}}
.ebtn{{flex:1;padding:8px 4px;border:1.5px solid var(--border);border-radius:9px;background:#f8fafc;color:var(--muted);font-family:'Barlow',sans-serif;font-size:11px;font-weight:700;cursor:pointer;text-align:center;transition:all .12s;-webkit-appearance:none}}
.ebtn:active{{transform:scale(.95)}}
.e-ok.on{{background:#16a34a;color:#fff;border-color:#16a34a}}
.e-rev.on{{background:#d97706;color:#fff;border-color:#d97706}}
.e-baja.on{{background:#dc2626;color:#fff;border-color:#dc2626}}

/* VEHÍCULOS LISTA */
.vlista{{
  display:none;background:#fff;
  border:1px solid var(--border);border-top:1px solid #f0f4f9;
  border-bottom-left-radius:10px;border-bottom-right-radius:10px;
  margin-bottom:5px;margin-top:-5px;overflow:hidden;
}}
.mod-row.open + .est-row + .vlista{{display:block}}
.mod-row.open + .vlista{{display:block}}
.vrow{{display:flex;align-items:center;gap:10px;padding:9px 12px;border-bottom:1px solid #f8fafc}}
.vrow:last-child{{border-bottom:none}}
.vri-box{{display:flex;flex-direction:column;align-items:center;background:#f0f4f9;border-radius:7px;padding:3px 8px;min-width:44px;text-align:center;flex-shrink:0}}
.vri-s{{font-size:9px;font-weight:700;color:var(--muted);line-height:1}}
.vri-n{{font-family:'Barlow Condensed',sans-serif;font-size:17px;font-weight:800;color:var(--dark);line-height:1.1}}
.vdata{{flex:1;min-width:0}}
.vpat{{font-size:12px;font-weight:700}}
.vtipo{{font-size:9px;color:var(--muted);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.vdep{{font-size:10px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:1px}}
.vanio{{font-size:11px;font-weight:700;color:var(--muted);flex-shrink:0}}

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
  </div>
  <div class="sbox">
    <span class="sico">\U0001f50d</span>
    <input id="buscar" class="sinp" type="search" autocomplete="off" autocorrect="off"
      spellcheck="false" placeholder="RI, patente, modelo, dependencia...">
  </div>
</div>

<div class="pills" id="pills"></div>
<div class="content" id="content"></div>

<div class="btm">
  <div class="sblk"><div class="sn ok" id="s-ok">0</div><div class="slbl">✅ Activos</div></div>
  <div class="dvd"></div>
  <div class="sblk"><div class="sn rev" id="s-rev">0</div><div class="slbl">⚠️ Revisar</div></div>
  <div class="dvd"></div>
  <div class="sblk"><div class="sn baja" id="s-baja">0</div><div class="slbl">❌ De baja</div></div>
  <div class="dvd"></div>
  <button class="xbtn" onclick="exportar()">\U0001f4cb Exportar</button>
</div>

<script>
const VEH={data_js};
const SCFG={SCFG_JS};
const SACT={SACT_JS};
const SK='flota_bhi_v3';
let EST=JSON.parse(localStorage.getItem(SK)||'{{}}');
let serie='TODAS', q='';

// ── Pills ────────────────────────────────────────────────────
const pillsEl=document.getElementById('pills');
function mkPill(s,lbl,n,col){{
  const b=document.createElement('button');
  b.className='pill'+(s==='TODAS'?' sel':'');
  b.id='pill-'+s;
  if(s==='TODAS')b.style.background='#0f172a';
  b.innerHTML=lbl+(n!==undefined?` <span class="cnt">${{n}}</span>`:'');
  b.onclick=()=>selS(s,col);
  pillsEl.appendChild(b);
}}
mkPill('TODAS','\U0001f697 Todas',VEH.length,'#0f172a');
SACT.forEach(s=>{{
  const c=SCFG[s];if(!c)return;
  mkPill(s,c.emoji+' '+c.label,VEH.filter(v=>v.serie===s).length,c.color);
}});

function selS(s,col){{
  serie=s;q='';document.getElementById('buscar').value='';
  document.querySelectorAll('.pill').forEach(p=>{{p.classList.remove('sel');p.style.background=''}});
  const p=document.getElementById('pill-'+s);
  if(p){{p.classList.add('sel');p.style.background=col||'#0f172a'}}
  render();
}}

document.getElementById('buscar').addEventListener('input',e=>{{
  q=e.target.value.toLowerCase().trim();
  if(q){{serie='TODAS';document.querySelectorAll('.pill').forEach(p=>{{p.classList.remove('sel');p.style.background=''}})}}
  render();
}});

// ── Render ────────────────────────────────────────────────────
function render(){{
  let lista=VEH;
  if(serie!=='TODAS')lista=lista.filter(v=>v.serie===serie);
  if(q)lista=lista.filter(v=>(v.ri+' '+v.modelo+' '+v.patente+' '+v.dep+' '+v.tipo+' '+v.marca+' '+v.modelo_norm).toLowerCase().includes(q));
  const el=document.getElementById('content');
  if(!lista.length){{
    el.innerHTML='<div class="empty"><div class="empty-ico">\U0001f50d</div><div class="empty-txt">Sin resultados para "'+q+'"</div></div>';
    return;
  }}
  let html='';
  if(q){{
    html+='<div class="busq-info">\U0001f50d '+lista.length+' resultado'+(lista.length!==1?'s':'')+' para "'+q+'"</div>';
    html+=renderMarcaModelo(lista,null);
  }}else if(serie==='TODAS'){{
    html+='<div class="grid">';
    SACT.forEach(s=>{{
      const c=SCFG[s];if(!c)return;
      const n=VEH.filter(v=>v.serie===s).length;
      html+=`<div class="scard" style="border-top-color:${{c.color}}" onclick="selS('${{s}}','${{c.color}}')">
        <div class="scard-ico">${{c.emoji}}</div>
        <div class="scard-n" style="color:${{c.color}}">${{n}}</div>
        <div class="scard-lbl">${{c.label}}</div>
      </div>`;
    }});
    html+='</div>';
    html+=renderMarcaModelo(lista,null);
  }}else{{
    const c=SCFG[serie];
    const marcas=new Set(lista.map(v=>v.marca));
    if(c)html+=`<div class="sec-hdr"><span class="sec-ico">${{c.emoji}}</span><div>
      <div class="sec-tit">${{c.label}}</div>
      <div class="sec-sub">${{lista.length}} vehículos · ${{marcas.size}} marcas</div>
    </div></div>`;
    html+=renderMarcaModelo(lista,c);
  }}
  el.innerHTML=html;
  bindMarcas();
}}

function renderMarcaModelo(lista, cfg){{
  // Nivel 1: agrupar por serie+marca
  const gMarca={{}};
  lista.forEach(v=>{{
    const km=v.serie+'|'+(v.marca||'SIN MARCA');
    if(!gMarca[km])gMarca[km]={{serie:v.serie,marca:v.marca||'SIN MARCA',veh:[]}};
    gMarca[km].veh.push(v);
  }});
  const marcasOrd=Object.entries(gMarca).sort((a,b)=>b[1].veh.length-a[1].veh.length);

  return marcasOrd.map(([km,gm])=>{{
    const c=SCFG[gm.serie]||{{color:'#64748b',emoji:'\U0001f697'}};

    // Nivel 2: agrupar por modelo_norm
    const gMod={{}};
    gm.veh.forEach(v=>{{
      const kmod=km+'|'+(v.modelo_norm||'Sin modelo');
      if(!gMod[kmod])gMod[kmod]={{mod:v.modelo_norm||'Sin modelo',tipo:v.tipo,veh:[]}};
      gMod[kmod].veh.push(v);
    }});
    const modsOrd=Object.entries(gMod).sort((a,b)=>b[1].veh.length-a[1].veh.length);

    const modCards=modsOrd.map(([kmod,gmod])=>{{
      const est=EST[kmod]||'';
      const ico=est==='ok'?'✅':est==='rev'?'⚠️':est==='baja'?'❌':'○';
      const kattr=kmod.replace(/&/g,'&amp;').replace(/"/g,'&quot;');
      return `<div class="mod-row" data-kmod="${{kattr}}" onclick="togMod(this)">
  <div class="mod-color" style="background:${{c.color}}"></div>
  <div class="mod-info">
    <div class="mod-nombre">${{gmod.mod}}</div>
    <div class="mod-tipo">${{gmod.tipo||''}}</div>
  </div>
  <div class="mod-right">
    <span class="mod-est">${{ico}}</span>
    <span class="mod-n">${{gmod.veh.length}}</span>
    <span class="mod-arrow">›</span>
  </div>
</div>
<div class="est-row" style="display:none">
  <button class="ebtn e-ok ${{est==='ok'?'on':''}}" onclick="setE(event,'ok')">✅ Activo</button>
  <button class="ebtn e-rev ${{est==='rev'?'on':''}}" onclick="setE(event,'rev')">⚠️ Revisar</button>
  <button class="ebtn e-baja ${{est==='baja'?'on':''}}" onclick="setE(event,'baja')">❌ De baja</button>
</div>
<div class="vlista" style="display:none">
  ${{gmod.veh.sort((a,b)=>a.ri.localeCompare(b.ri)).map(v=>`
  <div class="vrow">
    <div class="vri-box"><span class="vri-s">${{v.ri[0]}}</span><span class="vri-n">${{v.ri.slice(1)}}</span></div>
    <div class="vdata">
      <div class="vpat">${{v.patente||'Sin patente'}}</div>
      <div class="vtipo">${{v.tipo||''}}</div>
      <div class="vdep">${{v.dep||'—'}}</div>
    </div>
    <span class="vanio">${{v.anio||'—'}}</span>
  </div>`).join('')}}
</div>`;
    }}).join('');

    const initials=gm.marca.split(' ').map(w=>w[0]||'').join('').substring(0,3);
    return `<div class="marca-wrap" data-km="${{km.replace(/"/g,'&quot;')}}">
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

function bindMarcas(){{}}

function togMarca(km){{
  document.querySelectorAll('.marca-wrap').forEach(el=>{{
    if(el.dataset.km===km)el.classList.toggle('closed');
  }});
}}

function togMod(row){{
  const wasOpen=row.classList.contains('open');
  row.classList.toggle('open');
  const estRow=row.nextElementSibling;
  const vlista=estRow?.nextElementSibling;
  if(estRow&&estRow.classList.contains('est-row'))estRow.style.display=wasOpen?'none':'flex';
  if(vlista&&vlista.classList.contains('vlista'))vlista.style.display=wasOpen?'none':'block';
}}

function setE(e,val){{
  e.stopPropagation();
  const row=e.target.closest('.est-row');
  const modRow=row?.previousElementSibling;
  const k=modRow?.dataset?.kmod;
  if(!k)return;
  EST[k]=EST[k]===val?'':val;
  localStorage.setItem(SK,JSON.stringify(EST));
  updSum();
  row?.querySelectorAll('.ebtn').forEach(b=>b.classList.remove('on'));
  const cls={{'ok':'e-ok','rev':'e-rev','baja':'e-baja'}}[EST[k]];
  if(cls)row?.querySelector('.'+cls)?.classList.add('on');
  if(modRow?.classList.contains('mod-row')){{
    const ico=modRow.querySelector('.mod-est');
    if(ico)ico.textContent=EST[k]==='ok'?'✅':EST[k]==='rev'?'⚠️':EST[k]==='baja'?'❌':'○';
  }}
}}

function updSum(){{
  let ok=0,rev=0,baja=0;
  Object.values(EST).forEach(e=>{{if(e==='ok')ok++;else if(e==='rev')rev++;else if(e==='baja')baja++}});
  document.getElementById('s-ok').textContent=ok;
  document.getElementById('s-rev').textContent=rev;
  document.getElementById('s-baja').textContent=baja;
}}

function exportar(){{
  const gs={{}};
  VEH.forEach(v=>{{
    const k=v.serie+'|'+(v.marca||'SIN MARCA')+'|'+(v.modelo_norm||'Sin modelo');
    if(!gs[k])gs[k]={{marca:v.marca,mod:v.modelo_norm,serie:v.serie,tipo:v.tipo,veh:[]}};
    gs[k].veh.push(v);
  }});
  let txt='FLOTA MUNICIPAL BAHIA BLANCA\\n';
  txt+='Generado: '+new Date().toLocaleString('es-AR')+'\\n\\n';
  [['ok','ACTIVOS'],['rev','A REVISAR'],['baja','DE BAJA'],['','SIN CLASIFICAR']].forEach(([est,tit])=>{{
    const items=Object.entries(gs).filter(([k])=>(EST[k]||'')===est);
    if(!items.length)return;
    const total=items.reduce((s,[,g])=>s+g.veh.length,0);
    txt+='=== '+tit+' ('+total+' unidades / '+items.length+' modelos) ===\\n';
    items.sort((a,b)=>a[1].marca.localeCompare(b[1].marca)||a[1].mod.localeCompare(b[1].mod));
    items.forEach(([k,g])=>{{
      txt+='  '+g.marca+' '+g.mod+' — '+g.veh.length+' unidad'+(g.veh.length!==1?'es':'')+' | RIs: '+g.veh.map(v=>v.ri).join(', ')+'\\n';
    }});
    txt+='\\n';
  }});
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([txt],{{type:'text/plain;charset=utf-8'}}));
  a.download='flota-'+new Date().toISOString().slice(0,10)+'.txt';
  a.click();
}}

render();updSum();
</script>
</body>
</html>'''
