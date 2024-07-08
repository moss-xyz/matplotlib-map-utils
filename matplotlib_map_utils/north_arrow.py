# Default packages
import warnings
import math
import copy
# Math packages
import numpy
# Geo packages
import cartopy
import pyproj
# Graphical packages
import matplotlib
import matplotlib.artist
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.patheffects
import matplotlib.offsetbox
# matplotlib's useful validation functions
import matplotlib.rcsetup
# Finally, the types we use in this script
from typing import Tuple, TypedDict, Literal, get_args

### TYPE HINTS ###
# This section of the code is for defining structured dictionaries and lists
# for the custom data structures we've created (such as the style dictionaries)
# so that intellisense can help with autocompletion
class _TYPE_BASE(TypedDict, total=False):
    coords: numpy.array # must be 2D numpy array
    location: Literal["upper right", "upper left", "lower left", "lower right", 
                      "center left", "center right", "lower center", "upper center"] # can be https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html (see: loc)
    scale: float # between 0 and inf
    facecolor: str # any color value for matplotlib
    edgecolor: str # any color value for matplotlib
    linewidth: float | int # between 0 and inf
    zorder: int # any integer

class _TYPE_FANCY(TypedDict, total=False):
    coords: numpy.array # must be 2D numpy array
    facecolor: str # any color value for matplotlib
    zorder: int # any integer

class _TYPE_LABEL(TypedDict, total=False):
    text: str # any string that you want to display ("N" or "North" being the most common)
    position: Literal["top", "bottom", "left", "right"]  # from matplotlib documentation
    ha: Literal["left", "center", "right"] # from matplotlib documentation
    va: Literal["baseline", "bottom", "center", "center_baseline", "top"] # from matplotlib documentation
    fontsize: str | float | int # any fontsize value for matplotlib
    fontfamily: Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"] # from matplotlib documentation
    fontstyle: Literal["normal", "italic", "oblique"] # from matplotlib documentation
    color: str # any color value for matplotlib
    fontweight: Literal["normal", "bold", "heavy", "light", "ultrabold", "ultralight"] # from matplotlib documentation
    stroke_width: float | int # between 0 and infinity
    stroke_color: str # any color value for matplotlib
    rotation: float | int # between -360 and 360
    zorder: int # any integer

class _TYPE_SHADOW(TypedDict, total=False):
    offset: Tuple[float | int, float | int] # two-length tuple or list of x,y values in points
    alpha: float | int # between 0 and 1
    shadow_rgbFace: str # any color vlaue for matplotlib

class _TYPE_PACK(TypedDict, total=False):
    sep: float | int # between 0 and inf
    align: Literal["top", "bottom", "left", "right", "center", "baseline"] # from matplotlib documentation
    pad: float | int # between 0 and inf
    width: float | int # between 0 and inf
    height: float | int # between 0 and inf
    mode: Literal["fixed", "expand", "equal"] # from matplotlib documentation

class _TYPE_AOB(TypedDict, total=False):
    facecolor: str # NON-STANDARD: used to set the facecolor of the offset box (i.e. to white), any color vlaue for matplotlib
    edgecolor: str # NON-STANDARD: used to set the edge of the offset box (i.e. to black), any color vlaue for matplotlib
    alpha: float | int # NON-STANDARD: used to set the transparency of the face color of the offset box^, between 0 and 1
    pad: float | int # between 0 and inf
    borderpad: float | int # between 0 and inf
    prop: str | float | int # any fontsize value for matplotlib
    frameon: bool # any bool
    # bbox_to_anchor: None
    # bbox_transform: None

class _TYPE_ROTATION(TypedDict, total=False):
    degrees: float | int # anything between -360 and 360, or None for "auto"
    crs: str | int | pyproj.CRS # only required if degrees is None: should be a valid cartopy or pyproj crs, or a string that can be converted to that
    reference: Literal["axis", "data", "center"] # only required if degrees is None: should be either "axis" or "data" or "center"
    coords: Tuple[float | int, float | int] # only required if degrees is None: should be a tuple of coordinates in the relevant reference window

### DEFAULT VALUES ###
# This section of the code is for storing default values 
# that will be fed into the various classes upon creation

# Defaults for the base arrow class
_COORDS_BASE = numpy.array([
    (0.50, 1.00),
    (0.10, 0.00),
    (0.50, 0.10),
    (0.90, 0.00),
    (0.50, 1.00)
])

_DEFAULT_BASE = {
    "coords":_COORDS_BASE, 
    "location":"upper right", 
    "scale":0.50, 
    "facecolor":"white", 
    "edgecolor":"black", 
    "linewidth":1, 
    "zorder":98 
}

# Defaults for the "fancy" arrow, i.e. the patch overlaid on top
_COORDS_FANCY = numpy.array([
    (0.50, 0.85),
    (0.50, 0.20),
    (0.80, 0.10),
    (0.50, 0.85)
])

_DEFAULT_FANCY = {
    "coords":_COORDS_FANCY,
    "facecolor":"black",
    "zorder":99
}

# Defaults for the label of the arrow
_DEFAULT_LABEL = {
    "text":"N",
    "position":"top",
    "ha":"center",
    "va":"baseline",
    "fontsize":"large",
    "fontfamily":"sans-serif",
    "fontstyle":"normal",
    "color":"black",
    "fontweight":"regular",
    "stroke_width":1,
    "stroke_color":"white",
    "rotation":0,
    "zorder":99
}

# Defaults for the shadow of the arrow
_DEFAULT_SHADOW = {
    "offset":(4,-4),
    "alpha":0.5,
    "shadow_rgbFace":"black",
}

