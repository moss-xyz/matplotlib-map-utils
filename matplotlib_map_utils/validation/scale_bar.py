############################################################
# validation/scale_bar.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Pydantic type validation
from typing import Annotated, Union, Tuple, List, Optional, Literal, Any
from pydantic import ConfigDict, BaseModel, Field, BeforeValidator, model_validator
from .shared import MatplotlibColor, MatplotlibFontsize, CRSInput, _validate_crs_input
from .. import config
from ..defaults import scale_bar as sbd

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
    "preferred_divs", "convert_dict", "units_standard",
    "ScaleBarPrimaryModel", "ScaleBarBarModel", "ScaleBarLabelsModel", "ScaleBarUnitsModel", "ScaleBarTextModel", "ScaleBarAobModel"
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
    style: Literal["ticks","boxes"]
    location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]
    zorder: int

def _validate_scalebar_projection(v):
    if isinstance(v, str) and v.lower() in ["px","pixel","pixels","pt","point","points","dx","custom","axis"]:
        return v.lower()
    return _validate_crs_input(v)
    
ScaleBarProjection = Annotated[Any, BeforeValidator(_validate_scalebar_projection)]

class ScaleBarBarModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    projection: ScaleBarProjection
    unit: Optional[Literal["m","km","ft","yd","mi","nmi"]] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    max: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    length: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    height: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    reverse: bool
    major_div: Annotated[Optional[int], Field(ge=1)] = None
    minor_div: Annotated[Optional[int], Field(ge=0)] = None
    minor_frac: Annotated[Optional[Union[float, int]], Field(ge=0, le=1)] = None
    minor_type: Optional[Literal["all","first","none"]] = None
    major_mult: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    facecolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    edgecolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    edgewidth: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    tick_loc: Optional[Literal["above","below","middle"]] = None
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
    style: Literal["major","first_last","last_only","minor_all","minor_first"]
    loc: Optional[Literal["above","below"]] = None
    fontsize: Optional[MatplotlibFontsize] = None
    textcolors: Optional[Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]] = None
    fontfamily: Optional[Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]] = None
    fontstyle: Optional[Literal["normal", "italic", "oblique"]] = None
    fontweight: Optional[Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"]] = None
    stroke_width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    stroke_color: Optional[MatplotlibColor] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[Literal["anchor","default"]] = None
    sep: Annotated[Union[float, int], Field(ge=0)]
    pad: Annotated[Union[float, int], Field(ge=0)]

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][1]
        return defaults | data

class ScaleBarUnitsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    label: Optional[str] = None
    loc: Optional[Literal["bar","text","opposite"]] = None
    fontsize: Optional[MatplotlibFontsize] = None
    textcolor: Optional[MatplotlibColor] = None
    fontfamily: Optional[Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]] = None
    fontstyle: Optional[Literal["normal", "italic", "oblique"]] = None
    fontweight: Optional[Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"]] = None
    stroke_width: Annotated[Optional[Union[float, int]], Field(ge=0)] = None
    stroke_color: Optional[MatplotlibColor] = None
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[Literal["anchor","default"]] = None
    sep: Annotated[Union[float, int], Field(ge=0)]
    pad: Annotated[Union[float, int], Field(ge=0)]

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = sbd._DEFAULTS_SB[_get_size_key(size)][2]
        return defaults | data

class ScaleBarTextModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    fontsize: MatplotlibFontsize
    textcolor: Union[MatplotlibColor, List[MatplotlibColor], Tuple[MatplotlibColor, ...]]
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]
    fontstyle: Literal["normal", "italic", "oblique"]
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"]
    stroke_width: Annotated[Union[float, int], Field(ge=0)]
    stroke_color: MatplotlibColor
    rotation: Annotated[Optional[Union[float, int]], Field(ge=-360, le=360)] = None
    rotation_mode: Optional[Literal["anchor","default"]] = None

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
