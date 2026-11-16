"""Generate every teaching diagram used in the three notebooks.

Run:  python figures/make_figures.py      (writes PNG files next to this script)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle

OUT = Path(__file__).parent

# ---------------------------------------------------------------- style
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
VIOLET, RED, MAGENTA = "#6250d6", "#e34948", "#e87ba4"
INK, INK2, MUTED, LINE = "#0b0b0b", "#52514e", "#8a8984", "#c9c8c2"
SURF = "#ffffff"


def tint(hex_color, a=0.18):
    """Mix a colour with white -> soft fill."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (int(255 - (255 - c) * a) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "text.color": INK,
    "axes.edgecolor": LINE,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "figure.facecolor": SURF,
    "savefig.facecolor": SURF,
})


def canvas(w, h, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*(xlim or (0, w)))
    ax.set_ylim(*(ylim or (0, h)))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / name, dpi=110, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("saved", name)


def box(ax, x, y, w, h, text="", color=BLUE, fs=12, mono=False, bold=False,
        fill=None, tc=INK, lw=1.8, r=0.08, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fill if fill is not None else tint(color), ec=color, lw=lw, ls=ls)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
                family="DejaVu Sans Mono" if mono else "DejaVu Sans",
                weight="bold" if bold else "normal", color=tc)
    return p


def arrow(ax, p1, p2, color=INK2, lw=1.8, style="-|>", rad=0.0, ms=16, ls="-"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=color,
                        lw=lw, connectionstyle=f"arc3,rad={rad}", ls=ls,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)


def text(ax, x, y, s, fs=12, color=INK, mono=False, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va,
            family="DejaVu Sans Mono" if mono else "DejaVu Sans", **kw)


def grid(ax, x0, y0, values, cell=0.6, colors=None, fs=12, ec=INK2, default=None):
    """Draw a 2-D array; values[0] is the TOP row. colors: same shape, fill colours or None."""
    values = np.atleast_2d(values)
    rows, cols = values.shape
    for i in range(rows):
        for j in range(cols):
            fc = default or "#f6f6f4"
            if colors is not None and colors[i][j]:
                fc = colors[i][j]
            x, y = x0 + j * cell, y0 + (rows - 1 - i) * cell
            ax.add_patch(Rectangle((x, y), cell, cell, fc=fc, ec=ec, lw=1.2))
            v = values[i, j]
            if v is not None and v != "":
                text(ax, x + cell / 2, y + cell / 2, str(v), fs=fs, mono=True)
    return rows * cell, cols * cell


# ===================================================================== S1
def roadmap():
    fig, ax = canvas(12, 3.6)
    items = [
        ("Session 1", "Python core", "types, lists, dicts\nif / for / functions\nnames & mutability\nclasses & inheritance", BLUE),
        ("Session 2", "Python for numbers", "dunder methods, generators\nNumPy arrays\nMatplotlib\nperceptron from scratch", AQUA),
        ("Session 3", "PyTorch & CNN", "tensors & autograd\nnn.Module, DataLoader\nMLP on MNIST\nCNN", ORANGE),
    ]
    for i, (s, t, body, c) in enumerate(items):
        x = 0.2 + i * 4.0
        box(ax, x, 0.2, 3.4, 3.1, color=c)
        text(ax, x + 1.7, 2.95, s, fs=11, color=INK2)
        text(ax, x + 1.7, 2.5, t, fs=15, weight="bold")
        text(ax, x + 1.7, 1.25, body, fs=11, color=INK2, linespacing=1.6)
        if i < 2:
            arrow(ax, (x + 3.45, 1.75), (x + 3.95, 1.75), lw=2.2)
    save(fig, "s1_roadmap.png")


def list_indexing():
    fig, ax = canvas(10, 3.2)
    vals = ["'a'", "'b'", "'c'", "'d'", "'e'", "'f'"]
    cell = 1.2
    x0, y0 = 1.4, 1.0
    for j, v in enumerate(vals):
        hl = 1 <= j < 4
        ax.add_patch(Rectangle((x0 + j * cell, y0), cell, cell,
                               fc=tint(ORANGE, .3) if hl else "#f6f6f4", ec=INK2, lw=1.4))
        text(ax, x0 + j * cell + cell / 2, y0 + cell / 2, v, fs=14, mono=True)
        text(ax, x0 + j * cell + cell / 2, y0 + cell + 0.3, str(j), fs=13, color=BLUE, weight="bold")
        text(ax, x0 + j * cell + cell / 2, y0 - 0.3, str(j - 6), fs=13, color=RED, weight="bold")
    text(ax, 0.2, y0 + cell + 0.3, "index", fs=11, color=BLUE, ha="left")
    text(ax, 0.2, y0 - 0.3, "negative", fs=11, color=RED, ha="left")
    text(ax, 0.2, y0 + cell / 2, "x =", fs=14, mono=True, ha="left")
    # slice bracket
    xa, xb = x0 + 1 * cell, x0 + 4 * cell
    ax.plot([xa, xa, xb, xb], [2.75, 2.9, 2.9, 2.75], color=ORANGE, lw=2)
    text(ax, (xa + xb) / 2, 3.12, "x[1:4]  ->  ['b', 'c', 'd']   (stop index 4 is NOT included)",
         fs=12, mono=True, color=INK)
    save(fig, "s1_list_indexing.png")


