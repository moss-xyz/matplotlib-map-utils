# matplotlib-map-utils
 
---

**Documentation**: See `docs` folder

**Source Code**: Find the project on GitHub

---

### Introduction

`matplotlib_map_utils` is intended to be a package that provides various functions and objects that assist with the the creation of maps using [`matplotlib`](https://matplotlib.org/stable/).

As of `v2.x` (the current version), this includes two tools: 

* `north_arrow.py`, which generates a high quality, context-aware north arrow for a given plot. 

* `scale_bar.py`, which generates a high quality, context-aware scale bar to a given plot. 

Future releases (if the project is continued) might provide a similar tool inset maps, or other functions that I have created myself that give more control in the formatting of maps.

---

### Installation

This package is available on PyPi, and can be installed like so:

```bash
pip install matplotlib-map-utils
```

The requirements for this package are:

* `python >= 3.9.0` (due to the dictionary-concatenation method utilized)

* `matplotlib >= 3.9.0` (might work with lower versions but not guaranteed)

* `cartopy >= 0.23.0` (due to earlier bug with calling `copy()` on `CRS` objects)

---

### Package Structure

The package is arrayed in the following way:

```bash
package_name/
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── north_arrow.py
│   ├── scale_bar.py
├── validation/
│   ├── __init__.py
│   ├── functions.py
│   ├── north_arrow.py
│   └── scale_bar.py
├── defaults/
│   ├── __init__.py
│   ├── north_arrow.py
│   └── scale_bar.py
```

Where:

* `core` contains the main functions and classes for each object

* `validation` contains type hints for each variable and functions to validate inputs

* `defaults` contains default settings for each object at different paper sizes

---

### North Arrow

<details>
<summary><i>Expand instructions</i></summary>

#### Quick Start

Importing the North Arrow functions and classes can be done like so:

```py
from matplotlib_map_utils.core.north_arrow import NorthArrow, north_arrow
```

The quickest way to add a single north arrow to a single plot is to use the `north_arrow` function:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(5,5), dpi=150)
# Adding a north arrow to the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
north_arrow.north_arrow(ax=ax, location="upper right", rotation={"degrees":0})
```

An object-oriented approach is also supported:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(5,5), dpi=150)
# Creating a north arrow for the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
na = north_arrow.NorthArrow(location="upper right", rotation={"degrees":0})
# Adding the artist to the plot
ax.add_artist(na)
```

Both of these will create an output like the following:

![Example north arrow](matplotlib_map_utils/docs/assets/readme_northarrow.png)

#### Customization

Both the object-oriented and functional approaches can be customized to allow for fine-grained control over formatting:

```python
north_arrow(
    ax,
    location = "upper right", # accepts a valid string from the list of locations
    scale = 0.5, # accepts a valid positive float or integer
    # each of the follow accepts arguments from a customized style dictionary
    base = {"facecolor":"green"},
    fancy = False,
    label = {"text":"North"},
    shadow = {"alpha":0.8},
    pack = {"sep":6},
    aob = {"pad":2},
    rotation = {"degrees": 35}
)
```

Refer to `docs\howto_north_arrow` for details on how to customize each facet of the north arrow.

#### Rotation

The north arrow object is also capable of pointing towards "true north", given a CRS and reference point:

![Example north arrow rotation](matplotlib_map_utils/docs/assets/readme_northarrow_rotation.png)

Instructions for how to do so can be found in `docs\howto_north_arrow`.
</details>

---

### Scale Bar

<details>
<summary><i>Expand instructions</i></summary>

#### Quick Start

Importing the Scale Bar functions and classes can be done like so:

```py
from matplotlib_map_utils.core.scale_bar import ScaleBar, scale_bar
```

There are two available styles for the scale bars: `boxes` and `ticks`. The quickest way to add one to a single plot is to use the `scale_bar` function:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(5,5), dpi=150)
# Adding a scale bar to the upper-right corner of the axis, in the same projection as whatever geodata you plotted
# Here, this scale bar will have the "boxes" style
scale_bar(ax=ax, location="upper right", style="boxes", bar={"projection":3857})
```

An object-oriented approach is also supported:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(5,5), dpi=150)
# Adding a scale bar to the upper-right corner of the axis, in the same projection as whatever geodata you plotted
# Here, we change the boxes to "ticks"
sb = ScaleBar(location="upper right", style="boxes", bar={"projection":3857})
# Adding the artist to the plot
ax.add_artist(sba)
```

Both of these will create an output like the following (function is left, class is right):

![Example scale bar](matplotlib_map_utils/docs/assets/readme_scalebar.png)

#### Customization

Both the object-oriented and functional approaches can be customized to allow for fine-grained control over formatting:

```python
scale_bar(
    ax,
    location = "upper right", # accepts a valid string from the list of locations
    style = "boxes", # accepts a valid positive float or integer
    # each of the follow accepts arguments from a customized style dictionary
    bar = {"unit":"mi", "length":2}, # converting the units to miles, and changing the length of the bar (in inches)
    labels = {"style":"major", "loc":"below"}, # placing a label on each major division, and moving them below the bar
    units = {"loc":"text"}, # changing the location of the units text to the major division labels
    text = {"fontfamily":"monospace"}, # changing the font family of all the text to monospace
)
```

This will create an output like the following:

![Customized scale bar](matplotlib_map_utils/docs/assets/readme_scalebar_customization.png)

Refer to `docs\howto_scale_bar` for details on how to customize each facet of the scale bar.

</details>

---

### Development Notes

#### Inspiration and Thanks

This project was heavily inspired by [`matplotlib-scalebar`](https://github.com/ppinard/matplotlib-scalebar/), and much of the code is either directly copied or a derivative of that project, since it uses the same "artist"-based approach.

Two more projects assisted with the creation of this script:

* [`EOmaps`](https://github.com/raphaelquast/EOmaps/discussions/231) provided code for calculating the rotation required to point to "true north" for an arbitrary point and CRS for the north arrow.

* [`Cartopy`](https://github.com/SciTools/cartopy/issues/2361) fixed an issue inherent to calling `.copy()` on `CRS` objects.

#### Future Roadmap

With the release of `v2.x`, and the addition of **Scale Bar** tools, this project has achieved the two main objectives that I set out to.

If I continue development of this project, I will be looking to add or fix the following features:

* **North Arrow:** 

  * Copy the image-rendering functionality of the Scale Bar to allow for rotation of the entire object, label and arrow together
  
  * Create more styles for the arrow, potentiallly including a compass rose and a line-only arrow

* **Scale Bar:**

  * Fix/improve the `dual_bars()` function, which currently doesn't work great with rotations

  * Clean up the variable naming scheme (consistency on `loc` vs `position`, `style` vs `type`, etc.)

  * Create more styles for the bar, potentiallly including dual boxes and a sawtooth bar

If that goes well, `v3` can then either create a tool for generating inset maps (which `matplotlib` has *some* support for), or the various functions that I have created in the past that assist with formatting a map "properly", such as centering on a given object and coverting FIPS codes.

I am also open to ideas for other extensions to create!

#### Support and Contributions

If you notice something is not working as intended or if you'd like to add a feature yourself, I welcome PRs - just be sure to be descriptive as to what you are changing and why, including code examples!

If you are having issues using this script, feel free to leave a post explaining your issue, and I will try and assist, though I have no guaranteed SLAs as this is just a hobby project.

---

### License

I know nothing about licensing, so I went with the GPL license. If that is incompatible with any of the dependencies, please let me know.