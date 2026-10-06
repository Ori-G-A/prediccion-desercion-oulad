"""Figuras analíticas usadas por notebooks y regeneración desde salidas guardadas."""
import numpy as np
import matplotlib.pyplot as plt
try:
    from .estilo_visual import BLUE, ACCENT, MUTED, GRAY, SERIES, SEQUENTIAL, line_style, sequential_text
except ImportError:
    from estilo_visual import BLUE, ACCENT, MUTED, GRAY, SERIES, SEQUENTIAL, line_style, sequential_text


def momento_retiro(segments):
    names = {'sin_fecha':'Sin fecha de retiro', 'antes_inicio':'Antes del inicio', 'dias_0_27':'Días 0 a 27', 'dia_28':'Día 28', 'despues_28':'Después del día 28'}
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(segments.momento_retiro.map(names), segments.inscripciones, color=BLUE)
    ax.set_xlabel('Inscripciones'); ax.set_title('Momento del retiro en la fuente completa')
    ax.set_axisbelow(True); ax.grid(axis='x')
    return fig


def poblacion_cortes(population):
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (column, label) in enumerate([('inscripciones','Inscripciones elegibles'), ('retiros','Retiros futuros'), ('prevalencia_pct','Porcentaje de retiro')]):
        actual = 'eventos' if column == 'retiros' and 'eventos' in population else column
        ax.plot(population.corte, 100*population[actual]/population[actual].iloc[0], label=label, **line_style(i))
    ax.set_xticks(population.corte); ax.set_ylim(0, 105)
    ax.set_xlabel('Día del corte'); ax.set_ylabel('Índice, corte 7 = 100')
    ax.legend(fontsize=9); ax.set_axisbelow(True); ax.grid(axis='y')
    return fig


def distribuciones_cortes(datasets):
    # Colores complementarios para esta comparación; se conserva el azul base.
    colors = {
        7: BLUE,
        14: '#007F73',
        28: '#8B5AA5',
        42: '#C56A22',
        56: '#B93C60',
    }
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.7))
    for cut, frame in sorted(datasets.items()):
        for ax, variable in zip(axes, ['proporcion_dias_activos','recencia_relativa']):
            series = frame[variable].dropna().sort_values()
            ax.plot(series, np.arange(1,len(series)+1)/len(series), label=str(cut),
                    color=colors[cut], linestyle='-', linewidth=2, marker='None')
    axes[0].set_xlabel('Proporción de días activos'); axes[1].set_xlabel('Recencia relativa (solo actividad)')
    for ax in axes:
        ax.set_ylabel('Distribución acumulada')
        ax.set_axisbelow(True); ax.grid(axis='y')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title='Día de corte', ncol=5, fontsize=9,
               loc='lower center', bbox_to_anchor=(.5, 1.0), handlelength=3.2)
    return fig


def efectos_cortes(effects, cuts):
    fig, ax = plt.subplots(figsize=(8, 4.3))
    labels = {'proporcion_dias_activos':'Proporción de días activos', 'coef_variacion_clics':'Variabilidad de clics',
              'cv_intensidad_activa':'Variabilidad entre días activos', 'log_ratio_7d':'Tendencia de 7 días',
              'proporcion_programadas_entregadas':'Proporción programada entregada'}
    for i, (variable, label) in enumerate(labels.items()):
        rows = effects.loc[effects.variable.eq(variable)].dropna(subset=['efecto'])
        ax.plot(rows.corte, rows.efecto, label=label, **line_style(i))
        ax.fill_between(rows.corte, rows.IC95_inferior, rows.IC95_superior, color=SERIES[i], alpha=.12)
    ax.axhline(0, color=GRAY, ls='--'); ax.set_xticks(cuts)
    ax.set_xlabel('Día del corte'); ax.set_ylabel('Efecto biserial')
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(.5, 1.30), ncol=2)
    return fig


def fechas_retiro(base, cuts):
    fig, ax = plt.subplots(figsize=(8, 4))
    dates = base.date_unregistration.dropna()
    ax.hist(dates, bins=np.arange(dates.min(), dates.max()+7, 7), color=BLUE)
    ax.axvspan(dates.min(), 0, color=ACCENT, alpha=.3)
    for cut in [0, *cuts]:
        ax.axvline(cut, color='black' if cut == 0 else MUTED, linestyle='--', linewidth=.7)
    ax.set_xlabel('Día del retiro respecto del inicio'); ax.set_ylabel('Inscripciones con fecha de retiro')
    return fig


def calendario_evaluaciones(first, cuts):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    labels = first.code_module.astype(str)+' '+first.code_presentation.astype(str)
    ax.scatter(first.primera_fecha, np.arange(len(first)), s=24, color=BLUE)
    ax.set_yticks(np.arange(len(first)), labels, fontsize=8)
    for cut in cuts:
        ax.axvline(cut, color=GRAY, linestyle='--', linewidth=.6)
    ax.set_xlabel('Día de primera evaluación continua')
    return fig


def disponibilidad_indicadores(datasets):
    select = ['proporcion_dias_activos','coef_variacion_clics','cv_intensidad_activa','recencia_relativa',
              'log_ratio_7d','log_ratio_14d','proporcion_programadas_entregadas']
    matrix = np.array([[100*frame[v].notna().mean() for frame in datasets.values()] for v in select])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(matrix, vmin=0, vmax=100, cmap=SEQUENTIAL, aspect='auto')
    ax.set_xticks(range(len(datasets)), list(datasets))
    ax.set_yticks(range(len(select)), ['Días activos (proporción)','CV calendario','CV días activos','Recencia relativa','Tendencia 7 días','Tendencia 14 días','Proporción entregada'])
    for y in range(len(select)):
        for x in range(len(datasets)):
            text = f'{matrix[y,x]:.1f}'.replace('.', ',')+' %'
            ax.text(x, y, text, ha='center', va='center', color=sequential_text(matrix[y,x]), fontsize=8)
    ax.set_xlabel('Corte'); fig.colorbar(im, ax=ax, label='Porcentaje observable')
    return fig
