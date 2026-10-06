"""Segunda integración editorial desde un respaldo versionado, sin recalcular OULAD."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'Plantilla_ProyAplicado'
OLD=ROOT/'respaldo/2026-09-13_pre_cv_y_lectura/Plantilla_ProyAplicado'


def main():
    text=(OLD/'desarrollo2.tex').read_text(encoding='utf-8')
    start=text.index('El sumando 1 de la tendencia')
    stop=text.index('\n\n',start)
    smoothing=text[start:stop]
    text=text[:start]+r'\input{ejemplo_cv}'+text[stop:]
    # La explicación del suavizado se consulta junto a la fórmula de tendencia.
    point=text.index('El término 1 permite razones finitas')
    end=text.index('\n\n',point)
    text=text[:point]+smoothing+text[end:]
    (P/'desarrollo2.tex').write_text(text,encoding='utf-8')
    text=(OLD/'descripcion.tex').read_text(encoding='utf-8')
    text=text.replace('A continuación se precisan los conceptos centrales empleados a lo largo del documento.',
        'El desarrollo parte de la plataforma y de la definición del abandono, continúa con los indicadores observables y presenta después los modelos candidatos. La metodología CRISP-DM organiza estas actividades y el apartado de SHAP delimita cómo se prevé interpretar las predicciones. Esta secuencia permite distinguir el fenómeno educativo, su representación mediante datos y las herramientas utilizadas para estudiarlo.')
    # Párrafos con una función argumentativa identificable; se conservan citas y fórmulas.
    text=text.replace('La denominación no es estable en la literatura, debido a que, en sentido estricto,', '\n\nLa denominación varía en la literatura. En sentido estricto,')
    text=text.replace('Es así como la variación terminológica obliga a fijar una convención antes de emplear los términos. Este trabajo adopta', 'Para mantener una convención de lectura, el estudio adopta')
    text=text.replace('La deserción carece de una definición unívoca, y su delimitación condiciona la forma en la que se mide qué estudiantes se cuentan como desertores, cuál es su prevalencia y, en un problema de clasificación supervisada, qué observaciones reciben la etiqueta positiva',
        'La delimitación de la deserción determina qué estudiantes se cuentan como desertores y cuál es la prevalencia del fenómeno. En una tarea de clasificación supervisada, también determina qué observaciones reciben la etiqueta positiva')
    text=text.replace('La inconsistencia entre estudios proviene en buena medida de esa ausencia de un criterio común, pues un mismo comportamiento admite clasificaciones opuestas según el punto de referencia adoptado.',
        '\n\nUn mismo comportamiento puede recibir clasificaciones diferentes según el punto de referencia adoptado.')
    text=text.replace('Su distinción respecto a la minería de datos educativos se debe más al énfasis que al objeto:', '\n\nLa distinción respecto a la minería de datos educativos se relaciona con el énfasis:')
    text=text.replace('Su formulación exige distinguir dos periodos, de cuya extensión dependen los resultados obtenidos: primero, el tramo del curso sobre el cual se acumulan y calculan las variables predictivas, el cual llamaremos la ventana de observación, mientras que el horizonte de predicción es el intervalo futuro sobre el cual el modelo genera su estimación.',
        '\n\nLa formulación exige distinguir dos periodos. La ventana de observación es el tramo sobre el que se acumulan los datos y se calculan los predictores. El horizonte de predicción corresponde al intervalo futuro en el que se observa el evento. La extensión de ambos periodos condiciona la interpretación de los resultados.')
    text=text.replace('La predicción del abandono se formula en este trabajo como una tarea de clasificación binaria supervisada. Sea',
        'La predicción del abandono se formula como una tarea de clasificación binaria supervisada. En un corte fijado, cada inscripción elegible se representa mediante sus características observables; el modelo buscará relacionarlas con la presencia o ausencia de retiro posterior. La estimación de probabilidad y la asignación de una clase son pasos distintos, porque esta última requiere un umbral de decisión.\n\nSea')
    text=text.replace('La selección de los algoritmos candidatos obedece a dos criterios ya enunciados (desempeño reportado en la literatura sobre predicción de abandono y compatibilidad con el análisis de interpretabilidad) y a un tercero de orden estructural: la conveniencia de cubrir familias metodológicas distintas antes que múltiples variantes de una misma.',
        'La selección de los algoritmos candidatos considera el desempeño reportado en la literatura, la compatibilidad con el análisis de interpretabilidad y la representación de familias metodológicas distintas.')
    text=text.replace('La comparación entre familias resulta pertinente porque', '\n\nLa comparación entre familias resulta pertinente porque')
    text=text.replace('de manera que $e^{\\beta_{j}}$ cuantifica el cambio multiplicativo en la razón de probabilidades: como ejemplo hipotético y no como resultado del estudio,',
        'de manera que $e^{\\beta_{j}}$ cuantifica el cambio multiplicativo en la razón de probabilidades.\n\nComo ejemplo hipotético, no como resultado del estudio,')
    text=text.replace('Las condiciones de validez del modelo derivan del mismo supuesto que lo hace legible.',
        'La interpretación de los coeficientes depende de la forma funcional y de las condiciones del ajuste.')
    text=text.replace('salvo que se especifiquen de forma explícita; la inferencia convencional supone independencia entre observaciones, condición que requiere atención por las inscripciones repetidas, y la estimación puede resultar inestable ante colinealidad severa,',
        'salvo que se especifiquen de forma explícita.\n\nLa inferencia convencional supone independencia entre observaciones, condición que requiere atención por las inscripciones repetidas. La estimación también puede resultar inestable ante colinealidad severa,')
    text=text.replace('Estas expresiones hacen explícito el papel de cada hiperparámetro. El coeficiente',
        '\n\nLa regularización controla aspectos diferentes del árbol. El coeficiente')
    text=text.replace('La tasa $\\nu$ escala cada actualización,', '\n\nLa tasa $\\nu$ escala cada actualización,')
    text=text.replace('A ello se añaden un algoritmo de búsqueda de cortes consciente de la dispersión,',
        '\n\nLa implementación añade un algoritmo de búsqueda de cortes consciente de la dispersión,')
    text=text.replace('La dispersión de las máscaras se induce además mediante un término de entropía añadido a la pérdida,',
        '\n\nLa dispersión de las máscaras se induce además mediante un término de entropía añadido a la pérdida,')
    text=text.replace('El enunciado preciso y su demostración se encuentran en \\cite{lundberg2017}, y la caracterización axiomática de la que parte, en \\cite{shapley1953}. La primera de esas tres propiedades es la que confiere sentido operativo a la explicación, pues garantiza que las atribuciones reconstruyen exactamente la predicción:',
        'El enunciado preciso y su demostración se encuentran en \\cite{lundberg2017}, y su fundamento axiomático, en \\cite{shapley1953}. La propiedad de exactitud local se expresa mediante la siguiente identidad:')
    text=text.replace('Este algoritmo aporta además la posibilidad de agregar las atribuciones locales en medidas globales de importancia,',
        '\n\nLas atribuciones locales pueden agregarse en medidas globales de importancia,')
    text=text.replace('En ambos casos las atribuciones se reportan como descripciones', 'En ambos casos las atribuciones se reportarán como descripciones')
    (P/'descripcion.tex').write_text(text,encoding='utf-8')
    print('Ejemplo CV integrado y párrafos del marco reorganizados; fórmulas preservadas.')


if __name__=='__main__':
    main()
