# mmmpl

mmmpl is a wrapper around Matplotlib's pyplot that adds some trimmings
and monkey patches a couple of functions.

## Usage

To use mmmpl, import it along with pyplot (which can be used as usual),
e.g.,

```python
import matplotlib.pyplot as plt
import numpy as np
import mmmpl

x = np.linspace(0, 10 * np.pi, 1000)
plt.plot(x, np.sin(x))
plt.show()
```

### Extra rcParams

mmmpl's `pyplot.rc_context()` accepts a custom set of rcParams that can
be used (among other things) to set the plot style and size to conform
to a specific journal's requirements, e.g.,

```python
rc = {
    # Document style can be 'aps', 'standard', etc.
    "mmmpl.doc": "aps",

    # Make the figure a square with side equal to axis 0's length.
    "mmmpl.square": 0,

    # Convenient alias for text.usetex.
    "mmmpl.tex": True,

    # Set LaTeX font.  Can be 'cmbright', 'mathtime', etc.
    "mmmpl.tex.font": "cmbright",

    # Append to the current LaTeX preamble.
    "mmmpl.tex.preamble": "\usepackage{siunitx}",

    # Choose two-column/wider figure size.
    "mmmpl.wide": True,
}

with plt.rc_context(rc):
    # plotting code
```

### Crop and optimize PDFs and PNGs

Even with `bbox_inches="tight"` and `pad_inches=0`, `pyplot.savefig()`
doesn't always properly crop the figure to the plot's bounding box.
Because of this, mmmpl includes a version of `pyplot.savefig()` which
can be used to crop (and optimize) PDFs and PNGs.  For PDFs, this
requires [pdfcrop][pdfcrop] and [pdfsizeopt][pdfsizeopt], and for PNGs,
this requires [mogrify] (from ImageMagick) and [optipng][optipng].

```python
plt.savefig("file.pdf", crop=True, optimize=True)
plt.savefig("file.png", crop=True, optimize=True)
```

## License

Public domain.  See the file UNLICENSE for more details.

[mogrify]: https://imagemagick.org/script/mogrify.php
[optipng]: http://optipng.sourceforge.net/
[pdfcrop]: https://www.ctan.org/pkg/pdfcrop
[pdfsizeopt]: https://github.com/pts/pdfsizeopt
