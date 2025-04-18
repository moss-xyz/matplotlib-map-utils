############################################################
# validation/scale_bar.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Geo packages
import pyproj
# matplotlib's useful validation functions
import matplotlib.rcsetup
# The types we use in this script
from typing import TypedDict, Literal, get_args
# Finally, the validation functions
from . import functions as vf

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "preferred_divs", "convert_dict", "units_standard",
    "_TYPE_BAR", "_TYPE_LABELS", "_TYPE_UNITS", "_TYPE_TEXT", "_TYPE_AOB"
]

### CONSTANTS ###
# These are constants that we use elsewhere in the script
# when setting up a scale bar

# A list of preferred "highest" numbers
# And the corresponding major and min divs
preferred_divs = {
    2:[4,2],
    2.5:[5,1],
    3:[3,3],
    4:[4,2],
    5:[5,1],
    6:[3,2],
    7:[2,1],
    8:[4,2],
    9:[3,3],
    10:[5,2],
}

# For converting between units
# Everything is relative to the meter
convert_dict = {
    "m":1,
    "ft":0.3048,
    "yd":0.9144,
    "mi":1609.34,
    "nmi":1852,
    "km":1000,
}

# Standardizing the text of the units
units_standard = {
    # degrees
    # note these are not valid units to convert INTO
    # "deg":"deg", "deg":"degree",
    # feet
    # the last one at the end is how many projections report it
    "ft":"ft", "ftUS":"ft", "foot":"ft", "feet":"ft", "US survey foot":"ft",
    # yards
    "yd":"yd", "yard":"yd", "yards":"yd",
    # miles
    "mi":"mi", "mile":"mi", "miles":"mi",
    # nautical miles
    # note that nm is NOT accepted - that is nanometers!
    "nmi":"nmi", "nautical":"nmi", "nautical mile":"nmi", "nautical miles":"nmi",
    # meters
    "m":"m", "meter":"m", "metre":"m", "meters":"m", "metres":"m",
    # kilometers
    "km":"km", "kilometer":"km", "kilometers":"km", "kilometre":"km", "kilometres":"km",
}

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the inputs necessary for object creation we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion

class _TYPE_BAR(TypedDict, total=False):
    projection: str | int | pyproj.CRS # should be a valid cartopy or pyproj crs, or a string or int that can be converted to that
    unit: Literal["m","km","ft","yd","mi","nmi"] # the units you want to convert the bar to, if different than the projection units
    rotation: float | int # between -360 and 360
    max: float | int # the max bar value, in desired units (as specified by units dict)
    length: float | int # the length of the bar in inches (if > 1) or as a % of the axis (if between 0 and 1)
    height: float | int # the height of the bar in inches
    reverse: bool # flag if the order of the elements should be reversed
    major_div: int # the number of major divisions on the bar
    minor_div: int # the number of minor divisions on the bar
    minor_frac: float # the fraction of the major division that the minor division should be (e.g. 0.5 = half the size of the major division)
    minor_type: Literal["all","first","none"] # whether the minor divisions should be drawn on all major divisions or just the first one
    # Boxes only
    facecolors: list | tuple | str # a color or list of colors to use for the faces of the boxes
    edgecolors: list | tuple | str # a color or list of colors to use for the edges of the boxes
    edgewidth: float | int # the line thickness of the edges of the boxes
    # Ticks only
    tick_loc: Literal["above","below","middle"] # the location of the ticks relative to the bar
    basecolors: list | tuple | str # a color or list of colors to use for the bottom bar
    tickcolors: list | tuple | str # a color or list of colors to use for the ticks
    tickwidth: float | int # the line thickness of the bottom bar and ticks


class _TYPE_LABELS(TypedDict, total=False):
    labels: list | tuple # a list of text labels to replace the default labels of the major elements
    format: str # a format string to apply to the default labels of the major elements
    format_int: bool # if True, float divisions that end in zero wil be converted to ints (e.g. 1.0 -> 1)
    style: Literal["major","first_last","last_only","minor_all","minor_first"] # each selection in the list creates a different set of labels
    loc: Literal["above","below"] # whether the major text elements should appear above or below the bar
    fontsize: str | float | int # any fontsize value for matplotlib
    textcolors: list | str # a color or list of colors to use for the major text elements
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity
    stroke_color: str # optional: any color value for matplotlib
    rotation: float | int # a value between -360 and 360 to rotate the text elements by
    rotation_mode: Literal["anchor","default"] # from matplotlib documentation
    sep: float | int # between 0 and inf, used to add separation between the labels and the bar
    pad: float | int # between 0 and inf, used to add separation between the labels and the bar


