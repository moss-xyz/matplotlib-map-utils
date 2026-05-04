############################################################
# north_arrow.py contains all the main objects and functions
# for creating the north arrow artist rendered to plots
############################################################

### IMPORTING PACKAGES ###

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
import matplotlib.artist
import matplotlib.patches
import matplotlib.patheffects
import matplotlib.offsetbox
# The types we use in this script
from typing import Literal
# The information contained in our helper scripts (validation and defaults)
from .. import config
from ..validation import north_arrow as nat

### CLASSES ###

# The main object model of the north arrow
# Note that, except for location, all the components for the artist are dictionaries
# These can be accessed and updated with dot notation (like NorthArrow.base)
class NorthArrow(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self, size: str=None, location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right",
                       scale: None | float | int=None,
                       base: None | bool | dict = None, fancy: None | bool | dict = None, 
                       label: None | bool | dict = None, shadow: None | bool | dict = None, 
                       pack: None | dict = None, aob: None | dict = None, rotation: None | dict = None,
                       zorder: int=99,):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # If a dictionary is passed to any of the elements, validate that it is "correct", and then store the information
        # Note that we also merge the provided dict with the default style dict, so no keys are missing
        # If a specific component is not desired, it should be set to False during initialization

        # Location is stored as just a string
        self._size = size if size is not None else config.DEFAULT_SIZE
        primary = nat.NorthArrowPrimaryModel(location=location, zorder=zorder, scale=scale, size=self._size)
        self._location = primary.location
        self._zorder = primary.zorder
        self._scale = primary.scale
        
        def _build(model, input_val):
            if input_val is False: return False
            data = input_val.copy() if isinstance(input_val, dict) else {}
            data['size'] = self._size
            return model(**data).model_dump()

        # Main elements
        self._base = _build(nat.NorthArrowBaseModel, base)
        self._fancy = _build(nat.NorthArrowFancyModel, fancy)
        self._label = _build(nat.NorthArrowLabelModel, label)
        self._shadow = _build(nat.NorthArrowShadowModel, shadow)

        # Other properties
        self._pack = _build(nat.NorthArrowPackModel, pack)
        self._aob = _build(nat.NorthArrowAobModel, aob)
        self._rotation = _build(nat.NorthArrowRotationModel, rotation)

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of properties
    # Each property will have the same pair of functions
    # 1) calling the property itself returns its dictionary (NorthArrow.base will output {...})
    # 2) passing a dictionary will update key values (NorthArrow.base = {...} will update present keys)

    # location/loc
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        self._location = nat.NorthArrowPrimaryModel(location=val, scale=self._scale if self._scale is not None else 0, zorder=self._zorder).location
    
    @property
    def loc(self):
        return self._location

    @loc.setter
    def loc(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        self._location = nat.NorthArrowPrimaryModel(location=val, scale=self._scale if self._scale is not None else 0, zorder=self._zorder).location

    # scale
    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val: float | int):
        self._scale = nat.NorthArrowPrimaryModel(location=self._location, scale=val, zorder=self._zorder, size=self._size).scale

    # base
    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, val: dict):
        if val is False: self._base = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._base = nat.NorthArrowBaseModel.model_validate(data).model_dump()
    
    # fancy
    @property
    def fancy(self):
        return self._fancy

    @fancy.setter
    def fancy(self, val: dict):
        if val is False: self._fancy = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._fancy = nat.NorthArrowFancyModel.model_validate(data).model_dump()
    
    # label
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val: dict):
        if val is False: self._label = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._label = nat.NorthArrowLabelModel.model_validate(data).model_dump()
    
    # shadow
    @property
    def shadow(self):
        return self._shadow

    @shadow.setter
    def shadow(self, val: dict):
        if val is False: self._shadow = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._shadow = nat.NorthArrowShadowModel.model_validate(data).model_dump()
    
    # pack
    @property
    def pack(self):
        return self._pack

    @pack.setter
    def pack(self, val: dict):
        if val is False: self._pack = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._pack = nat.NorthArrowPackModel.model_validate(data).model_dump()
    
    # aob
    @property
    def aob(self):
        return self._aob

    @aob.setter
    def aob(self, val: dict):
        if val is False: self._aob = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._aob = nat.NorthArrowAobModel.model_validate(data).model_dump()
    
    # rotation
    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, val: dict):
        if val is False: self._rotation = False
        else:
            data = val.copy() if isinstance(val, dict) else {}
            data['size'] = self._size
            self._rotation = nat.NorthArrowRotationModel.model_validate(data).model_dump()

    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val: int):
        self._zorder = nat.NorthArrowPrimaryModel(location=self._location, scale=self._scale if self._scale is not None else 0, zorder=val, size=self._size).zorder
    
    ## COPY FUNCTION ##
    # This is solely to get around matplotlib's restrictions around re-using an artist across multiple axes
    # Instead, you can use add_artist() like normal, but with add_artist(na.copy())
    # Thank you to the cartopy team for helping fix a bug with this!
    def copy(self):
        return copy.deepcopy(self)

    ## DRAW FUNCTION ##
    # Calling ax.add_artist() on this object triggers the following draw() function
    # THANK YOU to matplotlib-scalebar for figuring this out
    # Note that we never specify the renderer - the axis takes care of it!
    def draw(self, renderer, *args, **kwargs):
        # Can re-use the drawing function we already established, but return the object instead
        na_artist = north_arrow(ax=self.axes, location=self._location, scale=self._scale, draw=False,
                                base=self._base, fancy=self._fancy,
                                label=self._label, shadow=self._shadow,
                                pack=self._pack, aob=self._aob, rotation=self._rotation,
                                zorder=self._zorder)
        # This handles the actual drawing
        na_artist.axes = self.axes
        na_artist.set_figure(self.axes.get_figure())
        na_artist.set_zorder(self._zorder)
        na_artist.draw(renderer)
    
    ## SIZE FUNCTION ##
    # This function will update the default dictionaries used based on the size of map being created
    # See defaults.py for more information on the dictionaries used here
    def set_size(size: Literal["xs","xsmall","x-small",
                               "sm","small",
                               "md","medium",
                               "lg","large",
                               "xl","xlarge","x-large"]):
        pass

