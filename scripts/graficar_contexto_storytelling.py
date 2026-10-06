r"""Figuras de contexto con jerarquía visual y denominadores explícitos.

Desde la raíz: .venv\Scripts\python.exe scripts/graficar_contexto_storytelling.py
Reutiliza resultados guardados y verifica su correspondencia con el anexo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import Normalize, to_rgb
from matplotlib.patches import Rectangle
from matplotlib.transforms import blended_transform_factory

from graficar_contexto import ROOT, VARIABLES, entero, label, porcentaje, verify

sys.path.insert(0, str(ROOT / 'src'))
from estilo_visual import apply_style, INK, MUTED, BLUE as ACCENT, ACCENT as HIGHLIGHT, GRAY as NEUTRAL, GRID, PALE, SEQUENTIAL as CMAP
NORM = Normalize(0, 40)
GROUPS = {"age_band": "Edad", "disability": "Discapacidad registrada", "imd_band": "Privación del área (IMD)", "region": "Región"}


def theme():
    return apply_style(11)


def text_in(fig, x, y, text, **kwargs):
    """Place text in inches, keeping layouts consistent across figure heights."""
    width, height = fig.get_size_inches()
    return fig.text(x / width, y / height, text, **kwargs)


def header(fig, number, section, title, subtitle):
    height = fig.get_size_inches()[1]
    text_in(fig, .55, height - .30, f"{number:02d}  /  {section.upper()}", fontsize=10, color=ACCENT, weight="bold", va="top")
    fig.add_artist(plt.Line2D([.55 / 12, 1.12 / 12], [(height-.53)/height]*2, transform=fig.transFigure, color=HIGHLIGHT, linewidth=3))
    text_in(fig, .55, height - .66, title, fontsize=23, weight="bold", va="top", linespacing=1.1)
    text_in(fig, .55, height - 1.57, subtitle, fontsize=11.5, color=MUTED, va="top", linespacing=1.35)


def footer(fig, lines):
    width, _ = fig.get_size_inches()
    fig.add_artist(plt.Line2D([.55 / width, 11.40 / width], [1.11 / fig.get_size_inches()[1]] * 2,
                             transform=fig.transFigure, color=GRID, linewidth=.8))
    for i, line in enumerate(lines):
        text_in(fig, .55, .94 - .21 * i, line, fontsize=9.3, color=MUTED, va="top")
    text_in(fig, .55, .20, "Fuente: OULAD; salidas guardadas del proyecto, versión correcciones_2026_09_10. Visualización: 04/10/2026.",
            fontsize=8.4, color=MUTED, va="bottom")


def bar_figure(data, variable, cut, index):
    group = data[(data.corte == cut) & (data.variable == variable)].copy()
    total_n = int(group.n.sum())
    total_w = int(group.retiros.sum())
    baseline = 100 * total_w / total_n
    note = "Los porcentajes son descriptivos, sin ajuste por otras variables; no demuestran causalidad ni significancia estadística."
    if variable == "age_band":
        order = ["0-35", "35-55", "55<="]
        group = group.set_index("nivel").loc[order].reset_index()
        old = group[group.nivel == "55<="].iloc[0]
        title = "Las bandas de edad reúnen grupos\nde tamaños muy distintos"
        subtitle = f"La banda de 55 o más años reúne {entero(old.n)} de las {entero(total_n)} inscripciones elegibles al día {cut}."
        selected = group.nivel.eq("55<=").to_numpy()
        extra = "Se conservan las bandas de edad de OULAD. El resaltado permite reconocer el grupo de menor tamaño."
    elif variable == "disability":
        group = group.set_index("nivel").loc[["N", "Y"]].reset_index()
        no, yes = group.iloc[0], group.iloc[1]
        difference = float(yes.tasa_pct - no.tasa_pct)
        assert difference > 0, "Revisar la narrativa: cambió la dirección de la diferencia."
        title = "El porcentaje de retiro es mayor entre las\ninscripciones con discapacidad registrada"
        difference_label = f"{difference:.1f}".replace(".", ",")
        subtitle = (f"{porcentaje(yes.tasa_pct)} frente a {porcentaje(no.tasa_pct)}. Diferencia observada: "
                    f"{difference_label} puntos porcentuales.")
        selected = group.nivel.eq("Y").to_numpy()
        extra = "El registro de discapacidad describe el grupo; esta comparación no identifica la causa de la diferencia."
    elif variable == "imd_band":
        observed = group[group.nivel != "No disponible"]
        assert not (observed.tasa_pct.is_monotonic_increasing or observed.tasa_pct.is_monotonic_decreasing), "Revisar la narrativa de IMD."
        title = "El porcentaje de retiro varía entre bandas\nde privación, sin un orden uniforme"
        subtitle = "El IMD resume carencias del área de residencia; no mide los ingresos de cada persona."
        selected = group.nivel.ne("No disponible").to_numpy()
        extra = "Las bandas de IMD se conservan en su orden original; los casos sin dato se muestran separados, en gris."
    else:
        group = group.sort_values("tasa_pct", ascending=False, kind="stable").reset_index(drop=True)
        low, high = float(group.tasa_pct.min()), float(group.tasa_pct.max())
        title = f"El porcentaje de retiro varía entre regiones:\nde {porcentaje(low)} a {porcentaje(high)}"
        subtitle = "Regiones ordenadas por porcentaje observado; se resaltan los extremos para facilitar su lectura."
        selected = np.zeros(len(group), dtype=bool)
        selected[[0, len(group) - 1]] = True
        extra = "Los nombres geográficos se conservan como en OULAD; se omite la palabra Region para abreviar las etiquetas."
    height = 5.10 + .27 * len(group)
    fig = plt.figure(figsize=(12, height))
    header(fig, index, f"{GROUPS[variable]} · día {cut}", title, subtitle)
    bottom, top = 1.54, height - 2.43
    ax = fig.add_axes([3.32 / 12, bottom / height, 5.30 / 12, (top - bottom) / height])
    positions = np.arange(len(group), dtype=float)
    if variable == "imd_band":
        positions[group.nivel.eq("No disponible")] += .42
    ax.set_ylim(positions[-1] + .66, -.66)
    ax.set_xlim(0, 35)
    ax.set_xticks([0, 10, 20, 30], ["0 %", "10 %", "20 %", "30 %"])
    ax.tick_params(axis="x", length=0, labelsize=10, pad=5)
    ax.set_yticks([])
    ax.grid(axis="x", color=GRID, linewidth=.7)
    ax.set_axisbelow(True)
    colors = [HIGHLIGHT if focus and variable != 'imd_band' else ACCENT for focus in selected]
    if variable == 'imd_band':
        colors = [ACCENT if focus else NEUTRAL for focus in selected]
    bars = ax.barh(positions, group.tasa_pct, height=.48, color=colors, edgecolor=ACCENT, linewidth=.45)
    assert np.allclose([bar.get_width() for bar in bars], group.tasa_pct, atol=0, rtol=0)
    assert float(group.tasa_pct.max()) + 3 < ax.get_xlim()[1]
    ax.axvline(baseline, color=MUTED, linestyle=(0, (3, 3)), linewidth=.9, zorder=0)
    ax.text(baseline, 1.025, f"Total: {porcentaje(baseline)}", transform=ax.get_xaxis_transform(), fontsize=9.7, color=MUTED, ha="center", va="bottom")
    for spine in ax.spines.values():
        spine.set_visible(False)
    blend = blended_transform_factory(fig.transFigure, ax.transData)
    for y, row, focus in zip(positions, group.itertuples(), selected):
        name = label(variable, str(row.nivel)).replace("\n", " ")
        if variable == "region":
            name = name.replace(" Region", "")
        if variable == "disability":
            name = name.replace(" registrada", "\nregistrada")
        text_focus = focus and variable != "imd_band"
        color = ACCENT if text_focus else INK
        weight = "bold" if text_focus else "normal"
        ax.text(.55 / 12, y, name, transform=blend, ha="left", va="center", fontsize=11.5, color=color, weight=weight)
        ax.text(row.tasa_pct + .42, y, porcentaje(row.tasa_pct), va="center", fontsize=11.5, color=color, weight=weight,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": .5})
        ax.text(9.83 / 12, y, entero(row.n), transform=blend, ha="right", va="center", fontsize=11.5, weight=weight)
        ax.text(11.37 / 12, y, entero(row.retiros), transform=blend, ha="right", va="center", fontsize=11.5, color=MUTED)
    category_label = {"imd_band": "Banda de IMD", "age_band": "Banda de edad"}.get(variable, "Categoría")
    for x, word, align in [(.55, category_label, "left"), (5.7, "Retiro futuro dentro de cada categoría", "center"),
                           (9.83, "Inscripciones", "right"), (11.37, "Retiros", "right")]:
        text_in(fig, x, top + .40, word, fontsize=10, color=MUTED, weight="bold", ha=align)
    text_in(fig, 5.97, 1.20, f"Referencia general: {entero(total_w)} retiros / {entero(total_n)} inscripciones", fontsize=9.5, color=MUTED, ha="center")
    footer(fig, [f"Retiro futuro: registrado después del día {cut} y hasta el final del curso. La unidad es la inscripción, no la persona.", extra, note])
    return fig, f"{index:02d}_{variable}_dia_{cut}"


def contrasting_text(color):
    rgb = np.asarray(to_rgb(color))
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    luminance = float(linear @ np.array([.2126, .7152, .0722]))
    # Choose the stronger black/white contrast; at least 4.5:1 is attainable.
    black, white = (luminance + .05) / .05, 1.05 / (luminance + .05)
    assert max(black, white) >= 4.5
    return "#FFFFFF" if white > black else "#000000"


def heat_figure(data, variables, index):
    cuts = sorted(data.corte.unique())
    totals = data[data.variable.eq("age_band")].groupby("corte")[["n", "retiros"]].sum().loc[cuts]
    entries = []
    y = .15
    for variable in variables:
        entries.append(("heading", y, variable, None))
        y += .94
        group = data[data.variable.eq(variable)]
        levels = group.nivel.drop_duplicates().tolist()
        if variable == "region":
            # Keep the same alphabetic order for all cutoffs; no implied ranking over time.
            levels = sorted(levels)
        pivot = group.pivot(index="nivel", columns="corte", values="tasa_pct").loc[levels, cuts]
        for level in levels:
            if level == "No disponible":
                y += .3
            entries.append(("data", y, (variable, level), pivot.loc[level].to_numpy()))
            y += 1
        y += .52
    entries.append(("total", y, None, (100 * totals.retiros / totals.n).to_numpy()))
    height = 4.23 + .31 * (y + .7)
    fig = plt.figure(figsize=(12, height))
    groups_text = "Edad, discapacidad e IMD" if len(variables) > 1 else "Región"
    header(fig, index, f"{groups_text} · cinco cortes", "Cada corte describe una población\ny un tiempo de seguimiento diferentes",
           "Porcentaje de retiro futuro dentro de cada categoría. Un tono más oscuro representa un porcentaje mayor.")
    bottom, top = 1.73, height - 2.45
    ax = fig.add_axes([4.12 / 12, bottom / height, 7.2 / 12, (top - bottom) / height])
    ax.set_xlim(-.5, 4.5)
    ax.set_ylim(y + .64, -.7)
    ax.set_axis_off()
    blend = blended_transform_factory(fig.transFigure, ax.transData)
    for j, cut in enumerate(cuts):
        x = (4.12 + 7.2 / 5 * (j + .5))
        text_in(fig, x, top + .43, f"Día {cut}", fontsize=12, weight="bold", ha="center")
        text_in(fig, x, top + .20, f"n = {entero(totals.loc[cut, 'n'])}", fontsize=9.6, color=MUTED, ha="center")
    for kind, row_y, key, values in entries:
        if kind == "heading":
            ax.text(.55 / 12, row_y, GROUPS[key], transform=blend, fontsize=11.5, weight="bold", color=ACCENT, va="center")
            continue
        if kind == "total":
            name = "Total en cada corte"
        else:
            variable, level = key
            name = label(variable, level).replace("\n", " ")
            if variable == "region":
                name = name.replace(" Region", "")
        ax.text(.55 / 12, row_y, name, transform=blend, fontsize=11.3, va="center", weight="bold" if kind == "total" else "normal")
        for col, value in enumerate(values):
            color = PALE if kind == "total" else CMAP(NORM(value))
            ax.add_patch(Rectangle((col - .475, row_y - .445), .95, .89, facecolor=color, edgecolor="none"))
            ax.text(col, row_y, porcentaje(value), ha="center", va="center", fontsize=11.5,
                    color=contrasting_text(color), weight="bold" if kind == "total" else "normal")
    color_ax = fig.add_axes([4.67 / 12, 1.40 / height, 5.65 / 12, .09 / height])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=NORM, cmap=CMAP), cax=color_ax, orientation="horizontal", ticks=[0, 20, 40])
    cb.ax.set_xticklabels(["0 %", "20 %", "40 %"], fontsize=8.6)
    cb.ax.tick_params(length=0, pad=2)
    cb.outline.set_visible(False)
    footer(fig, ["n indica las inscripciones elegibles del corte; los conteos de cada categoría se conservan en la tabla del anexo.",
                 "Retiro futuro: registrado después del corte y hasta el final del curso. Cada columna tiene su propio horizonte.",
                 "Los porcentajes no siguen a un grupo fijo ni prueban cambios de riesgo individual o mejoras de la predicción."])
    return fig, f"{index:02d}_cortes_{'contexto' if len(variables) > 1 else 'region'}"


def verify_bounds(fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    outside = []
    for artist in fig.findobj(matplotlib.text.Text):
        if not artist.get_visible() or not artist.get_text():
            continue
        bounds = artist.get_window_extent(renderer)
        if bounds.x0 < -1 or bounds.y0 < -1 or bounds.x1 > canvas.width + 1 or bounds.y1 > canvas.height + 1:
            outside.append(artist.get_text())
    assert not outside, f"Texto fuera del lienzo: {outside}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corte", type=int, default=28, choices=[7, 14, 28, 42, 56])
    parser.add_argument("--fuente", type=Path, default=ROOT / "reportes/correcciones_2026_09_10/tablas/03_niveles.csv")
    parser.add_argument("--salida", type=Path, default=ROOT / "reportes/figuras_cuerpo_2026_10_04/laminas")
    parser.add_argument("--pdf", type=Path, default=ROOT / "output/pdf/figuras_contexto_javeriana.pdf")
    args = parser.parse_args()
    args.salida.mkdir(parents=True, exist_ok=True)
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(args.fuente, keep_default_na=False)
    checks = verify(data, (ROOT / "Plantilla_ProyAplicado/anexos.tex").read_text(encoding="utf-8"))
    checks["familia_tipografica"] = theme()
    outputs = []
    with PdfPages(args.pdf, metadata={"Title": "Variables de contexto: figuras revisadas", "Author": "Proyecto OULAD", "Subject": "Comparaciones descriptivas; versión visual del 4 de octubre de 2026"}) as pdf:
        figures = [bar_figure(data, variable, args.corte, i) for i, variable in enumerate(VARIABLES, 1)]
        figures.extend([heat_figure(data, VARIABLES[:3], 5), heat_figure(data, ["region"], 6)])
        for fig, stem in figures:
            verify_bounds(fig)
            fig.savefig(args.salida / f"{stem}.png", dpi=160)
            fig.savefig(args.salida / f"{stem}.svg")
            pdf.savefig(fig)
            outputs.append(stem)
            plt.close(fig)
    data[data.variable.isin(VARIABLES)].to_csv(args.salida / "datos_representados.csv", index=False, encoding="utf-8-sig")
    checks.update({"version_visual": 4, "figuras": outputs, "paginas_pdf": len(outputs), "corte_barras": args.corte,
                   "fuente": str(args.fuente), "sha256_fuente": hashlib.sha256(args.fuente.read_bytes()).hexdigest(),
                   "pdf": str(args.pdf), "analisis_oulad_repetido": False, "documento_principal_modificado_por_este_script": False,
                   "anchos_barras_verificados": True, "texto_dentro_de_lienzos": True,
                   "escala_comun_barras_pct": [0, 35], "escala_comun_colores_pct": [0, 40],
                   "contraste_texto_celdas_minimo": 4.5,
                   "limites": "Comparaciones descriptivas sin ajuste; no se estimaron intervalos ni pruebas nuevas."})
    (args.salida / "verificacion.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