# Defaults for the VPacker or HPacker (see north_arrow for where it is used)
_DEFAULT_PACK = {
    "sep":5,
    "align":"center",
    "pad":0,
    "width":None,
    "height":None,
    "mode":"fixed"
}

# Defaults for the AnchoredOffsetBox (see north_arrow for where it is used)
_DEFAULT_AOB = {
    "facecolor":None,
    "edgecolor":None,
    "alpha":None,
    "pad":0.4,
    "borderpad":0.5,
    "prop":"medium",
    "frameon":False,
    "bbox_to_anchor":None,
    "bbox_transform":None
}

# Defaults for rotating the arrow to point towards True North (see _rotate_arrow for how it is used)
_DEFAULT_ROTATION = {
    "degrees":None,
    "crs":None,
    "reference":None,
    "coords":None 
}

### CLASSES ###
# Defining the main object model of the north arrow
# Note that base, fancy, label, and shadow are actually all "child" classes
# and are accessible through their _ names (self._base, self._shadow, etc.)
class NorthArrow(matplotlib.artist.Artist):
    # Initialization upon first creation
    # TODO: MOVE LOCATION, RENDER, ROTATION, AND CRS IN THIS
    def __init__(self, base: bool=True, base_style: _TYPE_BASE=_DEFAULT_BASE, fancy: bool=True, fancy_style: _TYPE_FANCY=_DEFAULT_FANCY, label: bool=True, label_style: _TYPE_LABEL=_DEFAULT_LABEL, shadow: bool=True, shadow_style: _TYPE_SHADOW=_DEFAULT_SHADOW, packer_style: _TYPE_PACK=_DEFAULT_PACK, aob_style: _TYPE_AOB=_DEFAULT_AOB, rotation_style: _TYPE_ROTATION=_DEFAULT_ROTATION):
        # Starting up the artist object with the base properties
        matplotlib.artist.Artist.__init__(self)
        # If any of the child classes are set to True, initialize their class with the options we have
        # Otherwise, set them as False (so we're aware)
        # Note that we are setting the style FIRST, by merging the provided dict with the default style dict
        # This allows us to not repeat that operation twice, and just use that in the init of the child class
        # ArrowBase
        # Using our handy-dandy function to validate
        base_style = _validate_dict(_DEFAULT_BASE | base_style, _VALIDATE_BASE, return_clean=True)
        self._base_style = base_style
        if base==True:
            self._base = ArrowBase(self, **self._base_style)
        else:
            self._base = base
        # ArrowFancy
        fancy_style = _validate_dict(_DEFAULT_FANCY | fancy_style, _VALIDATE_FANCY, return_clean=True)
        self._fancy_style = fancy_style
        if fancy==True:
            self._fancy = ArrowFancy(self, **self._fancy_style)
        else:
            self._fancy = fancy
        # ArrowLabel
        label_style = _validate_dict(_DEFAULT_LABEL | label_style, _VALIDATE_LABEL, return_clean=True)
        self._label_style = label_style
        if label==True:
            self._label = ArrowLabel(self, **self._label_style)
        else:
            self._label = label
        # ArrowShadow
        shadow_style = _validate_dict(_DEFAULT_SHADOW | shadow_style, _VALIDATE_SHADOW, return_clean=True)
        self._shadow_style = shadow_style
        if shadow==True:
            self._shadow = ArrowShadow(self, **self._shadow_style)
        else:
            self._shadow = shadow
        # Other style properties
        packer_style = _validate_dict(_DEFAULT_PACK | packer_style, _VALIDATE_PACK, return_clean=True)
        self._packer_style = packer_style
        aob_style = _validate_dict(_DEFAULT_AOB | aob_style, _VALIDATE_AOB, return_clean=True)
        self._aob_style = aob_style
        rotation_style = _validate_dict(_DEFAULT_ROTATION | rotation_style, _VALIDATE_ROTATION, return_clean=True)
        self._rotation_style = rotation_style
    
    # We do set the zorder for our objects individually,
    # but we ALSO set it for the entire artist, here, for some reason
    # idk I just stole this from matplotlib-scalebar
    zorder = 99

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of class values

    # TODO: If these values change, then the class needs to be updated (either destroyed or created)
    # base
    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, val: bool):
        val = _validate_type("base", val, bool)
        self._base = _obj_setter(self, self._base, val, self._base_style)
    
    # TODO: if these values change, and an object already exists, diff the dict
    # I think you can get a current dict with https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields
    # And you can diff the dict using the pipe operator {new} | {old}
    # base_style
    @property
    def base_style(self):
        return self._base_style

    @base_style.setter
    def base_style(self, val: dict):
        val = _validate_type("base_style", val, dict)
        val = _validate_dict(val, _VALIDATE_BASE, return_clean=True)
        self._base_style = self._base_style | val
        if self._base:
            self._base = ArrowBase(self, **self._base_style)
    
    # fancy
    @property
    def fancy(self):
        return self._fancy

    @fancy.setter
    def fancy(self, val: bool):
        val = _validate_type("fancy", val, bool)
        self._fancy = _obj_setter(self, self._fancy, val, self._fancy_style)
    
    # fancy_style
    @property
    def fancy_style(self):
        return self._fancy_style

    @fancy_style.setter
    def fancy_style(self, val: dict):
        val = _validate_type("fancy_style", val, dict)
        val = _validate_dict(val, _VALIDATE_FANCY, return_clean=True)
        self._fancy_style = self._fancy_style | val
        if self._fancy:
            self._fancy = ArrowBase(self, **self._fancy_style)
    
    # label
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val: bool):
        val = _validate_type("label", val, bool)
        self._label = _obj_setter(self, self._label, val, self._label_style)
    
    # label_style
    @property
    def label_style(self):
        return self._label_style

    @label_style.setter
    def label_style(self, val: dict):
        val = _validate_type("label_style", val, dict)
        val = _validate_dict(val, _VALIDATE_LABEL, return_clean=True)
        self._label_style = self._label_style | val
        if self._label:
            self._label = ArrowBase(self, **self._label_style)
    
    # shadow
    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, val: bool):
        val = _validate_type("shadow", val, bool)
        self._shadow = _obj_setter(self, self._shadow, val, self._shadow_style)
    
    # shadow_style
    @property
    def shadow_style(self):
        return self._shadow_style

    @shadow_style.setter
    def shadow_style(self, val: dict):
        val = _validate_type("shadow_style", val, dict)
        val = _validate_dict(val, _VALIDATE_SHADOW, return_clean=True)
        self._shadow_style = self._shadow_style | val
        if self._shadow:
            self._shadow = ArrowBase(self, **self._shadow_style)
    
    # packer_style
    @property
    def packer_style(self):
        return self._packer_style

    @packer_style.setter
    def packer_style(self, val: dict):
        val = _validate_type("packer_style", val, dict)
        val = _validate_dict(val, _VALIDATE_PACK, return_clean=True)
        self._packer_style = self._packer_style | val
    
    # aob_style
    @property
    def aob_style(self):
        return self._aob_style

    @aob_style.setter
    def aob_style(self, val: dict):
        val = _validate_type("aob_style", val, dict)
        val = _validate_dict(val, _VALIDATE_AOB, return_clean=True)
        self._aob_style = self._aob_style | val
    
    ## COPY FUNCTION ##
    # This is solely to get around matplotlib's restrictions around re-using an artist across multiple axes
    # Instead, you can use add_artist() like normal, but with add_artist(na.copy())
    def copy(self):
        return copy.deepcopy(self)

    ## DRAW FUNCTION ##
    # Calling ax.add_artist() on this object triggers the following draw() function
    # THANK YOU to matplotlib-scalebar for figuring this out
    # Note that we never specify the renderer - the axis takes care of it!
    def draw(self, renderer, *args, **kwargs):
        # Can re-use the drawing function we already established, but return the object instead
        na_artist = north_arrow(ax=self.axes, draw=False, 
                                base=_draw_obj(self._base), base_style=_class_dict(self._base, "parent"),
                                fancy=_draw_obj(self._fancy), fancy_style=_class_dict(self._fancy, "parent"),
                                label=_draw_obj(self._label), label_style=_class_dict(self._label, "parent"),
                                shadow=_draw_obj(self._shadow), shadow_style=_class_dict(self._shadow, "parent"),
                                packer_style=self._packer_style, aob_style=self._aob_style, rotation_style=self._rotation_style)
        # This handles the actual drawing
        na_artist.axes = self.axes
        na_artist.set_figure(self.axes.get_figure())
        na_artist.draw(renderer)

