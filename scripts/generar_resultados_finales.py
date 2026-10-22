"""Tablas, figuras y datos de comunicación desde resultados verificados."""
import os
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']: os.environ[k]='2'
import json,sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from estilo_visual import apply_style,BLUE,ACCENT,line_style
from entrenamiento_oulad import KEY
OUT=ROOT/'reportes/cierre_modelado_2026_10_21'
SRC=ROOT/'reportes/continuacion_modelado_2026_10_20'
DOC=ROOT/'Plantilla_ProyAplicado'
FIG=DOC/'figuras_resultados';FIG.mkdir(exist_ok=True)
TABLE=DOC/'tablas_resultados';TABLE.mkdir(exist_ok=True)
data=json.loads((OUT/'sintesis.json').read_text(encoding='utf-8'))
metrics=pd.read_csv(OUT/'metricas_todas.csv')
names={'regresion_logistica':'Logística','random_forest':'Random Forest','xgboost':'XGBoost','lightgbm':'LightGBM','tabnet':'TabNet','referencia':'Referencia constante','clase_mayoritaria':'Clase mayoritaria'}
labels={'clics_ultimos_7d':'Clics en últimos 7 días','clics_pre_inicio':'Clics antes del inicio','total_clics':'Clics acumulados','clics_7d_previos':'Clics en 7 días previos','n_evaluaciones_entregadas':'Evaluaciones entregadas','proporcion_programadas_entregadas':'Proporción entregada del calendario','n_evaluaciones_programadas':'Evaluaciones con vencimiento hasta el corte','cv_intensidad_activa':'Variabilidad en días activos','log_ratio_14d':'Cambio de actividad entre quincenas','dias_activos':'Días con actividad'}
def f(x,n=3): return f'{x:.{n}f}'.replace('.',',')
def tex_table(file,caption,label,headers,rows,spec):
    text='\\begin{table}[!htbp]\\centering\n\\caption{'+caption+'}\\label{'+label+'}\n\\begin{tabular}{'+spec+'}\n\\toprule\n'+' & '.join(headers)+r'\\'+'\n\\midrule\n'
    text+='\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+'\n\\bottomrule\n\\end{tabular}\n\\end{table}\n'
    (TABLE/file).write_text(text,encoding='utf-8')
def ci(cut,name,field):return next(x for x in data['intervalos'] if x['corte']==cut and x['modelo']==name and x['metrica']==field)
rows=[];class_rows=[];cal_rows=[];lead_rows=[]
for p in data['principales']:
    c=ci(p['corte'],p['modelo'],'ap')
    rows.append([p['corte'],names[p['modelo']],p['inscripciones'],p['personas'],p['eventos'],f(p['ap']),f"[{f(c['inferior'])}; {f(c['superior'])}]"])
    class_rows.append([p['corte'],f(p['umbral']),f(p['precision']),f(p['sensibilidad']),f(p['f1']),f(100*p['proporcion_alertas'],1)])
    ref=metrics[(metrics.corte==p['corte'])&(metrics.modelo=='referencia')].iloc[0]
    cal_rows.append([p['corte'],f(p['prevalencia']),f(p['roc_auc']),f(p['brier'],4),f(ref.brier,4)])
    lead_rows.append([p['corte'],int(p['tp']),int(p['fp']),int(p['fn']),f(p['anticipacion_tp']['q25'],1),f(p['anticipacion_tp']['mediana'],1),f(p['anticipacion_tp']['q75'],1)])
tex_table('principales.tex','Población de prueba y AP de la familia principal; intervalos percentiles del 95\\,\\%.','res:principales',['Día','Familia','Inscr.','Personas','Retiros','AP','Intervalo'],rows,'rlrrrrl')
tex_table('alertas.tex','Clasificación en prueba con los umbrales congelados; alertas en porcentaje de inscripciones.','res:alertas',['Día','Umbral','Precisión','Sensibilidad','F1','Alertas (\\%)'],class_rows,'rrrrrr')
tex_table('calibracion.tex','Prevalencia, discriminación y error probabilístico en prueba del candidato principal.','res:calibracion',['Día','Prevalencia','ROC-AUC','Brier principal','Brier referencia'],cal_rows,'rrrrr')
tex_table('anticipacion.tex','Errores y anticipación entre alertas correctas. Los cuartiles se expresan en días desde el corte hasta el retiro.','res:anticipacion',['Día','VP','FP','FN','Q25','Mediana','Q75'],lead_rows,'rrrrrrr')
models=list(names)[:5]
tex_table('comparacion.tex','AP de los candidatos congelados en prueba. La mayor cifra no redefine al principal.','res:comparacion',['Día','Logística','RF','LightGBM','XGBoost','TabNet'],[[c]+[f(metrics[(metrics.corte==c)&(metrics.modelo==m)].iloc[0].ap) for m in ['regresion_logistica','random_forest','lightgbm','xgboost','tabnet']] for c in [7,14,28,42,56]],'rrrrrr')
shap=pd.DataFrame(data['shap'])
tex_table('shap.tex','Indicador con mayor contribución absoluta media en las cien inscripciones explicadas de cada corte. La magnitud se expresa en puntos porcentuales de probabilidad.','res:shap',['Día','Indicador','Magnitud'],[[c,labels[g.iloc[0].predictor],f(g.iloc[0].media_absoluta*100,2)] for c,g in shap.sort_values('media_absoluta',ascending=False).groupby('corte')],'rp{.65\\linewidth}r')
apply_style(10)
fig,ax=plt.subplots(figsize=(7.0,4.2))
for idx,p in enumerate(data['principales']):
    c=ci(p['corte'],p['modelo'],'ap')
    ax.errorbar(p['ap'],idx,xerr=[[p['ap']-c['inferior']],[c['superior']-p['ap']]],fmt='o',color=BLUE,capsize=4,label='Principal: AP e intervalo del 95 %' if idx==0 else None)
    ax.scatter(p['prevalencia'],idx,color=ACCENT,marker='s',label='Referencia constante: AP = prevalencia' if idx==0 else None)
