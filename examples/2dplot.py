# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import charu

rc = {
    "charu.doc": "aps",
    "charu.tex": True,
}

with plt.rc_context(rc):
    fig, ax = plt.subplots()

    x = np.linspace(-3*np.pi, 3*np.pi, 1000)
    ax.plot(x, np.cos(x))
    ax.set_xlabel(r"$\vartheta$")
    ax.set_ylabel(r"$\sin(\vartheta)$")

    plt.savefig(
        "2dplot.pdf",
        crop=True,
        optimize=True,
        transparent=True,
        bbox_inches="tight",
        facecolor="none",
        pad_inches=0,
    )
    plt.show()
