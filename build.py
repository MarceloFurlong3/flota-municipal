import json

with open('C:/Users/furlo/flota-municipal/data.json', encoding='utf-8') as f:
    vehiculos = json.load(f)

data_js = json.dumps(vehiculos, ensure_ascii=False)
total = len(vehiculos)

SERIES = {
    'A': {'label': 'Autos',       'emoji': '\U0001f697', 'color': '#2563eb'},
    'B': {'label': 'Ambulancias', 'emoji': '\U0001f691', 'color': '#dc2626'},
    'C': {'label': 'Camiones',    'emoji': '\U0001f69b', 'color': '#7c3aed'},
    'E': {'label': 'Equipos',     'emoji': '⚙️', 'color': '#0891b2'},
    'K': {'label': 'Furgones K',  'emoji': '\U0001f4e6', 'color': '#64748b'},
    'M': {'label': 'Eq. Menores', 'emoji': '\U0001f33f', 'color': '#16a34a'},
    'N': {'label': 'Motos',       'emoji': '\U0001f3cd️', 'color': '#d97706'},
    'O': {'label': 'Omnibus',     'emoji': '\U0001f68c', 'color': '#9333ea'},
    'T': {'label': 'Camionetas',  'emoji': '\U0001f6fb', 'color': '#ea580c'},
    'V': {'label': 'Maq. Vial',   'emoji': '\U0001f3d7️', 'color': '#854d0e'},
    'W': {'label': 'Autos W',     'emoji': '\U0001f697', 'color': '#475569'},
}

series_activas = [s for s in SERIES if any(v['serie'] == s for v in vehiculos)]
SCFG_JS = json.dumps({k: v for k, v in SERIES.items() if k in series_activas}, ensure_ascii=False)
SACT_JS = json.dumps(series_activas, ensure_ascii=False)

