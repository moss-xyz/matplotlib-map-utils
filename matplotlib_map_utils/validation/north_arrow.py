############################################################
# validation/north_arrow.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
# The types we use in this script
from typing import Annotated, Union, Tuple, Optional, Literal, Any
# Pydantic type validation
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator, model_validator
from .shared import MatplotlibColor, Numpy2DArray, MatplotlibFontsize, CRSInput
from .. import config
from ..defaults import north_arrow as nad

def _get_size_key(size: Any) -> str:
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

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        if data.get('scale') is None:
            data['scale'] = nad._DEFAULTS_NA[_get_size_key(size)][0]
        return data

class NorthArrowBaseModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    coords: Numpy2DArray
    facecolor: MatplotlibColor
    edgecolor: MatplotlibColor
    linewidth: Annotated[Union[float, int], Field(ge=0)]
    zorder: int

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][1]
        return defaults | data

class NorthArrowFancyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    coords: Numpy2DArray
    facecolor: MatplotlibColor
    zorder: int

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][2]
        return defaults | data

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
    rotation: Annotated[Union[float, int], Field(ge=-360, le=360)]
    zorder: int

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][3]
        return defaults | data

class NorthArrowShadowModel(BaseModel):
    offset: Tuple[Union[float, int], Union[float, int]]
    alpha: Annotated[Optional[Union[float, int]], Field(ge=0, le=1)] = None
    shadow_rgbFace: MatplotlibColor

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][4]
        return defaults | data

class NorthArrowPackModel(BaseModel):
    sep: Annotated[Union[float, int], Field(ge=0)]
    align: Literal["top", "bottom", "left", "right", "center", "baseline"]
    pad: Annotated[Union[float, int], Field(ge=0)]
    width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    height: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    mode: Literal["fixed", "expand", "equal"]

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][5]
        return defaults | data

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

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = nad._DEFAULTS_NA[_get_size_key(size)][6]
        return defaults | data

class NorthArrowRotationModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    degrees: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    crs: Optional[CRSInput] = None
    reference: Optional[Literal["axis", "data", "center"]] = None
    coords: Optional[Tuple[Union[float, int], Union[float, int]]] = None

    @model_validator(mode='before')
    @classmethod
    def apply_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        data.pop('size', None) # ignore size
        defaults = nad._ROTATION_ALL
        return defaults | data

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