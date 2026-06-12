# Predicción de deserción estudiantil (OULAD)

Proyecto de **clasificación supervisada** para predecir la deserción estudiantil
sobre el dataset [OULAD (Open University Learning Analytics Dataset)](https://analyse.kmi.open.ac.uk/open_dataset).
El trabajo combina modelado predictivo, **interpretabilidad con SHAP** y un
**prototipo de visualización** de resultados, desarrollado bajo la metodología
**CRISP-DM** (comprensión del área, comprensión de los datos, preparación,
modelado, evaluación y despliegue).

## Estructura de carpetas

```
prediccion-desercion-oulad/
├── data/
│   ├── raw/            # CSVs originales de OULAD — intactos, ignorados por Git
│   └── processed/      # intermedios y dataset analítico final
├── notebooks/          # EDA, preparación, modelado, evaluación
├── src/                # funciones reutilizables (carga, features, modelos, viz)
├── outputs/
│   └── figures/        # figuras y tablas numeradas para el documento
├── docs/
│   └── bitacora.md     # bitácora de desarrollo
├── .gitignore
├── requirements.txt
└── README.md
```

## Objetivos

- **Comprender el fenómeno de la deserción** en el contexto de OULAD y definir
  operacionalmente el target (retiro formal e inactividad prolongada).
- **Explorar y caracterizar los datos** (EDA) por categorías de variables
  —académicas, conductuales y temporales— evaluando su calidad.
- **Preparar el dataset analítico**: ingeniería de variables, ventanas
  temporales y particionado estratificado.
- **Entrenar y comparar modelos** de clasificación supervisada, tratando el
  desbalance de clases de forma condicional cuando se detecte.
- **Evaluar e interpretar** los modelos mediante métricas adecuadas y análisis
  de interpretabilidad con SHAP.
- **Desarrollar un prototipo de visualización** que comunique los resultados y
  apoye la toma de decisiones.