def names_vs_boxes():
    fig, ax = canvas(11, 3.6)
    # left: MATLAB/C box model
    text(ax, 2.6, 3.35, "C / MATLAB: variable = box", fs=13, weight="bold")
    for k, (n, y) in enumerate([("a", 1.9), ("b", 0.5)]):
        box(ax, 1.5, y, 2.6, 1.0, "[1, 2, 3]", color=MUTED, mono=True, fs=13)
        text(ax, 1.1, y + 0.5, n, fs=16, mono=True, weight="bold")
    text(ax, 2.8, 0.15, "b = a  copies the content", fs=11, color=INK2)
    ax.plot([5.4, 5.4], [0.1, 3.4], color=LINE, lw=1.2)
    # right: python names
    text(ax, 8.3, 3.35, "Python: variable = name tag", fs=13, weight="bold")
    box(ax, 8.1, 1.15, 2.6, 1.0, "[1, 2, 3]", color=BLUE, mono=True, fs=13)
    text(ax, 9.4, 0.85, "one list object", fs=10, color=INK2)
    for n, y in [("a", 2.6), ("b", 0.3)]:
        box(ax, 6.0, y, 0.9, 0.6, n, color=ORANGE, mono=True, fs=15, bold=True)
        arrow(ax, (6.95, y + 0.3), (8.05, 1.65), color=ORANGE, lw=2)
    text(ax, 7.0, 0.05, "b = a  adds a 2nd name", fs=11, color=INK2)
    save(fig, "s1_names_vs_boxes.png")


def rebind_vs_mutate():
    fig, ax = canvas(12, 3.6)
    # left: a = a + [3]
    text(ax, 2.9, 3.35, "a = a + [3]    (new object)", fs=13, mono=True, weight="bold")
    box(ax, 2.6, 1.85, 2.4, 0.8, "[1, 2]", color=BLUE, mono=True)
    box(ax, 2.6, 0.45, 2.4, 0.8, "[1, 2, 3]", color=AQUA, mono=True)
    box(ax, 0.4, 1.95, 0.8, 0.6, "b", color=ORANGE, mono=True, bold=True)
    box(ax, 0.4, 0.55, 0.8, 0.6, "a", color=ORANGE, mono=True, bold=True)
    arrow(ax, (1.25, 2.25), (2.55, 2.25), color=ORANGE)
    arrow(ax, (1.25, 0.85), (2.55, 0.85), color=ORANGE)
    arrow(ax, (1.25, 1.0), (2.55, 2.0), color=MUTED, ls="--", lw=1.2)
    text(ax, 1.9, 1.55, "moved", fs=9, color=MUTED, rotation=37)
    text(ax, 2.9, 0.1, "b still sees [1, 2]", fs=11, color=INK2)
    ax.plot([6.0, 6.0], [0.1, 3.4], color=LINE, lw=1.2)
    # right: a += [3]
    text(ax, 9.0, 3.35, "a += [3]    (in-place)", fs=13, mono=True, weight="bold")
    box(ax, 8.9, 1.15, 2.6, 0.8, "[1, 2, 3]", color=BLUE, mono=True)
    for n, y in [("b", 2.3), ("a", 0.3)]:
        box(ax, 6.7, y, 0.8, 0.6, n, color=ORANGE, mono=True, bold=True)
        arrow(ax, (7.55, y + 0.3), (8.85, 1.55), color=ORANGE)
    text(ax, 9.0, 0.1, "b sees [1, 2, 3] too", fs=11, color=INK2)
    save(fig, "s1_rebind_vs_mutate.png")


def shallow_deep():
    fig, ax = canvas(14.4, 4.2)
    def outer(x, y, color, label):
        box(ax, x, y, 1.6, 1.6, color=color)
        text(ax, x + 0.8, y + 1.9, label, fs=12, mono=True, weight="bold")
        for k in range(2):
            ax.add_patch(Circle((x + 0.8, y + 1.15 - k * 0.7), 0.13, color=color))
        return [(x + 0.93, y + 1.15), (x + 0.93, y + 0.45)]
    def inner(x, y, s, color):
        box(ax, x, y, 1.5, 0.6, s, color=color, mono=True, fs=11)
        return (x - 0.05, y + 0.3)
    # shallow
    text(ax, 2.9, 4.0, "copy.copy  (shallow)", fs=13, weight="bold")
    p1 = outer(0.2, 1.0, BLUE, "weights")
    p2 = outer(2.0, 1.0, AQUA, "shallow")
    t1, t2 = inner(4.3, 2.2, "[1, 2]", ORANGE), inner(4.3, 1.0, "[3, 4]", ORANGE)
    for src in (p1, p2):
        arrow(ax, src[0], t1, lw=1.4)
        arrow(ax, src[1], t2, lw=1.4)
    text(ax, 3.0, 0.45, "inner lists are SHARED", fs=11, color=RED)
    ax.plot([6.2, 6.2], [0.2, 4.2], color=LINE, lw=1.2)
    # deep
    text(ax, 10.3, 4.0, "copy.deepcopy  (deep)", fs=13, weight="bold")
    q1 = outer(6.6, 1.0, BLUE, "weights")
    q2 = outer(12.5, 1.0, AQUA, "deep")
    a1, a2 = inner(8.5, 2.2, "[1, 2]", ORANGE), inner(8.5, 1.0, "[3, 4]", ORANGE)
    box(ax, 10.5, 2.2, 1.4, 0.6, "[1, 2]", color=VIOLET, mono=True, fs=11)
    box(ax, 10.5, 1.0, 1.4, 0.6, "[3, 4]", color=VIOLET, mono=True, fs=11)
    arrow(ax, q1[0], a1, lw=1.4); arrow(ax, q1[1], a2, lw=1.4)
    arrow(ax, (12.95, 2.15), (11.95, 2.5), lw=1.4); arrow(ax, (12.95, 1.45), (11.95, 1.3), lw=1.4)
    text(ax, 10.3, 0.45, "everything is independent", fs=11, color=AQUA)
    save(fig, "s1_shallow_deep.png")


