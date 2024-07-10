############################################################
# validation.py contains all the main objects and functions
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

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the inputs necessary for object creation we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion

class _TYPE_BASE(TypedDict, total=False):
    coords: numpy.array # must be 2D numpy array
    scale: float # between 0 and inf
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
    # bbox_transform: None

class _TYPE_ROTATION(TypedDict, total=False):
    degrees: float | int # anything between -360 and 360, or None for "auto"
    crs: str | int | pyproj.CRS # only required if degrees is None: should be a valid cartopy or pyproj crs, or a string that can be converted to that
    reference: Literal["axis", "data", "center"] # only required if degrees is None: should be either "axis" or "data" or "center"
    coords: Tuple[float | int, float | int] # only required if degrees is None: should be a tuple of coordinates in the relevant reference window

### VALIDITY CHECKS ###
# Functions and variables used for validating inputs for classes
# All have a similar form, taking in the name of the property (prop), the value (val)
# some parameters to check against (min/max, list, type, etc.),
# and whether or not None is acceptable value

def _validate_list(prop, val, list, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value in this list: {list}")
    elif none_ok==True and val is None:
        return val
    elif not val in list:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value in this list: {list}")
    return val

def _validate_range(prop, val, min, max, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif none_ok==True and val is None:
        return val
    elif max is not None:
        if not val >= min and not val <= max:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif max is None:
        if not val >= min:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value greater than {min}")
    return val

def _validate_type(prop, val, match, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {match}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==match:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {match}")
    return val

def _validate_coords(prop, val, numpy_type, dims, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==numpy_type:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif not val.ndim==dims:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a numpy array with {dims} dimensions")
    return val

def _validate_tuple(prop, val, length, types, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif none_ok==True and val is None:
        return val
    elif type(val)!=tuple:
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif len(val)!=length:
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    else:
        for item in val:
            if type(item) not in types:
                raise ValueError(f"{type(item)} is not a valid value for the items in {prop}, please provide a value of one of the following types: {types}")
    return val

def _validate_color_or_none(prop, val, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a color string acceptable to matplotlib instead")
    elif none_ok==True and val is None:
        return val
    else:
        matplotlib.rcsetup.validate_color(val)
    return val

# NOTE: This one is a bit messy, particularly with the rotation module, but I can't think of a better way to do it...
def _validate_crs(prop, val, rotation_dict, none_ok=False):
    degrees = rotation_dict.get("degrees",None)
    crs = rotation_dict.get("crs",None)
    reference = rotation_dict.get("reference",None)
    coords = rotation_dict.get("coords",None)
    
    if degrees is None:
        if reference == "center":
            if crs is None:
                raise ValueError(f"If degrees is set to None, and reference is 'center', then a valid crs must be supplied")
        else:
            if crs is None or reference is None or coords is None:
                raise ValueError(f"If degrees is set to None, then crs, reference, and coords cannot be None: please provide a valid input for each of these variables instead")
    elif (type(degrees)==int or type(degrees)==float) and (crs is None or reference is None or coords is None):
            warnings.warn(f"A value for rotation was supplied; values for crs, reference, and coords will be ignored")
            return val
    else:
        if none_ok==False and val is None:
            raise ValueError(f"If rotation is set to None, then {prop} cannot be None: please provide a valid CRS input for PyProj instead")
        elif none_ok==True and val is None:
            return val
    # This happens if (a) a value for CRS is supplied and (b) a value for degrees is NOT supplied
    if type(val)==pyproj.CRS:
        pass
    else:
        try:
            val = pyproj.CRS.from_user_input(val)
        except:
            raise Exception(f"Invalid CRS supplied ({val}), please provide a valid CRS input for PyProj instead")
    return val

### VALIDITY DICTS ###
# These compile the functions above^, as well as matplotlib's built-in validity functions
# into dictionaries that can be used to validate all the inputs to a dictionary at once

_VALIDATE_BASE = {
    "coords":{"func":_validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "scale":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "edgecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "linewidth":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_FANCY = {
    "coords":{"func":_validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALID_LABEL_POSITION = get_args(_TYPE_LABEL.__annotations__["position"])
_VALID_LABEL_HA = get_args(_TYPE_LABEL.__annotations__["ha"])
_VALID_LABEL_VA = get_args(_TYPE_LABEL.__annotations__["va"])
_VALID_LABEL_FONTFAMILY = get_args(_TYPE_LABEL.__annotations__["fontfamily"])
_VALID_LABEL_FONTSTYLE = get_args(_TYPE_LABEL.__annotations__["fontstyle"])
_VALID_LABEL_FONTWEIGHT = get_args(_TYPE_LABEL.__annotations__["fontweight"])

_VALIDATE_LABEL = {
    "text":{"func":_validate_type, "kwargs":{"match":str}}, # any string
    "position":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_POSITION}},
    "ha":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_HA}},
    "va":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_VA}},
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "fontfamily":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_FONTFAMILY}},
    "fontstyle":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_FONTSTYLE}},
    "color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_SHADOW = {
    "offset":{"func":_validate_tuple, "kwargs":{"length":2, "types":[float, int]}},
    "alpha":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "shadow_rgbFace":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
}

