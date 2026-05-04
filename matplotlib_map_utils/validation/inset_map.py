############################################################
# validation/inset_map.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Geo packages
import matplotlib.axes
# Pydantic type validation
from typing import Annotated, Union, Tuple, List, Optional, Literal, Any, Dict
from pydantic import ConfigDict, BaseModel, Field, model_validator
from .shared import MatplotlibColor, CRSInput
from .. import config
from ..defaults import inset_map as imd

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
    "InsetMapPlotModel", "InsetMapInsetModel", 
    "InsetMapExtentModel", "InsetMapDetailModel",
]

### COMPONENT MODELS ###

class InsetMapPlotModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    data: Optional[Any] = None
    kwargs: Optional[Dict[str, Any]] = None

class InsetMapInsetModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]
    size: Optional[Union[Annotated[Union[float, int], Field(ge=0)], Tuple[Annotated[Union[float, int], Field(ge=0)], Annotated[Union[float, int], Field(ge=0)]]]] = None
    pad: Optional[Union[Annotated[Union[float, int], Field(ge=0)], Tuple[Annotated[Union[float, int], Field(ge=0)], Annotated[Union[float, int], Field(ge=0)]]]] = None
    coords: Optional[Tuple[Union[float, int], Union[float, int]]] = None
    to_plot: Optional[Union[List[InsetMapPlotModel], Tuple[InsetMapPlotModel, ...]]] = None
    zorder: int

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size_profile', config.DEFAULT_SIZE)
        defaults = imd._DEFAULTS_IM[_get_size_key(size)][0]
        return defaults | data

class InsetMapExtentModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    pax: matplotlib.axes.Axes
    bax: matplotlib.axes.Axes
    pcrs: CRSInput
    bcrs: CRSInput
    straighten: bool
    pad: Annotated[Union[float, int], Field(ge=0)]
    plot: bool
    facecolor: MatplotlibColor
    linecolor: MatplotlibColor
    alpha: Annotated[Union[float, int], Field(ge=0)]
    linewidth: Annotated[Union[float, int], Field(ge=0)]
    zorder: int
    to_return: Optional[Literal["shape", "patch", "fig", "ax"]] = None

class InsetMapDetailModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    to_return: Optional[Literal["connectors", "lines"]] = None
    connector_color: MatplotlibColor
    connector_width: Annotated[Union[float, int], Field(ge=0)]
    zorder: int