def function_anatomy():
    fig, ax = canvas(12, 4.0)
    cw = 0.2155  # width of one monospace char at fontsize 20, in data units
    code = [("def ", VIOLET, "keyword"), ("relu", BLUE, "name"), ("(", INK, None), ("x", ORANGE, "parameter"),
            (", ", INK, None), ("alpha=0.0", AQUA, "default value"), ("):", INK, None)]
    x0, y = 0.6, 2.6
    col, k = 0, 0
    for s_, c, note in code:
        ax.text(x0 + col * cw, y, s_, fontsize=20, family="DejaVu Sans Mono", color=c, va="center")
        if note:
            xm = x0 + (col + len(s_.strip()) / 2) * cw
            ly = 3.15 if k % 2 == 0 else 3.6
            ax.plot([xm, xm], [2.85, ly - 0.12], color=c, lw=1)
            text(ax, xm, ly, note, fs=11, color=c, weight="bold")
            k += 1
        col += len(s_)
    ind = x0 + 4 * cw
    ax.text(ind, 1.85, '"""Leaky ReLU."""', fontsize=20, family="DejaVu Sans Mono", color=MUTED, va="center")
    ax.text(ind, 1.15, "return", fontsize=20, family="DejaVu Sans Mono", color=VIOLET, va="center")
    ax.text(ind + 7 * cw, 1.15, "max(alpha * x, x)", fontsize=20, family="DejaVu Sans Mono", color=INK, va="center")
    text(ax, 7.0, 1.85, "<- docstring (help text)", fs=11, color=MUTED, ha="left")
    text(ax, 7.0, 1.15, "<- value sent back to the caller", fs=11, color=VIOLET, ha="left")
    ax.add_patch(Rectangle((ind - 0.15, 0.8), 0.03, 1.4, color=LINE))
    text(ax, 0.25, 1.5, "body\n(indented\n4 spaces)", fs=9, color=INK2)
    save(fig, "s1_function_anatomy.png")

def class_object():
    fig, ax = canvas(12, 4.4)
    box(ax, 0.3, 0.6, 3.6, 3.4, color=BLUE)
    text(ax, 2.1, 3.65, "class Neuron", fs=14, mono=True, weight="bold")
    text(ax, 2.1, 3.25, "(blueprint)", fs=11, color=INK2)
    text(ax, 0.6, 2.55, "state:\n   self.w\n   self.b", fs=12, mono=True, ha="left", va="center")
    text(ax, 0.6, 1.25, "behaviour:\n   forward(x)", fs=12, mono=True, ha="left", va="center")
    objs = [("n1", "w = 2.0\nb = 1.0", 3.0), ("n2", "w = -1.0\nb = 0.0", 1.6), ("n3", "w = 0.5\nb = 0.3", 0.2)]
    for name, st, y in objs:
        box(ax, 6.8, y, 2.4, 1.2, st, color=AQUA, mono=True, fs=11)
        text(ax, 9.7, y + 0.6, name, fs=14, mono=True, weight="bold", color=ORANGE)
        arrow(ax, (3.95, 2.3), (6.75, y + 0.6), color=INK2, lw=1.5)
    text(ax, 5.3, 3.95, "Neuron(w, b)\ncreates an object", fs=11, color=INK2)
    text(ax, 8.0, 4.35, "objects (instances)", fs=12, weight="bold")
    text(ax, 11.6, 1.8, "same methods,\ndifferent data", fs=11, color=INK2)
    ax.set_xlim(0, 12.6)
    save(fig, "s1_class_object.png")


def inheritance():
    fig, ax = canvas(12, 4.6)
    box(ax, 3.9, 3.0, 4.2, 1.4, color=BLUE)
    text(ax, 6.0, 4.05, "Module   (parent)", fs=13, mono=True, weight="bold")
    text(ax, 6.0, 3.45, "__call__(x)  ->  self.forward(x)", fs=11, mono=True, color=INK2)
    kids = [("Linear(Module)", "forward: w*x + b", 0.2), ("ReLU(Module)", "forward: max(0, x)", 4.2),
            ("Net(Module)", "forward: fc2(relu(fc1(x)))", 8.2)]
    for name, body, x in kids:
        box(ax, x, 0.4, 3.6, 1.4, color=AQUA)
        text(ax, x + 1.8, 1.4, name, fs=12, mono=True, weight="bold")
        text(ax, x + 1.8, 0.85, body, fs=10, mono=True, color=INK2)
        arrow(ax, (x + 1.8, 1.85), (6.0, 2.95), color=INK2, lw=1.6)
    text(ax, 10.2, 2.55, "inherits __call__", fs=11, color=INK2, style="italic")
    text(ax, 1.4, 2.55, "children write only forward()", fs=11, color=INK2, style="italic")
    save(fig, "s1_inheritance.png")


# ===================================================================== S2
def dunder_dispatch():
    fig, ax = canvas(12, 4.2)
    rows = [("a + b", "a.__add__(b)"), ("a @ b", "a.__matmul__(b)"), ("x[0, 1:3]", "x.__getitem__((0, slice(1, 3)))"),
            ("len(d)", "d.__len__()"), ("model(x)", "model.__call__(x)")]
    for i, (l, r) in enumerate(rows):
        y = 3.5 - i * 0.8
        box(ax, 0.3, y - 0.3, 2.8, 0.6, l, color=ORANGE, mono=True, fs=13)
        box(ax, 5.2, y - 0.3, 6.4, 0.6, r, color=BLUE, mono=True, fs=13)
        arrow(ax, (3.15, y), (5.15, y), lw=1.8)
    text(ax, 1.7, 4.15, "you write", fs=12, weight="bold")
    text(ax, 8.4, 4.15, "Python actually calls", fs=12, weight="bold")
    save(fig, "s2_dunder_dispatch.png")