# Class constructor for the base of the north arrow
class ArrowBase:
    # Initialization upon first creation
    # Notice that these are all the keys of the _DEFAULT_BASE dictionary!
    # Except for Parent, which is our NorthArrow class
    # TODO: Do you have to make the parent call a weakref?
    # See: https://stackoverflow.com/questions/10791588/getting-container-parent-object-from-within-python
    def __init__(self, parent, coords: numpy.array, location: str, scale: float | int, facecolor: str, edgecolor: str, linewidth: float | int, zorder: int):
        self._coords = _validate(_VALIDATE_BASE, "coords", coords)
        self._location = _validate(_VALIDATE_BASE, "location", location)
        self._scale = _validate(_VALIDATE_BASE, "scale", scale)
        self._facecolor = _validate(_VALIDATE_BASE, "facecolor", facecolor)
        self._edgecolor = _validate(_VALIDATE_BASE, "edgecolor", edgecolor)
        self._linewidth = _validate(_VALIDATE_BASE, "linewidth", linewidth)
        self._zorder = _validate(_VALIDATE_BASE, "zorder", zorder)
        self._parent = parent
    
    ## INTERNAL PROPERTIES ##
    # coords
    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, val):
        val = _validate(_VALIDATE_BASE, "coords", val)
        self._coords = val
    
    # location
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        val = _validate(_VALIDATE_BASE, "location", val)
        self._location = val
    
    # scale
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        val = _validate(_VALIDATE_BASE, "scale", val)
        self._scale = val
    
    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        val = _validate(_VALIDATE_BASE, "facecolor", val)
        self._facecolor = val
    
    # edgecolor
    @property
    def edgecolor(self):
        return self._edgecolor

    @edgecolor.setter
    def edgecolor(self, val):
        val = _validate(_VALIDATE_BASE, "edgecolor", val)
        self._edgecolor = val
    
    # linewidth
    @property
    def linewidth(self):
        return self._linewidth

    @linewidth.setter
    def linewidth(self, val):
        val = _validate(_VALIDATE_BASE, "linewidth", val)
        self._linewidth = val
    
    # # rotation
    # @property
    # def rotation(self):
    #     return self._rotation

    # @rotation.setter
    # def rotation(self, val):
    #     val = _validate(_VALIDATE_BASE, "rotation", val)
    #     if self._crs is not None:
    #         warnings.warn(f"Setting the rotation overrides the current CRS value of {self._crs}")
    #         self._crs = None
    #         self._rotation = val
    #     elif self._crs is None and val is None:
    #         raise ValueError(f"One of rotation or CRS must be set; keeping rotation at current value")
    #     else:
    #         self._rotation = val
    
    # # crs
    # @property
    # def crs(self):
    #     return self._crs

    # @crs.setter
    # def crs(self, val):
    #     if self._rotation is not None:
    #         warnings.warn(f"Setting the CRS overrides the current rotation value of {self._rotation}")
    #         self._rotation = None
    #         val = _validate(_VALIDATE_BASE, "crs", val, kwargs={"rotation":self._rotation})
    #         self._crs = val
    #     elif self._rotation is None and val is None:
    #         raise ValueError(f"One of rotation or CRS must be set; keeping CRS at current value")
    #     else:
    #         self._crs = val
    
    # # rotation_ref
    # @property
    # def rotation_ref(self):
    #     return self._rotation_ref

    # @rotation_ref.setter
    # def rotation_ref(self, val):
    #     val = _validate(_VALIDATE_BASE, "rotation_ref", val)
    #     self._rotation_ref = val
    
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        # val = _validate_type("zorder", val, int)
        val = _validate(_VALIDATE_BASE, "zorder", val)
        self._zorder = val

