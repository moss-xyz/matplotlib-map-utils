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

### CONSTANTS ###

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
    elif type(val) != int and type(val) != float:
        raise ValueError(f"The supplied type is not valid for {prop}, please provide a float or integer between {min} and {max}")
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

def _validate_types(prop, val, matches, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {matches}")
    elif none_ok==True and val is None:
        return val
    elif not type(val) in matches:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {matches}")
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
    elif (type(degrees)==int or type(degrees)==float) and (crs is not None or reference is not None or coords is not None):
            warnings.warn(f"A value for degrees was supplied; values for crs, reference, and coords will be ignored")
            return val
    else:
        if none_ok==False and val is None:
            raise ValueError(f"If degrees is set to None, then {prop} cannot be None: please provide a valid CRS input for PyProj instead")
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

# This final one is used for keys that are not validated
def _skip_validation(val, none_ok=False):
    return val

# TODO: This is a new one, add it in
def _validate_projection(prop, val, none_ok=False):
    if type(val)==pyproj.CRS:
        pass
    else:
        try:
            val = pyproj.CRS.from_user_input(val)
        except:
            raise Exception(f"Invalid CRS supplied ({val}), please provide a valid CRS input for PyProj instead")
    return val    

# TODO: This is a new one, add it in
# It is specifically to apply another validation function to the items in a list 
# Ex. if we want to validate a LIST of colors instead of a single color
def _validate_iterable(prop, val, func, kwargs=None):
    # Making sure we wrap everything in a list
    if type(val) not in [tuple, list]:
        val = [val]
    # Then, we apply our validation func with optional kwargs to each item in said list, relying on it to return an error value
    if kwargs is not None:
        for v in val:
            v = func(prop=prop, val=v, **kwargs)
        return val
    # The matplotlib built-in functions DON'T have that, and only ever take the one value
    else:
        for v in val:
            v = func(v)
        return val
    
# TODO: This is a new one, add it in
# It is specifically to apply multiple validation functions to a value, if needed
# Ex. If an item can be a string OR a list of strings, we can use this to validate it
# "labels":{"func":_validate_multiple, "kwargs":{"funcs":[_validate_type, _validate_list], "kwargs":[{"match":str, "none_ok":True}, {"list":["major","first_last","minor_all","minor_first"], "none_ok":True}]}}, # any string or any item in the list
def _validate_multiple(prop, val, funcs, kwargs):
    # Simply iterate through each func and kwarg
    for f,k in zip(funcs,kwargs):
        # We wrap the attempts in a try block to suppress the errors
        try:
            v = f(prop=prop, val=v, **k)
             # If we pass, we can stop here and return the value
            return val
        except:
            continue
    # If we didn't return a value and exit the loop yet, then the passed value is incorrect, as we raise an error
    raise ValueError(f"{val} is not a valid value for {prop}, please provide check the documentation")


### MORE VALIDITY FUNCTIONS ###
# These are more customized, and so are separated from the _validate_* functions above
# Mainly, they can process the input dictionaries wholesale, as well as the individual functions in it
# TODO: this has been updated!
def _validate_dict(input_dict, default_dict, functions, to_validate=None, return_clean=False, parse_false=True):
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
        if to_validate == "input":
            values = {key: val for key, val in values.items() if key in input_dict.keys()}
            functions = {key: val for key, val in functions.items() if key in input_dict.keys()}
        elif to_validate is not None:
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
            # NOTE: This is messy but the only way to check the projection dict without keywords
            elif key=="projection":
                _ = func(prop=key, val=val)
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


#### NEW CONTENT ####
# Need to merge with validation.py

_VALIDATE_PRIMARY = {
    "style":{"func":_validate_list, "kwargs":{"list":["ticks","boxes"]}},
    "location":{"func":_validate_list, "kwargs":{"list":["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]}},
}

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
    minor_type: Literal["all","first"] # whether the minor divisions should be drawn on all major divisions or just the first one
    # Boxes only
    facecolors: list | tuple | str # a color or list of colors to use for the faces of the boxes
    edgecolors: list | tuple | str # a color or list of colors to use for the edges of the boxes
    edgewidth: float | int # the line thickness of the edges of the boxes
    # Ticks only
    tick_loc: Literal["above","below","middle"] # the location of the ticks relative to the bar
    basecolors: list | tuple | str # a color or list of colors to use for the bottom bar
    tickcolors: list | tuple | str # a color or list of colors to use for the ticks
    tickwidth: float | int # the line thickness of the bottom bar and ticks

_VALID_BAR_TICK_LOC = get_args(_TYPE_BAR.__annotations__["tick_loc"])

_VALIDATE_BAR = {
    "projection":{"func":_validate_projection}, # must be a valid CRS
    "unit":{"func":_validate_list, "kwargs":{"list":list(units_standard.keys()), "none_ok":True}}, # any of the listed unit values are accepted
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "max":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "length":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "height":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "reverse":{"func":_validate_type, "kwargs":{"match":bool}}, # any bool

    "major_div":{"func":_validate_range, "kwargs":{"min":1, "max":None, "none_ok":True}}, # between 0 and inf
    "minor_div":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "minor_frac":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # ticks only: between 0 and 1
    "minor_type":{"func":_validate_list, "kwargs":{"list":["all","first"]}}, # either item in the list

    "facecolors":{"func":_validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # boxes only: any color value for matplotlib
    "edgecolors":{"func":_validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # boxes only: any color value for matplotlib
    "edgewidth":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # boxes only: between 0 and inf

    "tick_loc":{"func":_validate_list, "kwargs":{"list":_VALID_BAR_TICK_LOC}}, # ticks only: any item in the list
    "basecolors":{"func":_validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # ticks only: any color value for matplotlib
    "tickcolors":{"func":_validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # ticks only: any color value for matplotlib
    "tickwidth":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # ticks only: between 0 and inf
}

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
    # zorder: int # any integer

_VALID_LABELS_STYLE = get_args(_TYPE_LABELS.__annotations__["style"])
_VALID_LABELS_LOC = get_args(_TYPE_LABELS.__annotations__["loc"])
_VALID_LABELS_FONTFAMILY = get_args(_TYPE_LABELS.__annotations__["fontfamily"])
_VALID_LABELS_FONTSTYLE = get_args(_TYPE_LABELS.__annotations__["fontstyle"])
_VALID_LABELS_FONTWEIGHT = get_args(_TYPE_LABELS.__annotations__["fontweight"])
_VALID_LABELS_ROTATION_MODE = get_args(_TYPE_LABELS.__annotations__["rotation_mode"])

_VALIDATE_LABELS = {
    "labels":{"func":_validate_iterable, "kwargs":{"func":_validate_types,"kwargs":{"matches":[str,bool], "none_ok":True}}}, # any list of strings
    # "labels":{"func":_validate_multiple, "kwargs":{"funcs":[_validate_list,_validate_iterable], "kwargs":[{"list":["major","first_last","last_only","minor_all","minor_first"],"none_ok":True},{"func":_validate_types,"kwargs":{"matches":[str,bool], "none_ok":True}}]}}, # any list of strings or a special keyword
    "format":{"func":_validate_type, "kwargs":{"match":str}}, # only check that it is a string, not that it is a valid format string
    "format_int":{"func":_validate_type, "kwargs":{"match":bool}}, # any bool
    "style":{"func":_validate_list, "kwargs":{"list":_VALID_LABELS_STYLE}}, # any item in the list
    "loc":{"func":_validate_list, "kwargs":{"list":_VALID_LABELS_LOC, "none_ok":True}}, # any string in the list we allow
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolors":{"func":_validate_iterable, "kwargs":{"func":matplotlib.rcsetup.validate_color}}, # any color value for matplotlib
    "fontfamily":{"func":_validate_list, "kwargs":{"list":_VALID_LABELS_FONTFAMILY}},
    "fontstyle":{"func":_validate_list, "kwargs":{"list":_VALID_LABELS_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":_validate_list, "kwargs":{"list":_VALID_LABELS_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
    "sep":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    # "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

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
    # zorder: int # any integer

_VALID_UNITS_LOC = get_args(_TYPE_UNITS.__annotations__["loc"])
_VALID_UNITS_FONTFAMILY = get_args(_TYPE_UNITS.__annotations__["fontfamily"])
_VALID_UNITS_FONTSTYLE = get_args(_TYPE_UNITS.__annotations__["fontstyle"])
_VALID_UNITS_FONTWEIGHT = get_args(_TYPE_UNITS.__annotations__["fontweight"])
_VALID_UNITS_ROTATION_MODE = get_args(_TYPE_UNITS.__annotations__["rotation_mode"])

_VALIDATE_UNITS = {
    "label":{"func":_validate_type, "kwargs":{"match":str, "none_ok":True}}, # any string
    "loc":{"func":_validate_list, "kwargs":{"list":_VALID_UNITS_LOC, "none_ok":True}}, # any string in the list we allow
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontfamily":{"func":_validate_list, "kwargs":{"list":_VALID_UNITS_FONTFAMILY}},
    "fontstyle":{"func":_validate_list, "kwargs":{"list":_VALID_UNITS_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":_validate_list, "kwargs":{"list":_VALID_UNITS_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
    "sep":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    # "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

class _TYPE_TEXT(TypedDict, total=False):
    fontsize: str | float | int # any fontsize value for matplotlib
    textcolor: list | str # a color or list of colors to use for all the text elements
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity TODO: verify
    stroke_color: str # optional: any color value for matplotlib TODO: verify
    # zorder: int # any integer
    rotation: float | int # a value between -360 and 360 to rotate the text elements by
    rotation_mode: Literal["anchor","default"] # from matplotlib documentation

_VALID_TEXT_FONTFAMILY = get_args(_TYPE_TEXT.__annotations__["fontfamily"])
_VALID_TEXT_FONTSTYLE = get_args(_TYPE_TEXT.__annotations__["fontstyle"])
_VALID_TEXT_FONTWEIGHT = get_args(_TYPE_TEXT.__annotations__["fontweight"])
_VALID_TEXT_ROTATION_MODE = get_args(_TYPE_TEXT.__annotations__["rotation_mode"])

_VALIDATE_TEXT = {
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize for matplotlib
    "textcolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontfamily":{"func":_validate_list, "kwargs":{"list":_VALID_TEXT_FONTFAMILY}},
    "fontstyle":{"func":_validate_list, "kwargs":{"list":_VALID_TEXT_FONTSTYLE}},
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # between -360 and 360 degrees
    "rotation_mode":{"func":_validate_list, "kwargs":{"list":_VALID_TEXT_ROTATION_MODE, "none_ok":True}}, # any string in the list we allow
    # "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

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

_VALIDATE_AOB = {
    "facecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "edgecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "alpha":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "borderpad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "prop":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "frameon":{"func":_validate_type, "kwargs":{"match":bool}}, # any bool
    "bbox_to_anchor":{"func":_skip_validation}, # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
    "bbox_transform":{"func":_skip_validation} # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
}