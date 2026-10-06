"""Identifica artefactos y evidencia existente; no ejecuta revisión visual."""
from pathlib import Path
from datetime import datetime, timezone
import ast, csv, hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reportes/correcciones_2026_09_10'

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))

def main():
    checks=read('verificaciones_independientes.json')
    assert len(checks)==49 and all(x['estado']=='correcta' for x in checks)
    doc=read('verificacion_documental.json');reports=read('verificacion_informes.json')
    assert not doc['errores_relevantes_latex']
    assert all(r['desbordamientos_latex']==0 and r['texto_dentro_margenes'] for r in reports)
    assert digest(ROOT/doc['pdf'])==doc['sha256_pdf']
    for r in reports:assert digest(OUT/'informes'/f"{r['informe']}.pdf")==r['sha256_pdf']
    previous=json.loads((ROOT/'reportes/multiventana_2026_09_08/fuentes.json').read_text(encoding='utf-8'))
    for name,info in read('fuentes.json').items():
        assert digest(ROOT/'data/raw'/f'{name}.csv')==info['sha256']==previous[name]['sha256']
    notebooks=sorted(ROOT.glob('0[123]*.ipynb'))
    for p in notebooks:
        for cell in json.loads(p.read_text(encoding='utf-8'))['cells']:
            if cell['cell_type']=='code':
                ast.parse(''.join(cell['source']))
                assert cell['execution_count'] is not None
                assert not any(o['output_type']=='error' for o in cell['outputs'])
    rows=[
      ('B01/B02/B22','mayor','parcial; ratificación pendiente','desarrollo2.tex / A3.1; decision_temporal.json','Evento registrado e inactividad complementaria explícitos; falta acuerdo académico. No se presume acta obligatoria.'),
      ('B03','mayor','implementado y comprobado','src/ventanas_oulad.py; corr:identidadcv; corr:cv','CV activo adicional; identidad general y comparación sobre casos comunes.'),
      ('B04','menor','no aplicable al error alegado','descripcion.tex / formulación probabilística','Se conserva Pr(Y=1 dado X=x).'),
      ('B05/B06','mayor','implementado y comprobado','corr:simbolos; corr:elegibilidad; corr:evento','Probabilidad individual, prevalencia, matrícula, retiro ausente o futuro, horizonte y preinicio diferenciados.'),
      ('B07','mayor','implementado y comprobado','corr:diccionario; 02_diccionario.csv','26 candidatos y conteo separado para auditoría; nombres del código.'),
      ('B08','menor','cerrado documentalmente para esta versión','desarrollo2.tex / selección de indicadores','Ausencia de diversidad justificada; utilidad no evaluada.'),
      ('B09','mayor','implementado','desarrollo2.tex / notación y tendencias','Suavizado, inversión de signo y pérdida de invariancia de escala precisados.'),
      ('B10','mayor','implementado y ejecutado','corr:pcasens; 03_sensibilidad_pca.csv','Tres especificaciones con los mismos casos; interpretación limitada de varianza.'),
      ('B11','menor','propuesta no incorporada','desarrollo1.tex / efecto biserial','No se usa equivalencia r-AUC como evaluación predictiva; desarrollo adicional opcional.'),
      ('B12','mayor','implementado','desarrollo1.tex / V de Cramér','Fórmula y límites; no se afirma aumento inevitable por desbalance.'),
      ('B13','mayor','parcial; protocolo de métricas pendiente','descripcion.tex / costes; desarrollo3.tex','Probabilidad individual precisada; AP, calibración y comparabilidad se fijarán en el protocolo.'),
      ('B14/B15','mayor','implementado con selección de figuras','corr:flujos; corr:calendario; corr:observabilidad; multi02:figpoblacion','Cascadas secuenciales, partición sin solapamientos, fechas, calendario y evolución con ejes numéricos.'),
      ('B16','mayor','cerrado para el conjunto candidato actual','src/ventanas_oulad.py; corr:vif','n_registros_vle excluido de los cinco conjuntos; VIF y n publicados.'),
      ('B17','menor','implementado en el alcance de la entrega','abstract.tex; descripcion.tex; anexos.tex','Denominadores, alcance de equidad, historia de versión y presentación.'),
      ('B18','menor','parcial: comprobado; desglose de pesos no añadido como tabla','01 / auditoría; desarrollo2.tex / entregas','No se impone total 200; se distingue evaluación programada de actividad de entrega.'),
      ('B19/V1','mayor','cerrado documentalmente','corr:niveles; corr:numericos; corr:flujos','Contexto y cascadas publicados en el trabajo de grado con remisiones; créditos e intentos añadidos.'),
      ('B20/B21','mayor','implementado; limitación declarada','desarrollo2.tex / notación y selección; desarrollo3.tex','13/27 primeros cortes posibles; 14/28 primeros elegidos; no se presume optimalidad ni prueba intacta.'),
      ('B23/V12','mayor','implementado y ejecutado','corr:bootstrap; verificaciones_ampliacion.json','5.000 remuestreos; 66/66 cambios dentro de 0,005; máximo 0,00299394.'),
      ('B24','menor','parcial / pendiente','revision_bitacora_2026_09_10/revision.md','No se declara bibliografía exhaustivamente verificada ni revisión del PDF anotado.'),
      ('P01','bloqueante','pendiente para comparación predictiva','desarrollo3.tex','Fijar generalización, particiones, métricas, calibración, umbral y tratamiento de exploración previa.'),
      ('P02','mayor','no iniciado','desarrollo3.tex; desarrollo4.tex; desarrollo5.tex','Comparación de clasificadores, SHAP y prototipo.'),
    ]
    with (OUT/'registro_hallazgos.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['version','id','severidad','estado','ubicacion','evidencia_o_condicion_de_cierre'])
        w.writerows([['correcciones_2026_09_10',*r] for r in rows])
    aux=(ROOT/'Plantilla_ProyAplicado/proyecto.aux').read_text(encoding='utf-8')
    locations={m.group(1):{'numero':m.group(2),'pagina_impresa':m.group(3)} for m in re.finditer(r'\\newlabel\{(corr:[^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',aux)}
    files=set(notebooks)
    for folder in ['src','scripts','Plantilla_ProyAplicado','data/processed/correcciones_2026_09_10','reportes/correcciones_2026_09_10']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.py','.ps1','.tex','.bib','.pdf','.csv','.parquet','.json','.md'] and '__pycache__' not in p.parts)
    files.update([ROOT/'README_REVISION.md',ROOT/'decision_temporal.json'])
    manifest=OUT/'version_entregada.json';files.discard(manifest)
    result={'version':'correcciones_2026_09_10','registrado_utc':datetime.now(timezone.utc).isoformat(),
            'fuentes_originales_sha256_coinciden':True,'comprobaciones_independientes':len(checks),
            'ampliacion':read('verificaciones_ampliacion.json'),'paginas_proyecto':doc['paginas'],
            'informes':[{'nombre':r['informe'],'paginas':r['paginas']} for r in reports],
            'ubicaciones_documentales':locations,'revision_visual':'Descrita en entrega.md; este script no la ejecuta.',
            'ajuste_posterior_a_ejecucion':read('ajuste_editorial_figura.json'),
            'archivos':{p.relative_to(ROOT).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(files)}}
    manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ['version','fuentes_originales_sha256_coinciden','comprobaciones_independientes','paginas_proyecto','informes','ubicaciones_documentales']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