# Class constructor for the "fancy" part of the north arrow (the right hand patch)
class ArrowFancy:
    # Initialization upon first creation
    # Notice that these are all the keys of the _DEFAULT_FANCY dictionary!
    def __init__(self, parent, coords: numpy.array, facecolor: str, zorder: int):
        self._coords = _validate(_VALIDATE_FANCY, "coords", coords)
        self._facecolor = _validate(_VALIDATE_FANCY, "facecolor", facecolor)
        self._zorder = _validate(_VALIDATE_FANCY, "zorder", zorder)
        self._parent = parent
    
    ## INTERNAL PROPERTIES ##
    # coords
    @property
    def coords(self):
        return self._coords

    @coords.setter
    def coords(self, val):
        val =_validate(_VALIDATE_FANCY, "coords", val)
        self._coords = val
    
    # facecolor
    @property
    def facecolor(self):
        return self._facecolor

    @facecolor.setter
    def facecolor(self, val):
        val =_validate(_VALIDATE_FANCY, "facecolor", val)
        self._facecolor = val
     
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        val =_validate(_VALIDATE_FANCY, "zorder", val)
        self._zorder = val

# Class constructor for the label of the north arrow (traditionally, the letter N)
# TODO: Get Rotation working on this one, which is a part of the textprops dict actually
class ArrowLabel:
    # Initialization upon first creation
    # Notice that these are all the keys of the _DEFAULT_FANCY dictionary!
    def __init__(self, parent, text: str, position: str, ha: str, va: str, fontsize: str | float | int, fontfamily: str, fontstyle: str, color: str, fontweight: str, stroke_width: float | int, stroke_color: str, rotation: float | int, zorder: int):
        self._text = _validate(_VALIDATE_LABEL, "text", text)
        self._position = _validate(_VALIDATE_LABEL, "position", position)
        self._ha = _validate(_VALIDATE_LABEL, "ha", ha)
        self._va = _validate(_VALIDATE_LABEL, "va", va)
        self._fontsize = _validate(_VALIDATE_LABEL, "fontsize", fontsize)
        self._fontfamily = _validate(_VALIDATE_LABEL, "fontfamily", fontfamily)
        self._fontstyle = _validate(_VALIDATE_LABEL, "fontstyle", fontstyle)
        self._color = _validate(_VALIDATE_LABEL, "color", color)
        self._fontweight = _validate(_VALIDATE_LABEL, "fontweight", fontweight)
        self._stroke_width = _validate(_VALIDATE_LABEL, "stroke_width", stroke_width)
        self._stroke_color = _validate(_VALIDATE_LABEL, "stroke_color", stroke_color)
        self._rotation = _validate(_VALIDATE_LABEL, "rotation", rotation)
        self._zorder = _validate(_VALIDATE_LABEL, "zorder", zorder)
        self._parent = parent
    
    ## INTERNAL PROPERTIES ##
    # text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        val = _validate(_VALIDATE_LABEL, "text", val)
        self._text = val
    
    # position
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, val):
        val = _validate(_VALIDATE_LABEL, "position", val)
        self._position = val
        
    # ha
    @property
    def ha(self):
        return self._ha

    @ha.setter
    def ha(self, val):
        val = _validate(_VALIDATE_LABEL, "ha", val)
        self._ha = val
        
    # va
    @property
    def va(self):
        return self._va

    @va.setter
    def va(self, val):
        val = _validate(_VALIDATE_LABEL, "va", val)
        self._va = val
    
    # fontsize
    @property
    def fontsize(self):
        return self._fontsize

    @fontsize.setter
    def fontsize(self, val):
        val = _validate(_VALIDATE_LABEL, "fontsize", val)
        self._fontsize = val
    
    # fontfamily
    @property
    def fontfamily(self):
        return self._fontfamily

    @fontfamily.setter
    def fontfamily(self, val):
        val = _validate(_VALIDATE_LABEL, "fontfamily", val)
        self._fontfamily = val
    
    # fontstyle
    @property
    def fontstyle(self):
        return self._fontstyle

    @fontstyle.setter
    def fontstyle(self, val):
        val = _validate(_VALIDATE_LABEL, "fontstyle", val)
        self._fontstyle = val
    
    # color
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        val = _validate(_VALIDATE_LABEL, "color", val)
        self._color = val
    
    # fontweight
    @property
    def fontweight(self):
        return self._fontweight

    @fontweight.setter
    def fontweight(self, val):
        val = _validate(_VALIDATE_LABEL, "fontweight", val)
        self._fontweight = val
    
    # stroke_width
    @property
    def stroke_width(self):
        return self._stroke_width

    @stroke_width.setter
    def stroke_width(self, val):
        val = _validate(_VALIDATE_LABEL, "stroke_width", val)
        self._stroke_width = val
    
    # stroke_color
    @property
    def stroke_color(self):
        return self._stroke_color

    @stroke_color.setter
    def stroke_color(self, val):
        val = _validate(_VALIDATE_LABEL, "stroke_color", val)
        self._stroke_color = val
    
    # rotation
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, val):
        val = _validate(_VALIDATE_LABEL, "rotation", val)
        self._rotation = val
     
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val):
        val = _validate(_VALIDATE_LABEL, "zorder", val)
        self._zorder = val

