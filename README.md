# charu

charu is a wrapper around Matplotlib's pyplot that adds some trimmings
and monkey patches a couple of functions.

## Usage

To use charu, import it along with pyplot (which can be used as usual),
e.g.,

```python
import matplotlib.pyplot as plt
import numpy as np
import charu

x = np.linspace(0, 10 * np.pi, 1000)
plt.plot(x, np.sin(x))
plt.show()
```

### Extra rcParams

charu's `pyplot.rc_context()` accepts a custom set of rcParams that can
be used (among other things) to set the plot style and size to conform
to a specific journal's requirements, e.g.,

```python
rc = {
    # Document style can be 'aps', 'standard', etc.
    "charu.doc": "aps",

    # Make the figure a square with side equal to axis 0's length.
    "charu.square": 0,

    # Convenient alias for text.usetex.
    "charu.tex": True,

    # Set LaTeX font.  Can be 'cmbright', 'mathtime', etc.
    "charu.tex.font": "cmbright",

    # Append to the current LaTeX preamble.
    "charu.tex.preamble": "\usepackage{siunitx}",

    # Choose two-column/wider figure size.
    "charu.wide": True,
}

with plt.rc_context(rc):
    # plotting code
```

### Crop and optimize PDFs and PNGs

Even with `bbox_inches="tight"` and `pad_inches=0`, `pyplot.savefig()`
doesn't always properly crop the figure to the plot's bounding box.
Because of this, charu includes a version of `pyplot.savefig()` which
can be used to crop (and optimize) PDFs and PNGs.  For PDFs, this
requires [pdfcrop][pdfcrop] and [pdfsizeopt][pdfsizeopt], and for PNGs,
this requires [mogrify] (from ImageMagick) and [optipng][optipng].

```python
plt.savefig("file.pdf", crop=True, optimize=True)
plt.savefig("file.png", crop=True, optimize=True)
```

### Generate formatted ticks and labels

The function `ticklabels` can be used to generate evenly-spaced ticks
and labels with proper formatting for fractions.

```python
>>> ticks, labels = charu.ticklabels(start=-2*np.pi, stop=2*np.pi, num=9, div=np.pi, divstr=r"\pi")
>>> ticks
array([-6.28318531, -4.71238898, -3.14159265, -1.57079633,  0.        ,
        1.57079633,  3.14159265,  4.71238898,  6.28318531])
>>> labels
['$-2\pi$', '$-3\pi/2$', '$-\pi$', '$-\pi/2$', '$0$', '$\pi/2$', '$\pi$', '$3\pi/2$', '$2\pi$']
```

## License

Public domain.  See the file UNLICENSE for more details.

[mogrify]: https://imagemagick.org/script/mogrify.php
[optipng]: http://optipng.sourceforge.net/
[pdfcrop]: https://www.ctan.org/pkg/pdfcrop
[pdfsizeopt]: https://github.com/pts/pdfsizeopt
