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

## X-SMALL DEFAULTS
# Should work well for ~A8ish paper (2 to 3 inches, or 5 to 8 cm)
# The arrow will appear to be ~1/10 of an inch in height

# Bar
_BAR_XS = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.05, # changed
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"none",
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":0.5, # changed
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":0.5 # changed
}

# Labels
_LABELS_XS = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"first_last", # changed
    "loc":"above",
    "pad":0,
    "sep":1.5, # changed
}

# Units
_UNITS_XS = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":1.5, # changed
}

# Text
_TEXT_XS = {
    "fontsize":4, # changed
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"regular",
    "stroke_width":0.5, # changed
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

# AOB
_AOB_XS = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.1, # changed
    "borderpad":0.1, # changed
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## SMALL DEFAULTS
# Should work well for ~A6 paper (4 to 6 inches, or 11 to 15 cm)
# The arrow will appear to be ~1/4 of an inch in height

# Bar
_BAR_SM = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.075, # changed
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"none",
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":0.75, # changed
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":0.75 # changed
}

# Labels
_LABELS_SM = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"first_last", # changed
    "loc":"above",
    "pad":0,
    "sep":3, # changed
}

# Units
_UNITS_SM = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":3, # changed
}

# Text
_TEXT_SM = {
    "fontsize":6, # changed
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"regular",
    "stroke_width":0.5, # changed
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

# AOB
_AOB_SM = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.33, # changed
    "borderpad":0.33, # changed
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## MEDIUM DEFAULTS
# Should work well for ~A4/Letter paper (8 to 12 inches, or 21 to 30 cm)
# The arrow will appear to be ~ 1/2 an inch or ~1 cm in height

# Bar
_BAR_MD = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.1, # changed
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"first",
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":1, # changed
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":1.5 # changed
}

# Labels
_LABELS_MD = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"major",
    "loc":"above",
    "pad":0,
    "sep":5, # changed
}

# Units
_UNITS_MD = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":5, # changed
}

# Text
_TEXT_MD = {
    "fontsize":12, # changed
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"regular",
    "stroke_width":1, # changed
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

# AOB
_AOB_MD = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.5, # changed
    "borderpad":0.5, # changed
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## LARGE DEFAULTS
# Should work well for ~A2 paper (16 to 24 inches, or 42 to 60 cm)
# The arrow will appear to be ~an inch in height

# Bar
_BAR_LG = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.2, # changed
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"first",
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":2, # changed
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":3 # changed
}

# Labels
_LABELS_LG = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"major",
    "loc":"above",
    "pad":0,
    "sep":8, # changed
}

# Units
_UNITS_LG = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":8, # changed
}

# Text
_TEXT_LG = {
    "fontsize":24, # changed
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"regular",
    "stroke_width":2, # changed
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

# AOB
_AOB_LG = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":1, # changed
    "borderpad":1, # changed
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## X-LARGE DEFAULTS
# Should work well for ~A0/Poster paper (33 to 47 inches, or 85 to 120 cm)
# The arrow will appear to be ~2 inches in height

# Bar
_BAR_XL = {
    "projection":None,
    "unit":None,
    "rotation":0,
    "max":None,
    "length":None,
    "height":0.4, # changed
    "reverse":False,
    "major_div":None,
    "minor_div":None,
    "minor_frac":0.66,
    "minor_type":"first",
    "facecolors":["black","white"],
    "edgecolors":"black",
    "edgewidth":4, # changed
    "tick_loc":"above",
    "basecolors":["black"],
    "tickcolors":["black"],
    "tickwidth":5 # changed
}

# Labels
_LABELS_XL = {
    "labels":None,
    "format":".2f",
    "format_int":True,
    "style":"major",
    "loc":"above",
    "pad":0,
    "sep":12, # changed
}

# Units
_UNITS_XL = {
    "label":None,
    "loc":"bar",
    "pad":0,
    "sep":12, # changed
}

# Text
_TEXT_XL = {
    "fontsize":48, # changed
    "textcolor":"black",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "fontweight":"regular",
    "stroke_width":4, # changed
    "stroke_color":"white",
    "rotation":None,
    "rotation_mode":"anchor",
}

# AOB
_AOB_XL = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":2, # changed
    "borderpad":2, # changed
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

## CONTAINER
# This makes an easy-to-call dictionary of all the defaults we've set, for easy unpacking by the set_size function
_DEFAULTS_SB = {
    "xs":[_BAR_XS, _LABELS_XS, _UNITS_XS, _TEXT_XS, _AOB_XS],
    "sm":[_BAR_SM, _LABELS_SM, _UNITS_SM, _TEXT_SM, _AOB_SM],
    "md":[_BAR_MD, _LABELS_MD, _UNITS_MD, _TEXT_MD, _AOB_MD],
    "lg":[_BAR_LG, _LABELS_LG, _UNITS_LG, _TEXT_LG, _AOB_LG],
    "xl":[_BAR_XL, _LABELS_XL, _UNITS_XL, _TEXT_XL, _AOB_XL],
}