class _TYPE_UNITS(TypedDict, total=False):
    label: str # an override for the units label
    loc: Literal["bar","text","opposite"] # where the units text should appear (in line with the bar, or the major div text, or opposite the major div text)
    fontsize: str | float | int # any fontsize value for matplotlib
    textcolor: str # any color value for matplotlib
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity
    stroke_color: str # any color value for matplotlib
    rotation: float | int # between -360 and 360
    rotation_mode: Literal["anchor","default"] # from matplotlib documentation
    sep: float | int # between 0 and inf, used to add separation between the units text and the bar ("opposite" only)
    pad: float | int # between 0 and inf, used to add separation between the units text and the bar ("opposite" only)


class _TYPE_TEXT(TypedDict, total=False):
    fontsize: str | float | int # any fontsize value for matplotlib
    textcolor: list | str # a color or list of colors to use for all the text elements
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity
    stroke_color: str # optional: any color value for matplotlib
    rotation: float | int # a value between -360 and 360 to rotate the text elements by
    rotation_mode: Literal["anchor","default"] # from matplotlib documentation


class _TYPE_AOB(TypedDict, total=False):
    facecolor: str # NON-STANDARD: used to set the facecolor of the offset box (i.e. to white), any color vlaue for matplotlib
    edgecolor: str # NON-STANDARD: used to set the edge of the offset box (i.e. to black), any color vlaue for matplotlib
    alpha: float | int # NON-STANDARD: used to set the transparency of the face color of the offset box^, between 0 and 1
    pad: float | int # between 0 and inf
    borderpad: float | int # between 0 and inf
    prop: str | float | int # any fontsize value for matplotlib
    frameon: bool # any bool
    # bbox_to_anchor: None # NOTE: currently unvalidated, use at your own risk!
    # bbox_transform: None # NOTE: currently unvalidated, use at your own risk!

### VALIDITY DICTS ###
# These compile the functions in validation/functions, as well as matplotlib's built-in validity functions
# into dictionaries that can be used to validate all the inputs to a dictionary at once