def loader_batches():
    fig, ax = canvas(12, 4.0)
    cell = 0.8
    text(ax, 0.2, 3.55, "dataset (len = 10)", fs=12, ha="left", weight="bold")
    for j in range(10):
        ax.add_patch(Rectangle((0.2 + j * cell, 2.6), cell, cell, fc="#f6f6f4", ec=INK2))
        text(ax, 0.2 + j * cell + cell / 2, 3.0, str(j), fs=13, mono=True)
    order = [7, 2, 9, 0, 4, 1, 8, 5, 3, 6]
    cols = [BLUE] * 4 + [AQUA] * 4 + [ORANGE] * 2
    text(ax, 0.2, 1.75, "shuffle -> cut into batches of 4", fs=12, ha="left", weight="bold")
    x = 0.2
    for k, (idx, c) in enumerate(zip(order, cols)):
        if k in (4, 8):
            x += 0.4
        ax.add_patch(Rectangle((x, 0.6), cell, cell, fc=tint(c, .35), ec=c, lw=1.6))
        text(ax, x + cell / 2, 1.0, str(idx), fs=13, mono=True)
        x += cell
    for label, x0, n, c in [("batch 1", 0.2, 4, BLUE), ("batch 2", 3.8, 4, AQUA), ("batch 3", 7.4, 2, ORANGE)]:
        text(ax, x0 + n * cell / 2, 0.3, label, fs=11, color=c, weight="bold")
    text(ax, 10.6, 1.0, "<- the last batch\n    can be smaller", fs=10, color=INK2, ha="left")
    arrow(ax, (4.2, 2.55), (4.2, 2.0), lw=1.6)
    ax.set_xlim(0, 12.6)
    save(fig, "s2_loader_batches.png")


def ndarray_dims():
    fig, ax = canvas(12, 4.0)
    # 1D
    grid(ax, 0.3, 1.6, [[1, 2, 3, 4]], cell=0.6, default=tint(BLUE, .25))
    text(ax, 1.5, 0.9, "1-D   shape (4,)", fs=12, mono=True)
    text(ax, 1.5, 0.45, "a vector", fs=11, color=INK2)
    # 2D
    grid(ax, 3.6, 1.3, np.arange(12).reshape(3, 4), cell=0.5, default=tint(AQUA, .25))
    text(ax, 4.6, 0.9, "2-D   shape (3, 4)", fs=12, mono=True)
    text(ax, 4.6, 0.45, "rows x cols (a table)", fs=11, color=INK2)
    ax.annotate("", xy=(3.55, 1.3), xytext=(3.55, 2.8), arrowprops=dict(arrowstyle="<-", color=RED, lw=1.6))
    text(ax, 3.3, 2.05, "axis 0", fs=10, color=RED, rotation=90)
    ax.annotate("", xy=(3.6, 2.9), xytext=(5.6, 2.9), arrowprops=dict(arrowstyle="<-", color=VIOLET, lw=1.6))
    text(ax, 4.6, 3.1, "axis 1", fs=10, color=VIOLET)
    # 3D: stacked sheets
    for k in range(3)[::-1]:
        ox, oy = 7.9 + k * 0.35, 1.3 + k * 0.35
        grid(ax, ox, oy, np.full((3, 4), ""), cell=0.45, default=tint(ORANGE, .2 + .15 * (2 - k)))
    text(ax, 9.6, 0.9, "3-D   shape (3, 3, 4)", fs=12, mono=True)
    text(ax, 9.6, 0.45, "e.g. a batch of 3 small images", fs=11, color=INK2)
    save(fig, "s2_ndarray_dims.png")


def slicing_2d():
    m = np.arange(12).reshape(3, 4)
    fig, ax = canvas(12, 3.4)
    specs = [("m[1]", lambda i, j: i == 1, BLUE), ("m[:, 2]", lambda i, j: j == 2, AQUA),
             ("m[:2, 1:3]", lambda i, j: i < 2 and 1 <= j < 3, ORANGE), ("m[m > 8]", lambda i, j: m[i, j] > 8, VIOLET)]
    for k, (title, f, c) in enumerate(specs):
        x0 = 0.3 + k * 3.0
        colors = [[tint(c, .45) if f(i, j) else None for j in range(4)] for i in range(3)]
        grid(ax, x0, 0.5, m, cell=0.55, colors=colors, fs=11)
        text(ax, x0 + 1.1, 2.4, title, fs=13, mono=True, weight="bold")
    save(fig, "s2_slicing_2d.png")


def view_vs_copy():
    fig, ax = canvas(11, 3.2)
    grid(ax, 2.5, 1.2, [[100, 1, 2, 3, 4, 5]], cell=0.75,
         colors=[[tint(ORANGE, .5), tint(ORANGE, .25), tint(ORANGE, .25), None, None, None]])
    text(ax, 1.3, 1.57, "memory", fs=12, color=INK2)
    box(ax, 0.2, 2.45, 1.2, 0.55, "data", color=BLUE, mono=True, bold=True)
    box(ax, 5.4, 2.45, 1.2, 0.55, "view", color=ORANGE, mono=True, bold=True)
    arrow(ax, (1.45, 2.6), (2.6, 1.98), color=BLUE)
    arrow(ax, (5.35, 2.6), (3.4, 1.98), color=ORANGE)
    text(ax, 2.5 + 1.1, 0.85, "view = data[:3]", fs=12, mono=True)
    text(ax, 2.5 + 2.25, 0.4, "view[0] = 100 changes data too (same memory)", fs=11, color=RED)
    save(fig, "s2_view_vs_copy.png")


