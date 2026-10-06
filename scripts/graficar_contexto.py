r"""Propone figuras de contexto a partir de resultados guardados; no recalcula OULAD.

Uso: .venv\Scripts\python.exe scripts/graficar_contexto.py --corte 28
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from estilo_visual import apply_style, BLUE, MUTED, GRID, INK, SEQUENTIAL
VARIABLES = ["age_band", "disability", "imd_band", "region"]
TITLES = ["Edad", "Discapacidad registrada", "Privación del área de residencia (IMD)", "Región"]
ANNEX_NAMES = {"age_band": "Edad", "disability": "Discapacidad", "imd_band": "IMD", "region": "Región"}


def entero(value):
    return f"{int(value):,}".replace(",", ".")


def porcentaje(value):
    return f"{value:.1f}".replace(".", ",") + " %"


def label(variable, level):
    if variable == "disability":
        return {"N": "Sin discapacidad registrada", "Y": "Con discapacidad registrada"}[level]
    if variable == "imd_band":
        return level if level == "No disponible" else level.replace("%", "").replace("-", "–") + " %"
    if variable == "age_band":
        return {"0-35": "0–35", "35-55": "35–55", "55<=": "55 o más"}[level]
    return "\n".join(textwrap.wrap(level, width=24))


def verify(data, annex):
    assert not data.duplicated(["corte", "variable", "nivel"]).any()
    assert (data.n > 0).all()
    assert ((data.retiros >= 0) & (data.retiros <= data.n)).all()
    assert np.allclose(data.tasa_pct, 100 * data.retiros / data.n, atol=1e-10, rtol=0)
    totals = data.groupby(["corte", "variable"])[["n", "retiros"]].sum()
    for _, group in totals.groupby(level="corte"):
        assert group.n.nunique() == group.retiros.nunique() == 1
    cuts = sorted(data.corte.unique())
    checked = 0
    for variable in VARIABLES:
        subset = data[data.variable.eq(variable)]
        for level, group in subset.groupby("nivel", sort=False):
            prefix = f"{ANNEX_NAMES[variable]} / {level}".replace("%", r"\%")
            rows = [line for line in annex.splitlines() if line.startswith(prefix + " &")]
            assert len(rows) == 1, prefix
            values = re.findall(r"(\d[\d,]*)/(\d[\d,]*) \(([\d,]+)%\)", rows[0].replace("\\", ""))
            assert len(values) == len(cuts), prefix
            expected = group.set_index("corte").loc[cuts]
            for (_, row), (withdrawals, n, rate) in zip(expected.iterrows(), values):
                assert int(withdrawals.replace(",", "")) == row.retiros
                assert int(n.replace(",", "")) == row.n
                assert abs(float(rate.replace(",", ".")) - row.tasa_pct) <= 0.0500001
                checked += 1
    return {"filas_csv": len(data), "celdas_anexo_cotejadas": checked,
            "conteos_y_porcentajes_coinciden": True,
            "totales_por_corte": {str(cut): {k: int(v) for k, v in group.iloc[0].items()}
                                   for cut, group in totals.groupby(level="corte")}}


def save(fig, out, stem):
    fig.savefig(out / f"{stem}.png", dpi=135, facecolor="white")
    fig.savefig(out / f"{stem}.svg", facecolor="white")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corte", type=int, default=28, choices=[7, 14, 28, 42, 56])
    parser.add_argument("--fuente", type=Path, default=ROOT / "reportes/correcciones_2026_09_10/tablas/03_niveles.csv")
    parser.add_argument("--salida", type=Path, default=ROOT / "reportes/graficos_contexto_2026_09_30")
    args = parser.parse_args()
    data = pd.read_csv(args.fuente, keep_default_na=False)
    out = args.salida
    out.mkdir(parents=True, exist_ok=True)
    checks = verify(data, (ROOT / "Plantilla_ProyAplicado/anexos.tex").read_text(encoding="utf-8"))
    current = data[data.corte.eq(args.corte) & data.variable.isin(VARIABLES)]
    denominator = current[current.variable.eq("age_band")].n.sum()
    withdrawals = current[current.variable.eq("age_band")].retiros.sum()
    baseline = withdrawals / denominator * 100
    apply_style(12)
    fig, axes = plt.subplots(2, 2, figsize=(17, 15), gridspec_kw={"height_ratios": [3, 10]})
    fig.subplots_adjust(left=.19, right=.955, top=.87, bottom=.125, wspace=.92, hspace=.40)
    fig.suptitle(f"Retiro futuro según variables de contexto · día {args.corte}", x=.035, ha="left", y=.977, fontsize=22)
    fig.text(.035, .943, f"{entero(withdrawals)} retiros posteriores al corte entre {entero(denominator)} inscripciones elegibles ({porcentaje(baseline)}).", fontsize=14)
    fig.text(.035, .917, "La línea discontinua indica el porcentaje general. Cada barra muestra el porcentaje dentro de su categoría.", fontsize=12)
    for ax, variable, title in zip(axes.flat, VARIABLES, TITLES):
        group = current[current.variable.eq(variable)]
        y = np.arange(len(group))
        ax.barh(y, group.tasa_pct, color=BLUE, height=.61)
        ax.axvline(baseline, color=MUTED, linestyle="--", linewidth=1.25)
        ax.set_yticks(y, [label(variable, str(r.nivel)) + f"\n(n = {entero(r.n)})" for r in group.itertuples()])
        ax.tick_params(axis="y", length=0, labelsize=11)
        ax.invert_yaxis()
        ax.set_xlim(0, 35)
        ax.set_xticks([0, 10, 20, 30])
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
        ax.set_xlabel("Inscripciones con retiro futuro")
        ax.set_title(title, loc="left", pad=14, fontsize=14)
        ax.grid(axis="x", color=GRID, linewidth=.7)
        ax.set_axisbelow(True)
        for i, rate in enumerate(group.tasa_pct):
            ax.text(rate + .5, i, porcentaje(rate), va="center", fontsize=11)
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
    footer = ("n = inscripciones de la categoría; una persona puede tener varias inscripciones. Retiro futuro: registrado después del corte y hasta el final del curso.\n"
              "El día 28 se utiliza como ejemplo de lectura; no se ha seleccionado una ventana óptima. Las diferencias son descriptivas, sin ajuste por otras variables.\n"
              "IMD: categorías del índice de privación del área; los porcentajes rotulan sus bandas, no ingresos personales. No disponible se conserva como categoría.\n"
              "Edad: se mantienen las bandas de OULAD. Fuente: 03_niveles.csv, versión correcciones_2026_09_10. Figura generada a partir de salidas guardadas.")
    # The caveat about the illustrative cutoff applies to any requested cutoff.
    footer = footer.replace("El día 28", f"El día {args.corte}")
    fig.text(.035, .025, footer, fontsize=10, va="bottom", linespacing=1.65)
    save(fig, out, f"barras_contexto_dia_{args.corte}")

    fig, axes = plt.subplots(2, 2, figsize=(15, 14), gridspec_kw={"height_ratios": [3, 9]})
    fig.subplots_adjust(left=.16, right=.96, top=.86, bottom=.16, wspace=.83, hspace=.46)
    fig.suptitle("Retiro futuro por categoría y día de corte", x=.03, ha="left", y=.978, fontsize=22)
    fig.text(.03, .94, "Cada celda muestra el porcentaje dentro de su categoría. Un color más oscuro indica un porcentaje mayor.", fontsize=12)
    cuts = sorted(data.corte.unique())
    for ax, variable, title in zip(axes.flat, VARIABLES, TITLES):
        group = data[data.variable.eq(variable)]
        levels = group.nivel.drop_duplicates().tolist()
        table = group.pivot(index="nivel", columns="corte", values="tasa_pct").loc[levels, cuts]
        plotted = ax.imshow(table, cmap=SEQUENTIAL, vmin=0, vmax=40, aspect="auto")
        ax.set_yticks(range(len(levels)), [label(variable, str(level)) for level in levels], fontsize=11)
        ax.set_xticks(range(len(cuts)), cuts)
        ax.set_xlabel("Día de corte")
        ax.set_title(title, loc="left", pad=14, fontsize=13)
        ax.tick_params(length=0)
        for row in range(len(levels)):
            for col in range(len(cuts)):
                rate = table.iloc[row, col]
                ax.text(col, row, f"{rate:.1f}".replace(".", ","), ha="center", va="center", fontsize=11,
                        color="white" if rate > 24 else INK)
        for spine in ax.spines.values():
            spine.set_visible(False)
    color_ax = fig.add_axes([.38, .103, .36, .014])
    colorbar = fig.colorbar(plotted, cax=color_ax, orientation="horizontal", ticks=[0, 10, 20, 30, 40])
    colorbar.ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    fig.text(.03, .025, "En cada corte cambian la población elegible y el tiempo restante hasta el final del curso: no se sigue un grupo fijo.\n"
             "Las diferencias son descriptivas; no prueban causalidad ni una mejora de la predicción al cambiar el corte.\n"
             "Los conteos exactos se conservan en la tabla del anexo. Fuente: 03_niveles.csv, versión correcciones_2026_09_10.",
             fontsize=11, linespacing=1.6)
    save(fig, out, "mapa_contexto_cinco_cortes")
    checks.update({"fuente": str(args.fuente), "sha256": hashlib.sha256(args.fuente.read_bytes()).hexdigest(),
                   "corte_barras": args.corte, "analisis_oulad_repetido": False,
                   "alcance": "Propuesta visual; documento principal sin cambios."})
    (out / "verificacion.json").write_text(json.dumps(checks, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(checks, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
