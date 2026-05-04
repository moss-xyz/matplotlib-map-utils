############################################################
# validation/shared.py contains code re-used across objects
# for the purposes of the validation
############################################################

import numpy
import pyproj
import matplotlib.rcsetup
from typing import Annotated, Any
from pydantic import BeforeValidator

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