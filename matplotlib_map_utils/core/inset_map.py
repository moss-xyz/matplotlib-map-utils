############################################################
# inset_map.py contains all the main objects and functions
# for creating the inset map axis and its indicators
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
import copy
# Math packages
import numpy
# Geo packages
import pyproj
import shapely
# Graphical packages
import matplotlib
import matplotlib.artist
import matplotlib.patches
import matplotlib.colors
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
# Note these are really just to be convenient when storing the 
# configuration options that are used by the drawing functions instead

# The main object model of the inset map
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
        val = imf._validate(imt._VALIDATE_INSET, "size", val)
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
        
        # If data is passed to to_plot, then we plot that on the newly created axis as well
        for d in self._to_plot:
            if d is not None:
                if "kwargs" in d.keys():
                    d["data"].plot(ax=iax, **d["kwargs"])
                else:
                    d["data"].plot(ax=iax)
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

# The main object model of the extent indicator
class ExtentIndicator(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 to_return: imt._TYPE_EXTENT["to_return"]=None,
                 straighten: imt._TYPE_EXTENT["straighten"]=True,
                 pad: imt._TYPE_EXTENT["pad"]=0.05,
                 plot: imt._TYPE_EXTENT["plot"]=True,
                 facecolor: imt._TYPE_EXTENT["facecolor"]="red",
                 linecolor: imt._TYPE_EXTENT["linecolor"]="red",
                 alpha: imt._TYPE_EXTENT["alpha"]=0.5,
                 linewidth: imt._TYPE_EXTENT["linewidth"]=1,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # Validating each of the passed parameters
        self._to_return = imf._validate(imt._VALIDATE_EXTENT, "to_return", to_return)
        self._straighten = imf._validate(imt._VALIDATE_EXTENT, "straighten", straighten)
        self._pad = imf._validate(imt._VALIDATE_EXTENT, "pad", pad)
        self._plot = imf._validate(imt._VALIDATE_EXTENT, "plot", plot)
        self._facecolor = imf._validate(imt._VALIDATE_EXTENT, "facecolor", facecolor)
        self._linecolor = imf._validate(imt._VALIDATE_EXTENT, "linecolor", linecolor)
        self._alpha = imf._validate(imt._VALIDATE_EXTENT, "alpha", alpha)
        self._linewidth = imf._validate(imt._VALIDATE_EXTENT, "linewidth", linewidth)

        self._kwargs = kwargs # not validated!
    
    # We do set the zorder for our objects individually,
    # but we ALSO set it for the entire artist, here
    # Thank you to matplotlib-scalebar for this tip
    zorder = 99

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of properties
    # Each property will have the same pair of functions
    # 1) calling the property itself returns its value (ExtentIndicator.facecolor will output color)
    # 2) passing a value will update it (ExtentIndicator.facecolor = color will update it)

    # to_return
    @property
    def to_return(self):
        return self._to_return

    @to_return.setter
    def to_return(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "to_return", val)
        self._to_return = val

    # straighten
    @property
    def straighten(self):
        return self._straighten

    @straighten.setter
    def straighten(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "straighten", val)
        self._straighten = val

    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "pad", val)
        self._pad = val

    # plot
    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "plot", val)
        self._plot = val

    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "facecolor", val)
        self._facecolor = val

    # linecolor
    @property
    def linecolor(self):
        return self._linecolor

    @linecolor.setter
    def linecolor(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "linecolor", val)
        self._linecolor = val

    # alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "alpha", val)
        self._alpha = val

    # linewidth
    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "linewidth", val)
        self._linewidth = val

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

    ## COPY FUNCTION ##
    # This is solely to get around matplotlib's restrictions around re-using an artist across multiple axes
    # Instead, you can use add_artist() like normal, but with add_artist(na.copy())
    # Thank you to the cartopy team for helping fix a bug with this!
    def copy(self):
        return copy.deepcopy(self)

    ## CREATE FUNCTION ##
    # Calling ExtentIndicator.create(ax) will create an inset map with the specified parameters on the given axis
    # Note that this is different than the way NorthArrows and ScaleBars are rendered (via draw/add_artist())!
    def create(self,
               pax: imt._TYPE_EXTENT["pax"],
               bax: imt._TYPE_EXTENT["bax"],
               pcrs: imt._TYPE_EXTENT["pcrs"],
               bcrs: imt._TYPE_EXTENT["bcrs"], **kwargs):
        
        # Can re-use the drawing function we already established, but return the object instead
        exi = indicate_extent(pax=pax, bax=bax, pcrs=pcrs, bcrs=bcrs, 
                              to_return=self._to_return, straighten=self._straighten,
                              pad=self._pad, plot=self._plot,
                              facecolor=self._facecolor, linecolor=self._linecolor,
                              alpha=self._alpha, linewidth=self._linewidth,
                              **self._kwargs, **kwargs)
        
        # The indicator will be drawn automatically if plot is True
        # If we have anything to return from to_return, we will do so here
        if exi is not None:
            return exi

