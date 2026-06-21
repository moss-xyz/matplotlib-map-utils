############################################################
# validation/inset_map.py contains all the main objects
# for checking inputs passed to class definitions
############################################################

### IMPORTING PACKAGES ###

# Geo packages
import matplotlib.axes
# Pydantic type validation
from typing import Annotated, Union, Tuple, List, Optional, Literal, Any, Dict, TypedDict
from pydantic import ConfigDict, BaseModel, Field, model_validator
from .shared import MatplotlibColor, CRSInput, _get_size_key, Location, ExtentReturn, DetailReturn
from .. import config
from ..defaults import inset_map as imd

### ALL ###
# This code tells other packages what to import if not explicitly stated
__all__ = [
    "InsetMapPlotModel", "InsetMapInsetModel",
    "InsetMapExtentModel", "InsetMapDetailModel",
    "InsetMapPlotDict",
]

### COMPONENT MODELS ###

class InsetMapPlotModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid')
    data: Optional[Any] = None
    kwargs: Optional[Dict[str, Any]] = None

class InsetMapInsetModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    location: Location
    imsize: Optional[Union[Annotated[Union[float, int], Field(ge=0)], Tuple[Annotated[Union[float, int], Field(ge=0)], Annotated[Union[float, int], Field(ge=0)]]]] = None
    pad: Optional[Union[Annotated[Union[float, int], Field(ge=0)], Tuple[Annotated[Union[float, int], Field(ge=0)], Annotated[Union[float, int], Field(ge=0)]]]] = None
    coords: Optional[Tuple[Union[float, int], Union[float, int]]] = None
    to_plot: Optional[Union[List[InsetMapPlotModel], Tuple[InsetMapPlotModel, ...]]] = None
    zorder: int

    @model_validator(mode='before')
    @classmethod
    def apply_size_defaults(cls, data: Any) -> Any:
        if data is None or data is True: data = {}
        if not isinstance(data, dict): return data
        size = data.pop('size', config.DEFAULT_SIZE)
        defaults = imd._DEFAULTS_IM[_get_size_key(size)][0]
        merged = defaults | data
        # Auto-wrap a single dict for to_plot into a list
        if isinstance(merged.get('to_plot'), dict):
            merged['to_plot'] = [merged['to_plot']]
        return merged

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
    to_return: Optional[ExtentReturn] = None

class InsetMapDetailModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    to_return: Optional[DetailReturn] = None
    connector_color: MatplotlibColor
    connector_width: Annotated[Union[float, int], Field(ge=0)]
    zorder: int

### TYPED DICTS ###
# Inset-map objects take their settings as individual keyword arguments rather
# than nested config dicts, so (unlike ScaleBar/NorthArrow) there is no dict
# literal to complete - the enumerated kwargs are typed with the shared Literal
# aliases directly in core/inset_map.py. The one place a dict literal IS passed
# is each element of `to_plot`, so we expose a TypedDict for that shape. It is
# never validated at runtime (InsetMapPlotModel does that); it exists only so
# `to_plot=[{"data": ..., "kwargs": ...}]` autocompletes its keys.

class InsetMapPlotDict(TypedDict, total=False):
    data: Any
    kwargs: dict