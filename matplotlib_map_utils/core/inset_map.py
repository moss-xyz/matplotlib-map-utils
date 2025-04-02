############################################################
# inset_map.py contains all the main objects and functions
# for creating the inset map axis and its indicators
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
import math
import copy
import re
# Math packages
import numpy
# Geo packages
import cartopy
import pyproj
from great_circle_calculator.great_circle_calculator import distance_between_points
# Graphical packages
import PIL.Image
import matplotlib
import matplotlib.artist
import matplotlib.lines
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.patheffects
import matplotlib.offsetbox
import matplotlib.transforms
import matplotlib.font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg
# matplotlib's useful validation functions
import matplotlib.rcsetup
# The types we use in this script
from typing import Literal
# The information contained in our helper scripts (validation and defaults)
from ..defaults import inset_map as imd
from ..validation import inset_map as imt
from ..validation import functions as imf

### INITIALIZATION ###

# Setting the defaults to the "medium" size, which is roughly optimized for A4/Letter paper
# Making these as globals is important for the set_size() function to work later
_DEFAULT_INSET_MAP = imd._DEFAULTS_IM["md"][0]

### CLASSES ###

# The main object model of the inset map
# Note this is really just to be convenient when storing the configuration
# options that are used by the inset_map() function instead
class InsetMap(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="lower left", 
                 size: imt._TYPE_INSET["size"]=None,
                 pad: imt._TYPE_INSET["pad"]=None,
                 coords: imt._TYPE_INSET["coords"]=None,
                 transform=None,
                 to_plot=None,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # Validating each of the passed parameters
        self._location = imf._validate(imt._VALIDATE_INSET, "location", location)
        self._size = imf._validate(imt._VALIDATE_INSET, "size", size)
        self._pad = imf._validate(imt._VALIDATE_INSET, "pad", pad)
        self._coords = imf._validate(imt._VALIDATE_INSET, "coords", coords)
        self._to_plot = imf._validate(imt._VALIDATE_INSET, "to_plot", to_plot)

        # Checking if we need to override values for size and pad
        if self._size is None:
            self._size = _DEFAULT_INSET_MAP["size"]
        if self._pad is None:
            self._pad = _DEFAULT_INSET_MAP["pad"]
        
        self._transform = transform # not validated!
        self._kwargs = kwargs # not validated!
    
    # We do set the zorder for our objects individually,
    # but we ALSO set it for the entire artist, here
    # Thank you to matplotlib-scalebar for this tip
    zorder = 99

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of properties
    # Each property will have the same pair of functions
    # 1) calling the property itself returns its value (InsetMap.size will output (width,height))
    # 2) passing a value will update it (InsetMap.size = (width,height) will update it)

    # location/loc
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        val = imf._validate(imt._VALIDATE_INSET, "location", val)
        self._location = val
    
    @property
    def loc(self):
        return self._location

    @loc.setter
    def loc(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        val = imf._validate(imt._VALIDATE_INSET, "location", val)
        self._location = val

    # size
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        val = imf._validate(imt._VALIDATE_INSET, "location", val)
        if val is not None:
            self._size = val
        else:
            self._size = _DEFAULT_INSET_MAP["size"]
    
    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        val = imf._validate(imt._VALIDATE_INSET, "pad", val)
        if val is not None:
            self._pad = val
        else:
            self._pad = _DEFAULT_INSET_MAP["pad"]
    
    # coords
    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, val):
        val = imf._validate(imt._VALIDATE_INSET, "coords", val)
        self._coords = val
    
    # transform
    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, val):
        self._transform = val

    # kwargs
    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, val):
        if isinstance(val, dict):
            self._kwargs = self._kwargs | val
        else:
            raise ValueError("kwargs expects a dictionary, please try again")
    
    # to_plot
    @property
    def to_plot(self):
        return self._to_plot

    @to_plot.setter
    def to_plot(self, val):
        val = imf._validate(imt._VALIDATE_INSET, "to_plot", val)
        self._to_plot = val

    ## COPY FUNCTION ##
    # This is solely to get around matplotlib's restrictions around re-using an artist across multiple axes
    # Instead, you can use add_artist() like normal, but with add_artist(na.copy())
    # Thank you to the cartopy team for helping fix a bug with this!
    def copy(self):
        return copy.deepcopy(self)

    ## CREATE FUNCTION ##
    # Calling InsetMap.create(ax) will create an inset map with the specified parameters on the given axis
    # Note that this is different than the way NorthArrows and ScaleBars are rendered (via draw/add_artist())!
    def create(self, pax, **kwargs):
        # Can re-use the drawing function we already established, but return the object instead
        iax = inset_map(ax=pax, location=self._location, size=self._size,
                        pad=self._pad, coords=self._coords, transform=self._transform,
                        **self._kwargs, **kwargs)
        
        for d in self._to_plot:
            if d is not None:
                d["data"].plot(ax=iax, **d["kwargs"])
        # Instead of "drawing", we have to return the axis, for further manipulation
        return iax
    
    ## SIZE FUNCTION ##
    # This function will update the default dictionaries used based on the size of map being created
    # See defaults.py for more information on the dictionaries used here
    def set_size(size: Literal["xs","xsmall","x-small",
                               "sm","small",
                               "md","medium",
                               "lg","large",
                               "xl","xlarge","x-large"]):
        # Bringing in our global default values to update them
        global _DEFAULT_INSET_MAP
        # Changing the global default values as required
        if size.lower() in ["xs","xsmall","x-small"]:
            _DEFAULT_INSET_MAP = imd._DEFAULTS_IM["xs"][0]
        elif size.lower() in ["sm","small"]:
            _DEFAULT_INSET_MAP = imd._DEFAULTS_IM["sm"][0]
        elif size.lower() in ["md","medium"]:
            _DEFAULT_INSET_MAP = imd._DEFAULTS_IM["md"][0]
        elif size.lower() in ["lg","large"]:
            _DEFAULT_INSET_MAP = imd._DEFAULTS_IM["lg"][0]
        elif size.lower() in ["xl","xlarge","x-large"]:
            _DEFAULT_INSET_MAP = imd._DEFAULTS_IM["xl"][0]
        else:
            raise ValueError("Invalid value supplied, try one of ['xsmall', 'small', 'medium', 'large', 'xlarge'] instead")