# The main object model of the detail indicator
class DetailIndicator(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 to_return: imt._TYPE_DETAIL["to_return"]=None,
                 straighten: imt._TYPE_EXTENT["straighten"]=True,
                 pad: imt._TYPE_EXTENT["pad"]=0.05,
                 plot: imt._TYPE_EXTENT["plot"]=True,
                 facecolor: imt._TYPE_EXTENT["facecolor"]="none",
                 linecolor: imt._TYPE_EXTENT["linecolor"]="black",
                 alpha: imt._TYPE_EXTENT["alpha"]=1,
                 linewidth: imt._TYPE_EXTENT["linewidth"]=1,
                 connector_color: imt._TYPE_DETAIL["connector_color"]="black",
                 connector_width: imt._TYPE_DETAIL["connector_width"]=1,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # Validating each of the passed parameters
        self._straighten = imf._validate(imt._VALIDATE_EXTENT, "straighten", straighten)
        self._pad = imf._validate(imt._VALIDATE_EXTENT, "pad", pad)
        self._plot = imf._validate(imt._VALIDATE_EXTENT, "plot", plot)
        self._facecolor = imf._validate(imt._VALIDATE_EXTENT, "facecolor", facecolor)
        self._linecolor = imf._validate(imt._VALIDATE_EXTENT, "linecolor", linecolor)
        self._alpha = imf._validate(imt._VALIDATE_EXTENT, "alpha", alpha)
        self._linewidth = imf._validate(imt._VALIDATE_EXTENT, "linewidth", linewidth)
        self._to_return = imf._validate(imt._VALIDATE_DETAIL, "to_return", to_return)
        self._connector_color = imf._validate(imt._VALIDATE_DETAIL, "connector_color", connector_color)
        self._connector_width = imf._validate(imt._VALIDATE_DETAIL, "connector_width", connector_width)

        self._kwargs = kwargs # not validated!
    
    # We do set the zorder for our objects individually,
    # but we ALSO set it for the entire artist, here
    # Thank you to matplotlib-scalebar for this tip
    zorder = 99

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of properties
    # Each property will have the same pair of functions
    # 1) calling the property itself returns its value (DetailIndicator.facecolor will output color)
    # 2) passing a value will update it (DetailIndicator.facecolor = color will update it)

    # to_return
    @property
    def to_return(self):
        return self._to_return

    @to_return.setter
    def to_return(self, val):
        val = imf._validate(imt._VALIDATE_DETAIL, "to_return", val)
        self._to_return = val

    # straighten
    @property
    def straighten(self):
        return self._straighten

    @straighten.setter
    def straighten(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "straighten", val)
        self._straighten = val

    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "pad", val)
        self._pad = val

    # plot
    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "plot", val)
        self._plot = val

    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "facecolor", val)
        self._facecolor = val

    # linecolor
    @property
    def linecolor(self):
        return self._linecolor

    @linecolor.setter
    def linecolor(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "linecolor", val)
        self._linecolor = val

    # alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "alpha", val)
        self._alpha = val

    # linewidth
    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, val):
        val = imf._validate(imt._VALIDATE_EXTENT, "linewidth", val)
        self._linewidth = val

    # connector_color
    @property
    def connector_color(self):
        return self._connector_color

    @connector_color.setter
    def connector_color(self, val):
        val = imf._validate(imt._VALIDATE_DETAIL, "connector_color", val)
        self._connector_color = val

    # connector_width
    @property
    def connector_width(self):
        return self._connector_width

    @connector_width.setter
    def connector_width(self, val):
        val = imf._validate(imt._VALIDATE_DETAIL, "connector_width", val)
        self._connector_width = val

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

    ## COPY FUNCTION ##
    # This is solely to get around matplotlib's restrictions around re-using an artist across multiple axes
    # Instead, you can use add_artist() like normal, but with add_artist(na.copy())
    # Thank you to the cartopy team for helping fix a bug with this!
    def copy(self):
        return copy.deepcopy(self)

    ## CREATE FUNCTION ##
    # Calling DetailIndicator.create(ax) will create an inset map with the specified parameters on the given axis
    # Note that this is different than the way NorthArrows and ScaleBars are rendered (via draw/add_artist())!
    def create(self,
               pax: imt._TYPE_EXTENT["pax"],
               iax: imt._TYPE_EXTENT["bax"],
               pcrs: imt._TYPE_EXTENT["pcrs"],
               icrs: imt._TYPE_EXTENT["bcrs"], **kwargs):
        
        # Can re-use the drawing function we already established, but return the object instead
        dti = indicate_detail(pax=pax, iax=iax, pcrs=pcrs, icrs=icrs,
                              to_return=self._to_return, straighten=self._straighten,
                              pad=self._pad, plot=self._plot,
                              facecolor=self._facecolor, linecolor=self._linecolor,
                              alpha=self._alpha, linewidth=self._linewidth,
                              connector_color=self._connector_color,
                              connector_width=self._connector_width,
                              **self._kwargs, **kwargs)
        
        # The indicator will be drawn automatically if plot is True
        # If we have anything to return from to_return, we will do so here
        if dti is not None:
            return dti