_VALID_PACK_ALIGN = get_args(_TYPE_PACK.__annotations__["align"])
_VALID_PACK_MODE = get_args(_TYPE_PACK.__annotations__["mode"])

_VALIDATE_PACK = {
    "sep":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "align":{"func":_validate_list, "kwargs":{"list":_VALID_PACK_ALIGN}},
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "width":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "height":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "mode":{"func":_validate_list, "kwargs":{"list":_VALID_PACK_MODE}}
}

_VALIDATE_AOB = {
    "facecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "edgecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "alpha":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "borderpad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "prop":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "frameon":{"func":_validate_type, "kwargs":{"match":bool}}, # any bool
    # "bbox_to_anchor":None, # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
    # "bbox_transform":None # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
}

_VALID_ROTATION_REFERENCE = get_args(_TYPE_ROTATION.__annotations__["reference"])

_VALIDATE_ROTATION = {
    "degrees":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "crs":{"func":_validate_crs, "kwargs":{"none_ok":True}}, # see _validate_crs for details on what is accepted
    "reference":{"func":_validate_list, "kwargs":{"list":_VALID_ROTATION_REFERENCE, "none_ok":True}}, # see _VALID_ROTATION_REFERENCE for accepted values
    "coords":{"func":_validate_tuple, "kwargs":{"length":2, "types":[float, int], "none_ok":True}} # only required if degrees is None: should be a tuple of coordinates in the relevant reference window
}

### MORE VALIDITY FUNCTIONS ###
# These are more customized, and so are separated from the _validate_* functions above
# Mainly, they can process the input dictionaries wholesale, as well as the individual functions in it

def _validate_dict(input_dict, default_dict, functions, to_validate: list=None, return_clean=False, parse_false=True):
    if input_dict == False:
        if parse_false == True:
            return None
        else:
            return False
    elif input_dict is None or input_dict == True:
        return default_dict
    elif type(input_dict) != dict:
        raise ValueError(f"A dictionary (NoneType) must be provided, please double-check your inputs")
    else:
        values = default_dict | input_dict
        # Pre-checking that no invalid keys are passed
        invalid = [key for key in values.keys() if key not in functions.keys() and key not in ["bbox_to_anchor", "bbox_transform"]]
        if len(invalid) > 0:
            print(f"Warning: Invalid keys detected ({invalid}). These will be ignored.")
        # First, trimming our values to only those we need to validate
        if to_validate is not None:
            values = {key: val for key, val in values.items() if key in to_validate}
            functions = {key: val for key, val in functions.items() if key in values.keys()}
        else:
            values = {key: val for key, val in values.items() if key in functions.keys()}
            functions = {key: val for key, val in functions.items() if key in values.keys()}
        # Now, running the function with the necessary kwargs
        for key,val in values.items():
            fd = functions[key]
            func = fd["func"]
            # NOTE: This is messy but the only way to get the rotation value to the crs function
            if key=="crs":
                _ = func(prop=key, val=val, rotation_dict=values, **fd["kwargs"])
            # Our custom functions always have this dictionary key in them, so we know what form they take
            elif "kwargs" in fd:
                _ = func(prop=key, val=val, **fd["kwargs"])
            # The matplotlib built-in functions DON'T have that, and only ever take the one value
            else:
                _ = func(val)
        if return_clean==True:
            return values

# This function can process the _VALIDATE dictionaries we established above, but for single variables at a time
def _validate(validate_dict, prop, val, return_val=True, kwargs={}):
    fd = validate_dict[prop]
    func = fd["func"]
    # Our custom functions always have this dictionary key in them, so we know what form they take
    if "kwargs" in fd:
        val = func(prop=prop, val=val, **(fd["kwargs"] | kwargs))
    # The matplotlib built-in functions DON'T have that, and only ever take the one value
    else:
        val = func(val)
    if return_val==True:
        return val