def axis_sum():
    m = np.arange(12).reshape(3, 4)
    fig, ax = canvas(12, 3.8)
    # axis 0
    grid(ax, 0.6, 1.0, m, cell=0.6, default=tint(BLUE, .15))
    for j in range(4):
        arrow(ax, (0.9 + j * 0.6, 2.75), (0.9 + j * 0.6, 0.95), color=BLUE, lw=1.4, ms=10)
    grid(ax, 0.6, 0.1, [m.sum(0)], cell=0.6, default=tint(BLUE, .45))
    text(ax, 1.8, 3.3, "m.sum(axis=0)  ->  shape (4,)", fs=12, mono=True, weight="bold")
    text(ax, 4.3, 0.4, "one number\nper column", fs=10, color=INK2, ha="left")
    # axis 1
    grid(ax, 7.0, 1.0, m, cell=0.6, default=tint(ORANGE, .15))
    for i in range(3):
        arrow(ax, (7.0, 2.5 - i * 0.6 + 0.1 - 0.1), (9.45, 2.5 - i * 0.6), color=ORANGE, lw=1.4, ms=10)
    grid(ax, 9.7, 1.0, m.sum(1).reshape(3, 1), cell=0.6, default=tint(ORANGE, .45))
    text(ax, 8.5, 3.3, "m.sum(axis=1)  ->  shape (3,)", fs=12, mono=True, weight="bold")
    text(ax, 10.45, 1.9, "one number\nper row", fs=10, color=INK2, ha="left")
    text(ax, 6.0, -0.3, "rule: the axis you name is the one that DISAPPEARS", fs=12, color=RED)
    ax.set_ylim(-0.6, 3.8)
    save(fig, "s2_axis_sum.png")


def reshape_fig():
    fig, ax = canvas(12, 3.2)
    colors = [tint(c, .4) for c in [BLUE, AQUA, ORANGE, VIOLET] * 3]
    flat = np.arange(12)
    grid(ax, 0.2, 2.2, [flat], cell=0.55, colors=[colors], fs=10)
    text(ax, 3.5, 3.0, "np.arange(12)   shape (12,)", fs=12, mono=True)
    grid(ax, 1.0, 0.1, flat.reshape(3, 4), cell=0.55, colors=np.array(colors).reshape(3, 4).tolist(), fs=10)
    text(ax, 2.1, 1.95, ".reshape(3, 4)", fs=12, mono=True)
    grid(ax, 5.0, 0.1 - 0.0, flat.reshape(4, 3)[:, :], cell=0.42, colors=np.array(colors).reshape(4, 3).tolist(), fs=9)
    text(ax, 5.65, 1.95, ".reshape(4, -1)", fs=12, mono=True)
    text(ax, 9.6, 1.2, "same 12 numbers,\nsame order,\nnew shape", fs=12, color=INK2)
    arrow(ax, (0.7, 2.15), (0.95, 1.7), lw=1.4)
    save(fig, "s2_reshape.png")


def broadcasting():
    fig, ax = canvas(12, 4.0)
    def panel(x0, A, B, title):
        grid(ax, x0, 1.4, A, cell=0.5, default=tint(BLUE, .25), fs=10)
        text(ax, x0 + 2.25, 2.0, "+", fs=18)
        bv = np.atleast_2d(B)
        real = [[tint(ORANGE, .5)] * bv.shape[1] for _ in range(bv.shape[0])]
        full = np.broadcast_to(bv, (3, 4))
        cols = [[tint(ORANGE, .5) if (i < bv.shape[0] and j < bv.shape[1]) else tint(ORANGE, .15)
                 for j in range(4)] for i in range(3)]
        grid(ax, x0 + 2.6, 1.4, full, cell=0.5, colors=cols, fs=10, ec=MUTED)
        text(ax, x0 + 2.4, 3.4, title, fs=12, mono=True, weight="bold")
    A = np.zeros((3, 4), dtype=int)
    panel(0.2, A, np.array([[10, 20, 30, 40]]), "(3, 4) + (4,)")
    panel(6.4, A, np.array([[1], [2], [3]]), "(3, 4) + (3, 1)")
    text(ax, 6.2, 0.75, "dark = the real data,  light = virtually repeated (no memory copy)", fs=11, color=INK2)
    text(ax, 6.2, 0.25, "compare shapes from the RIGHT: each pair must be equal, or one of them must be 1",
         fs=11, color=RED)
    save(fig, "s2_broadcasting.png")


def matmul_shapes():
    fig, ax = canvas(12, 3.8)
    box(ax, 0.3, 0.6, 1.6, 2.6, "X\n(N, in)\n5 x 3", color=BLUE, fs=12, mono=True)
    text(ax, 2.25, 1.9, "@", fs=22)
    box(ax, 2.6, 1.4, 1.6, 1.0, "W\n(in, out)\n3 x 2", color=AQUA, fs=11, mono=True)
    text(ax, 4.55, 1.9, "+", fs=22)
    box(ax, 4.9, 1.65, 1.2, 0.5, "b  (out,)", color=VIOLET, fs=10, mono=True)
    text(ax, 6.45, 1.9, "=", fs=22)
    box(ax, 6.8, 0.6, 1.1, 2.6, "Y\n(N, out)\n5 x 2", color=ORANGE, fs=11, mono=True)
    ax.plot([1.45, 1.45], [3.35, 3.55], color=RED, lw=2); ax.plot([2.85, 2.85], [3.35, 3.55], color=RED, lw=2)
    ax.plot([1.45, 2.85], [3.55, 3.55], color=RED, lw=2)
    text(ax, 2.15, 3.75, "must match", fs=11, color=RED)
    text(ax, 10.2, 2.4, "(5, 3) @ (3, 2) -> (5, 2)", fs=12, mono=True)
    text(ax, 10.2, 1.8, "inner numbers vanish,", fs=11, color=INK2)
    text(ax, 10.2, 1.4, "outer numbers remain", fs=11, color=INK2)
    text(ax, 10.2, 0.8, "this IS one neural-net layer", fs=11, color=INK2, style="italic")
    ax.set_ylim(0.2, 4.0)
    save(fig, "s2_matmul_shapes.png")