### DRAWING FUNCTIONS ###
# See here for doc: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.inset_axes.html
# See here for kwargs: https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.axes_grid1.inset_locator.inset_axes.html#mpl_toolkits.axes_grid1.inset_locator.inset_axes

# Function for creating an inset map, independent of the InsetMap object model
# It is intended to be an easier-to-use API than the default inset_axes
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
    
    # Casting size to width and height
    if isinstance(size, (tuple, list)):
        inset_width, inset_height = size
    else:
        inset_width = size 
        inset_height = size

    ## PADDING ##
    # Padding is expressed in inches here, unlike traditional matplotlib
    # which expresses it as a fraction of the font size
    if isinstance(pad, (tuple, list)):
        pad_x, pad_y = pad
    else:
        pad_x = pad 
        pad_y = pad
    
    ## RESIZING ##
    # Getting the current dimensions of the parent axis in inches (ignoring ticks and labels - just the axis itself)
    parent_axis_bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    # Expressing the desired height and width of the inset map as a fraction of the parent
    # We do this because, later on, we're assuming everything is in ax.transAxes
    # which ranges from 0 to 1, as a fraction of the parent axis
    inset_width = inset_width / parent_axis_bbox.width
    inset_height = inset_height / parent_axis_bbox.height
    # and doing the same for the padding
    pad_x = pad_x / parent_axis_bbox.width
    pad_y = pad_y / parent_axis_bbox.height

    ## PLACEMENT ##
    # Calculating the start coordinate (which is always the bottom-left corner) of the inset map
    # based on the desired location, padding (inches) from the side, and the height and width of the inset map
    if coords is None:
        # First, the x coordinate
        if location in ["upper left", "center left", "lower left"]:
            x = pad_x
        elif location in ["upper center", "center", "lower center"]:
            x = (1 - (inset_width + pad_x)) / 2
        elif location in ["upper right", "center right", "lower right"]:
            x = 1 - (inset_width + pad_x)
        # Then the y coordinate
        if location in ["upper left", "upper center", "upper right"]:
            y = 1 - (inset_height + pad_y)
        elif location in ["center left", "center", "center right"]:
            y = (1 - (inset_height + pad_y)) / 2
        elif location in ["lower left", "lower center", "lower right"]:
            y = pad_y
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
            x = coords[0] - (inset_width / 2)
        elif location in ["upper right", "center right", "lower right"]:
            x = coords[0] - inset_width
        # Then the y coordinate
        if location in ["upper left", "upper center", "upper right"]:
            y = coords[1] - inset_height
        elif location in ["center left", "center", "center right"]:
            y = coords[1] - (inset_height / 2)
        elif location in ["lower left", "lower center", "lower right"]:
            y = coords[1]
    
    ## DRAWING ##
    # Creating the new inset map with the specified height, width, and location
    # by default, inset_axes requires everything to be in ax.transAxes coordinates
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

