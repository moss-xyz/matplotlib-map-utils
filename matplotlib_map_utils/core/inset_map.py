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
from typing import Literal, Any
# The information contained in our helper scripts (validation and defaults)
from pydantic import TypeAdapter
from .. import config
from ..validation import inset_map as imt

### CLASSES ###
# Note these are really just to be convenient when storing the 
# configuration options that are used by the drawing functions instead

# The main object model of the inset map
class InsetMap(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 size_profile: str=None,
                 location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="lower left", 
                 size: Any=None,
                 pad: Any=None,
                 coords: Any=None,
                 transform=None,
                 to_plot=None,
                 zorder: int=99,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        self._size_profile = size_profile if size_profile is not None else config.DEFAULT_SIZE
        # Validating each of the passed parameters
        # We pass size_profile to the validator, which automatically applies the defaults if size/pad are None
        kwargs_model = {"location": location, "coords": coords, "to_plot": to_plot, "zorder": zorder, "size_profile": self._size_profile}
        if size is not None: kwargs_model["size"] = size
        if pad is not None: kwargs_model["pad"] = pad
            
        inset_model = imt.InsetMapInsetModel(**kwargs_model)
        self._location = inset_model.location
        self._size = inset_model.size
        self._pad = inset_model.pad
        self._coords = inset_model.coords
        self._to_plot = inset_model.model_dump(exclude_unset=True).get('to_plot', None)
        self._zorder = inset_model.zorder


        self._transform = transform # not validated!
        self._kwargs = kwargs # not validated!

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
        self._location = TypeAdapter(imt.InsetMapInsetModel.model_fields['location'].annotation).validate_python(val)
    
    @property
    def loc(self):
        return self._location

    @loc.setter
    def loc(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        self._location = TypeAdapter(imt.InsetMapInsetModel.model_fields['location'].annotation).validate_python(val)

    # size
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        if val is not None:
            self._size = TypeAdapter(imt.InsetMapInsetModel.model_fields['size'].annotation).validate_python(val)
        else:
            self._size = imt.InsetMapInsetModel(size_profile=self._size_profile, location=self._location, zorder=self._zorder).size
    
    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        if val is not None:
            self._pad = TypeAdapter(imt.InsetMapInsetModel.model_fields['pad'].annotation).validate_python(val)
        else:
            self._pad = imt.InsetMapInsetModel(size_profile=self._size_profile, location=self._location, zorder=self._zorder).pad
    
    # coords
    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, val):
        self._coords = TypeAdapter(imt.InsetMapInsetModel.model_fields['coords'].annotation).validate_python(val)
    
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
        if val is not None:
            validated = TypeAdapter(imt.InsetMapInsetModel.model_fields['to_plot'].annotation).validate_python(val)
            self._to_plot = [d.model_dump(exclude_unset=True) if d is not None else None for d in validated]
        else:
            self._to_plot = None
    
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        self._zorder = TypeAdapter(imt.InsetMapInsetModel.model_fields['zorder'].annotation).validate_python(val)

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
        iax = inset_map(ax=pax, size_profile=self._size_profile, location=self._location, size=self._size,
                        pad=self._pad, coords=self._coords, transform=self._transform, zorder=self._zorder,
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
    

# The main object model of the extent indicator
class ExtentIndicator(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 to_return: Any=None,
                 straighten: bool=True,
                 pad: Any=0.05,
                 plot: bool=True,
                 facecolor: Any="red",
                 linecolor: Any="red",
                 alpha: Any=0.5,
                 linewidth: Any=1,
                 zorder: int=99,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # Validating each of the passed parameters
        self._to_return = TypeAdapter(imt.InsetMapExtentModel.model_fields['to_return'].annotation).validate_python(to_return)
        self._straighten = TypeAdapter(imt.InsetMapExtentModel.model_fields['straighten'].annotation).validate_python(straighten)
        self._pad = TypeAdapter(imt.InsetMapExtentModel.model_fields['pad'].annotation).validate_python(pad)
        self._plot = TypeAdapter(imt.InsetMapExtentModel.model_fields['plot'].annotation).validate_python(plot)
        self._facecolor = TypeAdapter(imt.InsetMapExtentModel.model_fields['facecolor'].annotation).validate_python(facecolor)
        self._linecolor = TypeAdapter(imt.InsetMapExtentModel.model_fields['linecolor'].annotation).validate_python(linecolor)
        self._alpha = TypeAdapter(imt.InsetMapExtentModel.model_fields['alpha'].annotation).validate_python(alpha)
        self._linewidth = TypeAdapter(imt.InsetMapExtentModel.model_fields['linewidth'].annotation).validate_python(linewidth)
        self._zorder = TypeAdapter(imt.InsetMapExtentModel.model_fields['zorder'].annotation).validate_python(zorder)

        self._kwargs = kwargs # not validated!

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
        self._to_return = TypeAdapter(imt.InsetMapExtentModel.model_fields['to_return'].annotation).validate_python(val)

    # straighten
    @property
    def straighten(self):
        return self._straighten

    @straighten.setter
    def straighten(self, val):
        self._straighten = TypeAdapter(imt.InsetMapExtentModel.model_fields['straighten'].annotation).validate_python(val)

    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        self._pad = TypeAdapter(imt.InsetMapExtentModel.model_fields['pad'].annotation).validate_python(val)

    # plot
    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, val):
        self._plot = TypeAdapter(imt.InsetMapExtentModel.model_fields['plot'].annotation).validate_python(val)

    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        self._facecolor = TypeAdapter(imt.InsetMapExtentModel.model_fields['facecolor'].annotation).validate_python(val)

    # linecolor
    @property
    def linecolor(self):
        return self._linecolor

    @linecolor.setter
    def linecolor(self, val):
        self._linecolor = TypeAdapter(imt.InsetMapExtentModel.model_fields['linecolor'].annotation).validate_python(val)

    # alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        self._alpha = TypeAdapter(imt.InsetMapExtentModel.model_fields['alpha'].annotation).validate_python(val)

    # linewidth
    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, val):
        self._linewidth = TypeAdapter(imt.InsetMapExtentModel.model_fields['linewidth'].annotation).validate_python(val)
    
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        self._zorder = TypeAdapter(imt.InsetMapExtentModel.model_fields['zorder'].annotation).validate_python(val)

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
               pax: matplotlib.axes.Axes,
               bax: matplotlib.axes.Axes,
               pcrs: Any,
               bcrs: Any, **kwargs):
        
        # Can re-use the drawing function we already established, but return the object instead
        exi = indicate_extent(pax=pax, bax=bax, pcrs=pcrs, bcrs=bcrs, 
                              to_return=self._to_return, straighten=self._straighten,
                              pad=self._pad, plot=self._plot,
                              facecolor=self._facecolor, linecolor=self._linecolor,
                              alpha=self._alpha, linewidth=self._linewidth, zorder=self._zorder,
                              **self._kwargs, **kwargs)
        
        # The indicator will be drawn automatically if plot is True
        # If we have anything to return from to_return, we will do so here
        if exi is not None:
            return exi

