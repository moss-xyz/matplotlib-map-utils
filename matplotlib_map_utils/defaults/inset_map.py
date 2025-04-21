#################################################################
# defaults/inset_map.py contains default values for the InsetMaps
# at difference plot sizes (xsmall to xlarge)
# see their corresponding sizes under each default heading
#################################################################

# The main variables that update are the following:
# inset map: size, pad
# labels: sep, style
# units: sep
# text: fontsize, stroke_width (also changes labels and units)
# aob: pad, borderpad

## X-SMALL DEFAULTS
# Should work well for ~A8ish paper (2 to 3 inches, or 5 to 8 cm)

# Map
_INSET_MAP_XS = {
    "size":0.5,
    "pad":0.05,
}

## SMALL DEFAULTS
# Should work well for ~A6 paper (4 to 6 inches, or 11 to 15 cm)

# Map
_INSET_MAP_SM = {
    "size":1,
    "pad":0.1,
}

## MEDIUM DEFAULTS
# Should work well for ~A4/Letter paper (8 to 12 inches, or 21 to 30 cm)

# Map
_INSET_MAP_MD = {
    "size":2,
    "pad":0.25,
}

## LARGE DEFAULTS
# Should work well for ~A2 paper (16 to 24 inches, or 42 to 60 cm)

# Map
_INSET_MAP_LG = {
    "size":4,
    "pad":0.5,
}

## X-LARGE DEFAULTS
# Should work well for ~A0/Poster paper (33 to 47 inches, or 85 to 120 cm)

# Map
_INSET_MAP_XL = {
    "size":8,
    "pad":1,
}

## CONTAINER
# This makes an easy-to-call dictionary of all the defaults we've set, for easy unpacking by the set_size function
_DEFAULTS_IM = {
    "xs":[_INSET_MAP_XS],
    "sm":[_INSET_MAP_SM],
    "md":[_INSET_MAP_MD],
    "lg":[_INSET_MAP_LG],
    "xl":[_INSET_MAP_XL],
}