// Verifica datos y controles con un DOM mínimo; no sustituye inspección visual en navegador.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(__dirname+'/OULAD.html','utf8');
const htmlIds=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
assert.equal(new Set(htmlIds).size,htmlIds.length,'Identificadores HTML duplicados');
class Element{
 constructor(){this.children=[];this.style={};this.value='';this.textContent='';this.handlers={};}
 append(...items){this.children.push(...items);if(this.value===''&&items[0]?.value!=='')this.value=String(items[0]?.value??'');}
 replaceChildren(){this.children=[];this.value='';}
 addEventListener(name,fn){this.handlers[name]=fn;}
}
const ids={};const document={getElementById(id){assert(htmlIds.includes(id),'Falta elemento HTML: '+id);return ids[id]??=(new Element());},createElement(){return new Element();}};
document.getElementById('cut').value='7';
document.getElementById('group').value='age_band';
const context=vm.createContext({document,console});
const data=fs.readFileSync(__dirname+'/datos.js','utf8');
assert(!data.includes('id_student'));vm.runInContext(data,context);vm.runInContext(fs.readFileSync(__dirname+'/app.js','utf8'),context);
let tested=0;
for(const cut of ['7','14','28','42','56']){
 ids.cut.value=cut;ids.cut.handlers.change();assert(ids.title.textContent.includes('Día '+cut));
 assert.equal(ids.models.children.length,7);assert.equal(ids.case.children.length,100);assert.equal(ids.cards.children.length,4);
 assert.equal(ids.apChart.children.length,7);assert(ids.calChart.children.length>0);
 assert(!ids.takeaway.textContent.includes('NaN'));
 for(const id of ['alertStack','recallStack']){const widths=ids[id].children.map(e=>parseFloat(e.style.width));assert(Math.abs(widths.reduce((a,b)=>a+b,0)-100)<1e-9);}
 for(const id of ['apChart','calChart'])for(const row of ids[id].children){for(const mark of row.children[1].children){if(mark.style.left)assert(parseFloat(mark.style.left)>=0&&parseFloat(mark.style.left)<=100);if(mark.style.width)assert(parseFloat(mark.style.width)>=0&&parseFloat(mark.style.width)<=100);}}
 for(const group of ['age_band','disability','imd_band','region']){ids.group.value=group;ids.group.handlers.change();assert(ids.eda.children.length>0);assert(!ids.edaPopulation.textContent.includes('NaN'));}
 for(let i=0;i<100;i++){ids.case.value=String(i);ids.case.handlers.change();assert(ids.caseInfo.textContent.includes('Probabilidad:'));assert.equal(ids.local.children.length,8);assert(!ids.remainder.textContent.includes('NaN'));
  for(const row of ids.local.children){assert(row.children[0].children[0].textContent.startsWith('Valor observado:'));const bar=row.children[1].children[0];const width=parseFloat(bar.style.width),left=parseFloat(bar.style.left);assert(width>=0&&width<=50);assert(left>=0&&left+width<=100.00001);if(bar.className.includes('negative'))assert(Math.abs(left+width-50)<1e-8);else assert.equal(left,50);}
  tested++;}
}
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];assert.equal(scripts.length,2);scripts.forEach(s=>new vm.Script(s[1]));assert(!html.includes('<script src='));
const result={correcto:true,cortes:5,casos_probados:tested,consultas_exploratorias:20,barras_con_cero_central:true,graficos_narrativos:true,identificadores_html_verificados:true,archivo_autonomo:true,identificadores_exportados:false,
 limite:'Prueba de funciones y eventos con DOM mínimo; revisión visual y uso real en navegador pendientes por fallo de herramienta CUA.'};
fs.writeFileSync(__dirname+'/verificacion_funcional.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