### DRAWING FUNCTIONS ###

# See here for doc: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.inset_axes.html
# See here for kwargs: https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.axes_grid1.inset_locator.inset_axes.html#mpl_toolkits.axes_grid1.inset_locator.inset_axes
def inset_map(ax, 
              location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right", 
              size: imt._TYPE_INSET["size"]=None,
              pad: imt._TYPE_INSET["pad"]=None,
              coords: imt._TYPE_INSET["coords"]=None,
              transform=None,
              **kwargs):
    
    ## VALIDATION ##
    location = imf._validate(imt._VALIDATE_INSET, "location", location)
    size = imf._validate(imt._VALIDATE_INSET, "size", size)
    pad = imf._validate(imt._VALIDATE_INSET, "pad", pad)
    coords = imf._validate(imt._VALIDATE_INSET, "coords", coords)

    if size is None:
        size = _DEFAULT_INSET_MAP["size"]
    if pad is None:
        pad = _DEFAULT_INSET_MAP["pad"]

    ## SET-UP ##
    # Getting the figure
    fig = ax.get_figure()

    ## SIZE ##
    # Setting the desired dimensions of the inset map
    # The default inset_axis() function does this as a fraction of the parent axis
    # But the size variable expects dimensions in inches
    
    # First, casting size to width and height
    if isinstance(size, (tuple, list)):
        inset_width, inset_height = size
    else:
        inset_width = size 
        inset_height = size

    # Getting the current dimensions of the parent axis in inches (ignoring ticks and labels - just the axis)
    parent_axis_bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    
    # Expressing the desired height and width of the inset map as a fraction of the parent
    inset_width = inset_width / parent_axis_bbox.width
    inset_height = inset_height / parent_axis_bbox.height

    ## PADDING ##
    # Padding is expressed in inches as well
    # First, casting size to width and height
    if isinstance(pad, (tuple, list)):
        pad_x, pad_y = pad
    else:
        pad_x = pad 
        pad_y = pad

    ## PLACEMENT ##
    # Calculating the start coordinate (which is always the bottom-left corner) of the inset map
    # based on the desired location, padding (inches) from the side, and the height and width of the inset map
    if coords is None:
        # First, the x coordinate
        if location in ["upper left", "center left", "lower left"]:
            x = pad_x / parent_axis_bbox.width
        elif location in ["upper center", "center", "lower center"]:
            x = (parent_axis_bbox.width - width) / 2 / parent_axis_bbox.width
        elif location in ["upper right", "center right", "lower right"]:
            x = ((parent_axis_bbox.width - width - pad_x) / parent_axis_bbox.width)
        # Then the y coordinate
        if location in ["upper left", "upper center", "upper right"]:
            y = ((parent_axis_bbox.height - height - pad_y) / parent_axis_bbox.height)
        elif location in ["center left", "center", "center right"]:
            y = (parent_axis_bbox.height - height) / 2 / parent_axis_bbox.height
        elif location in ["lower left", "lower center", "lower right"]:
            y = pad_y / parent_axis_bbox.height
    # If coordinates are passed, calculate references with respect to that
    # NOTE: in this case, padding is ignored!
    else:
        # Transforming the passed coordinates to transAxes coordinates
        if transform is not None and transform != ax.transAxes:
            # Coords needs to be x,y
            coords = transform.transform(coords)  # Transforming the coordinates to display units
            coords = ax.transAxes.inverted().transform(coords)  # Converting back to ax.transAxes
        # Now coords can be treated as basically an offset value
        # Here, we use inset_width and inset_height, because we are expressing everything in relative axis units
        # That's what the transformations were for!
        # First, the x coordinate
        if location in ["upper left", "center left", "lower left"]:
            x = coords[0]
        elif location in ["upper center", "center", "lower center"]:
            x = coords[0] - inset_width / 2
        elif location in ["upper right", "center right", "lower right"]:
            x = coords[0] - inset_width
        # Then the y coordinate
        if location in ["upper left", "upper center", "upper right"]:
            y = coords[1] - inset_height
        elif location in ["center left", "center", "center right"]:
            y = coords[1] - inset_height / 2
        elif location in ["lower left", "lower center", "lower right"]:
            y = coords[1]

    # Creating the new inset map with the specified height, width, and location
    iax = ax.inset_axes([x, y, inset_width, inset_height], **kwargs)
    
    # We also set the anchor here, such that it stays fixed when any resizing takes place
    loc_anchors = {
        "upper left": "NW", "upper center": "N", "upper right": "NE",
        "center left": "W", "center": "C", "center right": "E",
        "lower left": "SW", "lower center": "S", "lower right": "SE"
    }
    iax.set_anchor(anchor=loc_anchors[location])
    
    # The new inset axis is returned
    return iax