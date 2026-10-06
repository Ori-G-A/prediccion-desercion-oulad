"""Comprobaciones numéricas de fórmulas; no equivalen a entrenamiento de modelos."""
from pathlib import Path
import itertools,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reportes/revision_marco_2026_09_09'

def main():
    checks=[]
    def check(name,result,detail):
        assert bool(result),name
        checks.append({'verificacion':name,'estado':'correcta','evidencia':detail})
    odds=math.exp(.4)
    check('Ejemplo de odds logísticas',abs((odds-1)*100-49.182469764)<1e-8,{'razon_odds':odds,'incremento_porcentual':(odds-1)*100})
    p=np.linspace(.001,.999,999)
    for fp,fn in [(1,1),(2,7),(5,2)]:
        tau=fp/(fp+fn)
        selected=np.where(p>tau,fp*(1-p),fn*p)
        check(f'Umbral Bayes con costes {fp},{fn}',np.allclose(selected,np.minimum(fp*(1-p),fn*p)),{'umbral':tau,'probabilidades_evaluadas':len(p),'empates':'ambas decisiones minimizan el coste'})
    rng=np.random.default_rng(20260909)
    B=13;rho=.27;variance=2.4
    cov=variance*((1-rho)*np.eye(B)+rho*np.ones((B,B)))
    lhs=np.ones(B)@cov@np.ones(B)/B**2;rhs=rho*variance+(1-rho)*variance/B
    check('Varianza de promedio equicorrelacionado',np.isclose(lhs,rhs),{'matriz_covarianza':float(lhs),'formula':float(rhs),'B':B,'rho':rho})
    z=np.linspace(-4,4,15);y=np.array([0,1]*8)[:15];epsilon=1e-4
    loss=lambda zz:np.logaddexp(0,zz)-y*zz
    g=(loss(z+epsilon)-loss(z-epsilon))/(2*epsilon)
    h=(loss(z+epsilon)-2*loss(z)+loss(z-epsilon))/epsilon**2
    pi=1/(1+np.exp(-z))
    check('Derivadas logísticas respecto de puntuación, no probabilidad',np.allclose(g,pi-y,atol=1e-8) and np.allclose(h,pi*(1-pi),atol=3e-7),{'diferencias_finitas':epsilon,'puntos':len(z)})
    G=rng.normal(size=20);H=rng.uniform(.2,10,size=20);lam=.6;w=-G/(H+lam)
    obj=lambda weights:G*weights+.5*(H+lam)*weights**2
    check('Mínimo cuadrático de hojas XGBoost',np.allclose(G+(H+lam)*w,0) and (obj(w)<=obj(w+.2)).all() and (obj(w)<=obj(w-.2)).all(),{'hojas':len(w),'lambda':lam,'hessianos_positivos':True})
    GL,GR=-2.,1.2;HL,HR=3.,2.;gamma=.1
    parent=-.5*(GL+GR)**2/(HL+HR+lam)+gamma
    children=-.5*(GL**2/(HL+lam)+GR**2/(HR+lam))+2*gamma
    gain=.5*(GL**2/(HL+lam)+GR**2/(HR+lam)-(GL+GR)**2/(HL+HR+lam))-gamma
    check('Ganancia XGBoost como diferencia de mínimos',np.isclose(parent-children,gain),{'ganancia':gain})
    n=1000;a=.2;b=.1;inclusion=b/(1-a);weight=(1-a)/b
    check('Convención GOSS: fracción del total y peso inverso',np.isclose(inclusion*weight,1) and np.isclose((a+b)*n,300),{'seleccionados':int((a+b)*n),'probabilidad_entre_restantes':inclusion,'peso':weight})
    first=np.array([.4,.6]);prior=1-first;second_scores=prior*np.array([1.,0.])
    # Proyección sparsemax al simplex en dimensión 2; ambos pesos son positivos.
    second=second_scores-(second_scores.sum()-1)/2
    check('Contraejemplo a exclusión binaria por prior TabNet gamma=1',(first>0).all() and (second>0).all() and np.isclose(second.sum(),1),{'primera_mascara':first.tolist(),'prior':prior.tolist(),'segunda_mascara':second.tolist(),'alcance':'La ecuación de prior por sí sola no prohíbe reutilización'})
    x=np.array([1.,2.,3.]);f=lambda v:float(v[0]+2*v[1]+v[0]*v[2]);players=range(3)
    def value(S):return f(np.array([x[j] if j in S else 0. for j in players]))
    phi=[]
    for j in players:
        rest=[k for k in players if k!=j];total=0.
        for size in range(3):
            for S in itertools.combinations(rest,size):
                factor=math.factorial(size)*math.factorial(2-size)/math.factorial(3)
                total+=factor*(value(set(S)|{j})-value(set(S)))
        phi.append(total)
    check('Aditividad Shapley para juego y referencia fijados',np.isclose(sum(phi)+value(set()),f(x)),{'atribuciones':phi,'base':value(set()),'salida':f(x),'referencia':'vector cero; juego no condicional'})
    OUT.mkdir(exist_ok=True)
    (OUT/'verificacion_matematica.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(checks)} comprobaciones matemáticas satisfactorias; sin entrenar modelos.')

if __name__=='__main__':main()
