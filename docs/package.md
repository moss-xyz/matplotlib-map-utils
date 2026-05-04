---
title: Package Information
icon: lucide/package
---

### :lucide-handshake: Inspiration and Thanks

This project was heavily inspired by [`matplotlib-scalebar`](https://github.com/ppinard/matplotlib-scalebar/), and much of the code is either directly copied or derived from that project, since it uses the same "artist"-based approach.

Three more projects assisted with the creation of this package:

* [`EOmaps`](https://github.com/raphaelquast/EOmaps/discussions/231) provided code for calculating the rotation required to point to "true north" for an arbitrary point and CRS for the north arrow.

* [`Cartopy`](https://github.com/SciTools/cartopy/issues/2361) fixed an issue inherent to calling `.copy()` on `CRS` objects.

* [`Ultraplot`](https://github.com/moss-xyz/matplotlib-map-utils/issues/16) fixed a compatibility issue between their extension of matplotlib and this project, while also giving some tips that influenced the future development of this work.

---

### :lucide-save: Release Notes

- `v1.0.x`: Initial releases featuring the North Arrow element, along with some minor bug fixes.

- `v2.0.0`: Initial release of the Scale Bar element.

	- `v2.0.1`: Fixed a bug in the `dual_bars()` function that prevented empty dictionaries to be passed. Also added a warning when auto-calculated bar widths appear to be exceeding the dimension of the axis (usually occurs when the axis is <2 kilometers or miles long, depending on the units selected).

	- `v2.0.2`: Changed f-string formatting to alternate double and single quotes, so as to maintain compatibility with versions of Python before 3.12 (see [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/3)). However, this did reveal that another aspect of the code, namely concatenating `type` in function arguments, requires 3.10, and so the minimum python version was incremented.

	- `v2.1.0`: Added a utility class, `USA`, for filtering subsets of US states and territories based on FIPS code, name, abbreviation, region, division, and more. This is considered a beta release, and might be subject to change later on.

- `v3.0.0`: Release of inset map and extent and detail indicator classes and functions.

	- `v3.0.1`: Fixed a bug that led to an incorrect Scale Bar being rendered when using the function method (`scale_bar()`) on a plot containing raster data (see [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/10) for details).

	- `v3.1.0`: Overhauled the functionality for specifying the the length of a scale bar, including support for custom units/projections (similar to `matplotlib-scalebar`'s `dx` argument) and to specify the length of a major division instead of the entire scale bar, as requested [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/10). Added ability to set artist-level `zorder` variables for all elements, with both the function and class method approaches, as requested [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/9) and [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/10). Also fixed a bug related to custom division labels on the scale bar.

	- `v3.1.1`: Fixed a bug that led to errors when creating a `scale_bar` at resolutions below 5km or 1 mile, due to a bug in the backend configuration functions (namely, `_config_bar_dim()`), which was fixed by correctly instantiating the necessary variable `ax_units` in other cases via an `else` statement (see [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/14) for details).

	- `v3.1.2`: Fixed a compatibility issue with [Ultraplot](https://github.com/Ultraplot/UltraPlot), primarily affecting the `ScaleBar` element, where text would rasterize at a low resolution (see [here](https://github.com/moss-xyz/matplotlib-map-utils/issues/16) and [here](https://github.com/moss-xyz/matplotlib-map-utils/pull/17) for details). A big thank you to cvanelteren on the Ultraplot team for identifying and implementing the necessary fixes, as well as making adjustments to the Ultraplot package to improve compatibility!

- `v4.0.0`: Transition of documentation from Jupyter Notebooks hosted within the package itself to a new standalone static site, built with Zensical.

	- `v4.1.0`: Transition to Pydantic for type hinting and validation, instead of the previous method that utilised custom logic functions. This ended up changing a fair amount of the backend construction logic, and all the functionality surrounding default values and `set_size` was re-written, which might introduce breaking changes! *Unlike most of the code up until this point, I leaned on AI extensively here, and expect there to be tricky bugs that will need squashing later*.

#### Future Roadmap

With the release of `v3.x`, this project has achieved full coverage of the "main" map elements I think are necessary.

If I continue development of this project, I will be looking to add or fix the following features:

* **North Arrow:** 

	* Copy the image-rendering functionality of the Scale Bar to allow for rotation of the entire object, label and arrow together

	* Create more styles for the arrow, potentially including a compass rose and a line-only arrow

* **Scale Bar:**

	* Allow for custom unit definitions (instead of just metres/feet/miles/kilometres/etc.), so that the scale bar can be used on arbitrary plots (such as inches/cm/mm, mathmatical plots, and the like)

	* Fix/improve the `dual_bars()` function, which currently doesn't work great with rotations

	* Clean up the variable naming scheme (consistency on `loc` vs `position`, `style` vs `type`, etc.)

	* Create more styles for the bar, potentially including dual boxes and a sawtooth bar

* **Inset Map:**

	* Clean up the way that connectors are drawn for detail indicators

	* New functionality for placing multiple inset maps at once (with context-aware positioning to prevent overlap with each other)

* **Utils:**

	* (USA): Stronger fuzzy search mechanics, so that it will accept flexible inputs for FIPS/abbr/name

	* (USA): More integrated class types to allow for a more fully-formed object model (USA being a `Country`, with subclasses related to `State` and `Territory` that have their own classes of attributes, etc.)

	* (USA): Stronger typing options, so you don't have to recall which `region` or `division` types are available, etc.

	* (USA): Allowance for method chaining of single-type filters to allow for easier chaining, and potential `OR` fields

	& (USA): Improve compatibility with Pandas and Polars
	
	* Other functions that I have created myself that give more control in the formatting of maps. 
	
		* I am also open to ideas for other extensions to create!

#### Support and Contributions

If you notice something is not working as intended or if you'd like to add a feature yourself, I welcome PRs - <span class="emphasis-fg">just be sure to be descriptive as to what you are changing and why, including code examples!</span>

If you are having issues using this script, feel free to leave a post explaining your issue, and I will try and assist, though I have no guaranteed SLAs as this is just a hobby project.

<span class="emphasis-ac">I am open to contributions, especially to help tackle the roadmap above!</span>

---

### :lucide-scale: License and Citation

I know nothing about licensing, so I went with the GPL license. If that is incompatible with any of the dependencies, please let me know.

No need to cite this package if you use it in your academic or professional work - just happy to see it being used!

---

### :lucide-folder-closed: Package Structure

```bash
package_name/
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── inset_map.py
│   ├── north_arrow.py
│   ├── scale_bar.py
├── validation/
│   ├── __init__.py
│   ├── shared.py
│   └── inset_map.py
│   ├── north_arrow.py
│   └── scale_bar.py
├── defaults/
│   ├── __init__.py
│   ├── north_arrow.py
│   └── scale_bar.py
│   └── inset_map.py
├── utils/
│   ├── __init__.py
│   ├── usa.py
│   └── usa.json
```

Where:

* `core` contains the main functions and classes for each object

* `validation` contains type hints for each variable and functions to validate inputs

* `defaults` contains default settings for each object at different paper sizes

* `utils` contains utility functions and objects

---

