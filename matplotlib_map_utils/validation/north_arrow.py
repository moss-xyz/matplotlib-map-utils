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
from typing import Annotated, Union, Tuple, Optional, Literal, Any
# Pydantic type validation
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator, model_validator
from .shared import MatplotlibColor, Numpy2DArray, MatplotlibFontsize, CRSInput

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "NorthArrowPrimaryModel", "NorthArrowBaseModel", "NorthArrowFancyModel", 
    "NorthArrowLabelModel", "NorthArrowShadowModel", "NorthArrowPackModel", 
    "NorthArrowAobModel", "NorthArrowRotationModel"
]

### COMPONENT MODELS ###
class NorthArrowPrimaryModel(BaseModel):
    location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]
    scale: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    zorder: int

class NorthArrowBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    coords: Numpy2DArray
    facecolor: MatplotlibColor
    edgecolor: MatplotlibColor
    linewidth: Annotated[Union[float, int], Field(ge=0)]
    zorder: int

class NorthArrowFancyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    coords: Numpy2DArray
    facecolor: MatplotlibColor
    zorder: int

class NorthArrowLabelModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    text: str
    position: Literal["top", "bottom", "left", "right"]
    ha: Literal["left", "center", "right"]
    va: Literal["baseline", "bottom", "center", "center_baseline", "top"]
    fontsize: MatplotlibFontsize
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]
    fontstyle: Literal["normal", "italic", "oblique"]
    color: MatplotlibColor
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"]
    stroke_width: Annotated[Union[float, int], Field(ge=0)]
    stroke_color: MatplotlibColor
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    zorder: int

class NorthArrowShadowModel(BaseModel):
    offset: Tuple[Union[float, int], Union[float, int]]
    alpha: Annotated[Optional[Union[float, int]], Field(ge=0, le=1)] = None
    shadow_rgbFace: MatplotlibColor

class NorthArrowPackModel(BaseModel):
    sep: Annotated[Union[float, int], Field(ge=0)]
    align: Literal["top", "bottom", "left", "right", "center", "baseline"]
    pad: Annotated[Union[float, int], Field(ge=0)]
    width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    height: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    mode: Literal["fixed", "expand", "equal"]

class NorthArrowAobModel(BaseModel):
    facecolor: Optional[MatplotlibColor] = None
    edgecolor: Optional[MatplotlibColor] = None
    alpha: Annotated[Optional[Union[float, int]], Field(ge=0, le=1)] = None
    pad: Annotated[Union[float, int], Field(ge=0)]
    borderpad: Annotated[Union[float, int], Field(ge=0)]
    prop: MatplotlibFontsize
    frameon: bool
    bbox_to_anchor: Optional[Any] = None
    bbox_transform: Optional[Any] = None

class NorthArrowRotationModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    degrees: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    crs: Optional[CRSInput] = None
    reference: Optional[Literal["axis", "data", "center"]] = None
    coords: Optional[Tuple[Union[float, int], Union[float, int]]] = None

    @model_validator(mode="after")
    def validate_rotation_logic(self):
        if self.degrees is None:
            if self.reference == "center":
                if self.crs is None:
                    raise ValueError("If degrees is None and reference is 'center', a valid crs must be supplied")
            else:
                if self.crs is None or self.reference is None or self.coords is None:
                    raise ValueError("If degrees is None, crs, reference, and coords cannot be None: please provide a valid input for each of these variables instead")
        elif isinstance(self.degrees, (int, float)) and (self.crs is not None or self.reference is not None or self.coords is not None):
            warnings.warn("A value for degrees was supplied; values for crs, reference, and coords will be ignored")
        return self