def matplotlib_anatomy():
    fig, ax = plt.subplots(figsize=(9, 5))
    e = np.arange(1, 31)
    ax.plot(e, np.exp(-e / 8), color=BLUE, lw=2, label="train")
    ax.plot(e, np.exp(-e / 8) + 0.1, color=ORANGE, lw=2, label="validation")
    ax.set_title("loss curve"); ax.set_xlabel("epoch"); ax.set_ylabel("loss")
    leg = ax.legend(loc="upper right", frameon=True, edgecolor=LINE); ax.grid(alpha=.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.patch.set_edgecolor(VIOLET); fig.patch.set_linewidth(3)
    fig.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.88)
    kw = dict(fontsize=11, family="DejaVu Sans Mono", color=RED, va="center",
              arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4, shrinkA=4, shrinkB=4),
              annotation_clip=False)
    # every arrow is anchored to the real artist, so it always lands on the right element
    ax.annotate("ax.set_title(...)", xy=(1.0, 0.5), xycoords=ax.title,
                xytext=(40, 0), textcoords="offset points", ha="left", **kw)
    ax.annotate("ax.legend()", xy=(0.0, 0.5), xycoords=leg,
                xytext=(0.5, 0.80), textcoords="axes fraction", ha="center", **kw)
    ax.annotate("ax.plot(x, y, label=...)", xy=(6, np.exp(-6 / 8) + 0.1),
                xytext=(0.38, 0.6), textcoords="axes fraction", ha="left", **kw)
    ax.annotate("ax.set_ylabel(...)", xy=(1.0, 0.5), xycoords=ax.yaxis.label,
                xytext=(0.05, 0.22), textcoords="axes fraction", ha="left", **kw)
    ax.annotate("ax.set_xlabel(...)", xy=(1.0, 0.5), xycoords=ax.xaxis.label,
                xytext=(60, 0), textcoords="offset points", ha="left", **kw)
    fig.text(0.975, 0.5, "fig  (the whole window)", rotation=90, va="center", color=VIOLET, fontsize=11)
    fig.text(0.5, 0.03, "ax = one plotting area inside the figure  ( fig, ax = plt.subplots() )",
             ha="center", color=INK2, fontsize=11)
    save(fig, "s2_matplotlib_anatomy.png")


def perceptron_fig():
    fig, ax = canvas(12, 4.0)
    for i, (n, y) in enumerate([("x1", 3.0), ("x2", 1.8), ("1", 0.6)]):
        ax.add_patch(Circle((0.9, y), 0.38, fc=tint(BLUE, .3), ec=BLUE, lw=1.8))
        text(ax, 0.9, y, n, fs=13, mono=True)
        lbl = ["w1", "w2", "b"][i]
        arrow(ax, (1.3, y), (4.25, 1.8), color=INK2, lw=1.6)
        text(ax, 2.6, (y + 1.8) / 2 + 0.18, lbl, fs=12, mono=True, color=ORANGE, weight="bold")
    ax.add_patch(Circle((4.7, 1.8), 0.45, fc=tint(AQUA, .3), ec=AQUA, lw=1.8))
    text(ax, 4.7, 1.8, "Σ", fs=20)
    arrow(ax, (5.2, 1.8), (6.4, 1.8), lw=1.6)
    box(ax, 6.45, 1.35, 1.4, 0.9, "sign", color=VIOLET, fs=13, mono=True)
    arrow(ax, (7.9, 1.8), (8.9, 1.8), lw=1.6)
    text(ax, 9.3, 1.8, "y ∈ {-1, +1}", fs=13, mono=True, ha="left")
    text(ax, 6.0, 3.6, "y = sign(x · w + b)", fs=15, mono=True, weight="bold")
    text(ax, 5.0, 0.45, "if wrong:  w ← w + η·t·x ,   b ← b + η·t", fs=12, mono=True, color=INK2, ha="left")
    save(fig, "s2_perceptron.png")


# ===================================================================== S3
def tensor_nchw():
    fig, ax = canvas(12, 4.2)
    cols = [tint(RED, .45), tint(AQUA, .45), tint(BLUE, .45)]
    for n in range(3):
        bx = 0.6 + n * 2.9
        for c in range(3)[::-1]:
            ox, oy = bx + c * 0.28, 0.7 + c * 0.28
            ax.add_patch(Rectangle((ox, oy), 1.9, 1.9, fc=cols[c], ec=INK2, lw=1.2))
        text(ax, bx + 1.2, 3.75, f"image {n}", fs=12, weight="bold")
    text(ax, 1.55, 0.4, "W (width)", fs=11, color=INK2)
    text(ax, 0.3, 1.65, "H (height)", fs=11, color=INK2, rotation=90)
    text(ax, 1.8, 3.4, "C = 3 channels (R, G, B)", fs=10, color=INK2)
    text(ax, 10.4, 2.6, "(N, C, H, W)", fs=16, mono=True, weight="bold")
    text(ax, 10.4, 2.0, "= (3, 3, 32, 32)", fs=13, mono=True, color=INK2)
    text(ax, 10.4, 1.2, "MNIST batch:\n(128, 1, 28, 28)", fs=11, mono=True, color=INK2)
    ax.set_xlim(0, 12.2)
    save(fig, "s3_tensor_nchw.png")

