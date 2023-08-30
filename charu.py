# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as pyplot
import mpl_toolkits
import numpy as np
import subprocess
import warnings
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path
from fractions import Fraction

__all__ = []

# Some of these parameter choices come from
#
#   Yi-Xin Liu's mpltex: https://github.com/liuyxpp/mpltex
#   John Garrett's SciencePlots: https://github.com/garrettj403/SciencePlots
#   Johannes Meyer's rsmf: https://github.com/johannesjmeyer/rsmf
#
# And the global list of rcParams is at:
#
#   https://matplotlib.org/stable/api/matplotlib_configuration_api.html

# Point to inch conversion as Matplotlib only accepts dimensions in
# inches: 72 pt = 1 inch.
pt = 1.0 / 72.0

# Golden ratio.
golden = 1.618033

CHARU_RC = {
    "charu.doc.common": {
        "axes.linewidth": 0.5,
        "axes.titlepad": 10,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "sans-serif"],
        "grid.color": "#cccccc",
        "grid.linestyle": "--",
        "grid.linewidth": 0.5,
        "legend.fontsize": 9.0,
        "legend.frameon": False,
        "lines.linewidth": 0.75,
        "lines.markersize": 1.5,
        "contour.linewidth": 0.75,
        "mathtext.fontset": "stixsans",
        "savefig.dpi": 600,
        "xtick.major.width": 0.5,
        "xtick.minor.visible": True,
        "xtick.minor.width": 0.5,
        "ytick.major.width": 0.5,
        "ytick.minor.visible": True,
        "ytick.minor.width": 0.5,
        "scatter.edgecolors": "none",
    },

    # For usage with REVTeX.
    "charu.doc.aps": {
        "figure.figsize": [246 * pt, 246 / golden * pt],
        "figure.widefigsize": [505 * pt, 246 * 0.75 * pt],
        "font.size": 8.0,
        "legend.fontsize": 7.5,
        "legend.handlelength": 1.45,
        "legend.labelspacing": 0.2,
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
    },

    # For usage with RSPA.
    "charu.doc.rspa": {
        "figure.figsize": [400 * 0.5 * pt, 400 * 0.5 / golden * pt],
        "font.size": 8.0,
        "legend.fontsize": 7.5,
        "legend.handlelength": 1.45,
        "legend.labelspacing": 0.2,
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
    },

    # For usage with the standard LaTeX classes article, book, etc.
    "charu.doc.standard": {
        "figure.figsize": [260 * pt, 260 / golden * pt],
        "figure.widefigsize": [315 * pt, 315 / golden * pt],
        "font.size": 8.0
    },

    # Matplotlib loads certain LaTeX package according to the sans and serif
    # fonts we set.  These packages often conflict with the ones that we
    # load in the custom preamble, so we blank the sans and serif fonts.
    "charu.tex.font.common": {
        "font.sans-serif": "",
        "font.serif": "",
    },
    "charu.tex.font.lmodern": {
        "text.latex.preamble": r"\usepackage{amsfonts,amssymb,bm,lmodern}",
        "font.family": "serif"
    },
    "charu.tex.font.cmbright": {
        "text.latex.preamble": r"\usepackage{amsfonts,amssymb,bm,cmbright}"
    },
    "charu.tex.font.fourier": {
        "text.latex.preamble": r"""\usepackage{fourierx}
        \usepackage[sans]{fammath}
        """
    },
    "charu.tex.font.mathtime": {
        "text.latex.preamble": r"""\usepackage{mathtime}
        \usepackage[sans]{fammath}
        """
    },
    "charu.tex.font.newtx": {
        "text.latex.preamble": r"""\usepackage[newtx]{mathtime}
        \usepackage[sans]{fammath}
        """
    },
    "charu.tex.font.sansmath": {
        "text.latex.preamble": r"""\usepackage{lmodern,amsfonts,amssymb,bm}
        \usepackage[sans]{fammath}
        """
    },
    "charu.tex": {
        "text.usetex": True
    },
}

CHARU_RC_MISC = ["charu.wide", "charu.square", "charu.tex", "charu.tex.preamble"]

# rcParams that are not standard.
WEED_KEYS = ["figure.widefigsize"]

def make_rc(rc):
    """Function to make valid rcParams from supplied ones."""
    true_rc = {}

    for key, val in rc.items():
        if key in CHARU_RC_MISC or key in pyplot.rcParams:
            continue

        common = "{}.{}".format(key, "common")
        if common in CHARU_RC:
            true_rc.update(CHARU_RC[common])

        true_key = "{}.{}".format(key, val)
        if true_key in CHARU_RC:
            true_rc.update(CHARU_RC[true_key])
        else:
            raise ValueError("'{}': '{}' is an invalid rcParam.".format(key, val))

    # Override charu's settings with actual rc keys if present.
    for key, val in rc.items():
        if key in pyplot.rcParams:
            true_rc.update({ key: val })

    if rc.get("charu.tex", False):
        true_rc.update(CHARU_RC["charu.tex"])

    if rc.get("charu.wide", False) and "figure.widefigsize" in true_rc:
        true_rc["figure.figsize"] = true_rc["figure.widefigsize"]

    if "charu.square" in rc and "figure.figsize" in true_rc:
        val = rc["charu.square"]
        if val in (0, 1):
            size = true_rc["figure.figsize"]
            true_rc["figure.figsize"] = [size[val], size[val]]
        else:
            raise ValueError("'charu.square' must be 0 or 1.")

    # Append LaTeX preamble if any.
    preamble = true_rc.get("text.latex.preamble", "") + rc.get("charu.tex.preamble", "")
    true_rc.update({ "text.latex.preamble": preamble })

    for key in WEED_KEYS:
        if key in true_rc:
            true_rc.pop(key)

    return true_rc