ax.set_yticks(range(5),[f"Día {p['corte']} · {names[p['modelo']]}" for p in data['principales']]);ax.invert_yaxis()
ax.set_xlim(0,.36);ax.set_xlabel('Precisión promedio (AP) en prueba');ax.grid(axis='x');ax.legend(loc='upper center',bbox_to_anchor=(.43,-.17),fontsize=9)
fig.tight_layout();fig.savefig(FIG/'ap_principales.pdf',bbox_inches='tight');fig.savefig(FIG/'ap_principales.png',dpi=160,bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(7,4.5))
ax.plot([0,1],[0,1],color='#999999',linestyle='--',label='Coincidencia ideal')
for idx,p in enumerate(data['principales']):
    bins=pd.read_csv(SRC/f"evaluacion/corte_{p['corte']:02d}/calibracion_{p['modelo']}.csv").dropna()
    ax.plot(bins.probabilidad_media,bins.frecuencia_retiro,label=f"Día {p['corte']}",**line_style(idx))
ax.set(xlim=(0,.6),ylim=(0,.6),xlabel='Probabilidad media en el intervalo',ylabel='Proporción observada de retiros')
ax.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,-.18));ax.grid(alpha=.4);fig.tight_layout()
fig.savefig(FIG/'calibracion_principales.pdf',bbox_inches='tight');fig.savefig(FIG/'calibracion_principales.png',dpi=160,bbox_inches='tight');plt.close(fig)
# Exportación local para el prototipo: sin identificadores personales, sin reajuste.
prototype=ROOT/'prototipo';prototype.mkdir(exist_ok=True)
payload={'principales':data['principales'],'metricas':metrics.astype(object).where(pd.notna(metrics),None).to_dict('records'),'intervalos':data['intervalos'],'nombres':names,'labels':labels,'shap':{},'casos':{},'calibracion':{}}
for p in data['principales']:
    cut=p['corte'];sf=SRC/f'shap/resultados/corte_{cut:02d}'
    payload['shap'][str(cut)]=shap[shap.corte.eq(cut)].head(8).to_dict('records')
    contrib=pd.read_parquet(sf/'contribuciones.parquet')
    pred=pd.read_parquet(SRC/f'evaluacion/corte_{cut:02d}/predicciones.parquet')
    joined=contrib.merge(pred[KEY+['retiro_futuro']],on=KEY,validate='one_to_one')
    payload['casos'][str(cut)]=[{'caso':i+1,'probabilidad':r.probabilidad,'base':r['base'],'retiro':int(r.retiro_futuro),
             'contribuciones':sorted([{'predictor':col,'valor':r[col]} for col in json.loads((SRC/'paquete_evaluacion.json').read_text())['predictores']],key=lambda x:-abs(x['valor']))} for i,(_,r) in enumerate(joined.iterrows())]
    bins=pd.read_csv(SRC/f'evaluacion/corte_{cut:02d}/calibracion_{p["modelo"]}.csv').dropna()
    payload['calibracion'][str(cut)]=bins.to_dict('records')
(prototype/'datos.js').write_text('const DATA = '+json.dumps(payload,ensure_ascii=False,allow_nan=False)+';',encoding='utf-8')
html=(prototype/'index.html').read_text(encoding='utf-8')
html=html.replace('<script src="datos.js"></script>','<script>'+(prototype/'datos.js').read_text(encoding='utf-8')+'</script>')
html=html.replace('<script src="app.js"></script>','<script>'+(prototype/'app.js').read_text(encoding='utf-8')+'</script>')
(prototype/'OULAD.html').write_text(html,encoding='utf-8')
print('Tablas, figuras y datos del prototipo generados.')
from completar_prototipo import main as completar_prototipo
completar_prototipo()