_VALIDATE_PRIMARY = {
    "style":{"func":vf._validate_list, "kwargs":{"list":["ticks","boxes"]}},
    "location":{"func":vf._validate_list, "kwargs":{"list":["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]}},
}

_VALID_BAR_TICK_LOC = get_args(_TYPE_BAR.__annotations__["tick_loc"])
_VALID_BAR_MINOR_TYPE = get_args(_TYPE_BAR.__annotations__["minor_type"]) 

_VALIDATE_BAR = {
    "projection":{"func":vf._validate_projection, "kwargs":{"none_ok":False}}, # must be a valid CRS
    "unit":{"func":vf._validate_list, "kwargs":{"list":list(units_standard.keys()), "none_ok":True}}, # any of the listed unit values are accepted
    "rotation":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "max":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "length":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "height":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "reverse":{"func":vf._validate_type, "kwargs":{"match":bool}}, # any bool

    "major_div":{"func":vf._validate_range, "kwargs":{"min":1, "max":None, "none_ok":True}}, # between 0 and inf
    "minor_div":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "minor_frac":{"func":vf._validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # ticks only: between 0 and 1
    "minor_type":{"func":vf._validate_list, "kwargs":{"list":_VALID_BAR_MINOR_TYPE, "none_ok":True}}, # any item in the list, or None (for no minor)

    "facecolors":{"func":vf._validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # boxes only: any color value for matplotlib
    "edgecolors":{"func":vf._validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # boxes only: any color value for matplotlib
    "edgewidth":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # boxes only: between 0 and inf

    "tick_loc":{"func":vf._validate_list, "kwargs":{"list":_VALID_BAR_TICK_LOC}}, # ticks only: any item in the list
    "basecolors":{"func":vf._validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # ticks only: any color value for matplotlib
    "tickcolors":{"func":vf._validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # ticks only: any color value for matplotlib
    "tickwidth":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # ticks only: between 0 and inf
}

_VALID_LABELS_STYLE = get_args(_TYPE_LABELS.__annotations__["style"])
_VALID_LABELS_LOC = get_args(_TYPE_LABELS.__annotations__["loc"])
_VALID_LABELS_FONTFAMILY = get_args(_TYPE_LABELS.__annotations__["fontfamily"])
_VALID_LABELS_FONTSTYLE = get_args(_TYPE_LABELS.__annotations__["fontstyle"])
_VALID_LABELS_FONTWEIGHT = get_args(_TYPE_LABELS.__annotations__["fontweight"])
_VALID_LABELS_ROTATION_MODE = get_args(_TYPE_LABELS.__annotations__["rotation_mode"])

_VALIDATE_LABELS = {
    "labels":{"func":vf._validate_iterable, "kwargs":{"func":vf._validate_types,"kwargs":{"matches":[str,bool], "none_ok":True}}}, # any list of strings
    "format":{"func":vf._validate_type, "kwargs":{"match":str}}, # only check that it is a string, not that it is a valid format string
    "format_int":{"func":vf._validate_type, "kwargs":{"match":bool}}, # any bool
    "style":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABELS_STYLE}}, # any item in the list
    "loc":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABELS_LOC, "none_ok":True}}, # any string in the list we allow
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolors":{"func":vf._validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # any color value for matplotlib
    "fontfamily":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABELS_FONTFAMILY}},
    "fontstyle":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABELS_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABELS_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
    "sep":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "pad":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
}

_VALID_UNITS_LOC = get_args(_TYPE_UNITS.__annotations__["loc"])
_VALID_UNITS_FONTFAMILY = get_args(_TYPE_UNITS.__annotations__["fontfamily"])
_VALID_UNITS_FONTSTYLE = get_args(_TYPE_UNITS.__annotations__["fontstyle"])
_VALID_UNITS_FONTWEIGHT = get_args(_TYPE_UNITS.__annotations__["fontweight"])
_VALID_UNITS_ROTATION_MODE = get_args(_TYPE_UNITS.__annotations__["rotation_mode"])

_VALIDATE_UNITS = {
    "label":{"func":vf._validate_type, "kwargs":{"match":str, "none_ok":True}}, # any string
    "loc":{"func":vf._validate_list, "kwargs":{"list":_VALID_UNITS_LOC, "none_ok":True}}, # any string in the list we allow
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontfamily":{"func":vf._validate_list, "kwargs":{"list":_VALID_UNITS_FONTFAMILY}},
    "fontstyle":{"func":vf._validate_list, "kwargs":{"list":_VALID_UNITS_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":vf._validate_list, "kwargs":{"list":_VALID_UNITS_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
    "sep":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "pad":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
}

_VALID_TEXT_FONTFAMILY = get_args(_TYPE_TEXT.__annotations__["fontfamily"])
_VALID_TEXT_FONTSTYLE = get_args(_TYPE_TEXT.__annotations__["fontstyle"])
_VALID_TEXT_FONTWEIGHT = get_args(_TYPE_TEXT.__annotations__["fontweight"])
_VALID_TEXT_ROTATION_MODE = get_args(_TYPE_TEXT.__annotations__["rotation_mode"])

_VALIDATE_TEXT = {
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontfamily":{"func":vf._validate_list, "kwargs":{"list":_VALID_TEXT_FONTFAMILY}},
    "fontstyle":{"func":vf._validate_list, "kwargs":{"list":_VALID_TEXT_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":vf._validate_list, "kwargs":{"list":_VALID_TEXT_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
}

_VALIDATE_AOB = {
    "facecolor":{"func":vf._validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "edgecolor":{"func":vf._validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "alpha":{"func":vf._validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "pad":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "borderpad":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "prop":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "frameon":{"func":vf._validate_type, "kwargs":{"match":bool}}, # any bool
    "bbox_to_anchor":{"func":vf._skip_validation}, # NOTE: currently unvalidated, use at your own risk!
    "bbox_transform":{"func":vf._skip_validation}, # NOTE: currently unvalidated, use at your own risk!
}