class ExecutableNotFound(Warning):
    pass

# Don't print Python code during warnings.
_fmtwarn = warnings.formatwarning
fmtwarn = lambda *args, line=None: _fmtwarn(*(args[:-1]), line="")
warnings.formatwarning = fmtwarn

def execute(*args, **kwargs):
    """Run an executable, but suppress its output."""
    try:
        return subprocess.run(*args, check=True, stdout=subprocess.DEVNULL, **kwargs)
    except FileNotFoundError:
        warnings.warn(
            "{} not in path, skipping".format(args[0][0]),
            ExecutableNotFound,
        )

@pyplot._copy_docstring_and_deprecators(pyplot.savefig)
def savefig(name, crop=False, optimize=False, **kwargs):
    """Monkey-patched pyplot.savefig() with cropping and optimization."""
    _savefig(name, **kwargs)
    p = Path(name)
    if not p.is_file():
        return

    if p.suffix.lower() == ".pdf":
        if crop:
            execute(["pdfcrop", "--pdfversion", "none", name, name])
        if optimize:
            execute([
                "pdfsizeopt",
                "--quiet",
                "--do-optimize-images=no",
                name,
                name,
            ])
    elif p.suffix.lower() == ".png":
        if crop:
            execute(["mogrify", "-trim", name])
        if optimize:
            execute(["optipng", "-clobber", "-quiet", name])

_savefig = pyplot.savefig
pyplot.savefig = savefig

@pyplot._copy_docstring_and_deprecators(pyplot.rc_context)
def rc_context(rc=None, fname=None):
    if rc:
        rc = make_rc(rc)

    return matplotlib.rc_context(rc, fname)

pyplot.rc_context = rc_context

# By default, Matplotlib uses 5 minor ticks between major ticks if the
# number of ticks are not supplied.  But we like 4 ticks.
@pyplot._copy_docstring_and_deprecators(AutoMinorLocator)
class MinorLocator(AutoMinorLocator):
    def __init__(self, n=4):
        super().__init__(n=n)

matplotlib.ticker.AutoMinorLocator = MinorLocator

# Better 3D axes.
class Axes3Dx(mpl_toolkits.mplot3d.axes3d.Axes3D):
    name = "3dx"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(True)
        self.patch.set_alpha(0)

        # Tweaks for all axes.
        for axis in (self.xaxis, self.yaxis, self.zaxis):
            axis._axinfo["tick"].update({ "inward_factor": 0, "outward_factor": 0.25 })
            axis.pane.fill = False
            axis.set_rotate_label(False)

        # Tweaks for x and y axes.
        for axis in (self.xaxis, self.yaxis):
            axis.pane.set_edgecolor("black")
            axis.pane.set_linewidth(matplotlib.rcParams["axes.linewidth"])

        # Tweaks just for the zaxis.
        self.zaxis._axinfo.update({
            # Use this to reposition the spine of a particular axis.  This is an
            # undocumented part of the Matplotlib API and may break any time.
            # In fact, the conventions have changed from the time of this 2018
            # StackOverflow answer: https://stackoverflow.com/a/49601745
            "juggled": (1, 2, 1),
            # Align the ticks along the y axis.
            "tickdir": 1,
        })

    # Right align z labels because now the z axis is on the left.
    def set_zticklabels(self, labels, ha="right", **kwargs):
        return super().set_zticklabels(labels, ha=ha, **kwargs)

matplotlib.projections.register_projection(Axes3Dx)

def ticklabels(start, stop, num=10, div=1, divstr=None, digits=5):
    """Return evenly spaced fractional ticks and labels over an interval."""
    a, b = Fraction(round(start / div, digits)), Fraction(round(stop / div, digits))
    step = (b-a) / (num-1)
    ticks, labels = [], []
    for i in range(num):
        f = a + i*step
        ticks.append(div * float(f))
        if (divstr is None) or (f == 0):
            labels.append(r"${}$".format(f))
        else:
            if abs(f.denominator) == 1:
                if f == 1:
                    labels.append(r"${}$".format(divstr))
                elif f == -1:
                    labels.append(r"$-{}$".format(divstr))
                else:
                    labels.append(r"${}{}$".format(f.numerator, divstr))
            elif abs(f.numerator) == 1:
                if f > 0:
                    labels.append(r"${}/{}$".format(divstr, f.denominator))
                else:
                    labels.append(r"$-{}/{}$".format(divstr, f.denominator))
            else:
                labels.append(r"${}{}/{}$".format(f.numerator, divstr, f.denominator))

    return np.array(ticks), labels
