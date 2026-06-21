############################################################
# validation/shared.py contains code re-used across objects
# for the purposes of the validation
############################################################

import numpy
import pyproj
import matplotlib.rcsetup
from typing import Annotated, Any, Literal
from pydantic import BeforeValidator

### SHARED LITERAL ALIASES ###
# These name the enumerated value-sets used across the validation models.
# They are referenced by BOTH the pydantic models (for runtime validation) and
# the TypedDicts (for editor intellisense), so the allowed values can never drift
# between the two representations.

# Shared across components
Location = Literal["upper right", "upper left", "lower left", "lower right",
                   "center left", "center right", "lower center", "upper center", "center"]
FontFamily = Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]
FontStyle = Literal["normal", "italic", "oblique"]
FontWeight = Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"]
RotationMode = Literal["anchor", "default"]

# scale_bar-specific
ScaleBarStyle = Literal["ticks", "boxes"]
BarUnit = Literal["m", "km", "ft", "yd", "mi", "nmi"]
MinorType = Literal["all", "first", "none"]
TickLoc = Literal["above", "below", "middle"]
LabelStyle = Literal["major", "first_last", "last_only", "minor_all", "minor_first"]
LabelsLoc = Literal["above", "below"]
UnitsLoc = Literal["bar", "text", "opposite"]

# north_arrow-specific
LabelPosition = Literal["top", "bottom", "left", "right"]
HAlign = Literal["left", "center", "right"]
VAlign = Literal["baseline", "bottom", "center", "center_baseline", "top"]
PackAlign = Literal["top", "bottom", "left", "right", "center", "baseline"]
PackMode = Literal["fixed", "expand", "equal"]
RotationReference = Literal["axis", "data", "center"]

# inset_map-specific
ExtentReturn = Literal["shape", "patch", "fig", "ax"]
DetailReturn = Literal["connectors", "lines"]

def _validate_color(v):
    if v is None:
        return v
    matplotlib.rcsetup.validate_color(v)
    return v

MatplotlibColor = Annotated[Any, BeforeValidator(_validate_color)]

def _validate_2d_array(v):
    if isinstance(v, (list, tuple)):
        v = numpy.array(v)
    if not isinstance(v, numpy.ndarray):
        raise ValueError("must be a numpy.ndarray")
    if v.ndim != 2:
        raise ValueError("must be a 2D numpy array")
    return v

Numpy2DArray = Annotated[numpy.ndarray, BeforeValidator(_validate_2d_array)]

def _validate_fontsize(v):
    if v is None:
        return v
    matplotlib.rcsetup.validate_fontsize(v)
    return v

MatplotlibFontsize = Annotated[Any, BeforeValidator(_validate_fontsize)]

def _validate_crs_input(v):
    if v is None:
        return v
    if isinstance(v, pyproj.CRS):
        return v
    try:
        return pyproj.CRS.from_user_input(v)
    except Exception:
        raise ValueError(f"Invalid CRS supplied ({v}), please provide a valid CRS input that PyProj can use instead")

CRSInput = Annotated[Any, BeforeValidator(_validate_crs_input)]

def _get_size_key(size: Any) -> str:
    """Convert a size string (e.g. 'medium', 'x-small') to its canonical short key."""
    if not isinstance(size, str):
        return "md"
    size_map = {
        "xs": "xs", "xsmall": "xs", "x-small": "xs",
        "sm": "sm", "small": "sm",
        "md": "md", "medium": "md",
        "lg": "lg", "large": "lg",
        "xl": "xl", "xlarge": "xl", "x-large": "xl"
    }
    return size_map.get(size.lower(), "md")

def _del_keys(d: dict, to_remove: list) -> dict:
    """Return a copy of dict *d* with the specified keys removed."""
    return {key: val for key, val in d.items() if key not in to_remove}