#####################################################################
# defaults/north_arrow.py contains default values for the NorthArrows
# at difference plot sizes (xsmall to xlarge)
# see their corresponding sizes under each default heading
#####################################################################

# The main variables that update are the following:
# base: scale, linewidth
# fancy: coords (xsmall only)
# label: fontsize, stroke_width 
# shadow: offset
# pack: sep
# aob: pad, borderpad

### IMPORTING PACKAGES ###

# Math packages
import numpy

### INDEPENDENT DEFAULT VALUES ###

# Defaults for rotating the arrow to point towards True North (see _rotate_arrow for how it is used)
# This default is the only one that is static: the rest can and should change depending on the size of your figure
_ROTATION_ALL = {
    "degrees":0,
    "crs":None,
    "reference":None,
    "coords":None 
}

# We also use the same coordinates for the arrow's base, regardless of size
# This is because we can scale the arrow larger/smaller using the scale parameter instead
_COORDS_BASE = numpy.array([
    (0.50, 1.00),
    (0.10, 0.00),
    (0.50, 0.10),
    (0.90, 0.00),
    (0.50, 1.00)
])

# Similarly, we use the same coordinates for the arrows "fancy" part
# EXCEPT when it gets too small (x-small), as rasterization makes it difficult to see the white edge
_COORDS_FANCY = numpy.array([
    (0.50, 0.85),
    (0.50, 0.20),
    (0.80, 0.10),
    (0.50, 0.85)
])

_COORDS_FANCY_XS = numpy.array([
    (0.50, 1.00),
    (0.50, 0.10),
    (0.90, 0.00),
    (0.50, 1.00)
])

### BASE DEFAULTS ###
# These contain every key with its "universal" default value.
# Size-specific overrides are applied on top of these.

_BASE_DEFAULT = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":1, 
    "zorder":98 
}

_FANCY_DEFAULT = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

_LABEL_DEFAULT = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":16,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"normal",
    "stroke_width":1,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

_SHADOW_DEFAULT = {
    "offset":(4,-4),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

_PACK_DEFAULT = {
    "sep":5,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

_AOB_DEFAULT = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.5,
    "borderpad":0.5,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

# Default scale (md)
_SCALE_DEFAULT = 0.50

### SIZE-SPECIFIC OVERRIDES ###
# Only the values that differ from the base are listed here.
# Sizes: xs (A8), sm (A6), md (A4/Letter), lg (A2), xl (A0/Poster)

_OVERRIDES = {
    "xs": {
        # Should work well for ~A8ish paper (2 to 3 inches, or 5 to 8 cm)
        # The arrow will appear to be ~1/10 of an inch in height
        # Here is also the only place that we use the _COORDS_FANCY_XS array!
        "scale":  0.12,
        "base":   {"linewidth":0.7},
        "fancy":  {"coords":_COORDS_FANCY_XS},
        "label":  {"fontsize":6, "stroke_width":0.5},
        "shadow": {"offset":(1,-1)},
        "pack":   {"sep":1.5},
        "aob":    {"pad":0.2, "borderpad":0.2},
    },
    "sm": {
        # Should work well for ~A6 paper (4 to 6 inches, or 11 to 15 cm)
        # The arrow will appear to be ~1/4 of an inch in height
        "scale":  0.25,
        "base":   {"linewidth":0.5},
        "fancy":  {},
        "label":  {"fontsize":8, "stroke_width":0.5},
        "shadow": {"offset":(2,-2)},
        "pack":   {"sep":3},
        "aob":    {"pad":0.33, "borderpad":0.33},
    },
    "md": {
        # Should work well for ~A4/Letter paper (8 to 12 inches, or 21 to 30 cm)
        # The arrow will appear to be ~1/2 an inch or ~1 cm in height
        # This is the base size, so no overrides are needed
        "scale":  0.50,
        "base":   {},
        "fancy":  {},
        "label":  {},
        "shadow": {},
        "pack":   {},
        "aob":    {},
    },
    "lg": {
        # Should work well for ~A2 paper (16 to 24 inches, or 42 to 60 cm)
        # The arrow will appear to be ~an inch in height
        "scale":  1,
        "base":   {"linewidth":2},
        "fancy":  {},
        "label":  {"fontsize":32, "stroke_width":2},
        "shadow": {"offset":(8,-8)},
        "pack":   {"sep":8},
        "aob":    {"pad":1, "borderpad":1},
    },
    "xl": {
        # Should work well for ~A0/Poster paper (33 to 47 inches, or 85 to 120 cm)
        # The arrow will appear to be ~2 inches in height
        "scale":  2,
        "base":   {"linewidth":4},
        "fancy":  {},
        "label":  {"fontsize":64, "stroke_width":4},
        "shadow": {"offset":(16,-16)},
        "pack":   {"sep":12},
        "aob":    {"pad":2, "borderpad":2},
    },
}

### ACCESSOR ###
# Returns the fully-merged defaults for a given size key.

def get_defaults(size_key: str) -> list:
    """Return [scale, base, fancy, label, shadow, pack, aob] defaults for the given size key."""
    overrides = _OVERRIDES.get(size_key, _OVERRIDES["md"])
    return [
        overrides.get("scale", _SCALE_DEFAULT),
        _BASE_DEFAULT   | overrides.get("base", {}),
        _FANCY_DEFAULT  | overrides.get("fancy", {}),
        _LABEL_DEFAULT  | overrides.get("label", {}),
        _SHADOW_DEFAULT | overrides.get("shadow", {}),
        _PACK_DEFAULT   | overrides.get("pack", {}),
        _AOB_DEFAULT    | overrides.get("aob", {}),
    ]

## CONTAINER (LEGACY)
# Kept for backwards compatibility — callers that index _DEFAULTS_NA[size_key][n]
# will continue to work identically.
_DEFAULTS_NA = {key: get_defaults(key) for key in ["xs", "sm", "md", "lg", "xl"]}