# This function will display the extent/bounds of one axis on the other
# This is can be used on an inset map to show where the bounds of the parent axis lay
# or, it is called by detail_indicator to show where the bounds of an inset axis lay on the parent
# here, PAX means "plotting axis" (where the indicator is plotted) 
# and BAX means "bounds axis" (where the extent is derived from)
def indicate_extent(pax: imt._TYPE_EXTENT["pax"],
                    bax: imt._TYPE_EXTENT["bax"],
                    pcrs: imt._TYPE_EXTENT["pcrs"],
                    bcrs: imt._TYPE_EXTENT["bcrs"],
                    to_return: imt._TYPE_EXTENT["to_return"]=None,
                    straighten: imt._TYPE_EXTENT["straighten"]=True,
                    pad: imt._TYPE_EXTENT["pad"]=0.05,
                    plot: imt._TYPE_EXTENT["plot"]=True,
                    facecolor: imt._TYPE_EXTENT["facecolor"]="red",
                    linecolor: imt._TYPE_EXTENT["linecolor"]="red",
                    alpha: imt._TYPE_EXTENT["alpha"]=0.5,
                    linewidth: imt._TYPE_EXTENT["linewidth"]=1,
                    **kwargs):
    
    ## VALIDATION ##
    pax = imf._validate(imt._VALIDATE_EXTENT, "pax", pax)
    bax = imf._validate(imt._VALIDATE_EXTENT, "bax", bax)
    pcrs = imf._validate(imt._VALIDATE_EXTENT, "pcrs", pcrs)
    bcrs = imf._validate(imt._VALIDATE_EXTENT, "bcrs", bcrs)
    to_return = imf._validate(imt._VALIDATE_EXTENT, "to_return", to_return)
    straighten = imf._validate(imt._VALIDATE_EXTENT, "straighten", straighten)
    pad = imf._validate(imt._VALIDATE_EXTENT, "pad", pad)
    plot = imf._validate(imt._VALIDATE_EXTENT, "plot", plot)
    facecolor = imf._validate(imt._VALIDATE_EXTENT, "facecolor", facecolor)
    linecolor = imf._validate(imt._VALIDATE_EXTENT, "linecolor", linecolor)
    alpha = imf._validate(imt._VALIDATE_EXTENT, "alpha", alpha)
    linewidth = imf._validate(imt._VALIDATE_EXTENT, "linewidth", linewidth)
    
    # Make sure the figure layout is calculated
    fig = pax.get_figure()
    fig.draw_without_rendering()
    
    # Get the limits of the bounds axis (which will be in its own crs)
    ymin, ymax = bax.get_ylim()
    yrange = abs(ymax-ymin)
    xmin, xmax = bax.get_xlim()
    xrange = abs(xmax-xmin)

    # Buffering the points, if desired
    # Note that this is treated as a percentage increase/decrease!
    if pad is not None and isinstance(pad, (float, int)):
        pad_data = min(yrange, xrange)*pad
    else:
        pad_data = 0

    # Converting it into a tuple of coordinates
    # in the order of lower-left, upper-left, upper-right, lower-right
    extent_corners = [(xmin-pad_data, ymin-pad_data), (xmin-pad_data, ymax+pad_data), 
                      (xmax+pad_data, ymax+pad_data), (xmax+pad_data, ymin-pad_data)]

    # Converting the points
    # This is now ready to be plotted on the parent axis, if desired
    transform_crs = pyproj.Transformer.from_crs(bcrs, pcrs, always_xy=True)
    extent_points = numpy.array([transform_crs.transform(p[0],p[1]) for p in extent_corners])
    extent_shape = shapely.Polygon(extent_points)

    # Straightening the points if desired
    if straighten == True:
        extent_shape = shapely.envelope(extent_shape)

    # return extent_shape
    
    # Plotting, if desired
    if plot == True:
        # Note that the alpha ONLY applies to the facecolor!
        extent_patch = matplotlib.patches.Polygon(list(extent_shape.exterior.coords), transform=pax.transData,
                                                  facecolor=matplotlib.colors.to_rgba(facecolor, alpha=alpha), 
                                                  edgecolor=linecolor, linewidth=linewidth, **kwargs)
        pax.add_artist(extent_patch)

    # Deciding what we need to return
    if to_return is None:
        pass
    elif to_return == "shape":
        return extent_shape
    elif to_return == "patch":
        return extent_patch
    elif to_return == "fig":
        return [fig.transFigure.inverted().transform(pax.transData.transform(p)) for p in list(extent_shape.exterior.coords)[::-1]]
    elif to_return == "ax":
        return [pax.transAxes.inverted().transform(pax.transData.transform(p)) for p in list(extent_shape.exterior.coords)[::-1]]
    else:
        pass

