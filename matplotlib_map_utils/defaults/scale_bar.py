#################################################################
# defaults/scale_bar.py contains default values for the ScaleBars
# at difference plot sizes (xsmall to xlarge)
# see their corresponding sizes under each default heading
#################################################################

# The main variables that update are the following:
# bar: height, edgewidth, tickwidth
# labels: sep, style
# units: sep
# text: fontsize, stroke_width (also changes labels and units)
# aob: pad, borderpad

### BASE DEFAULTS ###
# These contain every key with its "universal" default value.
# Size-specific overrides are applied on top of these.

_BAR_BASE = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.1,
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"none",
    "major_mult":None,
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":1,
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":1.5,
    "interpolation":"none",
    "dpi_cor":True,
    "resample":False,
    "raster_dpi":None,
    "raster_dpi_scale":1,
}

_LABELS_BASE = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"major",
    "loc":"above",
    "pad":0,
    "sep":5,
}

_UNITS_BASE = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":5,
}

_TEXT_BASE = {
    "fontsize":12,
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"normal",
    "stroke_width":1,
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

_AOB_BASE = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.5,
    "borderpad":0.5,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None,
}

### SIZE-SPECIFIC OVERRIDES ###
# Only the values that differ from the base are listed here.
# Sizes: xs (A8), sm (A6), md (A4/Letter), lg (A2), xl (A0/Poster)

_OVERRIDES = {
    "xs": {
        # Should work well for ~A8ish paper (2 to 3 inches, or 5 to 8 cm)
        # The bar will appear to be ~1/10 of an inch in height
        "bar":    {"height":0.05, "edgewidth":0.5, "tickwidth":0.5, "minor_type":"none"},
        "labels": {"style":"first_last", "sep":1.5},
        "units":  {"sep":1.5},
        "text":   {"fontsize":4, "stroke_width":0.5},
        "aob":    {"pad":0.1, "borderpad":0.1},
    },
    "sm": {
        # Should work well for ~A6 paper (4 to 6 inches, or 11 to 15 cm)
        # The bar will appear to be ~1/4 of an inch in height
        "bar":    {"height":0.075, "edgewidth":0.75, "tickwidth":0.75, "minor_type":"none"},
        "labels": {"style":"first_last", "sep":3},
        "units":  {"sep":3},
        "text":   {"fontsize":6, "stroke_width":0.5},
        "aob":    {"pad":0.33, "borderpad":0.33},
    },
    "md": {
        # Should work well for ~A4/Letter paper (8 to 12 inches, or 21 to 30 cm)
        # The bar will appear to be ~1/2 an inch or ~1 cm in height
        # This is the base size, so overrides are minimal
        "bar":    {"minor_type":"first"},
        "labels": {},
        "units":  {},
        "text":   {},
        "aob":    {},
    },
    "lg": {
        # Should work well for ~A2 paper (16 to 24 inches, or 42 to 60 cm)
        # The bar will appear to be ~an inch in height
        "bar":    {"height":0.2, "edgewidth":2, "tickwidth":3, "minor_type":"first"},
        "labels": {"sep":8},
        "units":  {"sep":8},
        "text":   {"fontsize":24, "stroke_width":2},
        "aob":    {"pad":1, "borderpad":1},
    },
    "xl": {
        # Should work well for ~A0/Poster paper (33 to 47 inches, or 85 to 120 cm)
        # The bar will appear to be ~2 inches in height
        "bar":    {"height":0.4, "edgewidth":4, "tickwidth":5, "minor_type":"first"},
        "labels": {"sep":12},
        "units":  {"sep":12},
        "text":   {"fontsize":48, "stroke_width":4},
        "aob":    {"pad":2, "borderpad":2},
    },
}

### ACCESSOR ###
# Returns the fully-merged defaults for a given size key.

def get_defaults(size_key: str) -> list:
    """Return [bar, labels, units, text, aob] defaults for the given size key."""
    overrides = _OVERRIDES.get(size_key, _OVERRIDES["md"])
    return [
        _BAR_BASE    | overrides.get("bar", {}),
        _LABELS_BASE | overrides.get("labels", {}),
        _UNITS_BASE  | overrides.get("units", {}),
        _TEXT_BASE   | overrides.get("text", {}),
        _AOB_BASE    | overrides.get("aob", {}),
    ]

## CONTAINER (LEGACY)
# Kept for backwards compatibility — callers that index _DEFAULTS_SB[size_key][n]
# will continue to work identically.
_DEFAULTS_SB = {key: get_defaults(key) for key in ["xs", "sm", "md", "lg", "xl"]}