html = f'''<!DOCTYPE html>
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
.hdr-brand{{flex:1}}
.hdr-titulo{{font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:800;color:#fff;letter-spacing:1px;line-height:1}}
.hdr-sub{{font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;text-transform:uppercase;margin-top:2px}}
.hdr-badge{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:5px 12px;color:rgba(255,255,255,.8);font-size:12px;font-weight:700}}
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

/* SERIES GRID */
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:16px}}
.scard{{background:#fff;border-radius:14px;padding:12px;text-align:center;cursor:pointer;border:1px solid var(--border);border-top:3px solid;transition:transform .12s}}
.scard:active{{transform:scale(.96)}}
.scard-ico{{font-size:22px;margin-bottom:4px}}
.scard-n{{font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;line-height:1}}
.scard-lbl{{font-size:9px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-top:2px}}

/* BUSQUEDA */
.busq-info{{background:#eff6ff;border:1.5px solid #bfdbfe;border-radius:10px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:#1d4ed8;font-weight:700}}

/* SECTION HEADER (dentro de serie) */
.sec-hdr{{display:flex;align-items:center;gap:10px;margin-bottom:12px;padding:12px 14px;background:#fff;border-radius:12px;border:1px solid var(--border)}}
.sec-ico{{font-size:26px}}
.sec-tit{{font-size:15px;font-weight:800}}
.sec-sub{{font-size:11px;color:var(--muted);margin-top:2px}}

/* TIPO HEADER — nivel 1 (MOTONIVELADORA, TRACTOR...) */
.tipo-hdr{{
  display:flex;align-items:center;gap:10px;
  padding:11px 14px;margin-top:12px;margin-bottom:4px;
  background:linear-gradient(90deg,var(--tipo-color,#0f172a) 0%,transparent 100%);
  border-radius:10px;cursor:pointer;user-select:none;
}}
.tipo-hdr:first-child{{margin-top:0}}
.tipo-dot{{width:8px;height:8px;border-radius:50%;background:rgba(255,255,255,.7);flex-shrink:0}}
.tipo-nombre{{flex:1;font-size:12px;font-weight:800;color:#fff;text-transform:uppercase;letter-spacing:.8px}}
.tipo-n{{font-family:'Barlow Condensed',sans-serif;font-size:17px;font-weight:800;color:rgba(255,255,255,.9);background:rgba(0,0,0,.2);border-radius:7px;padding:2px 9px;min-width:30px;text-align:center}}
.tipo-arrow{{color:rgba(255,255,255,.6);font-size:14px;transition:transform .2s;display:inline-block}}
.tipo-wrap.closed .tipo-arrow{{transform:rotate(-90deg)}}
.tipo-wrap.closed .tipo-body{{display:none}}
.tipo-body{{padding-left:8px;margin-bottom:8px}}

/* MODELO CARD — nivel 2 */
.mcard{{background:#fff;border-radius:12px;margin-bottom:6px;border:1px solid var(--border);overflow:hidden;box-shadow:0 1px 3px rgba(15,23,42,.04)}}
.mhdr{{display:flex;align-items:center;gap:10px;padding:11px 13px;cursor:pointer;user-select:none;-webkit-user-select:none}}
.mhdr:active{{background:#f8fafc}}
.mcolor-bar{{width:4px;height:36px;border-radius:2px;flex-shrink:0}}
.minfo{{flex:1;min-width:0}}
.mnombre{{font-size:12px;font-weight:800;color:var(--text);line-height:1.3}}
.mnombre.sin-modelo{{color:var(--muted);font-style:italic;font-weight:600}}
.mright{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.mn{{font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:800;background:var(--bg);border-radius:8px;padding:3px 9px;min-width:32px;text-align:center;line-height:1.2}}
.mest{{font-size:17px}}
.marrow{{color:var(--muted);font-size:14px;transition:transform .2s;display:inline-block}}
.mcard.open .marrow{{transform:rotate(90deg)}}

/* ESTADO BOTONES */
.est-row{{display:flex;gap:5px;padding:7px 11px 9px;border-top:1px solid #f0f4f9}}
.ebtn{{flex:1;padding:8px 4px;border:1.5px solid var(--border);border-radius:9px;background:#f8fafc;color:var(--muted);font-family:'Barlow',sans-serif;font-size:11px;font-weight:700;cursor:pointer;text-align:center;transition:all .12s;-webkit-appearance:none}}
.ebtn:active{{transform:scale(.95)}}
.e-ok.on{{background:#16a34a;color:#fff;border-color:#16a34a}}
.e-rev.on{{background:#d97706;color:#fff;border-color:#d97706}}
.e-baja.on{{background:#dc2626;color:#fff;border-color:#dc2626}}

/* VEHÍCULOS LISTA */
.vlista{{display:none;border-top:1px solid #f0f4f9}}
.mcard.open .vlista{{display:block}}
.vrow{{display:flex;align-items:center;gap:10px;padding:9px 13px;border-bottom:1px solid #f8fafc}}
.vrow:last-child{{border-bottom:none}}
.vri{{font-family:'Barlow Condensed',sans-serif;font-size:13px;font-weight:800;background:#f0f4f9;border-radius:7px;padding:3px 8px;white-space:nowrap;color:var(--dark)}}
.vdata{{flex:1;min-width:0}}
.vpat{{font-size:12px;font-weight:700}}
.vdep{{font-size:10px;color:var(--muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
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
  .tipo-nombre{{font-size:11px}}
}}
</style>
</head>
<body>

<div class="hdr">
  <div class="hdr-row">
    <div class="hdr-brand">
      <div class="hdr-titulo">\U0001f3db️ Flota Municipal</div>
      <div class="hdr-sub">Bahía Blanca — Taller Central</div>
    </div>
    <div class="hdr-badge">{total} vehículos</div>
  </div>
  <div class="sbox">
    <span class="sico">\U0001f50d</span>
    <input id="buscar" class="sinp" type="search" autocomplete="off" autocorrect="off"
      spellcheck="false" placeholder="Buscar RI, modelo, patente, dependencia...">
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
const SK='flota_bhi_v2';
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

// ── Búsqueda ─────────────────────────────────────────────────
document.getElementById('buscar').addEventListener('input',e=>{{
  q=e.target.value.toLowerCase().trim();
  if(q){{serie='TODAS';document.querySelectorAll('.pill').forEach(p=>{{p.classList.remove('sel');p.style.background=''}})}}
  render();
}});

// ── Render principal ──────────────────────────────────────────
function render(){{
  let lista=VEH;
  if(serie!=='TODAS')lista=lista.filter(v=>v.serie===serie);
  if(q)lista=lista.filter(v=>(v.ri+' '+v.modelo+' '+v.patente+' '+v.dep+' '+v.tipo).toLowerCase().includes(q));
  const el=document.getElementById('content');
  if(!lista.length){{
    el.innerHTML='<div class="empty"><div class="empty-ico">\U0001f50d</div><div class="empty-txt">Sin resultados para "'+q+'"</div></div>';
    return;
  }}
  let html='';
  if(q){{
    html+='<div class="busq-info">\U0001f50d '+lista.length+' resultado'+(lista.length!==1?'s':'')+' para "'+q+'"</div>';
    html+=renderDosNiveles(lista,null);
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
    html+=renderDosNiveles(lista,null);
  }}else{{
    const c=SCFG[serie];
    const tipos=new Set(lista.map(v=>v.tipo||'Sin tipo').filter(Boolean));
    if(c)html+=`<div class="sec-hdr"><span class="sec-ico">${{c.emoji}}</span><div>
      <div class="sec-tit">${{c.label}}</div>
      <div class="sec-sub">${{lista.length}} vehículos · ${{tipos.size}} tipos</div>
    </div></div>`;
    html+=renderDosNiveles(lista,c);
  }}
  el.innerHTML=html;
  bindToggleTipo();
}}

// ── Dos niveles: TIPO → MODELO ────────────────────────────────
function renderDosNiveles(lista, cfg){{
  // Nivel 1: agrupar por serie+tipo
  const porTipo={{}};
  lista.forEach(v=>{{
    const tipo=(v.tipo||'Sin tipo').trim();
    const ks=v.serie+'|'+tipo;
    if(!porTipo[ks])porTipo[ks]={{serie:v.serie,tipo,veh:[]}};
    porTipo[ks].veh.push(v);
  }});

  // Ordenar tipos por cantidad desc
  const tiposOrds=Object.entries(porTipo).sort((a,b)=>b[1].veh.length-a[1].veh.length);

  return tiposOrds.map(([ks,gt])=>{{
    const c=SCFG[gt.serie]||{{color:'#64748b'}};
    const color=c.color;

    // Nivel 2: dentro del tipo, agrupar por modelo
    const porMod={{}};
    gt.veh.forEach(v=>{{
      const mod=(v.modelo||'Sin modelo especificado').trim();
      const km=ks+'|'+mod;
      if(!porMod[km])porMod[km]={{mod,veh:[]}};
      porMod[km].veh.push(v);
    }});
    const modsOrds=Object.entries(porMod).sort((a,b)=>b[1].veh.length-a[1].veh.length);

    const modCards=modsOrds.map(([km,gm])=>{{
      const est=EST[km]||'';
      const ico=est==='ok'?'✅':est==='rev'?'⚠️':est==='baja'?'❌':'○';
      const kj=JSON.stringify(km);
      const sinMod=gm.mod==='Sin modelo especificado';
      return `<div class="mcard">
  <div class="mhdr" onclick="togM(this.parentElement,${{kj}})">
    <div class="mcolor-bar" style="background:${{color}}"></div>
    <div class="minfo">
      <div class="mnombre${{sinMod?' sin-modelo':''}}">${{gm.mod}}</div>
    </div>
    <div class="mright">
      <span class="mest">${{ico}}</span>
      <span class="mn">${{gm.veh.length}}</span>
      <span class="marrow">›</span>
    </div>
  </div>
  <div class="est-row">
    <button class="ebtn e-ok ${{est==='ok'?'on':''}}" onclick="setE(event,${{kj}},'ok')">✅ Activo</button>
    <button class="ebtn e-rev ${{est==='rev'?'on':''}}" onclick="setE(event,${{kj}},'rev')">⚠️ Revisar</button>
    <button class="ebtn e-baja ${{est==='baja'?'on':''}}" onclick="setE(event,${{kj}},'baja')">❌ De baja</button>
  </div>
  <div class="vlista">
    ${{gm.veh.map(v=>`
    <div class="vrow">
      <span class="vri">${{v.ri}}</span>
      <div class="vdata"><div class="vpat">${{v.patente||'Sin patente'}}</div><div class="vdep">${{v.dep||'—'}}</div></div>
      <span class="vanio">${{v.anio||'—'}}</span>
    </div>`).join('')}}
  </div>
</div>`;
    }}).join('');

    return `<div class="tipo-wrap" data-ks="${{ks.replace(/"/g,'&quot;')}}">
  <div class="tipo-hdr" style="--tipo-color:${{color}}" onclick="togTipo('${{ks.replace(/'/g,"\\\\'")}}')">
    <div class="tipo-dot"></div>
    <div class="tipo-nombre">${{gt.tipo}}</div>
    <div class="tipo-n">${{gt.veh.length}}</div>
    <span class="tipo-arrow">›</span>
  </div>
  <div class="tipo-body">${{modCards}}</div>
</div>`;
  }}).join('');
}}

function bindToggleTipo(){{}}

function togTipo(ks){{
  const els=document.querySelectorAll('.tipo-wrap');
  for(let el of els){{
    if(el.dataset.ks===ks){{el.classList.toggle('closed');return}}
  }}
}}

function togM(card){{card.classList.toggle('open')}}

function setE(e,k,val){{
  e.stopPropagation();
  EST[k]=EST[k]===val?'':val;
  localStorage.setItem(SK,JSON.stringify(EST));
  updSum();
  const card=e.target.closest('.mcard');if(!card)return;
  card.querySelectorAll('.ebtn').forEach(b=>b.classList.remove('on'));
  const cls={{'ok':'e-ok','rev':'e-rev','baja':'e-baja'}}[EST[k]];
  if(cls)card.querySelector('.'+cls)?.classList.add('on');
  const mestEl=card.querySelector('.mest');
  if(mestEl)mestEl.textContent=EST[k]==='✅'?'✅':EST[k]==='ok'?'✅':EST[k]==='rev'?'⚠️':EST[k]==='baja'?'❌':'○';
}}

function updSum(){{
  let ok=0,rev=0,baja=0;
  Object.values(EST).forEach(e=>{{if(e==='ok')ok++;else if(e==='rev')rev++;else if(e==='baja')baja++}});
  document.getElementById('s-ok').textContent=ok;
  document.getElementById('s-rev').textContent=rev;
  document.getElementById('s-baja').textContent=baja;
}}

function exportar(){{
  // Recopilar datos por estado
  const grupos={{}};
  VEH.forEach(v=>{{
    const tipo=(v.tipo||'Sin tipo').trim();
    const mod=(v.modelo||'Sin modelo').trim();
    const km=v.serie+'|'+tipo+'|'+mod;
    if(!grupos[km])grupos[km]={{tipo,mod,serie:v.serie,veh:[]}};
    grupos[km].veh.push(v);
  }});
  let txt='FLOTA MUNICIPAL - BAHIA BLANCA\n';
  txt+='Generado: '+new Date().toLocaleString('es-AR')+'\n\n';
  [['ok','ACTIVOS'],['rev','A REVISAR'],['baja','DE BAJA'],['','SIN CLASIFICAR']].forEach(([est,tit])=>{{
    const items=Object.entries(grupos).filter(([k])=>(EST[k]||'')===est);
    if(!items.length)return;
    const total=items.reduce((s,[,g])=>s+g.veh.length,0);
    txt+='=== '+tit+' ('+items.length+' modelos / '+total+' unidades) ===\n';
    items.sort((a,b)=>a[1].tipo.localeCompare(b[1].tipo));
    items.forEach(([k,g])=>{{
      txt+='  ['+g.tipo+'] '+g.mod+' — '+g.veh.length+' unidad'+(g.veh.length!==1?'es':'')+'\n';
      txt+='    RIs: '+g.veh.map(v=>v.ri).join(', ')+'\n';
    }});
    txt+='\n';
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

with open('C:/Users/furlo/flota-municipal/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'OK — {len(html)//1024} KB')
