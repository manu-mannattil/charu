# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import charu

rc = {
    "charu.doc": "aps",
    "charu.tex": True,
    "charu.tex.font": "lmodern",
    "charu.wide": True,
    "font.family": "serif",
}

with plt.rc_context(rc):
    fig, axes = plt.subplots(1, 2)

    # first axis ------------------------------------------------------------

    ax = axes[0]

    x = np.linspace(-3*np.pi, 3*np.pi, 1000)
    ax.plot(x, np.sin(x))
    ax.set_xlabel(r"$\vartheta$")
    ax.set_ylabel(r"$\sin(\vartheta)$")
    ax.set_title(r"First plot: cosine vs. angle")

    # second axis -----------------------------------------------------------

    ax = axes[1]

    x = np.linspace(-3*np.pi, 3*np.pi, 1000)
    ax.plot(x, np.cos(x))
    ax.set_xlabel(r"$\vartheta$")
    ax.set_ylabel(r"$\cos(\vartheta)$")
    ax.set_title(r"Second plot: cosine vs. angle")

    plt.tight_layout()
    plt.savefig(
        "2dplot_wide.pdf",
        crop=True,
        optimize=True,
        transparent=True,
        bbox_inches="tight",
        facecolor="none",
        pad_inches=0,
    )
    plt.show()