# Class constructor for the shadow underneath the base of the north arrow (the right hand patch)
class ArrowShadow:
    # Initialization upon first creation
    # Notice that these are all the keys of the _DEFAULT_FANCY dictionary!
    def __init__(self, parent, offset: tuple[float | int, float | int], alpha: float | int, shadow_rgbFace: str):
        self._offset = _validate(_VALIDATE_SHADOW, "offset", offset)
        self._alpha = _validate(_VALIDATE_SHADOW, "alpha", alpha)
        self._shadow_rgbFace = _validate(_VALIDATE_SHADOW, "shadow_rgbFace", shadow_rgbFace)
        self._parent = parent
    
    ## INTERNAL PROPERTIES ##
    # offset
    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, val):
        val = _validate(_VALIDATE_SHADOW, "offset", val)
        self._offset = val
    
    # alpha
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        val = _validate(_VALIDATE_SHADOW, "alpha", val)
        self._alpha = val
     
    # zorder
    @property
    def shadow_rgbFace(self):
        return self._shadow_rgbFace

    @shadow_rgbFace.setter
    def shadow_rgbFace(self, val):
        val = _validate(_VALIDATE_SHADOW, "shadow_rgbFace", val)
        self._shadow_rgbFace = val

### DRAWING FUNCTIONS ###
# These functions take care of the actual drawing of the object!
# You can use them independently of the class-based model
def north_arrow(ax, draw=True,
                base: bool=True, base_style: _TYPE_BASE=_DEFAULT_BASE, 
                fancy: bool=True, fancy_style: _TYPE_FANCY=_DEFAULT_FANCY, 
                label: bool=True, label_style: _TYPE_LABEL=_DEFAULT_LABEL, 
                shadow: bool=True, shadow_style: _TYPE_SHADOW=_DEFAULT_SHADOW,
                packer_style: _TYPE_PACK=_DEFAULT_PACK, aob_style: _TYPE_AOB=_DEFAULT_AOB, rotation_style: _TYPE_ROTATION=_DEFAULT_ROTATION):
    
    # Setting the styles for each component
    # The dict-concatenation ensures we always have SOMETHING available for each necessary attribute
    # But it means any overrides (to color, size, font, etc.) have to be manually specified
    _base_style = _DEFAULT_BASE | base_style
    _fancy_style = _DEFAULT_FANCY | fancy_style
    _label_style = _DEFAULT_LABEL | label_style
    _shadow_style = _DEFAULT_SHADOW | shadow_style
    _packer_style = _DEFAULT_PACK | packer_style
    _aob_style = _DEFAULT_AOB | aob_style
    _rotation_style = _DEFAULT_ROTATION | rotation_style

    # Validating that each element in each dictionary is valid
    for d,v in zip([_base_style, _fancy_style, _label_style, _shadow_style, _packer_style, _aob_style],
                   [_VALIDATE_BASE, _VALIDATE_FANCY, _VALIDATE_LABEL, _VALIDATE_SHADOW, _VALIDATE_PACK, _VALIDATE_AOB]):
        # Getting validate-able keys
        to_validate = [k for k in d.keys() if k in v.keys()]
        # Using our handy-dandy function to validate
        _ = _validate_dict(d, v, to_validate)
    
    # First, getting the figure for our axes
    fig = ax.get_figure()
    
    # We will place the arrow components in an AuxTransformBox so they are scaled in inches
    # Props to matplotlib-scalebar
    scale_box = matplotlib.offsetbox.AuxTransformBox(fig.dpi_scale_trans)

    ## BASE ARROW ##
    # Because everything is dependent on this component, it ALWAYS exists
    # However, if we don't want it (base=False), then we'll hide it
    base_artist = matplotlib.patches.Polygon(_base_style["coords"] * _base_style["scale"], closed=True, visible=base, **_del_keys(_base_style, ["coords","scale","location","rotation","crs","rotation_ref"]))

    ## ARROW SHADOW ##
    # This is not its own artist, but instead just something we modify about the base artist using a path effect
    if shadow==True:
        base_artist.set_path_effects([matplotlib.patheffects.withSimplePatchShadow(**_shadow_style)])
    
    # With our base arrow "done", we can add it to scale_box
    scale_box.add_artist(base_artist)
    
    ## FANCY ARROW ##
    # If we want the fancy extra patch, we need another artist
    if fancy==True:
        # Note that here, unfortunately, we are reliant on the scale attribute from the base arrow
        fancy_artist = matplotlib.patches.Polygon(_fancy_style["coords"] * _base_style["scale"], closed=True, visible=fancy, **_del_keys(_fancy_style, ["coords"]))
        # It is also added to the scale_box so it is scaled in-line
        scale_box.add_artist(fancy_artist)
    
    ## LABEL ##
    # The final artist is for the label
    if label==True:
        # Correctly constructing the textprops dict for the label
        text_props = _del_keys(_label_style, ["text","position","stroke_width","stroke_color"])
        # If we have stroke settings, create a path effect for them
        if _label_style["stroke_width"] > 0:
            label_stroke = [matplotlib.patheffects.withStroke(linewidth=_label_style["stroke_width"], foreground=_label_style["stroke_color"])]
            text_props["path_effects"] = label_stroke
        # This one is not added to the scale box, as that is handled on its own
        # Also, the dictionary does not need to be unpacked, textprops does that for us
        label_box = matplotlib.offsetbox.TextArea(_label_style["text"], textprops=text_props)

    ## STACKING THE ARTISTS ##
    # If we have multiple artists, we need to stack them using a V or H packer
    if label==True and (base==True or fancy==True):
        if _label_style["position"]=="top":
            pack_box = matplotlib.offsetbox.VPacker(children=[label_box, scale_box], **_packer_style)
        elif _label_style["position"]=="bottom":
            pack_box = matplotlib.offsetbox.VPacker(children=[scale_box, label_box], **_packer_style)
        elif _label_style["position"]=="left":
            pack_box = matplotlib.offsetbox.HPacker(children=[label_box, scale_box], **_packer_style)
        elif _label_style["position"]=="right":
            pack_box = matplotlib.offsetbox.HPacker(children=[scale_box, label_box], **_packer_style)
        else:
            raise Exception("Invalid position applied, try one of 'top', 'bottom', 'left', 'right'")
    # If we only have the base, then that's the only thing we'll add to the box
    else:
        pack_box = matplotlib.offsetbox.VPacker(children=[scale_box], **_packer_style)
    
    ## CREATING THE OFFSET BOX ##
    # The AnchoredOffsetBox allows us to place the pack_box relative to our axes
    # Note that the position string (upper left, lower right, center, etc.) comes from the base arrow
    aob_box = matplotlib.offsetbox.AnchoredOffsetbox(loc=_base_style["location"], child=pack_box, **_del_keys(_aob_style, ["facecolor","edgecolor","alpha"]))
    # Also setting the facecolor and transparency of the box
    if _aob_style["facecolor"] is not None:
        aob_box.patch.set_facecolor(_aob_style["facecolor"])
        aob_box.patch.set_visible(True)
    if _aob_style["edgecolor"] is not None:
        aob_box.patch.set_edgecolor(_aob_style["edgecolor"])
        aob_box.patch.set_visible(True)
    if _aob_style["alpha"]:
        aob_box.patch.set_alpha(_aob_style["alpha"])
        aob_box.patch.set_visible(True)
    
    ## ROTATING THE ARROW ##
    # If no rotation amount is passed, (attempt to) calculate it
    if _rotation_style["degrees"] is None:
        rotate_deg = _rotate_arrow(ax, _rotation_style)
    else:
        rotate_deg = _rotation_style["degrees"]
    # Then, apply the rotation to the aob box
    _iterative_rotate(aob_box, rotate_deg)
    
    ## DRAWING ##
    # If this option is set to true, we'll draw the final artists as desired
    if draw==True:
        ax.add_artist(aob_box)
    # If not, we'll return the aob_box as an object
    else:
        return aob_box

