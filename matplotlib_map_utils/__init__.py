# This handles importing of all the functions and classes
from .core.north_arrow import NorthArrow, north_arrow
from .core.scale_bar import ScaleBar, scale_bar, dual_bars
from .core.inset_map import InsetMap, inset_map, ExtentIndicator, indicate_extent, DetailIndicator, indicate_detail, inset_usa
from typing import Literal

# This defines what wildcard imports should import
__all__ = ["NorthArrow", "north_arrow", 
           "ScaleBar", "scale_bar", "dual_bars",
           "InsetMap","inset_map", "ExtentIndicator","indicate_extent", "DetailIndicator","indicate_detail", "inset_usa",
           "set_size"]

from . import config

def set_size(size: Literal["xs","xsmall","x-small",
                           "sm","small",
                           "md","medium",
                           "lg","large",
                           "xl","xlarge","x-large"]):
    
    # standardize the size string
    size_map = {
        "xs": "xs", "xsmall": "xs", "x-small": "xs",
        "sm": "sm", "small": "sm",
        "md": "md", "medium": "md",
        "lg": "lg", "large": "lg",
        "xl": "xl", "xlarge": "xl", "x-large": "xl"
    }
    
    if size.lower() not in size_map:
        raise ValueError("Invalid value supplied, try one of ['xsmall', 'small', 'medium', 'large', 'xlarge']")
        
    config.DEFAULT_SIZE = size_map[size.lower()]