# Detail indicators are for when the inset map shows a zoomed-in section of the parent map
# This will also, call extent_indicator too, as the two are linked
# here, PAX means "parent axis" (where the indicator is plotted) 
# and IAX means "inset axis" (which contains the detail/zoomed-in section)
def indicate_detail(pax: imt._TYPE_EXTENT["pax"], 
                    iax: imt._TYPE_EXTENT["bax"], 
                    pcrs: imt._TYPE_EXTENT["pcrs"], 
                    icrs: imt._TYPE_EXTENT["bcrs"],
                    to_return: imt._TYPE_DETAIL["to_return"]=None,
                    straighten: imt._TYPE_EXTENT["straighten"]=True,
                    pad: imt._TYPE_EXTENT["pad"]=0.05,
                    plot: imt._TYPE_EXTENT["plot"]=True,
                    facecolor: imt._TYPE_EXTENT["facecolor"]="none",
                    alpha: imt._TYPE_EXTENT["alpha"]=1,
                    linecolor: imt._TYPE_EXTENT["linecolor"]="black",
                    linewidth: imt._TYPE_EXTENT["linewidth"]=1,
                    # connector_color: imt._TYPE_DETAIL["connector_color"]="black",
                    # connector_width: imt._TYPE_DETAIL["connector_width"]=1,
                    **kwargs):
    
    fig = pax.get_figure()
    fig.draw_without_rendering()

    ## VALIDATION ##
    pax = imf._validate(imt._VALIDATE_EXTENT, "pax", pax)
    iax = imf._validate(imt._VALIDATE_EXTENT, "bax", iax)
    pcrs = imf._validate(imt._VALIDATE_EXTENT, "pcrs", pcrs)
    icrs = imf._validate(imt._VALIDATE_EXTENT, "bcrs", icrs)
    to_return = imf._validate(imt._VALIDATE_DETAIL, "to_return", to_return)
    straighten = imf._validate(imt._VALIDATE_EXTENT, "straighten", straighten)
    pad = imf._validate(imt._VALIDATE_EXTENT, "pad", pad)
    plot = imf._validate(imt._VALIDATE_EXTENT, "plot", plot)
    facecolor = imf._validate(imt._VALIDATE_EXTENT, "facecolor", facecolor)
    alpha = imf._validate(imt._VALIDATE_EXTENT, "alpha", alpha)
    linecolor = imf._validate(imt._VALIDATE_EXTENT, "linecolor", linecolor)
    linewidth = imf._validate(imt._VALIDATE_EXTENT, "linewidth", linewidth)
    # connector_color = imf._validate(imt._VALIDATE_DETAIL, "connector_color", connector_color)
    # connector_width = imf._validate(imt._VALIDATE_DETAIL, "connector_width", connector_width)

    # Drawing the extent indicator on the main map
    # Setting to_return="ax" gets us the corners of the patch in pax.transAxes coordinates
    # We only need the first 4 points - the fifth is a repeated point to enforce "closure"
    corners_extent = indicate_extent(pax=pax, bax=iax, pcrs=pcrs, bcrs=icrs, 
                                     straighten=straighten, pad=pad, plot=plot,
                                     facecolor=facecolor, linecolor=linecolor,
                                     alpha=alpha, linewidth=linewidth*1.25,
                                     to_return="ax", **kwargs)[:4]

    # Getting the inset axis points and transforming them to the parent axis CRS
    corners_inset = _inset_corners_to_parent(pax, iax)

    # Getting the center of both the extent and the inset, which we will then use to decide WHICH lines to draw
    center_extent_x = sum([p[0] for p in corners_extent]) / len(corners_extent)
    center_extent_y = sum([p[1] for p in corners_extent]) / len(corners_extent)
    center_inset_x = sum([p[0] for p in corners_inset]) / len(corners_inset)
    center_inset_y = sum([p[1] for p in corners_inset]) / len(corners_inset)

    ## CONNECTION ##
    # This part is quite tricky, and involves connecting the inset map to its extent indicator
    # To do so, we make an educated guess about which corners we need to connect, 
    # based on the relative position of each object
    
    # If our extent is horizontally centered with our inset, connect just the left or right edges
    if (abs(center_extent_y - center_inset_y) / abs(center_inset_y)) <= 0.30:
        if center_extent_x > center_inset_x:
            # extent lefts + inset rights
            connections = [[corners_extent[0], corners_inset[3]], [corners_extent[1], corners_inset[2]]]
        else:
            # extent rights + inset lefts
            connections = [[corners_extent[3], corners_inset[0]], [corners_extent[2], corners_inset[1]]]
    
    # If instead our extent is vertically centered, connect just the top or bottom edges
    elif (abs(center_extent_x - center_inset_x) / abs(center_inset_x)) <= 0.30:
        if center_extent_y > center_inset_y:
            # extent bottoms + inset tops
            connections = [[corners_extent[0], corners_inset[1]], [corners_extent[3], corners_inset[2]]]
        else:
            # extent tops + inset bottoms
            connections = [[corners_extent[1], corners_inset[0]], [corners_extent[2], corners_inset[3]]]
    
    # The most common cases will be when the inset is in a corner...
    elif center_extent_x > center_inset_x and center_extent_y > center_inset_y:
        # top-left and bottom-right corners for each
        connections = [[corners_extent[1], corners_inset[1]], [corners_extent[3], corners_inset[3]]]
    elif center_extent_x <= center_inset_x and center_extent_y > center_inset_y:
        # top-right and bottom-left corners for each
        connections = [[corners_extent[2], corners_inset[2]], [corners_extent[0], corners_inset[0]]]
    elif center_extent_x > center_inset_x and center_extent_y <= center_inset_y:
        # bottom-left and top-right corners for each
        connections = [[corners_extent[0], corners_inset[0]], [corners_extent[2], corners_inset[2]]]
    elif center_extent_x <= center_inset_x and center_extent_y <= center_inset_y:
        # top-right and bottom-left corners for each
        connections = [[corners_extent[2], corners_inset[2]], [corners_extent[0], corners_inset[0]]]

    ## PLOTTING ##
    if plot == True:
        # A manual plot call, to connect the corners to each other
        for c in connections:
            # This is listed as [extent_x, inset_x], [extent_y, inset_y]
            pax.plot([c[0][0], c[1][0]], [c[0][1], c[1][1]], 
                    color=linecolor, linewidth=linewidth, transform=pax.transAxes)
        
        # Also updating the linewidth and color of the inset map itsef, to match
        for a in ["top","bottom","left","right"]:
            iax.spines[a].set_linewidth(linewidth*1.2) # making this slightly thicker
            iax.spines[a].set_edgecolor(linecolor)
    
    # Returning as requested
    if to_return is None:
        pass 
    elif to_return == "connectors" or to_return == "lines":
        return connections
    else:
        pass