# This function calculates the desired rotation of the arrow
def _rotate_arrow(ax, rotate_dict) -> float | int:
    crs = rotate_dict["crs"]
    ref = rotate_dict["reference"]
    crd = rotate_dict["coords"] # should be (x,y) for axis ref, (lat,lng) for data ref

    ## CONVERTING FROM AXIS TO DATA COORDAINTES ##
    # If reference is set to axis, need to convert the axis coordinates (ranging from 0 to 1) to data coordinates (in native crs)
    if ref=="axis":
        # the transLimits transformation is for converting between data and axes units
        # so this code gets us the data (geographic) units of the chosen axis coordinates
        reference_point = ax.transLimits.inverted().transform((crd[0], crd[1]))
    # If reference is set to center, then do the same thing, but use the midpoint of the axis by default
    elif ref=="center":
        reference_point = ax.transLimits.inverted().transform((0.5,0.5))
    # Finally if the reference is set to data, we assume the provided coordinates are already in data units, no transformation needed!
    elif ref=="data":
        reference_point = crd
    
    ## CONVERTING TO GEODETIC COORDINATES ##
    # Initializing a CRS, so we can transform between coordinate systems appropriately
    if type(crs) == pyproj.CRS:
        og_proj = cartopy.crs.CRS(crs)
    else:
        try:
            og_proj = cartopy.crs.CRS(pyproj.CRS(crs))
        except:
            raise Exception("Invalid CRS Supplied")
    # Converting to the geodetic version of the CRS supplied
    gd_proj = og_proj.as_geodetic()
    # Converting reference point to the geodetic system
    reference_point_gd = gd_proj.transform_point(reference_point[0], reference_point[1], og_proj)
    # Converting the coordinates BACK to the original system
    reference_point = og_proj.transform_point(reference_point_gd[0], reference_point_gd[1], gd_proj)
    # And adding an offset to find "north", relative to that
    north_point = og_proj.transform_point(reference_point_gd[0], reference_point_gd[1] + 0.01, gd_proj)
    
    ## CALCULATING THE ANGLE ##
    # numpy.arctan2 wants coordinates in (y,x) because it flips them when doing the calculation
    # i.e. the angle found is between the line segment ((0,0), (1,0)) and ((0,0), (b,a)) when calling numpy.arctan2(a,b)
    try:
        rad = -1 * numpy.arctan2(north_point[0] - reference_point[0], north_point[1] - reference_point[1])
    except:
        warnings.warn("Unable to calculate rotation of arrow, setting to 0 degrees")
        rad = 0
    # Converting radians to degrees
    deg = math.degrees(rad)
    print(deg)
    # Returning the degree number
    return deg

