############################################################
# validation/inset_map.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Geo packages
import matplotlib.axes
import pyproj
# Graphical packages
import matplotlib
# matplotlib's useful validation functions
import matplotlib.rcsetup
# The types we use in this script
from typing import TypedDict, Literal
# Finally, the validation functions
from . import functions as vf

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "_TYPE_INSET", "_VALIDATE_INSET",
    "_TYPE_EXTENT", "_VALIDATE_EXTENT",
    "_TYPE_DETAIL", "_VALIDATE_DETAIL",
]

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the inputs necessary for object creation we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion

class _TYPE_INSET(TypedDict, total=False):
    size: int | float | tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between 0 and inf
    pad: int | float | tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between 0 and inf
    coords: tuple[int | float, int | float] | list[int | float, int | float] # each int or float should be between -inf and inf

class _TYPE_EXTENT(TypedDict, total=False):
    pax: matplotlib.axes.Axes # any Matplotlib Axes
    bax: matplotlib.axes.Axes # any Matplotlib Axes
    pcrs: str | int | pyproj.CRS # should be a valid cartopy or pyproj crs, or a string or int that can be converted to that
    bcrs: str | int | pyproj.CRS # should be a valid cartopy or pyproj crs, or a string or int that can be converted to that
    straighten: bool # either true or false
    pad: float | int # any positive float or integer
    plot: bool # either true or false
    to_return: Literal["shape","patch","fig","ax"] | None # any item in the list, or None if nothing should be returned
    facecolor: str # a color to use for the face of the box
    linecolor: str # a color to use for the edge of the box
    alpha: float | int # any positive float or integer
    linewidth: float | int # any positive float or integer

class _TYPE_DETAIL(TypedDict, total=False):
    to_return: Literal["connectors", "lines"] | None # any item in the list, or None if nothing should be returned
    connector_color: str # a color to use for the face of the box
    connector_width: float | int # any positive float or integer

### VALIDITY DICTS ###
# These compile the functions in validation/functions, as well as matplotlib's built-in validity functions
# into dictionaries that can be used to validate all the inputs to a dictionary at once

_VALIDATE_INSET = {
    "location":{"func":vf._validate_list, "kwargs":{"list":["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]}},
    "size":{"func":vf._validate_or, "kwargs":{"funcs":[vf._validate_range, vf._validate_and], "kwargs":[{"min":0, "none_ok":True}, {"funcs":[vf._validate_tuple, vf._validate_iterable], "kwargs":[{"length":2, "types":[float, int]}, {"func":vf._validate_range, "kwargs":{"min":0}}]}]}}, # between 0 and inf, or a two-tuple of (x,y) size, each between 0 and inf
    "pad":{"func":vf._validate_or, "kwargs":{"funcs":[vf._validate_range, vf._validate_and], "kwargs":[{"min":0, "none_ok":True}, {"funcs":[vf._validate_tuple, vf._validate_iterable], "kwargs":[{"length":2, "types":[float, int]}, {"func":vf._validate_range, "kwargs":{"min":0}}]}]}}, # between 0 and inf, or a two-tuple of (x,y) size, each between 0 and inf
    "coords":{"func":vf._validate_tuple, "kwargs":{"length":2, "types":[float, int], "none_ok":True}}, # a two-tuple of coordinates where you want to place the inset map
    "to_plot":{"func":vf._validate_iterable, "kwargs":{"func":vf._validate_keys, "kwargs":{"keys":["data","kwargs"], "none_ok":True}}}, # a list of dictionaries, where each contains "data" and "kwargs" keys
}

_VALIDATE_EXTENT = {
    "pax":{"func":vf._validate_type, "kwargs":{"match":matplotlib.axes.Axes}}, # any Matplotlib Axes
    "bax":{"func":vf._validate_type, "kwargs":{"match":matplotlib.axes.Axes}}, # any Matplotlib Axes
    "pcrs":{"func":vf._validate_projection, "kwargs":{"none_ok":False}}, # any valid projection input for PyProj
    "bcrs":{"func":vf._validate_projection, "kwargs":{"none_ok":False}}, # any valid projection input for PyProj
    "straighten":{"func":vf._validate_type, "kwargs":{"match":bool}}, # true or false
    "pad":{"func":vf._validate_range, "kwargs":{"min":0}}, # any positive number
    "plot":{"func":vf._validate_type, "kwargs":{"match":bool}}, # true or false
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "linecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "alpha":{"func":vf._validate_range, "kwargs":{"min":0}}, # any positive number
    "linewidth":{"func":vf._validate_range, "kwargs":{"min":0}}, # any positive number
    "to_return":{"func":vf._validate_list, "kwargs":{"list":["shape", "patch", "fig", "ax"], "none_ok":True}}, # any value in this list
}

_VALIDATE_DETAIL = {
    "to_return":{"func":vf._validate_list, "kwargs":{"list":["connectors", "lines"], "none_ok":True}}, # any value in this list
    "connector_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "connector_width":{"func":vf._validate_range, "kwargs":{"min":0}}, # any positive number
}