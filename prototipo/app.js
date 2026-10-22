'use strict';
const $=id=>document.getElementById(id);
const fmt=(x,n=3)=>x==null?'—':Number(x).toLocaleString('es-CO',{minimumFractionDigits:n,maximumFractionDigits:n});
const pct=x=>fmt(x*100,1)+' %';
const label=x=>DATA.labels[x]||x.replaceAll('_',' ');
const cell=x=>{const e=document.createElement('td');e.textContent=x;return e;};
const el=(tag,cls,text)=>{const e=document.createElement(tag);e.className=cls||'';if(text!=null)e.textContent=text;return e;};
// Escala única para todos los cortes; el cero nunca se trunca.
const apMax=Math.ceil(Math.max(...DATA.intervalos.filter(r=>r.metrica==='ap').map(r=>r.superior),...DATA.metricas.map(r=>r.ap))*10)/10;
function stack(id,yes,total){const c=$(id);c.replaceChildren();const a=el('div','segment detected'),b=el('div','segment other');a.style.width=(100*yes/total)+'%';b.style.width=(100*(total-yes)/total)+'%';c.append(a,b);}
function pairedRow(container,name,a,b,right,mode,highlight=false,lo=null,hi=null){
 const row=el('div','chart-row'+(highlight?' highlighted':'')),label=el('span','chart-label',name),track=el('div','plot-track');
 const scale=mode==='ap'?apMax:1;
 if(mode==='bar'){const bar=el('div','context-bar');bar.style.width=(100*a)+'%';track.append(bar);}
 else{const line=el('div','range');const lower=lo==null?Math.min(a,b):lo,upper=hi==null?Math.max(a,b):hi;line.style.left=(100*lower/scale)+'%';line.style.width=(100*(upper-lower)/scale)+'%';track.append(line);const dot=el('div','dot');dot.style.left=(100*a/scale)+'%';track.append(dot);if(mode!=='ap'){const second=el('div','dot observed-dot');second.style.left=(100*b/scale)+'%';track.append(second);}}
 row.append(label,track,el('span','chart-value',right));$(container).append(row);
}
function renderStory(p){
 $('takeaway').textContent=`Se detecta el ${fmt(p.sensibilidad*100,1)} % de los retiros; el ${fmt((1-p.precision)*100,1)} % de las alertas no corresponde a un retiro`;
 $('alertCaption').textContent=`${fmt(p.tp,0)} de ${fmt(p.tp+p.fp,0)} corresponden a retiros`;
 $('recallCaption').textContent=`${fmt(p.tp,0)} de ${fmt(p.eventos,0)} se detectan`;
 stack('alertStack',p.tp,p.tp+p.fp);stack('recallStack',p.tp,p.eventos);
 $('alertLabels').textContent=`Azul: ${fmt(p.tp,0)} alertas correctas · Gris: ${fmt(p.fp,0)} falsas alertas`;
 $('recallLabels').textContent=`Azul: ${fmt(p.tp,0)} retiros detectados · Gris: ${fmt(p.fn,0)} no detectados`;
 $('apChart').replaceChildren();
 for(const r of DATA.metricas.filter(r=>r.corte===p.corte)){
  const c=DATA.intervalos.find(x=>x.corte===p.corte&&x.modelo===r.modelo&&x.metrica==='ap');
  pairedRow('apChart',DATA.nombres[r.modelo]+(r.principal?' · principal':''),r.ap,r.ap,`${fmt(r.ap)} [${fmt(c.inferior)}; ${fmt(c.superior)}]`,'ap',r.principal,c.inferior,c.superior);
 }
 $('apScale').textContent=`AP · de 0 a ${fmt(apMax,1)} · Valores entre corchetes: intervalo del 95 %`;
 $('calChart').replaceChildren();const bins=DATA.calibracion[String(p.corte)];const largest=bins.reduce((a,b)=>a.n>b.n?a:b);
 $('calTakeaway').textContent=`En el grupo más numeroso (${fmt(largest.n,0)} inscripciones), la probabilidad media es ${pct(largest.probabilidad_media)} y se observa ${pct(largest.frecuencia_retiro)} de retiros.`;
 for(const r of bins)pairedRow('calChart',`${fmt(r.intervalo*10,0)}–${fmt((r.intervalo+1)*10,0)} % · n=${fmt(r.n,0)}`,r.probabilidad_media,r.frecuencia_retiro,`${pct(r.probabilidad_media)} / ${pct(r.frecuencia_retiro)}`,'pair',r===largest);
 const top=DATA.shap[String(p.corte)][0];$('globalHeadline').textContent=`${label(top.predictor)} presenta la mayor contribución media en la muestra explicada`;
}
function bars(target,items,signed,values){
  const container=$(target);container.replaceChildren();const max=Math.max(...items.map(x=>Math.abs(x.valor)),1e-12);
  for(const item of items){const row=document.createElement('div');row.className='contrib'+(!signed&&item!==items[0]?' secondary':'');const name=document.createElement('span');name.textContent=label(item.predictor);
    if(values){const observed=document.createElement('span');observed.className='observed';const v=values[item.predictor];observed.textContent='Valor observado: '+(v==null?'sin dato':fmt(v,Number.isInteger(v)?0:3));name.append(observed);}
    const track=document.createElement('div');track.className='track'+(signed?' signed':'');const bar=document.createElement('div');bar.className='bar'+(signed&&item.valor<0?' negative':'');const limit=signed?50:100;const width=Math.min(limit,limit*(Math.abs(item.valor)/max));bar.style.width=width+'%';if(signed)bar.style.left=(item.valor<0?50-width:50)+'%';track.append(bar);const value=document.createElement('span');value.textContent=(signed&&item.valor>0?'+':'')+fmt(item.valor*100,2)+' pp';row.append(name,track,value);container.append(row);}
}
function renderCase(){const cut=$('cut').value,p=DATA.principales.find(x=>x.corte===Number(cut));const r=DATA.casos[cut][Number($('case').value)];
 const alert=r.probabilidad>p.umbral;$('caseHeadline').textContent=alert?(r.retiro?'Una alerta que coincidió con un retiro posterior':'Una alerta no siempre anticipa un retiro'):(r.retiro?'Un retiro que quedó por debajo del umbral de alerta':'Un caso sin alerta y sin retiro posterior');
 $('caseInfo').textContent=`Probabilidad: ${pct(r.probabilidad)}. Referencia SHAP: ${pct(r.base)}. Regla congelada: ${r.probabilidad>p.umbral?'alerta':'sin alerta'}. Desenlace observado: ${r.retiro?'retiro posterior':'sin retiro posterior'}.`;
 bars('local',r.contribuciones.slice(0,8),true,r.valores);const rest=r.contribuciones.slice(8).reduce((a,b)=>a+b.valor,0);$('remainder').textContent=`Suma de las contribuciones restantes: ${fmt(rest*100,2)} pp. Referencia + todas las contribuciones = ${pct(r.base+r.contribuciones.reduce((a,b)=>a+b.valor,0))}.`;
}
function renderEDA(){const cut=Number($('cut').value), group=$('group').value;
 const rows=DATA.exploracion.filter(r=>r.corte===cut&&r.variable===group);$('eda').replaceChildren();$('edaChart').replaceChildren();
 const n=rows.reduce((a,r)=>a+r.n,0), events=rows.reduce((a,r)=>a+r.retiros,0);
 $('edaPopulation').textContent=`Día ${cut}: ${fmt(n,0)} inscripciones elegibles; ${fmt(events,0)} retiros posteriores (${pct(events/n)}).`;
 $('edaNote').textContent=group==='imd_band'?'IMD describe privación del área de residencia, no los recursos individuales. Las bandas bajas indican mayor privación; «No disponible» identifica datos ausentes.':group==='disability'?'Las categorías reflejan el registro disponible; no constituyen una valoración clínica.':'Se conservan las categorías originales de OULAD; los porcentajes deben leerse junto con los tamaños de los grupos.';
 for(const r of rows){const tr=document.createElement('tr');const level=group==='disability'?({Y:'Con discapacidad registrada',N:'Sin discapacidad registrada'}[r.nivel]||r.nivel):r.nivel==='55<='?'55 o más':r.nivel;[level,fmt(r.n,0),fmt(r.retiros,0),pct(r.retiros/r.n)].forEach(x=>tr.append(cell(x)));$('eda').append(tr);pairedRow('edaChart',level,r.retiros/r.n,0,`${pct(r.retiros/r.n)} · n=${fmt(r.n,0)}`,'bar');}
}
function render(){const cut=$('cut').value,p=DATA.principales.find(x=>x.corte===Number(cut));$('title').textContent=`Día ${cut} · Principal: ${DATA.nombres[p.modelo]}`;
 $('population').textContent=`Prueba: ${p.inscripciones} inscripciones, ${p.personas} personas y ${p.eventos} retiros posteriores. Prevalencia: ${pct(p.prevalencia)}.`;
 $('cards').replaceChildren();for(const [name,val] of [['Precisión',p.precision],['Sensibilidad',p.sensibilidad],['Inscripciones alertadas',p.proporcion_alertas],['Umbral fijo',p.umbral]]){const item=document.createElement('div');item.className='card';item.textContent=name;const b=document.createElement('b');b.textContent=pct(val);item.append(b);$('cards').append(item);}
 const interval=DATA.intervalos.find(x=>x.corte===p.corte&&x.modelo===p.modelo&&x.metrica==='ap');$('ci').textContent=`AP: ${fmt(p.ap)}; intervalo del 95 %: [${fmt(interval.inferior)}; ${fmt(interval.superior)}], a partir de 2.000 remuestreos por personas.`;
 $('errors').textContent=`Alertas correctas: ${p.tp}; falsas alertas: ${p.fp}; retiros no detectados: ${p.fn}. Anticipación mediana entre alertas correctas: ${fmt(p.anticipacion_tp.mediana,1)} días.`;
 $('models').replaceChildren();for(const row of DATA.metricas.filter(x=>x.corte===p.corte)){const tr=document.createElement('tr');if(row.principal)tr.className='principal';[DATA.nombres[row.modelo],fmt(row.ap),fmt(row.roc_auc),fmt(row.brier,4),fmt(row.f1)].forEach(x=>tr.append(cell(x)));$('models').append(tr);}
 $('calibration').replaceChildren();for(const row of DATA.calibracion[cut]){const tr=document.createElement('tr');[`${fmt(row.intervalo/10,1)} a ${fmt((row.intervalo+1)/10,1)}`,fmt(row.n,0),pct(row.probabilidad_media),pct(row.frecuencia_retiro)].forEach(x=>tr.append(cell(x)));$('calibration').append(tr);}
 bars('global',DATA.shap[cut].map(x=>({predictor:x.predictor,valor:x.media_absoluta})),false);
 $('case').replaceChildren();DATA.casos[cut].forEach((r,i)=>{const op=document.createElement('option');op.value=i;op.textContent=`Caso ${r.caso}`;$('case').append(op);});renderCase();renderEDA();renderStory(p);
}
$('cut').addEventListener('change',render);$('case').addEventListener('change',renderCase);$('group').addEventListener('change',renderEDA);render();