# Unfortunately, matplotlib doesn't allow AnchoredOffsetBoxes or V/HPackers to have a rotation transformation
# So, we have to set it on the individual child objects (namely the base arrow and fancy arrow patches)
def _iterative_rotate(artist, deg):
    # Building the affine rotation transformation
    transform_rotation = matplotlib.transforms.Affine2D().rotate_deg(deg)
    artist.set_transform(transform_rotation + artist.get_transform())
    if artist.get_children():
        for child in artist.get_children():
            _iterative_rotate(child, deg)

### HELPING FUNTIONS ###
# These are quick functions we use to help in other parts of this process

# This function will handle updating setter functions
def _obj_setter(oself, oval, nval, ostyle):
        # If we currently DON'T have this object, and set it to true, we need to create it
        # We can leverage the current _style dict to create it
        if oval==False and nval==True:
            return ArrowBase(oself, **ostyle)
        # If we currently have this object, but set it to false, we need to delete it
        elif oval and nval==False:
            return nval
        # If things stay the same, no need to do anything at all
        else:
            return oself

# This function will remove any keys we specify from a dictionary
# This is useful if we need to unpack on certain values from a dictionary!
def _del_keys(dict, to_remove):
    return {key: val for key, val in dict.items() if key not in to_remove}

# This function takes in a class, and returns its attribute dictionary
# The dictionary also has all of its leading underscores removed
def _class_dict(obj, to_remove=None):
    # Note that we wrap this in a try/except
    # For the cases where we just have a False instead of an initialized class
    try:
        dict = obj.__dict__
        clean = {key[1:]: val for key, val in dict.items()}
        if to_remove:
            clean = _del_keys(clean, to_remove)
        return clean
    except:
        return {}

# This function just returns true/false depending on if the object exists
def _draw_obj(obj):
    if obj == False:
        return False
    else:
        return True

### VALIDITY CHECKERS ###
# Functions and variables used for validating inputs for classes
def _validate_list(prop, val, list, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value in this list: {list}")
    elif none_ok==True and val is None:
        return val
    elif not val in list:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value in this list: {list}")
    return val

def _validate_range(prop, val, min, max, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif none_ok==True and val is None:
        return val
    elif max is not None:
        if not val >= min and not val <= max:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif max is None:
        if not val >= min:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value greater than {min}")
    return val

def _validate_type(prop, val, match, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {match}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==match:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {match}")
    return val

def _validate_coords(prop, val, numpy_type, dims, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==numpy_type:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif not val.ndim==dims:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a numpy array with {dims} dimensions")
    return val

def _validate_tuple(prop, val, length, types, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif none_ok==True and val is None:
        return val
    elif type(val)!=tuple:
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif len(val)!=length:
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    else:
        for item in val:
            if type(item) not in types:
                raise ValueError(f"{type(item)} is not a valid value for the items in {prop}, please provide a value of one of the following types: {types}")
    return val

def _validate_color_or_none(prop, val, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a color string acceptable to matplotlib instead")
    elif none_ok==True and val is None:
        return val
    else:
        matplotlib.rcsetup.validate_color(val)
    return val

# NOTE: This one is a bit messy, particularly with the rotation module, but I can't think of a better way to do it...
def _validate_crs(prop, val, rotation_dict, none_ok=False):
    degrees = rotation_dict.get("degrees",None)
    crs = rotation_dict.get("crs",None)
    reference = rotation_dict.get("reference",None)
    coords = rotation_dict.get("coords",None)
    print(degrees, crs, reference, coords)
    if degrees is None:
        if crs is None or reference is None or coords is None:
            raise ValueError(f"If degrees is set to None, then crs, reference, and coords cannot be None: please provide a valid input for each of these variables instead")
    elif (type(degrees)==int or type(degrees)==float) and (crs is None or reference is None or coords is None):
            warnings.warn(f"A value for rotation was supplied; values for crs, reference, and coords will be ignored")
            return val
    else:
        if none_ok==False and val is None:
            raise ValueError(f"If rotation is set to None, then {prop} cannot be None: please provide a valid CRS input for PyProj instead")
        elif none_ok==True and val is None:
            return val
    # This happens if (a) a value for CRS is supplied and (b) a value for degrees is NOT supplied
    if type(val)==pyproj.CRS:
        pass
    else:
        try:
            val = pyproj.CRS.from_user_input(val)
        except:
            raise Exception(f"Invalid CRS supplied ({val}), please provide a valid CRS input for PyProj instead")
    return val

## Set-up for each dictionary's specific validation rules

_VALID_BASE_LOCATIONS = get_args(_TYPE_BASE.__annotations__["location"])

_VALIDATE_BASE = {
    "coords":{"func":_validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "location":{"func":_validate_list, "kwargs":{"list":_VALID_BASE_LOCATIONS}}, # can be https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html (see: loc)
    "scale":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "edgecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "linewidth":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_FANCY = {
    "coords":{"func":_validate_coords, "kwargs":{"numpy_type":numpy.ndarray, "dims":2}}, # must be 2D numpy array
    "facecolor":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALID_LABEL_POSITION = get_args(_TYPE_LABEL.__annotations__["position"])
_VALID_LABEL_HA = get_args(_TYPE_LABEL.__annotations__["ha"])
_VALID_LABEL_VA = get_args(_TYPE_LABEL.__annotations__["va"])
_VALID_LABEL_FONTFAMILY = get_args(_TYPE_LABEL.__annotations__["fontfamily"])
_VALID_LABEL_FONTSTYLE = get_args(_TYPE_LABEL.__annotations__["fontstyle"])
_VALID_LABEL_FONTWEIGHT = get_args(_TYPE_LABEL.__annotations__["fontweight"])

_VALIDATE_LABEL = {
    "text":{"func":_validate_type, "kwargs":{"match":str}}, # any string
    "position":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_POSITION}},
    "ha":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_HA}},
    "va":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_VA}},
    "fontsize":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "fontfamily":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_FONTFAMILY}},
    "fontstyle":{"func":_validate_list, "kwargs":{"list":_VALID_LABEL_FONTSTYLE}},
    "color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "fontweight":{"func":matplotlib.rcsetup.validate_fontweight}, # any fontweight value for matplotlib
    "stroke_width":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "stroke_color":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
    "rotation":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "zorder":{"func":_validate_type, "kwargs":{"match":int}} # any integer
}