def comp_graph():
    fig, ax = canvas(12, 4.4)
    def node(x, y, s, c, r=0.45):
        ax.add_patch(Circle((x, y), r, fc=tint(c, .3), ec=c, lw=1.8))
        text(ax, x, y, s, fs=13, mono=True)
    node(1.0, 2.2, "w=3", BLUE, .55)
    node(4.2, 3.3, "w²", AQUA); node(4.2, 1.1, "2w", AQUA)
    node(7.2, 2.2, "+", VIOLET)
    node(10.0, 2.2, "y=15", ORANGE, .6)
    for a, b in [((1.55, 2.4), (3.75, 3.2)), ((1.55, 2.0), (3.75, 1.2)), ((4.65, 3.2), (6.75, 2.35)),
                 ((4.65, 1.2), (6.75, 2.05)), ((7.65, 2.2), (9.4, 2.2))]:
        arrow(ax, a, b, color=INK2, lw=1.8)
    # backward (red) with local derivatives
    for a, b, lbl, pos in [((6.8, 2.7), (4.5, 3.75), "×1", (5.9, 3.65)), ((6.8, 1.7), (4.5, 0.65), "×1", (5.9, 0.75)),
                           ((3.8, 3.75), (1.2, 2.85), "×2w = 6", (2.2, 3.75)), ((3.8, 0.65), (1.2, 1.55), "×2", (2.3, 0.7))]:
        arrow(ax, a, b, color=RED, lw=1.5, rad=0.25, ls="--")
        text(ax, *pos, lbl, fs=11, color=RED, mono=True)
    text(ax, 8.5, 3.9, "forward  →   (black)", fs=11, color=INK2, ha="left")
    text(ax, 8.5, 3.5, "backward ←   (red)", fs=11, color=RED, ha="left")
    text(ax, 1.0, 0.15, "w.grad = 6 + 2 = 8   (chain rule: multiply along a path, add the paths)",
         fs=12, mono=True, color=RED, ha="left", weight="bold")
    save(fig, "s3_comp_graph.png")

def train_loop():
    fig, ax = canvas(12, 6.0)
    steps = [("1. logits = model(x)", "forward pass", BLUE), ("2. loss = loss_fn(logits, y)", "how wrong are we?", AQUA),
             ("3. optimizer.zero_grad()", "clear old gradients", YELLOW), ("4. loss.backward()", "compute new gradients", VIOLET),
             ("5. optimizer.step()", "update the weights", ORANGE)]
    cx, cy, rx, ry = 6.0, 3.0, 4.0, 2.3
    angs = np.deg2rad(90 - np.arange(5) * 72)
    pts = [(cx + rx * np.cos(a), cy + ry * np.sin(a)) for a in angs]
    for (s_, sub, c), (x, y) in zip(steps, pts):
        box(ax, x - 1.85, y - 0.42, 3.7, 0.84, color=c)
        text(ax, x, y + 0.13, s_, fs=11, mono=True)
        text(ax, x, y - 0.22, sub, fs=9.5, color=INK2)
    for k in range(5):
        p1, p2 = np.array(pts[k]), np.array(pts[(k + 1) % 5])
        arrow(ax, tuple(p1 + 0.33 * (p2 - p1)), tuple(p1 + 0.67 * (p2 - p1)), lw=1.8, rad=-0.2)
    text(ax, cx, cy + 0.15, "for x, y in loader:", fs=13, mono=True, weight="bold")
    text(ax, cx, cy - 0.3, "(repeat for every batch)", fs=10, color=INK2)
    save(fig, "s3_train_loop.png")

def mlp_arch():
    fig, ax = canvas(12, 4.2)
    layers = [(784, 6, BLUE, "input\n784 = 28x28"), (128, 5, AQUA, "hidden\n128 + ReLU"), (10, 4, ORANGE, "output\n10 logits")]
    xs = [1.5, 5.5, 9.5]
    pos = []
    for (n, show, c, lbl), x in zip(layers, xs):
        ys = np.linspace(3.5, 0.9, show)
        pts = []
        for k, y in enumerate(ys):
            if k == show - 2:
                text(ax, x, y, "⋮", fs=16, color=INK2); continue
            ax.add_patch(Circle((x, y), 0.18, fc=tint(c, .4), ec=c, lw=1.5))
            pts.append((x, y))
        pos.append(pts)
        text(ax, x, 0.3, lbl, fs=11)
    for a, b in [(0, 1), (1, 2)]:
        for p in pos[a]:
            for q in pos[b]:
                ax.plot([p[0] + .18, q[0] - .18], [p[1], q[1]], color=LINE, lw=0.8, zorder=0)
    text(ax, 3.5, 3.95, "nn.Linear(784, 128)", fs=11, mono=True, color=INK2)
    text(ax, 7.5, 3.95, "nn.Linear(128, 10)", fs=11, mono=True, color=INK2)
    box(ax, -0.5, 1.4, 1.1, 1.1, color=MUTED)
    text(ax, 0.05, 1.95, "28x28", fs=9, color=INK2)
    arrow(ax, (0.65, 1.95), (1.2, 1.95), lw=1.2)
    text(ax, 0.05, 2.75, "flatten", fs=9, color=INK2)
    ax.set_xlim(-0.7, 11)
    save(fig, "s3_mlp_arch.png")


