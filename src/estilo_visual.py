"""Estilo compartido de figuras; no transforma datos ni decisiones analíticas."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgb, to_hex
from cycler import cycler

CONFIG = json.loads((Path(__file__).resolve().parents[1] / 'estilo_visual_javeriana.json').read_text(encoding='utf-8'))
BLUE, ACCENT = CONFIG['azul'], CONFIG['acento']
INK, MUTED, GRAY, GRID = [CONFIG[k] for k in ['texto', 'texto_secundario', 'gris', 'rejilla']]


def tint(color, white_fraction):
    return to_hex(tuple((1-white_fraction)*c+white_fraction for c in to_rgb(color)))


PALE = tint(BLUE, .95)
SERIES = [BLUE, ACCENT, MUTED, tint(BLUE, .35), CONFIG['azul_oscuro']]
LINES = ['-', '--', '-.', ':', (0, (5, 2, 1, 2))]
MARKERS = ['o', 's', 'D', '^', 'v']
SEQUENTIAL = LinearSegmentedColormap.from_list('javeriana_azul', [PALE, tint(BLUE, .48), BLUE])


def apply_style(font_size=10):
    family = CONFIG['fuente_graficos']
    font_dir = Path('C:/Windows/Fonts')
    if (font_dir / 'arial.ttf').exists():
        for filename in ['arial.ttf', 'arialbd.ttf', 'ariali.ttf', 'arialbi.ttf']:
            font_manager.fontManager.addfont(font_dir / filename)
    elif not any(f.name == family for f in font_manager.fontManager.ttflist):
        family = CONFIG['fuente_alternativa']
    plt.rcParams.update({'font.family': family, 'font.size': font_size,
        'axes.spines.top': False, 'axes.spines.right': False,
        'axes.titlelocation': 'left', 'axes.titlecolor': BLUE, 'axes.titleweight': 'bold',
        'axes.labelcolor': INK, 'text.color': INK, 'xtick.color': MUTED, 'ytick.color': MUTED,
        'axes.edgecolor': GRAY, 'grid.color': GRID, 'grid.alpha': 1,
        'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'legend.frameon': False, 'pdf.fonttype': 42, 'svg.fonttype': 'none',
        'axes.prop_cycle': cycler(color=SERIES), 'figure.dpi': 110})
    return family


def line_style(index, markers=True):
    style = {'color': SERIES[index % 5], 'linestyle': LINES[index % 5], 'linewidth': 1.8}
    if markers:
        style.update(marker=MARKERS[index % 5], markersize=5,
                     markeredgecolor=SERIES[index % 5], markeredgewidth=.6)
    return style


def sequential_text(value, max_value=100):
    rgb = SEQUENTIAL(value / max_value)[:3]
    linear = [c / 12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    lum = sum(a*b for a,b in zip(linear, [.2126, .7152, .0722]))
    return 'white' if 1.05/(lum+.05) > (lum+.05)/.05 else 'black'
