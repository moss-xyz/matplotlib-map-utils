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
    "degrees":None,
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

## X-SMALL DEFAULTS
# Should work well for ~A8ish paper (2 to 3 inches, or 5 to 8 cm)
# The arrow will appear to be ~1/10 of an inch in height
# Here is also the only place that we use the _COORDS_FANCY_XS array!

# Scale
_SCALE_XS = 0.12

# Base
_BASE_XS = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":0.7, 
    "zorder":98 
}

# Fancy
_FANCY_XS = {
    "coords":_COORDS_FANCY_XS,
    "facecolor":"black",
    "zorder":99
}

# Label
_LABEL_XS = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":6,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":0.5,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Shadow
_SHADOW_XS = {
    "offset":(1,-1),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# VPacker/HPacker
_PACK_XS = {
    "sep":1.5,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# AnchoredOffsetBox (AOB)
_AOB_XS = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.2,
    "borderpad":0.2,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## SMALL DEFAULTS
# Should work well for ~A6 paper (4 to 6 inches, or 11 to 15 cm)
# The arrow will appear to be ~1/4 of an inch in height

# Scale
_SCALE_SM = 0.25

# Base
_BASE_SM = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":0.5, 
    "zorder":98 
}

# Fancy
_FANCY_SM = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

# Label
_LABEL_SM = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":8,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":0.5,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Shadow
_SHADOW_SM = {
    "offset":(2,-2),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# VPacker/HPacker
_PACK_SM = {
    "sep":3,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# AnchoredOffsetBox (AOB)
_AOB_SM = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.33,
    "borderpad":0.33,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## MEDIUM DEFAULTS
# Should work well for ~A4/Letter paper (8 to 12 inches, or 21 to 30 cm)
# The arrow will appear to be ~ 1/2 an inch or ~1 cm in height

# Scale
_SCALE_MD = 0.50

# Base
_BASE_MD = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":1, 
    "zorder":98 
}

# Fancy
_FANCY_MD = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

# Label
_LABEL_MD = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":16,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":1,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Shadow
_SHADOW_MD = {
    "offset":(4,-4),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# VPacker/HPacker
_PACK_MD = {
    "sep":5,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# AnchoredOffsetBox (AOB)
_AOB_MD = {
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

## LARGE DEFAULTS
# Should work well for ~A2 paper (16 to 24 inches, or 42 to 60 cm)
# The arrow will appear to be ~an inch in height

# Scale
_SCALE_LG = 1

# Base
_BASE_LG = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":2, 
    "zorder":98 
}

# Fancy
_FANCY_LG = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

# Label
_LABEL_LG = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":32,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":2,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Shadow
_SHADOW_LG = {
    "offset":(8,-8),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# VPacker/HPacker
_PACK_LG = {
    "sep":8,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# AnchoredOffsetBox (AOB)
_AOB_LG = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":1,
    "borderpad":1,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## X-LARGE DEFAULTS
# Should work well for ~A0/Poster paper (33 to 47 inches, or 85 to 120 cm)
# The arrow will appear to be ~2 inches in height

# Scale
_SCALE_XL = 2

# Base
_BASE_XL = {
    "coords":_COORDS_BASE,
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":4, 
    "zorder":98 
}

# Fancy
_FANCY_XL = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

# Label
_LABEL_XL = {
    "text":"N",
    "position":"bottom",
    "ha":"center",
    "va":"baseline",
    "fontsize":64,
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":4,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Shadow
_SHADOW_XL = {
    "offset":(16,-16),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# VPacker/HPacker
_PACK_XL = {
    "sep":12,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# AnchoredOffsetBox (AOB)
_AOB_XL = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":2,
    "borderpad":2,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## CONTAINER
# This makes an easy-to-call dictionary of all the defaults we've set, for easy unpacking by the set_size function
_DEFAULTS_NA = {
    "xs":[_SCALE_XS, _BASE_XS, _FANCY_XS, _LABEL_XS, _SHADOW_XS, _PACK_XS, _AOB_XS],
    "sm":[_SCALE_SM, _BASE_SM, _FANCY_SM, _LABEL_SM, _SHADOW_SM, _PACK_SM, _AOB_SM],
    "md":[_SCALE_MD, _BASE_MD, _FANCY_MD, _LABEL_MD, _SHADOW_MD, _PACK_MD, _AOB_MD],
    "lg":[_SCALE_LG, _BASE_LG, _FANCY_LG, _LABEL_LG, _SHADOW_LG, _PACK_LG, _AOB_LG],
    "xl":[_SCALE_XL, _BASE_XL, _FANCY_XL, _LABEL_XL, _SHADOW_XL, _PACK_XL, _AOB_XL],
}