# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as pyplot
import mpl_toolkits
import subprocess
import warnings
from matplotlib.ticker import AutoMinorLocator
from pathlib import Path

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

MMMPL_RC = {
    "mmmpl.doc.common": {
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
        "mathtext.fontset": "stixsans",
        "savefig.dpi": 600,
        "xtick.major.width": 0.5,
        "xtick.minor.visible": True,
        "xtick.minor.width": 0.5,
        "ytick.major.width": 0.5,
        "ytick.minor.visible": True,
        "ytick.minor.width": 0.5,
    },

    # For usage with REVTeX.
    "mmmpl.doc.aps": {
        "figure.figsize": [246 * pt, 246 / golden * pt],
        "figure.widefigsize": [510 * pt, 246 * pt * 0.75],
        "font.size": 8.0,
        "legend.fontsize": 7.5,
        "legend.handlelength": 1.25,
        "legend.labelspacing": 0.2,
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
    },

    # For usage with the standard LaTeX classes article, book, etc.
    "mmmpl.doc.standard": {
        "figure.figsize": [260 * pt, 260 / golden * pt],
        "figure.widefigsize": [315 * pt, 315 / golden * pt],
        "font.size": 8.0
    },

    # Matplotlib loads certain LaTeX package according to the sans and serif
    # fonts we set.  These packages often conflict with the ones that we
    # load in the custom preamble, so we blank the sans and serif fonts.
    "mmmpl.tex.font.common": {
        "font.sans-serif": "",
        "font.serif": "",
    },
    "mmmpl.tex.font.cmbright": {
        "text.latex.preamble": r"\usepackage{amsfonts,amssymb,bm,cmbright}"
    },
    "mmmpl.tex.font.fourier": {
        "text.latex.preamble": r"""\usepackage[widespace]{fourier}
        \usepackage[scale=0.92]{tgheros}
        \usepackage{latinsans}
        \DeclareMathAlphabet{\mathcal}{OMS}{cmsy}{m}{n}
        \SetMathAlphabet{\mathcal}{bold}{OMS}{cmsy}{b}{n}
        """
    },
    "mmmpl.tex.font.mathtime": {
        "text.latex.preamble": r"""\usepackage{mathtime,latinsans}"""
    },
    "mmmpl.tex.font.newtx": {
        "text.latex.preamble": r"""\usepackage[newtx]{mathtime}
        \usepackage{latinsans}
        """
    },
    "mmmpl.tex.font.sansmath": {
        "text.latex.preamble": r"""\usepackage{lmodern,amsfonts,amssymb,bm,latinsans}"""
    },
    "mmmpl.tex": {
        "text.usetex": True
    },
}

MMMPL_RC_MISC = ["mmmpl.wide", "mmmpl.square", "mmmpl.tex", "mmmpl.tex.preamble"]

# rcParams that are not standard.
WEED_KEYS = ["figure.widefigsize"]

def make_rc(rc):
    """Function to make valid rcParams from supplied ones."""
    true_rc = {}

    for key, val in rc.items():
        if key in MMMPL_RC_MISC or key in pyplot.rcParams:
            continue

        common = "{}.{}".format(key, "common")
        if common in MMMPL_RC:
            true_rc.update(MMMPL_RC[common])

        true_key = "{}.{}".format(key, val)
        if true_key in MMMPL_RC:
            true_rc.update(MMMPL_RC[true_key])
        else:
            raise ValueError("'{}': '{}' is an invalid rcParam.".format(key, val))

    # Override mmmpl's settings with actual rc keys if present.
    for key, val in rc.items():
        if key in pyplot.rcParams:
            true_rc.update({ key: val })

    if rc.get("mmmpl.tex", False):
        true_rc.update(MMMPL_RC["mmmpl.tex"])

    if rc.get("mmmpl.wide", False) and "figure.widefigsize" in true_rc:
        true_rc["figure.figsize"] = true_rc["figure.widefigsize"]

    if "mmmpl.square" in rc and "figure.figsize" in true_rc:
        val = rc["mmmpl.square"]
        if val in (0, 1):
            size = true_rc["figure.figsize"]
            true_rc["figure.figsize"] = [size[val], size[val]]
        else:
            raise ValueError("'mmmpl.square' must be 0 or 1.")

    # Append LaTeX preamble if any.
    preamble = true_rc.get("text.latex.preamble", "") + rc.get("mmmpl.tex.preamble", "")
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
            axis._axinfo["tick"].update({"inward_factor": 0, "outward_factor": 0.25})
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
                # Aline the ticks along the y axis.
                "tickdir": 1,
        })

matplotlib.projections.register_projection(Axes3Dx)