def conv_sliding():
    rng = np.random.default_rng(3)
    img = rng.integers(0, 4, (5, 5))
    k = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    out = np.array([[(img[i:i + 3, j:j + 3] * k).sum() for j in range(3)] for i in range(3)])
    fig, ax = canvas(12, 4.2)
    cols = [[tint(BLUE, .45) if (i < 3 and 1 <= j < 4) else None for j in range(5)] for i in range(5)]
    grid(ax, 0.3, 0.6, img, cell=0.6, colors=cols)
    ax.add_patch(Rectangle((0.3 + 0.6, 0.6 + 1.2), 1.8, 1.8, fill=False, ec=BLUE, lw=3))
    text(ax, 1.8, 3.9, "input 5x5", fs=12, weight="bold")
    text(ax, 4.0, 2.1, "*", fs=24)
    grid(ax, 4.5, 1.2, k, cell=0.6, default=tint(VIOLET, .3))
    text(ax, 5.4, 3.3, "kernel 3x3", fs=12, weight="bold")
    text(ax, 5.4, 0.85, "(learned weights)", fs=10, color=INK2)
    text(ax, 6.9, 2.1, "=", fs=24)
    ocols = [[tint(ORANGE, .55) if (i == 0 and j == 1) else None for j in range(3)] for i in range(3)]
    grid(ax, 7.4, 1.2, out, cell=0.6, colors=ocols)
    text(ax, 8.3, 3.3, "output 3x3", fs=12, weight="bold")
    arrow(ax, (2.75, 3.35), (7.95 + 0.3, 2.95), color=ORANGE, rad=-0.25, lw=1.6)
    text(ax, 9.5, 2.1, "multiply the\nblue window by\nthe kernel, sum\n→ one number.\nThen slide.",
         fs=10.5, color=INK2, ha="left")
    text(ax, 6.0, 0.15, "out = (5 - 3) / 1 + 1 = 3     (no padding, stride 1)", fs=11, mono=True, color=INK2)
    ax.set_xlim(0, 12.2)
    save(fig, "s3_conv_sliding.png")


def maxpool_fig():
    m = np.array([[1, 3, 2, 0], [5, 2, 1, 4], [0, 1, 6, 2], [3, 2, 1, 1]])
    c = [BLUE, AQUA, ORANGE, VIOLET]
    cols = [[tint(c[(i // 2) * 2 + j // 2], .35) for j in range(4)] for i in range(4)]
    fig, ax = canvas(10, 3.4)
    grid(ax, 0.5, 0.3, m, cell=0.65, colors=cols)
    text(ax, 1.8, 3.15, "4x4 feature map", fs=12, weight="bold")
    arrow(ax, (3.4, 1.6), (5.0, 1.6), lw=1.8)
    text(ax, 4.2, 1.95, "MaxPool2d(2)", fs=11, mono=True)
    out = m.reshape(2, 2, 2, 2).max(axis=(1, 3))
    ocols = [[tint(c[i * 2 + j], .6) for j in range(2)] for i in range(2)]
    grid(ax, 5.4, 0.95, out, cell=0.65, colors=ocols)
    text(ax, 6.05, 2.6, "2x2", fs=12, weight="bold")
    text(ax, 7.6, 1.6, "keep the max of\neach 2x2 block\n→ H and W halve", fs=11, color=INK2, ha="left")
    save(fig, "s3_maxpool.png")


def cnn_pipeline():
    fig, ax = canvas(13, 4.4)
    stages = [("input", "1x28x28", 1, 2.4, MUTED), ("conv+ReLU", "16x28x28", 4, 2.4, BLUE),
              ("pool", "16x14x14", 4, 1.4, BLUE), ("conv+ReLU", "32x14x14", 6, 1.4, AQUA),
              ("pool", "32x7x7", 6, 0.8, AQUA)]
    x = 0.3
    for name, shape, nsheets, size, c in stages:
        for s in range(nsheets)[::-1]:
            ax.add_patch(Rectangle((x + s * 0.1, 1.0 + s * 0.1), size * 0.55, size, fc=tint(c, .25 + .05 * s),
                                   ec=c, lw=1))
        cx = x + size * 0.275 + nsheets * 0.05
        text(ax, cx, 0.65, name, fs=10.5, weight="bold")
        text(ax, cx, 0.3, shape, fs=10, mono=True, color=INK2)
        x += size * 0.55 + nsheets * 0.1 + 0.9
        arrow(ax, (x - 0.8, 2.0), (x - 0.15, 2.0), lw=1.4, ms=12)
    # flatten + linear
    box(ax, x, 0.9, 0.35, 2.6, color=VIOLET)
    text(ax, x + 0.18, 0.65, "flatten", fs=10.5, weight="bold"); text(ax, x + 0.18, 0.3, "1568", fs=10, mono=True, color=INK2)
    x += 1.2
    arrow(ax, (x - 0.8, 2.0), (x - 0.15, 2.0), lw=1.4, ms=12)
    box(ax, x, 1.4, 0.35, 1.3, color=ORANGE)
    text(ax, x + 0.18, 0.65, "linear", fs=10.5, weight="bold"); text(ax, x + 0.18, 0.3, "10", fs=10, mono=True, color=INK2)
    text(ax, 3.7, 4.05, "features: detect patterns (edges → strokes → parts)", fs=11, color=INK2)
    text(ax, x - 0.6, 4.05, "classifier", fs=11, color=INK2)
    ax.set_xlim(0, x + 0.8)
    save(fig, "s3_cnn_pipeline.png")


if __name__ == "__main__":
    for f in [roadmap, list_indexing, names_vs_boxes, rebind_vs_mutate, shallow_deep, function_anatomy,
              class_object, inheritance, dunder_dispatch, loader_batches, ndarray_dims, slicing_2d,
              view_vs_copy, axis_sum, reshape_fig, broadcasting, matmul_shapes, matplotlib_anatomy,
              perceptron_fig, tensor_nchw, comp_graph, train_loop, mlp_arch, conv_sliding, maxpool_fig,
              cnn_pipeline]:
        f()
