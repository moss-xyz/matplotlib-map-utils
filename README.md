# matplotlib-map-utils
 
---

**Documentation**: See `docs` folder

**Source Code**: Find the project on GitHub

---

### Introduction

`matplotlib_map_utils` is intended to be a package that provides various functions and objects that assist with the the creation of maps using [`matplotlib`](https://matplotlib.org/stable/).

As of `v1.x` (the current version), this only includes a single additional tool: `north_arrow.py`, which applies a high quality, context-aware north arrow to a given plot. Future releases (if the project is continued) might provide similar tools for creating scale bars or inset maps, or functions that I have created myself that give more control in the formatting of maps.

---

### Installation

This package is available on PyPi, and can be installed like so:

```bash
pip install matplotlib-map-utils
```

The requirements for this package are:

* python

* matplotlib

* cartopy

---

### North Arrow

#### Quick Start

The quickest way to add a single north arrow to a single plot is to use the `north_arrow` function:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(10,10), dpi=300)
# Adding a north arrow to the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
north_arrow.north_arrow(ax=ax, location="upper right", rotation={"degrees":0})
```

An object-oriented approach is also supported:

```python
# Setting up a plot
fig, ax = matplotlib.pyplot.subplots(1,1, figsize=(10,10), dpi=300)
# Creating a north arrow for the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
na = north_arrow.NorthArrow(ax=ax, location="upper right", rotation={"degrees":0})
# Adding the artist to the plot
ax.add_artist(na)
```

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

---

### Development Notes

#### Inspiration and Thanks

This project was heavily inspired by [`matplotlib-scalebar`](https://github.com/ppinard/matplotlib-scalebar/), and much of the code is either directly copied or a derivative of that project, since it uses the same "artist"-based approach.

Two more projects assisted with the creation of this script:

* [`EOmaps`](https://github.com/raphaelquast/EOmaps/discussions/231) provided code for calculating the rotation required to point to "true north" for an arbitrary point and CRS for the north arrow.

* [`Cartopy`](https://github.com/SciTools/cartopy/issues/2361) fixed an issue inherent to calling `.copy()` on `CRS` objects.

#### Future Roadmap

As stated in the intro, I am hoping this project will encompass more than just the north arrow object it currently does. In particular, I want `v2` to tackle making properly-formatted "map-style" scale bar objects, a la ArcGIS and QGIS.

If that goes well, `v3` can either create a tool for generating inset maps (which `matplotlib` has *some* support for), or the various functions that I have created in the past that assist with formatting a map "properly", such as centering on a given object.

I am also open to ideas for other extensions to create!

#### Support and Contributions

If you notice something is not working as intended or if you'd like to add a feature yourself, I welcome PRs - just be sure to be descriptive as to what you are changing and why, including code examples!

If you are having issues using this script, feel free to leave a post explaining your issue, and I will try and assist, though I have no guaranteed SLAs as this is just a hobby project.

---

### License

I know nothing about licensing, so I went with the GPL license. If that is incompatible with any of the dependencies, please let me know.