---
title: Documentation Home
icon: lucide/book
---

![matplotlib_map_utils logo](assets/index/mmu_logo_w_elements.png)
 
---

### :lucide-book: Introduction

`matplotlib_map_utils` is a package that that assists with the creation of maps using [`matplotlib`](https://matplotlib.org/stable/).

As of `v4.x` (the current version), this includes the ability to easily create three common map elements: 

* <span class="strong-fg">North arrows</span>, which automatically point to true north,

* <span class="strong-fg">Scale bars</span>, available in different styles and automatic unit conversion, and

* <span class="strong-fg">Inset maps</span>, including both detail and extent-style plots. 

The three elements listed above are all intended to be high-resolution, easily modifiable, and context-aware relative to your specific plot.

This package also contains a single utility object:

* <span class="strong-fg code-inline">USA</span>, a class that helps filter for states and territories within the USA based on given characteristics, used primarily for building queries based on FIPS codes or names.

Together, these allow for the (relatively) easy creation of a map such as the following:

![Map with all common elements added](assets/index/bigmap_w_elements.png)

---

### :lucide-save: Installation

This package is available on PyPi, and can be installed like so:

=== "pip"
	```bash
	pip install matplotlib-map-utils
	```

=== "uv"
	```bash
	uv add matplotlib-map-utils
	```

The requirements for this package are:

* `python >= 3.10` (due to the use of the pipe operator to concatenate dictionaries and types)

* `matplotlib >= 3.9` (might work with lower versions but not guaranteed)

* `cartopy >= 0.23` (due to earlier bug with calling `copy()` on `CRS` objects)

* `pydantic >= 2.13.3` (for type validation; might work with older versions, open an issue if you have questions)

---

### :lucide-compass: Guides

For a primer on how to import the package and use the primary functions and methods to create elements, see the [Quick Start guide](quick/).

Each part of the package also has a dedicated page that lays out usage and customisation options in more detail:

<div class="grid cards" markdown>

- <a class="nav-xul" href="north_arrows/">:lucide-mouse-pointer-2:  __North Arrows__</a>
- <a class="nav-xul" href="scale_bars/">:lucide-ruler:  __Scale Bars__</a>
- <a class="nav-xul" href="inset_maps/">:lucide-picture-in-picture-2:  __Inset Maps__</a>
- <a class="nav-xul" href="utilities/">:lucide-wrench:  __Utilities__</a>

</div>

Finally, the [Package Information page](package/) provides additional context around the development of and overall structure of the package.