### HELPING FUNCTIONS ###

# This is a top-level helping function
# that will return an axis with inset maps drawn for Alaska, Hawaii, DC, and/or Puerto Rico
# NOTE that as of this initial release, it assumes your map is in CRS 3857 for positioning
def inset_usa(ax, alaska=True, hawaii=True, dc=True, puerto_rico=True, size=None, pad=None, **kwargs):
    # This will return all of the axes we create
    to_return = []
    
    # Alaska and Hawaii are positioned relative to each other
    if alaska == True and hawaii == True:
        aax = inset_map(ax, "lower left", size, pad, **kwargs)
        to_return.append(aax)
        # Need to shift over the hawaii axis by the size of the alaska axis
        # Note that we add xmax and xmin together here, to account for the padding (xmin is the amount of padding)
        shift_right = float(aax.get_window_extent().transformed(ax.transAxes.inverted()).xmax) + float(aax.get_window_extent().transformed(ax.transAxes.inverted()).xmin)
        # also need to shift it up, by the amount of the padding (which we can crib from ymin)
        shift_up = float(aax.get_window_extent().transformed(ax.transAxes.inverted()).ymin)
        hax = inset_map(ax, "lower left", size, pad, coords=(shift_right, shift_up), **kwargs)
        to_return.append(hax)
    else:
        if alaska == True:
            aax = inset_map(ax, "lower_left", size, pad, **kwargs)
            to_return.append(aax)
        if hawaii == True:
            hax = inset_map(ax, "lower left", size, pad, **kwargs)
            to_return.append(hax)

    # Puerto Rico is positioned off the coast of Florida
    if puerto_rico == True:
        pax = inset_map(ax, "lower right", size, pad, **kwargs)
        to_return.append(pax)
    
    # DC is off the coast of DC
    if dc == True:
        dax = inset_map(ax, "center right", size, pad, **kwargs)
        to_return.append(dax)
    
    # Finally, returning everything
    return to_return


# This retrieves the position of the inset axes (iax)
# in the coordinates of its parent axis 
def _inset_corners_to_parent(pax, iax):
    # Make sure the figure layout is calculated
    fig = pax.get_figure()
    fig.draw_without_rendering()
    
    # Get positions as Bbox objects in figure coordinates (0-1)
    iax_pos = iax.get_position()
    
    # Extract corners in figure coordinates
    figure_corners = numpy.array([(iax_pos.x0, iax_pos.y0), (iax_pos.x0, iax_pos.y1), 
                                  (iax_pos.x1, iax_pos.y1), (iax_pos.x1, iax_pos.y0)])
    
    # Convert to parent axes coordinates (0-1, as a fraction of each axis)
    parent_corners = pax.transAxes.inverted().transform(
        fig.transFigure.transform(figure_corners)
    )

    return parent_corners