### DRAWING FUNCTIONS ###

# This function presents a way to draw the north arrow independent of the NorthArrow object model
# and is actually used by the object model when draw() is called anyways
def north_arrow(ax, draw=True, size: str=None, location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right",
                scale: None | float | int=None,
                base: None | bool | dict=None, 
                fancy: None | bool | dict=None,
                label: None | bool | dict=None, 
                shadow: None | bool | dict=None,
                pack: None | dict=None, 
                aob: None | dict=None, 
                rotation: None | dict=None,
                zorder: int=99,):
    
    if draw==True:
        na_obj = NorthArrow(size=size, location=location, scale=scale, base=base, fancy=fancy, label=label, shadow=shadow, pack=pack, aob=aob, rotation=rotation, zorder=zorder)
        return ax.add_artist(na_obj)
    
    # First, validating the three primary inputs
    primary = nat.NorthArrowPrimaryModel(location=location, zorder=zorder, scale=scale if scale is not None else 0, size=size if size is not None else config.DEFAULT_SIZE)
    _location = primary.location
    _zorder = primary.zorder
    _scale = primary.scale
    _size = primary.size

    # This works the same as it does with the NorthArrow object
    # If a dictionary is passed to any of the elements, first validate that it is "correct"
    # Note that we also merge the provided dict with the default style dict, so no keys are missing
    # If a specific component is not desired, it should be set to False in the function call
    def _build(model, input_val):
        if input_val is False: return False
        data = input_val.copy() if isinstance(input_val, dict) else {}
        data['size'] = _size
        return model(**data).model_dump()

    _base = _build(nat.NorthArrowBaseModel, base)
    _fancy = _build(nat.NorthArrowFancyModel, fancy)
    _label = _build(nat.NorthArrowLabelModel, label)
    _shadow = _build(nat.NorthArrowShadowModel, shadow)
    _pack = _build(nat.NorthArrowPackModel, pack)
    _aob = _build(nat.NorthArrowAobModel, aob)
    _rotation = _build(nat.NorthArrowRotationModel, rotation)
    
    # First, getting the figure for our axes
    fig = ax.get_figure()
    
    # We will place the arrow components in an AuxTransformBox so they are scaled in inches
    # Props to matplotlib-scalebar
    scale_box = matplotlib.offsetbox.AuxTransformBox(fig.dpi_scale_trans)

    ## BASE ARROW ##
    # Because everything is dependent on this component, it ALWAYS exists
    # However, if we don't want it (base=False), then we'll hide it
    if _base == False:
        _fallback = _build(nat.NorthArrowBaseModel, {})
        base_artist = matplotlib.patches.Polygon(_fallback["coords"] * _scale, closed=True, visible=False, **_del_keys(_fallback, ["coords","scale"]))
    else:
        base_artist = matplotlib.patches.Polygon(_base["coords"] * _scale, closed=True, visible=True, **_del_keys(_base, ["coords","scale"]))

    ## ARROW SHADOW ##
    # This is not its own artist, but instead just something we modify about the base artist using a path effect
    if _shadow:
        base_artist.set_path_effects([matplotlib.patheffects.withSimplePatchShadow(**_shadow)])
    
    # With our base arrow "done", we can add it to scale_box
    # which transforms our coordinates, multiplied by the scale factor, to inches
    # so a line from (0,0) to (0,1) would be 1 inch long, and from (0,0) to (0,0.5) half an inch, etc.
    scale_box.add_artist(base_artist)
    
    ## FANCY ARROW ##
    # If we want the fancy extra patch, we need another artist
    if _fancy:
        # Note that here, unfortunately, we are reliant on the scale attribute from the base arrow
        fancy_artist = matplotlib.patches.Polygon(_fancy["coords"] * _scale, closed=True, visible=bool(_fancy), **_del_keys(_fancy, ["coords"]))
        # It is also added to the scale_box so it is scaled in-line
        scale_box.add_artist(fancy_artist)
    
    ## LABEL ##
    # The final artist is for the label
    if _label:
        # Correctly constructing the textprops dict for the label
        text_props = _del_keys(_label, ["text","position","stroke_width","stroke_color"])
        # If we have stroke settings, create a path effect for them
        if _label["stroke_width"] > 0:
            label_stroke = [matplotlib.patheffects.withStroke(linewidth=_label["stroke_width"], foreground=_label["stroke_color"])]
            text_props["path_effects"] = label_stroke
        # The label is not added to scale_box, it lives in its own TextArea artist instead
        # Also, the dictionary does not need to be unpacked, textprops does that for us
        label_box = matplotlib.offsetbox.TextArea(_label["text"], textprops=text_props)

    ## STACKING THE ARTISTS ##
    # If we have multiple artists, we need to stack them using a V or H packer
    if _label and (_base or _fancy):
        if _label["position"]=="top":
            pack_box = matplotlib.offsetbox.VPacker(children=[label_box, scale_box], **_pack)
        elif _label["position"]=="bottom":
            pack_box = matplotlib.offsetbox.VPacker(children=[scale_box, label_box], **_pack)
        elif _label["position"]=="left":
            pack_box = matplotlib.offsetbox.HPacker(children=[label_box, scale_box], **_pack)
        elif _label["position"]=="right":
            pack_box = matplotlib.offsetbox.HPacker(children=[scale_box, label_box], **_pack)
        else:
            raise Exception("Invalid position applied, try one of 'top', 'bottom', 'left', 'right'")
    # If we only have the base, then that's the only thing we'll add to the box
    # I keep this in a VPacker just so that the rest of the code is functional, and doesn't depend on a million if statements
    else:
        pack_box = matplotlib.offsetbox.VPacker(children=[scale_box], **_pack)
    
    ## CREATING THE OFFSET BOX ##
    # The AnchoredOffsetBox allows us to place the pack_box relative to our axes
    # Note that the position string (upper left, lower right, center, etc.) comes from the location variable
    aob_box = matplotlib.offsetbox.AnchoredOffsetbox(loc=_location, child=pack_box, **_del_keys(_aob, ["facecolor","edgecolor","alpha"]))
    # Also setting the facecolor and transparency of the box
    if _aob["facecolor"] is not None:
        aob_box.patch.set_facecolor(_aob["facecolor"])
        aob_box.patch.set_visible(True)
    if _aob["edgecolor"] is not None:
        aob_box.patch.set_edgecolor(_aob["edgecolor"])
        aob_box.patch.set_visible(True)
    if _aob["alpha"]:
        aob_box.patch.set_alpha(_aob["alpha"])
        aob_box.patch.set_visible(True)
    
    ## ROTATING THE ARROW ##
    # If no rotation amount is passed, (attempt to) calculate it
    if _rotation["degrees"] is None:
        rotate_deg = _rotate_arrow(ax, _rotation)
    else:
        rotate_deg = _rotation["degrees"]
    # Then, apply the rotation to the aob box
    _iterative_rotate(aob_box, rotate_deg)

    aob_box.set_zorder(_zorder)
    return aob_box

### HELPING FUNTIONS ###
# These are quick functions we use to help in other parts of this process

# This function calculates the desired rotation of the arrow
# It uses 3 pieces of information: the CRS, the reference frame, and the coordinates of the reference point
# This code is 100% inspired by EOMaps, who also answered my questions about the inner workings of their equiavlent functions
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

    # Returning the degree number
    return deg

# Unfortunately, matplotlib doesn't allow AnchoredOffsetBoxes or V/HPackers to have a rotation transformation (why? No idea)
# So, we have to set it on the individual child objects (namely the base arrow and fancy arrow patches)
def _iterative_rotate(artist, deg):
    # Building the affine rotation transformation
    transform_rotation = matplotlib.transforms.Affine2D().rotate_deg(deg)
    artist.set_transform(transform_rotation + artist.get_transform())
    # Repeating the process if there is a child component
    if artist.get_children():
        for child in artist.get_children():
            _iterative_rotate(child, deg)

# This function will remove any keys we specify from a dictionary
# This is useful if we need to unpack on certain values from a dictionary, and is used in north_arrow()
def _del_keys(dict, to_remove):
    return {key: val for key, val in dict.items() if key not in to_remove}