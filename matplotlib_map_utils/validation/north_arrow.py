############################################################
# validation/north_arrow.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
# The types we use in this script
from typing import Annotated, Union, Tuple, Optional, Literal, Any, TypedDict
# Pydantic type validation
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator, model_validator
from .shared import (MatplotlibColor, Numpy2DArray, MatplotlibFontsize, CRSInput, _get_size_key,
                     Location, LabelPosition, HAlign, VAlign, FontFamily, FontStyle, FontWeight,
                     PackAlign, PackMode, RotationReference)
from .. import config
from ..defaults import north_arrow as nad

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "NorthArrowPrimaryModel", "NorthArrowBaseModel", "NorthArrowFancyModel",
    "NorthArrowLabelModel", "NorthArrowShadowModel", "NorthArrowPackModel",
    "NorthArrowAobModel", "NorthArrowRotationModel",
    "NorthArrowBaseDict", "NorthArrowFancyDict", "NorthArrowLabelDict", "NorthArrowShadowDict",
    "NorthArrowPackDict", "NorthArrowAobDict", "NorthArrowRotationDict"
]

### COMPONENT MODELS ###
class NorthArrowPrimaryModel(BaseModel):
    location: Location
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
    position: LabelPosition
    ha: HAlign
    va: VAlign
    fontsize: MatplotlibFontsize
    fontfamily: FontFamily
    fontstyle: FontStyle
    color: MatplotlibColor
    fontweight: FontWeight
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
    align: PackAlign
    pad: Annotated[Union[float, int], Field(ge=0)]
    width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    height: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    mode: PackMode

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
    reference: Optional[RotationReference] = None
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

### TYPED DICTS ###
# These mirror the user-facing fields of the models above, purely for editor
# intellisense (key + value autocomplete inside dict literals). They are never
# instantiated or validated at runtime - the plain dicts users pass still flow
# through the pydantic models above. total=False marks every key optional, since
# users supply partial configs. Literal-typed fields reuse the shared aliases so
# their allowed values stay in lockstep with the models.

class NorthArrowBaseDict(TypedDict, total=False):
    coords: Any
    facecolor: Any
    edgecolor: Any
    linewidth: float | int
    zorder: int

class NorthArrowFancyDict(TypedDict, total=False):
    coords: Any
    facecolor: Any
    zorder: int

class NorthArrowLabelDict(TypedDict, total=False):
    text: str
    position: LabelPosition
    ha: HAlign
    va: VAlign
    fontsize: float | int | str
    fontfamily: FontFamily
    fontstyle: FontStyle
    color: Any
    fontweight: FontWeight
    stroke_width: float | int
    stroke_color: Any
    rotation: float | int
    zorder: int

class NorthArrowShadowDict(TypedDict, total=False):
    offset: tuple
    alpha: float | int
    shadow_rgbFace: Any

class NorthArrowPackDict(TypedDict, total=False):
    sep: float | int
    align: PackAlign
    pad: float | int
    width: float | int
    height: float | int
    mode: PackMode

class NorthArrowAobDict(TypedDict, total=False):
    facecolor: Any
    edgecolor: Any
    alpha: float | int
    pad: float | int
    borderpad: float | int
    prop: float | int | str
    frameon: bool
    bbox_to_anchor: Any
    bbox_transform: Any

class NorthArrowRotationDict(TypedDict, total=False):
    degrees: float | int
    crs: Any
    reference: RotationReference
    coords: Any