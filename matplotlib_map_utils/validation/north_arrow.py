############################################################
# validation/north_arrow.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
# Math packages
import numpy
# Geo packages
import pyproj
# Graphical packages
import matplotlib
# matplotlib's useful validation functions
import matplotlib.rcsetup
# The types we use in this script
from typing import Tuple, TypedDict, Literal, get_args
# Finally, the validation functions
from . import functions as vf

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "_TYPE_BASE", "_TYPE_FANCY", "_TYPE_LABEL", "_TYPE_SHADOW", 
    "_TYPE_PACK", "_TYPE_AOB", "_TYPE_ROTATION"
]

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the inputs necessary for object creation we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion

class _TYPE_BASE(TypedDict, total=False):
    coords: numpy.array # must be 2D numpy array
    facecolor: str # any color value for matplotlib
    edgecolor: str # any color value for matplotlib
    linewidth: float | int # between 0 and inf
    zorder: int # any integer

class _TYPE_FANCY(TypedDict, total=False):
    coords: numpy.array # must be 2D numpy array
    facecolor: str # any color value for matplotlib
    zorder: int # any integer

class _TYPE_LABEL(TypedDict, total=False):
    text: str # any string that you want to display ("N" or "North" being the most common)
    position: Literal["top", "bottom", "left", "right"]  # from matplotlib documentation
    ha: Literal["left", "center", "right"] # from matplotlib documentation
    va: Literal["baseline", "bottom", "center", "center_baseline", "top"] # from matplotlib documentation
    fontsize: str | float | int # any fontsize value for matplotlib
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    color: str # any color value for matplotlib
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity
    stroke_color: str # any color value for matplotlib
    rotation: float | int # between -360 and 360
    zorder: int # any integer

class _TYPE_SHADOW(TypedDict, total=False):
    offset: Tuple[float | int, float | int] # two-length tuple or list of x,y values in points
    alpha: float | int # between 0 and 1
    shadow_rgbFace: str # any color vlaue for matplotlib

class _TYPE_PACK(TypedDict, total=False):
    sep: float | int # between 0 and inf
    align: Literal["top", "bottom", "left", "right", "center", "baseline"] # from matplotlib documentation
    pad: float | int # between 0 and inf
    width: float | int # between 0 and inf
    height: float | int # between 0 and inf
    mode: Literal["fixed", "expand", "equal"] # from matplotlib documentation

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

class _TYPE_ROTATION(TypedDict, total=False):
    degrees: float | int # anything between -360 and 360, or None for "auto"
    crs: str | int | pyproj.CRS # only required if degrees is None: should be a valid cartopy or pyproj crs, or a string that can be converted to that
    reference: Literal["axis", "data", "center"] # only required if degrees is None: should be either "axis" or "data" or "center"
    coords: Tuple[float | int, float | int] # only required if degrees is None: should be a tuple of coordinates in the relevant reference window

### VALIDITY DICTS ###
# These compile the functions in validation/functions, as well as matplotlib's built-in validity functions
# into dictionaries that can be used to validate all the inputs to a dictionary at once

_VALIDATE_PRIMARY = {
    "location":{"func":vf._validate_list, "kwargs":{"list":["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]}},
    "scale":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
}

_VALIDATE_BASE = {
    "coords":{"func":vf._validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "edgecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "linewidth":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "zorder":{"func":vf._validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_FANCY = {
    "coords":{"func":vf._validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "zorder":{"func":vf._validate_type, "kwargs":{"match":int}} # any integer
}

_VALID_LABEL_POSITION = get_args(_TYPE_LABEL.__annotations__["position"])
_VALID_LABEL_HA = get_args(_TYPE_LABEL.__annotations__["ha"])
_VALID_LABEL_VA = get_args(_TYPE_LABEL.__annotations__["va"])
_VALID_LABEL_FONTFAMILY = get_args(_TYPE_LABEL.__annotations__["fontfamily"])
_VALID_LABEL_FONTSTYLE = get_args(_TYPE_LABEL.__annotations__["fontstyle"])
_VALID_LABEL_FONTWEIGHT = get_args(_TYPE_LABEL.__annotations__["fontweight"])

_VALIDATE_LABEL = {
    "text":{"func":vf._validate_type, "kwargs":{"match":str}}, # any string
    "position":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABEL_POSITION}},
    "ha":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABEL_HA}},
    "va":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABEL_VA}},
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "fontfamily":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABEL_FONTFAMILY}},
    "fontstyle":{"func":vf._validate_list, "kwargs":{"list":_VALID_LABEL_FONTSTYLE}},
    "color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "zorder":{"func":vf._validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_SHADOW = {
    "offset":{"func":vf._validate_tuple, "kwargs":{"length":2, "types":[float, int]}},
    "alpha":{"func":vf._validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "shadow_rgbFace":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
}

_VALID_PACK_ALIGN = get_args(_TYPE_PACK.__annotations__["align"])
_VALID_PACK_MODE = get_args(_TYPE_PACK.__annotations__["mode"])

_VALIDATE_PACK = {
    "sep":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "align":{"func":vf._validate_list, "kwargs":{"list":_VALID_PACK_ALIGN}},
    "pad":{"func":vf._validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "width":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "height":{"func":vf._validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "mode":{"func":vf._validate_list, "kwargs":{"list":_VALID_PACK_MODE}}
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
    "bbox_transform":{"func":vf._skip_validation} # NOTE: currently unvalidated, use at your own risk!
}

_VALID_ROTATION_REFERENCE = get_args(_TYPE_ROTATION.__annotations__["reference"])

_VALIDATE_ROTATION = {
    "degrees":{"func":vf._validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "crs":{"func":vf._validate_crs, "kwargs":{"none_ok":True}}, # see _validate_crs for details on what is accepted
    "reference":{"func":vf._validate_list, "kwargs":{"list":_VALID_ROTATION_REFERENCE, "none_ok":True}}, # see _VALID_ROTATION_REFERENCE for accepted values
    "coords":{"func":vf._validate_tuple, "kwargs":{"length":2, "types":[float, int], "none_ok":True}} # only required if degrees is None: should be a tuple of coordinates in the relevant reference window
}