_VALIDATE_SHADOW = {
    "offset":{"func":_validate_tuple, "kwargs":{"length":2, "types":[float, int]}},
    "alpha":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "shadow_rgbFace":{"func":matplotlib.rcsetup.validate_color}, # any color value for matplotlib
}

_VALID_PACK_ALIGN = get_args(_TYPE_PACK.__annotations__["align"])
_VALID_PACK_MODE = get_args(_TYPE_PACK.__annotations__["mode"])

_VALIDATE_PACK = {
    "sep":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "align":{"func":_validate_list, "kwargs":{"list":_VALID_PACK_ALIGN}},
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "width":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "height":{"func":_validate_range, "kwargs":{"min":0, "max":None, "none_ok":True}}, # between 0 and inf
    "mode":{"func":_validate_list, "kwargs":{"list":_VALID_PACK_MODE}}
}

_VALIDATE_AOB = {
    "facecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "edgecolor":{"func":_validate_color_or_none, "kwargs":{"none_ok":True}}, # any color value for matplotlib OR NONE
    "alpha":{"func":_validate_range, "kwargs":{"min":0, "max":1, "none_ok":True}}, # any value between 0 and 1
    "pad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "borderpad":{"func":_validate_range, "kwargs":{"min":0, "max":None}}, # between 0 and inf
    "prop":{"func":matplotlib.rcsetup.validate_fontsize}, # any fontsize value for matplotlib
    "frameon":{"func":_validate_type, "kwargs":{"match":bool}}, # any bool
    # "bbox_to_anchor":None, # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
    # "bbox_transform":None # TODO: Currently unvalidated! Make sure to remove from _validate_dict once updated!
}

_VALID_ROTATION_REFERENCE = get_args(_TYPE_ROTATION.__annotations__["reference"])

_VALIDATE_ROTATION = {
    "degrees":{"func":_validate_range, "kwargs":{"min":-360, "max":360, "none_ok":True}}, # anything between -360 and 360, or None for "auto"
    "crs":{"func":_validate_crs, "kwargs":{"none_ok":True}}, # see _validate_crs for details on what is accepted
    "reference":{"func":_validate_list, "kwargs":{"list":_VALID_ROTATION_REFERENCE, "none_ok":True}}, # see _VALID_ROTATION_REFERENCE for accepted values
    "coords":{"func":_validate_tuple, "kwargs":{"length":2, "types":[float, int], "none_ok":True}} # only required if degrees is None: should be a tuple of coordinates in the relevant reference window
}

# This function can process the _VALIDATE dictionaries we established above
def _validate_dict(values, functions, to_validate: list=None, return_clean=False):
    # Pre-checking that no invalid keys are passed
    invalid = [key for key in values.keys() if key not in functions.keys() and key not in ["bbox_to_anchor", "bbox_transform"]]
    if len(invalid) > 0:
        print(f"Warning: Invalid keys detected ({invalid}). These will be ignored.")
    # First, trimming our values to only those we need to validate
    if to_validate is not None:
        values = {key: val for key, val in values.items() if key in to_validate}
        functions = {key: val for key, val in functions.items() if key in values.keys()}
    else:
        values = {key: val for key, val in values.items() if key in functions.keys()}
        functions = {key: val for key, val in functions.items() if key in values.keys()}
    # Now, running the function with the necessary kwargs
    for key,val in values.items():
        fd = functions[key]
        func = fd["func"]
        # NOTE: This is messy but the only way to get the rotation value to the crs function
        if key=="crs":
            _ = func(prop=key, val=val, rotation_dict=values, **fd["kwargs"])
        # Our custom functions always have this dictionary key in them, so we know what form they take
        elif "kwargs" in fd:
            _ = func(prop=key, val=val, **fd["kwargs"])
        # The matplotlib built-in functions DON'T have that, and only ever take the one value
        else:
            _ = func(val)
    if return_clean==True:
        return values

# This function can process the _VALIDATE dictionaries we established above, but for single variables at a time
def _validate(validate_dict, prop, val, return_val=True, kwargs={}):
    fd = validate_dict[prop]
    func = fd["func"]
    # Our custom functions always have this dictionary key in them, so we know what form they take
    if "kwargs" in fd:
        val = func(prop=prop, val=val, **(fd["kwargs"] | kwargs))
    # The matplotlib built-in functions DON'T have that, and only ever take the one value
    else:
        val = func(val)
    if return_val==True:
        return val