# The main object model of the detail indicator
class DetailIndicator(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self,
                 to_return: Any=None,
                 straighten: bool=True,
                 pad: Any=0.05,
                 plot: bool=True,
                 facecolor: Any="none",
                 linecolor: Any="black",
                 alpha: Any=1,
                 linewidth: Any=1,
                 connector_color: Any="black",
                 connector_width: Any=1,
                 zorder: int=99,
                 **kwargs):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # Validating each of the passed parameters
        self._to_return = TypeAdapter(imt.InsetMapDetailModel.model_fields['to_return'].annotation).validate_python(to_return)
        self._straighten = TypeAdapter(imt.InsetMapExtentModel.model_fields['straighten'].annotation).validate_python(straighten)
        self._pad = TypeAdapter(imt.InsetMapExtentModel.model_fields['pad'].annotation).validate_python(pad)
        self._plot = TypeAdapter(imt.InsetMapExtentModel.model_fields['plot'].annotation).validate_python(plot)
        self._facecolor = TypeAdapter(imt.InsetMapDetailModel.model_fields['facecolor'].annotation).validate_python(facecolor)
        self._linecolor = TypeAdapter(imt.InsetMapDetailModel.model_fields['linecolor'].annotation).validate_python(linecolor)
        self._alpha = TypeAdapter(imt.InsetMapDetailModel.model_fields['alpha'].annotation).validate_python(alpha)
        self._linewidth = TypeAdapter(imt.InsetMapDetailModel.model_fields['linewidth'].annotation).validate_python(linewidth)
        self._connector_color = TypeAdapter(imt.InsetMapDetailModel.model_fields['connector_color'].annotation).validate_python(connector_color)
        self._connector_width = TypeAdapter(imt.InsetMapDetailModel.model_fields['connector_width'].annotation).validate_python(connector_width)
        self._zorder = TypeAdapter(imt.InsetMapDetailModel.model_fields['zorder'].annotation).validate_python(zorder)

        self._kwargs = kwargs # not validated!

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
        self._to_return = TypeAdapter(imt.InsetMapDetailModel.model_fields['to_return'].annotation).validate_python(val)

    # straighten
    @property
    def straighten(self):
        return self._straighten

    @straighten.setter
    def straighten(self, val):
        self._straighten = TypeAdapter(imt.InsetMapExtentModel.model_fields['straighten'].annotation).validate_python(val)

    # pad
    @property
    def pad(self):
        return self._pad

    @pad.setter
    def pad(self, val):
        self._pad = TypeAdapter(imt.InsetMapExtentModel.model_fields['pad'].annotation).validate_python(val)

    # plot
    @property
    def plot(self):
        return self._plot

    @plot.setter
    def plot(self, val):
        self._plot = TypeAdapter(imt.InsetMapExtentModel.model_fields['plot'].annotation).validate_python(val)

    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        self._facecolor = TypeAdapter(imt.InsetMapDetailModel.model_fields['facecolor'].annotation).validate_python(val)

    # linecolor
    @property
    def linecolor(self):
        return self._linecolor

    @linecolor.setter
    def linecolor(self, val):
        self._linecolor = TypeAdapter(imt.InsetMapDetailModel.model_fields['linecolor'].annotation).validate_python(val)

    # alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        self._alpha = TypeAdapter(imt.InsetMapDetailModel.model_fields['alpha'].annotation).validate_python(val)

    # linewidth
    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, val):
        self._linewidth = TypeAdapter(imt.InsetMapExtentModel.model_fields['linewidth'].annotation).validate_python(val)

    # connector_color
    @property
    def connector_color(self):
        return self._connector_color

    @connector_color.setter
    def connector_color(self, val):
        self._connector_color = TypeAdapter(imt.InsetMapDetailModel.model_fields['connector_color'].annotation).validate_python(val)

    # connector_width
    @property
    def connector_width(self):
        return self._connector_width

    @connector_width.setter
    def connector_width(self, val):
        self._connector_width = TypeAdapter(imt.InsetMapDetailModel.model_fields['connector_width'].annotation).validate_python(val)
    
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        self._zorder = TypeAdapter(imt.InsetMapDetailModel.model_fields['zorder'].annotation).validate_python(val)

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
               pax: matplotlib.axes.Axes,
               iax: matplotlib.axes.Axes,
               pcrs: Any,
               icrs: Any, 
               **kwargs):
        
        # Can re-use the drawing function we already established, but return the object instead
        dti = indicate_detail(pax=pax, iax=iax, pcrs=pcrs, icrs=icrs,
                              to_return=self._to_return, straighten=self._straighten,
                              pad=self._pad, plot=self._plot,
                              facecolor=self._facecolor, linecolor=self._linecolor,
                              alpha=self._alpha, linewidth=self._linewidth,
                              connector_color=self._connector_color,
                              connector_width=self._connector_width,
                              zorder=self._zorder,
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
              size_profile: str=None,
              location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right", 
              size: Any=None,
              pad: Any=None,
              coords: Any=None,
              transform=None,
              zorder: int=99,
              **kwargs):
    
    ## VALIDATION ##
    kwargs_model = {"location": location, "coords": coords, "zorder": zorder, "size_profile": size_profile if size_profile is not None else config.DEFAULT_SIZE}
    if size is not None: kwargs_model["size"] = size
    if pad is not None: kwargs_model["pad"] = pad
        
    inset_model = imt.InsetMapInsetModel(**kwargs_model)
    _location = inset_model.location
    _size = inset_model.size
    _pad = inset_model.pad
    coords = inset_model.coords
    zorder = inset_model.zorder

    ## SET-UP ##
    # Getting the figure
    fig = ax.get_figure()

    ## SIZE ##
    # Setting the desired dimensions of the inset map
    # The default inset_axis() function does this as a fraction of the parent axis
    # But the size variable expects dimensions in inches
    
    # Casting size to width and height
    if isinstance(_size, (tuple, list)):
        inset_width, inset_height = _size
    else:
        inset_width, inset_height = _size, _size

    # Padding is expressed in inches here, unlike traditional matplotlib
    # which expresses it as a fraction of the font size
    if isinstance(_pad, (tuple, list)):
        pad_x, pad_y = _pad
    else:
        pad_x, pad_y = _pad, _pad
    
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
    iax = ax.inset_axes([x, y, inset_width, inset_height], zorder=zorder, **kwargs)
    
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
def indicate_extent(pax: matplotlib.axes.Axes,
                    bax: matplotlib.axes.Axes,
                    pcrs: Any,
                    bcrs: Any,
                    to_return: Any=None,
                    straighten: bool=True,
                    pad: Any=0.05,
                    plot: bool=True,
                    facecolor: Any="red",
                    linecolor: Any="red",
                    alpha: Any=0.5,
                    linewidth: Any=1,
                    zorder: int=99,
                    **kwargs):
    
    ## VALIDATION ##
    extent_model = imt.InsetMapExtentModel(pax=pax, bax=bax, pcrs=pcrs, bcrs=bcrs, to_return=to_return, straighten=straighten, pad=pad, plot=plot, facecolor=facecolor, linecolor=linecolor, alpha=alpha, linewidth=linewidth, zorder=zorder)
    pax = extent_model.pax
    bax = extent_model.bax
    pcrs = extent_model.pcrs
    bcrs = extent_model.bcrs
    to_return = extent_model.to_return
    straighten = extent_model.straighten
    pad = extent_model.pad
    plot = extent_model.plot
    facecolor = extent_model.facecolor
    linecolor = extent_model.linecolor
    alpha = extent_model.alpha
    linewidth = extent_model.linewidth
    zorder = extent_model.zorder
    
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
  
    # Plotting, if desired
    if plot == True:
        # Note that the alpha ONLY applies to the facecolor!
        extent_patch = matplotlib.patches.Polygon(list(extent_shape.exterior.coords), transform=pax.transData,
                                                  facecolor=matplotlib.colors.to_rgba(facecolor, alpha=alpha), 
                                                  edgecolor=linecolor, linewidth=linewidth, zorder=zorder, **kwargs)
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
def indicate_detail(pax: matplotlib.axes.Axes, 
                    iax: matplotlib.axes.Axes, 
                    pcrs: Any, 
                    icrs: Any,
                    to_return: Any=None,
                    straighten: bool=True,
                    pad: Any=0.05,
                    plot: bool=True,
                    facecolor: Any="none",
                    alpha: Any=1,
                    linecolor: Any="black",
                    linewidth: Any=1,
                    zorder: int=99,
                    **kwargs):
    
    fig = pax.get_figure()
    fig.draw_without_rendering()

    ## VALIDATION ##
    extent_model = imt.InsetMapExtentModel(pax=pax, bax=iax, pcrs=pcrs, bcrs=icrs, straighten=straighten, pad=pad, plot=plot, facecolor=facecolor, linecolor=linecolor, alpha=alpha, linewidth=linewidth, zorder=zorder)
    pax = extent_model.pax
    iax = extent_model.bax
    pcrs = extent_model.pcrs
    icrs = extent_model.bcrs
    straighten = extent_model.straighten
    pad = extent_model.pad
    plot = extent_model.plot
    facecolor = extent_model.facecolor
    alpha = extent_model.alpha
    linecolor = extent_model.linecolor
    linewidth = extent_model.linewidth
    zorder = extent_model.zorder
    to_return = TypeAdapter(imt.InsetMapDetailModel.model_fields['to_return'].annotation).validate_python(to_return)

    # Drawing the extent indicator on the main map
    # Setting to_return="ax" gets us the corners of the patch in pax.transAxes coordinates
    # We only need the first 4 points - the fifth is a repeated point to enforce "closure"
    corners_extent = indicate_extent(pax=pax, bax=iax, pcrs=pcrs, bcrs=icrs, 
                                     straighten=straighten, pad=pad, plot=plot,
                                     facecolor=facecolor, linecolor=linecolor,
                                     alpha=alpha, linewidth=linewidth*1.25,
                                     to_return="ax", zorder=zorder, **kwargs)[:4]

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
                    color=linecolor, linewidth=linewidth, transform=pax.transAxes, zorder=zorder+1)
        
        # Also updating the linewidth and color of the inset map itself, to match
        iax.spines[:].set_linewidth(linewidth*1.2) # making this slightly thicker
        iax.spines[:].set_edgecolor(linecolor)
        iax.set_zorder(zorder+2)
        iax.spines[:].set_zorder(zorder+2)
    
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
def inset_usa(ax, alaska=True, hawaii=True, dc=True, puerto_rico=True, size=None, pad=None, zorder: int=99, **kwargs):
    # This will return all of the axes we create
    to_return = []
    
    # Alaska and Hawaii are positioned relative to each other
    if alaska == True and hawaii == True:
        aax = inset_map(ax, "lower left", size, pad, zorder=zorder, **kwargs)
        to_return.append(aax)
        # Need to shift over the hawaii axis by the size of the alaska axis
        # Note that we add xmax and xmin together here, to account for the padding (xmin is the amount of padding)
        shift_right = float(aax.get_window_extent().transformed(ax.transAxes.inverted()).xmax) + float(aax.get_window_extent().transformed(ax.transAxes.inverted()).xmin)
        # also need to shift it up, by the amount of the padding (which we can crib from ymin)
        shift_up = float(aax.get_window_extent().transformed(ax.transAxes.inverted()).ymin)
        hax = inset_map(ax, "lower left", size, pad, zorder=zorder, coords=(shift_right, shift_up), **kwargs)
        to_return.append(hax)
    else:
        if alaska == True:
            aax = inset_map(ax, "lower_left", size, pad, zorder=zorder, **kwargs)
            to_return.append(aax)
        if hawaii == True:
            hax = inset_map(ax, "lower left", size, pad, zorder=zorder, **kwargs)
            to_return.append(hax)

    # Puerto Rico is positioned off the coast of Florida
    if puerto_rico == True:
        pax = inset_map(ax, "lower right", size, pad, zorder=zorder, **kwargs)
        to_return.append(pax)
    
    # DC is off the coast of DC
    if dc == True:
        dax = inset_map(ax, "center right", size, pad, zorder=zorder, **kwargs)
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