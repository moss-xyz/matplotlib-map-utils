############################################################
# validation/scale_bar.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Pydantic type validation
from typing import Annotated, Union, Tuple, List, Optional, Literal, Any, TypedDict
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator, model_validator
from .shared import (MatplotlibColor, MatplotlibFontsize, CRSInput, _validate_crs_input, _get_size_key,
                     ScaleBarStyle, Location, BarUnit, MinorType, TickLoc, LabelStyle, LabelsLoc, UnitsLoc,
                     FontFamily, FontStyle, FontWeight, RotationMode)
from .. import config
from ..defaults import scale_bar as sbd

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "preferred_divs", "convert_dict", "units_standard",
    "ScaleBarPrimaryModel", "ScaleBarBarModel", "ScaleBarLabelsModel", "ScaleBarUnitsModel", "ScaleBarTextModel", "ScaleBarAobModel",
    "ScaleBarBarDict", "ScaleBarLabelsDict", "ScaleBarUnitsDict", "ScaleBarTextDict", "ScaleBarAobDict"
]

### CONSTANTS ###
# These are constants that we use elsewhere in the script
# when setting up a scale bar

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
    10:[2,1],
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

### COMPONENT MODELS ###

class ScaleBarPrimaryModel(BaseModel):
    style: ScaleBarStyle
    location: Location
    zorder: int

def _validate_scalebar_projection(v):
    if isinstance(v, str) and v.lower() in ["px","pixel","pixels","pt","point","points","dx","custom","axis"]:
        return v.lower()
    return _validate_crs_input(v)
    
ScaleBarProjection = Annotated[Any, BeforeValidator(_validate_scalebar_projection)]

class ScaleBarBarModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    projection: ScaleBarProjection
    unit: Optional[BarUnit] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    max: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    length: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    height: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    reverse: bool
    major_div: Annotated[Optional[int], Field(ge=1)] = None
    minor_div: Annotated[Optional[int], Field(ge=0)] = None
    minor_frac: Annotated[Optional[Union[float, int]], Field(ge=0, le=1)] = None
    minor_type: Optional[MinorType] = None
    major_mult: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    facecolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    edgecolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    edgewidth: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    tick_loc: Optional[TickLoc] = None
    basecolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    tickcolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    tickwidth: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    interpolation: Optional[str] = None
    dpi_cor: bool
    resample: bool
    raster_dpi: Annotated[Optional[Union[float, int]], Field(ge=1)] = None
    raster_dpi_scale: Annotated[Optional[Union[float, int]], Field(ge=0.0001)] = None

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][0]
        return defaults | data

class ScaleBarLabelsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    labels: Optional[Union[List[Any], Tuple[Any, ...]]] = None
    format: str
    format_int: bool
    style: LabelStyle
    loc: Optional[LabelsLoc] = None
    fontsize: Optional[MatplotlibFontsize] = None
    textcolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    fontfamily: Optional[FontFamily] = None
    fontstyle: Optional[FontStyle] = None
    fontweight: Optional[FontWeight] = None
    stroke_width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    stroke_color: Optional[MatplotlibColor] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[RotationMode] = None
    sep: Annotated[Union[float, int], Field(ge=0)]
    pad: Annotated[Union[float, int], Field(ge=0)]

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        text_defaults = data.pop('text', None)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][1]
        merged = defaults | data
        # Apply text cascade: text properties act as fallbacks for labels
        if text_defaults is not None:
            text_fields = ['fontsize', 'fontfamily', 'fontstyle', 'fontweight',
                           'stroke_width', 'stroke_color', 'rotation', 'rotation_mode']
            for field in text_fields:
                if field in text_defaults and merged.get(field) is None:
                    merged[field] = text_defaults[field]
            # textcolor -> textcolors rename for labels
            if merged.get('textcolors') is None and 'textcolor' in text_defaults:
                merged['textcolors'] = text_defaults['textcolor']
        return merged

class ScaleBarUnitsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    label: Optional[str] = None
    loc: Optional[UnitsLoc] = None
    fontsize: Optional[MatplotlibFontsize] = None
    textcolor: Optional[MatplotlibColor] = None
    fontfamily: Optional[FontFamily] = None
    fontstyle: Optional[FontStyle] = None
    fontweight: Optional[FontWeight] = None
    stroke_width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    stroke_color: Optional[MatplotlibColor] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[RotationMode] = None
    sep: Annotated[Union[float, int], Field(ge=0)]
    pad: Annotated[Union[float, int], Field(ge=0)]

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        text_defaults = data.pop('text', None)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][2]
        merged = defaults | data
        # Apply text cascade: text properties act as fallbacks for units
        if text_defaults is not None:
            text_fields = ['fontsize', 'textcolor', 'fontfamily', 'fontstyle', 'fontweight',
                           'stroke_width', 'stroke_color', 'rotation', 'rotation_mode']
            for field in text_fields:
                if field in text_defaults and merged.get(field) is None:
                    merged[field] = text_defaults[field]
        return merged

class ScaleBarTextModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    fontsize: MatplotlibFontsize
    textcolor: Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]
    fontfamily: FontFamily
    fontstyle: FontStyle
    fontweight: FontWeight
    stroke_width: Annotated[Union[float, int], Field(ge=0)]
    stroke_color: MatplotlibColor
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[RotationMode] = None

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][3]
        return defaults | data

class ScaleBarAobModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
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
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][4]
        return defaults | data

### TYPED DICTS ###
# These mirror the user-facing fields of the models above, purely for editor
# intellisense (key + value autocomplete inside dict literals). They are never
# instantiated or validated at runtime - the plain dicts users pass still flow
# through the pydantic models above. total=False marks every key optional, since
# users supply partial configs. Literal-typed fields reuse the shared aliases so
# their allowed values stay in lockstep with the models.

class ScaleBarBarDict(TypedDict, total=False):
    projection: Any
    unit: BarUnit
    rotation: float | int
    max: float | int
    length: float | int
    height: float | int
    reverse: bool
    major_div: int
    minor_div: int
    minor_frac: float | int
    minor_type: MinorType
    major_mult: float | int
    facecolors: Any
    edgecolors: Any
    edgewidth: float | int
    tick_loc: TickLoc
    basecolors: Any
    tickcolors: Any
    tickwidth: float | int
    interpolation: str
    dpi_cor: bool
    resample: bool
    raster_dpi: float | int
    raster_dpi_scale: float | int

class ScaleBarLabelsDict(TypedDict, total=False):
    labels: list | tuple
    format: str
    format_int: bool
    style: LabelStyle
    loc: LabelsLoc
    fontsize: float | int | str
    textcolors: Any
    fontfamily: FontFamily
    fontstyle: FontStyle
    fontweight: FontWeight
    stroke_width: float | int
    stroke_color: Any
    rotation: float | int
    rotation_mode: RotationMode
    sep: float | int
    pad: float | int

class ScaleBarUnitsDict(TypedDict, total=False):
    label: str
    loc: UnitsLoc
    fontsize: float | int | str
    textcolor: Any
    fontfamily: FontFamily
    fontstyle: FontStyle
    fontweight: FontWeight
    stroke_width: float | int
    stroke_color: Any
    rotation: float | int
    rotation_mode: RotationMode
    sep: float | int
    pad: float | int

class ScaleBarTextDict(TypedDict, total=False):
    fontsize: float | int | str
    textcolor: Any
    fontfamily: FontFamily
    fontstyle: FontStyle
    fontweight: FontWeight
    stroke_width: float | int
    stroke_color: Any
    rotation: float | int
    rotation_mode: RotationMode

class ScaleBarAobDict(TypedDict, total=False):
    facecolor: Any
    edgecolor: Any
    alpha: float | int
    pad: float | int
    borderpad: float | int
    prop: float | int | str
    frameon: bool
    bbox_to_anchor: Any
    bbox_transform: Any
