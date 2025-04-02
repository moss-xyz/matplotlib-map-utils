############################################################
# validation/inset_map.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

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
    "_TYPE_INSET", "_VALIDATE_INSETS", "_TYPE_UNITS", "_TYPE_TEXT", "_TYPE_AOB"
]

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the inputs necessary for object creation we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion

class _TYPE_INSET(TypedDict, total=False):
    size: int | float | tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between 0 and inf
    pad: int | float | tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between 0 and inf
    coords: tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between 0 and inf

### VALIDITY DICTS ###
# These compile the functions in validation/functions, as well as matplotlib's built-in validity functions
# into dictionaries that can be used to validate all the inputs to a dictionary at once

_VALIDATE_INSET = {
    "location":{"func":vf._validate_list, "kwargs":{"list":["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]}},
    "size":{"func":vf._validate_or, "kwargs":{"funcs":[vf._validate_range, vf._validate_and], "kwargs":[{"min":0}, {"funcs":[vf._validate_tuple, vf._validate_iterable], "kwargs":[{"length":2, "types":[float, int]}, {"func":vf._validate_range, "kwargs":{"min":0}}]}]}},
    "pad":{"func":vf._validate_or, "kwargs":{"funcs":[vf._validate_range, vf._validate_and], "kwargs":[{"min":0}, {"funcs":[vf._validate_tuple, vf._validate_iterable], "kwargs":[{"length":2, "types":[float, int]}, {"func":vf._validate_range, "kwargs":{"min":0}}]}]}},
    "coords":{"func":vf._validate_tuple, "kwargs":{"length":2, "types":[float, int]}},
}