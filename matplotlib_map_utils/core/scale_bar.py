############################################################
# scale_bar.py contains all the main objects and functions
# for creating the scale bar artist rendered to plots
############################################################

### IMPORTING PACKAGES ###

# Default packages
import warnings
import math
import copy
# Math packages
import numpy
# Geo packages
import pyproj
from great_circle_calculator.great_circle_calculator import distance_between_points
# Graphical packages
import PIL.Image
import matplotlib.artist
import matplotlib.lines
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.patheffects
import matplotlib.offsetbox
import matplotlib.font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg
# The types we use in this script
from typing import Literal
# The information contained in our helper scripts (validation and defaults)
from ..defaults import scale_bar as sbd
from ..validation import scale_bar as sbt
from ..validation import functions as sbf

### INIT ###

_DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["md"]


### CLASSES ###

class ScaleBar(matplotlib.artist.Artist):
    
    ## INITIALIZATION ##
    def __init__(self, style: Literal["ticks","boxes"]="boxes",
                       location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right",
                       bar: None | bool | sbt._TYPE_BAR=None,
                       units: None | bool | sbt._TYPE_UNITS=None,
                       labels: None | bool | sbt._TYPE_LABELS=None,
                       text: None | bool | sbt._TYPE_TEXT=None,
                       aob: None | bool | sbt._TYPE_AOB=None,
                       zorder: int=99,
                       ):
        # Starting up the object with the base properties of a matplotlib Artist
        matplotlib.artist.Artist.__init__(self)
        
        # If a dictionary is passed to any of the elements, validate that it is "correct", and then store the information
        # Note that we also merge the provided dict with the default style dict, so no keys are missing
        # If a specific component is not desired, it should be set to False during initialization

        ##### VALIDATING #####
        style = sbf._validate(sbt._VALIDATE_PRIMARY, "style", style)
        self._style = style

        # Location is stored as just a string
        location = sbf._validate(sbt._VALIDATE_PRIMARY, "location", location)
        self._location = location

        zorder = sbf._validate(sbt._VALIDATE_PRIMARY, "zorder", zorder)
        self._zorder = zorder
        
        # Shared elements for both ticked and boxed bars
        # This validation is dependent on the type of bar we are constructing
        # So we modify the validation dictionary to remove the keys that are not relevant (throwing a warning if they exist in the input)
        if self._style == "boxes":
            bar = sbf._validate_dict(bar, _del_keys(_DEFAULT_BAR, ["minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]), 
                                                      _del_keys(sbt._VALIDATE_BAR, ["minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]), return_clean=True, to_validate="input")
        else:
            bar = sbf._validate_dict(bar, _del_keys(_DEFAULT_BAR, ["facecolors","edgecolors","edgewidth"]), 
                                                      _del_keys(sbt._VALIDATE_BAR, ["facecolors","edgecolors","edgewidth"]), return_clean=True, to_validate="input")
        self._bar = bar

        units = sbf._validate_dict(units, _DEFAULT_UNITS, sbt._VALIDATE_UNITS, return_clean=True, to_validate="input")
        self._units = units

        labels = sbf._validate_dict(labels, _DEFAULT_LABELS, sbt._VALIDATE_LABELS, return_clean=True, to_validate="input")
        self._labels = labels

        text = sbf._validate_dict(text, _DEFAULT_TEXT, sbt._VALIDATE_TEXT, return_clean=True, to_validate="input")
        self._text = text

        aob = sbf._validate_dict(aob, _DEFAULT_AOB, sbt._VALIDATE_AOB, return_clean=True, to_validate="input")
        self._aob = aob

    ## INTERNAL PROPERTIES ##
    # This allows for easy-updating of properties
    # Each property will have the same pair of functions
    # 1) calling the property itself returns its dictionary (ScaleBar.bar will output {...})
    # 2) passing a dictionary will update key values (ScaleBar.bar = {...} will update present keys)

    # style
    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, val: Literal["boxes","ticks"]):
        val = sbf._validate(sbt._VALIDATE_PRIMARY, "style", val)
        self._style = val

    # location/loc
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        val = sbf._validate(sbt._VALIDATE_PRIMARY, "location", val)
        self._location = val
    
    @property
    def loc(self):
        return self._location

    @loc.setter
    def loc(self, val: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]):
        val = sbf._validate(sbt._VALIDATE_PRIMARY, "location", val)
        self._location = val

    # bar
    @property
    def bar(self):
        return self._bar

    @bar.setter
    def bar(self, val: dict):
        val = sbf._validate_type("bar", val, dict)
        if self._style == "boxes":
            val = sbf._validate_dict(val, self._bar, _del_keys(sbt._VALIDATE_BAR, ["minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]), return_clean=True, parse_false=False)
        else:
            val = sbf._validate_dict(val, self._bar, _del_keys(sbt._VALIDATE_BAR, ["facecolors","edgecolors","edgewidth"]), return_clean=True, parse_false=False)
        self._bar = val
    
    # units
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, val: dict):
        val = sbf._validate_type("units", val, dict)
        val = sbf._validate_dict(val, self._units, sbt._VALIDATE_UNITS, return_clean=True, parse_false=False)
        self._units = val
    
    # labels
    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, val: dict):
        val = sbf._validate_type("labels", val, dict)
        val = sbf._validate_dict(val, self._labels, sbt._VALIDATE_LABELS, return_clean=True, parse_false=False)
        self._labels = val
    
    # text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val: dict):
        val = sbf._validate_type("text", val, dict)
        val = sbf._validate_dict(val, self._text, sbt._VALIDATE_TEXT, return_clean=True, parse_false=False)
        self._text = val
    
    # aob
    @property
    def aob(self):
        return self._aob

    @aob.setter
    def aob(self, val: dict):
        val = sbf._validate_type("aob", val, dict)
        val = sbf._validate_dict(val, self._aob, sbt._VALIDATE_AOB, return_clean=True, parse_false=False)
        self._aob = val
    
    # zorder
    @property
    def zorder(self):
        return self._zorder

    @zorder.setter
    def zorder(self, val: int):
        val = sbf._validate(sbt._VALIDATE_PRIMARY, "zorder", val)
        self._zorder = val
    
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
        # Prefer renderer dpi for class-based artists so exports stay sharp
        # when savefig(dpi=...) differs from the figure construction dpi.
        _bar = copy.deepcopy(self._bar)
        if _bar.get("raster_dpi", None) is None:
            _raster_dpi, _ = _resolve_raster_dpi(
                _bar, self.axes.get_figure(), renderer=renderer
            )
            _bar["raster_dpi"] = _raster_dpi
        # Can re-use the drawing function we already established, but return the object instead
        sb_artist = scale_bar(ax=self.axes, style=self._style, location=self._location, draw=False,
                                    bar=_bar, units=self._units,
                                    labels=self._labels, text=self._text, aob=self._aob,
                                    zorder=self._zorder)
        # This handles the actual drawing
        sb_artist.axes = self.axes
        sb_artist.set_figure(self.axes.get_figure())
        sb_artist.set_zorder(self._zorder)
        sb_artist.draw(renderer)
    
    ## SIZE FUNCTION ##
    # This function will update the default dictionaries used based on the size of map being created
    # See defaults_sb.py for more information on the dictionaries used here
    def set_size(size: Literal["xs","xsmall","x-small",
                               "sm","small",
                               "md","medium",
                               "lg","large",
                               "xl","xlarge","x-large"]):
        # Bringing in our global default values to update them
        global _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB
        # Changing the global default values as required
        if size.lower() in ["xs","xsmall","x-small"]:
            _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["xs"]
        elif size.lower() in ["sm","small"]:
            _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["sm"]
        elif size.lower() in ["md","medium"]:
            _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["md"]
        elif size.lower() in ["lg","large"]:
            _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["lg"]
        elif size.lower() in ["xl","xlarge","x-large"]:
            _DEFAULT_BAR, _DEFAULT_LABELS, _DEFAULT_UNITS, _DEFAULT_TEXT, _DEFAULT_AOB = sbd._DEFAULTS_SB["xl"]
        else:
            raise ValueError("Invalid value supplied, try one of ['xsmall', 'small', 'medium', 'large', 'xlarge'] instead")

### DRAWING FUNCTIONS ###

def scale_bar(ax, draw=True, style: Literal["ticks","boxes"]="boxes",
                  location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right",
                  bar: None | bool | sbt._TYPE_BAR=None,
                  units: None | bool | sbt._TYPE_UNITS=None,
                  labels: None | bool | sbt._TYPE_LABELS=None,
                  text: None | bool | sbt._TYPE_TEXT=None,
                  aob: None | bool | sbt._TYPE_AOB=None,
                  zorder: int=99,
                  return_aob: bool=True,):
    # For the default function mode, dispatch to the Artist class so final
    # rasterization happens at draw-time with the active renderer dpi.
    if draw == True and return_aob == True:
        _ = ax.add_artist(
            ScaleBar(
                style=style,
                location=location,
                bar=bar,
                units=units,
                labels=labels,
                text=text,
                aob=aob,
                zorder=zorder,
            )
        )
        return

    ##### VALIDATION #####
    _style = sbf._validate(sbt._VALIDATE_PRIMARY, "style", style)
    _location = sbf._validate(sbt._VALIDATE_PRIMARY, "location", location)
    _zorder = sbf._validate(sbt._VALIDATE_PRIMARY, "zorder", zorder)

    # This works the same as it does with the ScaleBar object(s)
    # If a dictionary is passed to any of the elements, first validate that it is "correct"
    # Note that we also merge the provided dict with the default style dict, so no keys are missing
    # If a specific component is not desired, it should be set to False in the function call
    if _style == "boxes":
        _bar = sbf._validate_dict(bar, _del_keys(_DEFAULT_BAR, ["minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]), 
                                                       _del_keys(sbt._VALIDATE_BAR, ["minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]), return_clean=True)
    else:
        _bar = sbf._validate_dict(bar, _del_keys(_DEFAULT_BAR, ["facecolors","edgecolors","edgewidth"]), 
                                                       _del_keys(sbt._VALIDATE_BAR, ["facecolors","edgecolors","edgewidth"]), return_clean=True)
    _units = sbf._validate_dict(units, _DEFAULT_UNITS, sbt._VALIDATE_UNITS, return_clean=True)
    _labels = sbf._validate_dict(labels, _DEFAULT_LABELS, sbt._VALIDATE_LABELS, return_clean=True)
    _text = sbf._validate_dict(text, copy.deepcopy(_DEFAULT_TEXT), sbt._VALIDATE_TEXT, return_clean=True) # this one has to be a deepcopy due to dictionary immutability
    _aob = sbf._validate_dict(aob, _DEFAULT_AOB, sbt._VALIDATE_AOB, return_clean=True)

    # Raster controls for the temporary rendered image.
    # These are kept explicit so output quality is not coupled to external rc state.
    _fig = ax.get_figure()
    _raster_dpi, _raster_dpi_scale = _resolve_raster_dpi(_bar, _fig)
    _raster_dpi = _raster_dpi * _raster_dpi_scale

    ##### CONFIGURING TEXT #####
    # First need to convert each string font size (if any) to a point size
    for d in [_text, _labels, _units]:
        if d is not None and "fontsize" in d.keys():
            d["fontsize"] = _convert_font_size(d["fontsize"])

    # The text dictionary acts as a shortcut for setting text properties elsewhere (units, major, and minor)
    # So the first order of business is to use it as an override for the other dictionaries as needed
    _units = _text | _units
    # Then change the textcolor key to textcolors so it fits in the major category
    _text["textcolors"] = _text["textcolor"] # if we hadn't made a deepcopy above, this would cause errors later (text shouldn't have textcolors as a key)
    _labels = _del_keys(_text, ["textcolor"]) | _labels
    
    ##### CONFIG #####

    # First, ensuring matplotlib knows the correct dimensions for everything
    # as we need it to be accurate to calculate out the plots!
    if draw:
        _fig.draw_without_rendering()

    # Getting the config for the bar (length, text, divs, etc.)
    bar_max, bar_length, units_label, major_div, minor_div = _config_bar(ax, _bar)

    # Getting the config for the segments (width, label, etc.)
    segments = _config_seg(bar_max, bar_length/major_div, major_div, minor_div, 
                           _bar["minor_type"], _labels["style"],
                           _labels["labels"], _labels["format"], _labels["format_int"])

    # Also setting the segment gap to be either the edgewidth or the tickwidth
    gap_width = _bar.get("edgewidth", _bar.get("edgewidth", 0))

    # Overwriting the units label, if needed
    if _units["label"] is not None:
        units_label = _units["label"]

    # Creating a temporary figure and axis for rendering later
    fig_temp, ax_temp = _temp_figure(ax, dpi=_raster_dpi)

    ##### BAR CONSTRUCTION #####

    # Defining the height and width of the bar
    # We call this "major" because we use the major divisions as the base for other calculations
    major_width = (bar_length/major_div)*72
    major_height = _bar["height"]*72

    # Initializing the bar with an invisible spacer, to align it with the text later
    # if all of these conditions are met, we do not need a spcer
    if _labels["style"] == "last_only" and major_div==1 and (minor_div==1 or minor_div==0):
        bar_artists = []
    # If we have minor divs, it will be equal to half the minor width
    elif minor_div > 1:
        bar_artists = [_make_boxes(major_width/minor_div/2, major_height, "none", "none", gap_width)]
    # if we don't, it will be equal to half the major width
    else:
        bar_artists = [_make_boxes(major_width/2, major_height, "none", "none", gap_width)]

    # If we are making a bar with boxes:
    if _style == "boxes":
        # First increasing the length of the number of facecolors and edgecolors to match the number of segments
        bar_facecolors = _expand_list(_bar["facecolors"], (major_div*minor_div), how="cycle")
        # These one has to be +1, because we have one more label (or tick) than divs (since labels (and ticks) are aligned on breaks)
        bar_edgecolors = _expand_list(_bar["edgecolors"], (major_div*minor_div)+1, how="cycle")

        # Getting the widths of the boxes from our segments
        # Note we drop the last segment - that is purely for the max value of the bar, which we don't represent with a segment, but does have a label
        box_widths = [s["width"] for s in segments[:-1] if s["type"]!="spacer"]
        # error checking the edge case when labels_style=="last_only" and major_div==1 and minor_div==0
        if len(box_widths)==0:
            box_widths = [segments[0]["width"]]
        # Now we actually make all the division boxes
        bar_artists += [_make_boxes(w, major_height, f, e, _bar["edgewidth"]) for w,f,e in zip(box_widths, bar_facecolors, bar_edgecolors)]

    # If instead we are making it with ticks:
    elif _style == "ticks":
        # First increasing the length of the number of facecolors and edgecolors to match the number of segments
        bar_basecolors = _expand_list(_bar["basecolors"], (major_div*minor_div), how="cycle")
        # These one has to be +1, because we have one more label (or tick) than divs (since labels (and ticks) are aligned on breaks)
        bar_tickcolors = _expand_list(_bar["tickcolors"], (major_div*minor_div)+1, how="cycle")

        # Uniquely, we need the height of the minor ticks here
        minor_height = major_height * _bar["minor_frac"]
        # Then appending the fully-built bar of ticks
        bar_artists += [_make_ticks(fig_temp, segments, _bar["tick_loc"], bar_max, bar_length, 
                                    major_width, major_height, minor_height, 
                                    bar_basecolors, bar_tickcolors, _bar["tickwidth"])]
        
    # If the units text is supposed to be aligned with the bar, then we add it to the end of the list in its own container
    if _units["loc"] == "bar":
        # If we're reversing everything, need the text to appear on the other side
        if _bar["reverse"] == True:
            units_ha = "right"
            units_x = major_width - _units["fontsize"]/2
        else:
            units_ha = "left"
            units_x = _units["fontsize"]/2
        bar_artists.append(_make_text(major_width, None, "none", "none", gap_width,
                                            units_label, units_x, None, "center_baseline", units_ha, _units["textcolor"], _units["fontsize"], 
                                            _units["rotation"], _units["rotation_mode"], _units["stroke_width"], _units["stroke_color"],
                                            **{k:v for k,v in _units.items() if k in ["fontfamily","fontstyle","fontweight"]}))

    # If needed, reverse the order of the boxes
    if _bar["reverse"] == True:
        bar_artists.reverse()

    # Now creating an HPacker for the box objects with zero padding and zero separation
    bar_pack = matplotlib.offsetbox.HPacker(children=bar_artists, pad=0, sep=0, align="center")

    ##### LABEL CONSTRUCTION #####
    # If the user wants the units label to appear alongside the text, we will append it here
    if _units["loc"] == "text":
        if segments[-1]["label"] is not None:
            segments[-1]["label"] += f" {units_label}"
        else:
            segments[-1]["label"] = units_label
    
    # other text inputs
    label_textcolors = _expand_list(_labels["textcolors"], (major_div*minor_div)+1, how="cycle")
    label_height = _labels["fontsize"] + _labels["stroke_width"]*2
    label_y = _labels["stroke_width"]
    if _labels["style"] == "last_only":
        if major_div==1 and (minor_div==1 or minor_div==0):
            label_ha = "center"
        elif _bar["reverse"] == True:
            label_ha = "left"
        else:
            label_ha = "right"
    else:
        label_ha = "center"

    # Creating the label artists
    label_artists = []
    # We already established the widths with the _config_seg function
    label_artists += [(_make_text(l["length"], label_height, "none", "none", gap_width,
                                       l["label"], l["length"]/2, label_y, "bottom", label_ha, c, _labels["fontsize"], 
                                       _labels["rotation"], _labels["rotation_mode"], _labels["stroke_width"], _labels["stroke_color"],
                                       **{k:v for k,v in _labels.items() if k in ["fontfamily","fontstyle","fontweight"]})) 
                    for l,c in zip(segments, label_textcolors)]

    # If needed, reverse the order of the text
    if _bar["reverse"] == True:
        label_artists.reverse()
        # Also need to change how we will align the VPacker
        pack_align = "right"
    else:
        pack_align = "left"
    
    # Now creating an HPacker for the text objects with zero padding and zero separation
    label_pack = matplotlib.offsetbox.HPacker(children=label_artists, pad=0, sep=0)

    ##### COMBINING #####

    # Storing the boxes and the text
    major_elements = [bar_pack, label_pack]

    # Reversing the order if we want the text above the bar
    if _labels["loc"]=="above":
        major_elements.reverse()
    
    # Vertically stacking the elements
    major_pack = matplotlib.offsetbox.VPacker(children=major_elements, sep=_labels["sep"], pad=_labels["pad"], align=pack_align)

    ##### UNITS (OPPOSITE ONLY) #####
    # This is only relevant if loc for units is set to opposite!
    # Which puts them on the opposite side of the text units
    if _units["loc"]=="opposite":
        if _bar["reverse"]==True:
            units_x = major_width/2
            units_ha = "left"
            units_align = "left"
        else:
            units_x = major_width
            units_ha = "right"
            units_align = "right"
        # Making the units text
        units = _make_text(major_width*1.5, None, "none", "none", gap_width,
                                 units_label, units_x, None, "center_baseline", units_ha, _units["textcolor"], _units["fontsize"], 
                                 _units["rotation"], _units["rotation_mode"], _units["stroke_width"], _units["stroke_color"],
                                 **{k:v for k,v in _units.items() if k in ["fontfamily","fontstyle","fontweight"]})
        # Stacking with the other elements
        units_elements = [units, major_pack]
        
        if _labels["loc"]=="above":
            units_elements.reverse()
        
        major_pack = matplotlib.offsetbox.VPacker(children=units_elements, sep=_units["sep"], pad=_units["pad"], align=units_align)

    ##### RENDERING #####
    # Here, we have to render the scale bar as an image on the temporary fig and ax we made
    # This is because it is honestly too difficult to keep the image as-is and apply our rotations
    # Mainly because Matplotlib doesn't let you place a nested OffsetBox inside of an AuxTransformBox with a rotation applied

    # AOB will contain the final artist
    aob_box = matplotlib.offsetbox.AnchoredOffsetbox(loc="center", child=major_pack, frameon=False, pad=0, borderpad=0)
    # Function that will handle invisibly rendering our object, returning an image
    img_scale_bar = _render_as_image(fig_temp, ax_temp, aob_box, _bar["rotation"])

    ##### FINAL RENDER #####

    # Placing the image in an OffsetBox, while rotating if desired
    # We have to set the zoom level to be relative to the DPI as well (image is in pixels)
    offset_img = matplotlib.offsetbox.OffsetImage(
        img_scale_bar,
        origin="upper",
        zoom=72/fig_temp.dpi,
        interpolation=_bar.get("interpolation", "none"),
        dpi_cor=_bar.get("dpi_cor", True),
        resample=_bar.get("resample", False),
    )
    # If desired, we can just return the rendered image in the final OffsetImage
    # This will override any aob or draw selections! Only the OffsetImage is returned!
    if return_aob==False:
        if aob is not None:
            warnings.warn(f"return_aob is set to False, but aob is not None: the settings for aob will be ignored, and an OffsetImage will instead be provided, which can be placed in an AnchoredOffsetBox of your choosing.")
        if draw==True:
            warnings.warn(f"return_aob is set to False, but draw is set to True: an OffsetImage of the ScaleBar will be returned by not drawn on the axis, which can be placed in an AnchoredOffsetBox of your choosing.")
        return offset_img

    # Then the offset image is placed in an AnchoredOffsetBox
    aob_img = matplotlib.offsetbox.AnchoredOffsetbox(loc=_location, child=offset_img, **_del_keys(_aob, ["facecolor","edgecolor","alpha"]))
    # Also setting the facecolor and transparency of the box
    if _aob["facecolor"] is not None:
        aob_img.patch.set_facecolor(_aob["facecolor"])
        aob_img.patch.set_visible(True)
    if _aob["edgecolor"] is not None:
        aob_img.patch.set_edgecolor(_aob["edgecolor"])
        aob_img.patch.set_visible(True)
    if _aob["alpha"]:
        aob_img.patch.set_alpha(_aob["alpha"])
        aob_img.patch.set_visible(True)
    
    aob_img.set_zorder(_zorder)

    # Finally, adding to the axis
    if draw == True:
        _ = ax.add_artist(aob_img)
    # If not, we'll return the aob_im as an artist object (the ScaleBar draw() functions use this)
    else:
        return aob_img

# This is a convenience function for creating two scale bars, with different units, aligned with each other
# The bars should be identical except for the units and the divisions
# NOTE: still under development, will tidy up if there is usage of it
def dual_bars(ax, draw=True, style: Literal["ticks","boxes"]="boxes",
                  location: Literal["upper right", "upper left", "lower left", "lower right", "center left", "center right", "lower center", "upper center", "center"]="upper right",
                  units_dual=["mi","km"], bar_maxes=[None,None], bar_lengths=[None,None], major_divs=[None, None], minor_divs=[None, None],
                  bar: None | bool | sbt._TYPE_BAR=None,
                  units: None | bool | sbt._TYPE_UNITS=None,
                  labels: None | bool | sbt._TYPE_LABELS=None,
                  text: None | bool | sbt._TYPE_TEXT=None,
                  aob: None | bool | sbt._TYPE_AOB=None,
                  zorder: int=99,
                  pad=0, sep=0,
                  return_aob: bool=True
                  ):
    
    _style = sbf._validate(sbt._VALIDATE_PRIMARY, "style", style)
    _location = sbf._validate(sbt._VALIDATE_PRIMARY, "location", location)
    _zorder = sbf._validate(sbt._VALIDATE_PRIMARY, "zorder", zorder)

    ##### CONCATENATION #####
    # NOTE: Probably a better way to do this, will investigate
    # Validation is done within each call of the scale_bar function, so don't need to do as much here
    if _style == "boxes":
        _bar = (_del_keys(_DEFAULT_BAR, ["rotation", "unit", "max", "length", "major_div", "minor_div",
                                         "minor_frac","tick_loc","basecolors","tickcolors","tickwidth"]) | bar)
    else:
        _bar = (_del_keys(_DEFAULT_BAR, ["rotation", "unit", "max", "length", "major_div", "minor_div",
                                         "facecolors","edgecolors","edgewidth"]) | bar)
    _units = _DEFAULT_UNITS | units if units is not None else _DEFAULT_UNITS
    _labels = _DEFAULT_LABELS | labels if labels is not None else _DEFAULT_LABELS
    _text = _DEFAULT_TEXT | text if text is not None else _DEFAULT_TEXT
    _aob = _DEFAULT_AOB | aob if aob is not None else _DEFAULT_AOB
    
    ##### VALIDATION #####
    if not isinstance(units_dual, (list, tuple)) or len(units_dual) != 2:
        raise ValueError("units_dual must be a list or tuple of length 2")
    if not isinstance(bar_maxes, (list, tuple)) or len(bar_maxes) != 2:
        raise ValueError("bar_maxes must be a list or tuple of length 2")
    if not isinstance(bar_lengths, (list, tuple)) or len(bar_lengths) != 2:
        raise ValueError("bar_lengths must be a list or tuple of length 2")
    if not isinstance(major_divs, (list, tuple)) or len(major_divs) != 2:
        raise ValueError("major_divs must be a list or tuple of length 2")
    if not isinstance(minor_divs, (list, tuple)) or len(minor_divs) != 2:
        raise ValueError("minor_divs must be a list or tuple of length 2")

    if _units.get("loc", None) == "opposite":
        raise ValueError("units['loc'] for units cannot be opposite for dual_bars, as it will not align correctly with the second scale bar")

    if _bar.get("rotation", None) is not None and bar.get("rotation", 0) != 0:
        warnings.warn("bar['rotation'] is not fully supported. It is recommended instead that you set rotation to zero and return the image by setting draw=False and return_aob=False, to return the OffsetImage of the dual scale bars instead.")
    if _bar.get("unit", None) is not None:
        warnings.warn("bar['unit'] is ignored for dual_bars, as it is set by units_dual")
        _ = _bar.pop("unit")
    if _bar.get("max", None) is not None:
        warnings.warn("bar['max'] is ignored for dual_bars, as it is (optionally) set by bar_maxes")
        _ = _bar.pop("max")
    if _bar.get("length", None) is not None:
        warnings.warn("bar['length'] is ignored for dual_bars, as it is (optionally) set by bar_lengths")
        _ = _bar.pop("length")
    if _bar.get("major_div", None) is not None:
        warnings.warn("bar['major_div'] is ignored for dual_bars, as it is (optionally) set by major_divs")
        _ = _bar.pop("major_div")
    if _bar.get("minor_div", None) is not None:
        warnings.warn("bar['minor_div'] is ignored for dual_bars, as it is (optionally) set by minor_divs")
        _ = _bar.pop("minor_div")
    
    _aob = sbf._validate_dict(_aob, _DEFAULT_AOB, sbt._VALIDATE_AOB, return_clean=True)
    
    ##### CREATION #####
    # Setting up the order of some other settings (label location, tick location)
    labels_loc = ["above","below"]
    tick_loc = ["above","below"]
    # Creating each bar in turn
    bars = []
    for unit,max,length,major_div,minor_div,label_loc,tick_loc in zip(units_dual, bar_maxes, bar_lengths, major_divs, minor_divs, labels_loc, tick_loc):
        # Making the settings for each possible selection
        bar_settings = {"unit":unit, "max":max, "length":length, "major_div":major_div, "minor_div":minor_div}
        if _style == "ticks":
            bar_settings["tick_loc"] = tick_loc
        label_settings = {"loc":label_loc}
        # Creating a bar
        # Because draw is False and return_aob is false, an OffsetImage will be returned
        bars.append(scale_bar(ax, draw=False, style=_style, location=location, 
                              bar=(_bar | bar_settings), 
                              units=_units, 
                              labels=(_labels | label_settings),
                              text=_text,
                              aob=None,
                              return_aob=False))

    ##### PACKING  #####
    # First need to know if we pack vertically or horizontally
    bar_vertical = _config_bar_vert(_bar["rotation"])
    packer = matplotlib.offsetbox.VPacker if bar_vertical == False else matplotlib.offsetbox.HPacker
    if bar["reverse"] == True:
        align = "right" if bar_vertical == False else "top"
    else:
        align = "left" if bar_vertical == False else "bottom"

    # Packing the bars together, with a separator between them
    # The separator is a fixed size, and is not scaled with the bars - it represents the space between them
    pack = packer(children=bars, align=align, pad=pad, sep=sep)

    ##### NUDGING #####
    # Placing the packer in the AOB first off
    aob_pack = matplotlib.offsetbox.AnchoredOffsetbox(loc=_location, child=pack, **_del_keys(_aob, ["facecolor","edgecolor","alpha"]))
    # Finding if and how much we need to nudge either image
    aob_pack = _align_dual(ax, aob_pack, bar_vertical, _bar["reverse"])
    
    ##### FINAL RENDER #####
    # If desired, we can just return the final packer
    # This will override any aob or draw selections! Only the Packer is returned!
    if return_aob==False:
        if aob is not None:
            warnings.warn(f"return_aob is set to False, but aob is not None: the settings for aob will be ignored, and a Packer will instead be provided, which can be placed in an AnchoredOffsetBox of your choosing.")
        if draw==True:
            warnings.warn(f"return_aob is set to False, but draw is set to True: the settings for draw will be ignored, and a Packer will instead be provided, which can be placed in an AnchoredOffsetBox of your choosing.")
        return pack

    # Also setting the facecolor and transparency of the box
    if _aob["facecolor"] is not None:
        aob_pack.patch.set_facecolor(_aob["facecolor"])
        aob_pack.patch.set_visible(True)
    if _aob["edgecolor"] is not None:
        aob_pack.patch.set_edgecolor(_aob["edgecolor"])
        aob_pack.patch.set_visible(True)
    if _aob["alpha"]:
        aob_pack.patch.set_alpha(_aob["alpha"])
        aob_pack.patch.set_visible(True)
    
    aob_pack.set_zorder(_zorder)

    # Finally, adding to the axis
    if draw == True:
        _ = ax.add_artist(aob_pack)
    # If not, we'll return the aob_im as an artist object (the ScaleBar draw() functions use this)
    else:
        return aob_pack

### OTHER FUNCTIONS ###

# This function will remove any keys we specify from a dictionary
# This is useful if we need to unpack on certain values from a dictionary, and is used in scale_bar()
def _del_keys(dict, to_remove):
    return {key: val for key, val in dict.items() if key not in to_remove}

# This function handles the configuration steps 
# (i.e. calculating the length of the bar, its divisions, etc.)
# that are shared across all the different scale bars
def _config_bar(ax, bar):

    ## ROTATION ##
    # Calculating if the rotation is vertical or horizontal
    bar_vertical = _config_bar_vert(bar["rotation"])

    ## DIM ##
    # Finding the size of the axis in inches
    # The size of the axis in the units requested by the user
    # and determining the appropriate units label to use
    ax_inches, ax_units, units_label = _config_bar_dim(ax, bar_vertical, bar["projection"], bar["unit"])

    ## LENGTH ##
    # Finding the size of the bar in inches
    # and the size of the bar in the units requested by the user
    # and the optimal major and minor bar divisions
    bar_max, bar_length, bar_major_div, bar_minor_div = _config_bar_length(bar["max"], bar["length"], bar["major_mult"], bar["major_div"], ax_inches, ax_units, bar["projection"])

    ## DIVISIONS ##
    # We've done most of the work here - just need to see if we want a minor div or not
    # If one is provided, override what we calculated above
    if bar["minor_div"] is not None:
        bar_minor_div = bar["minor_div"] 
    
    # Returning everything
    return bar_max, bar_length, units_label, bar_major_div, bar_minor_div

# A small function for calculating the number of 90 degree rotations that are being applied
# So we know if the bar is in a vertical or a horizontal rotation
def _config_bar_vert(degrees):
    # Figuring out how many quarter turns the rotation value is approximately
    quarters = int(round(degrees/90,0))
    
    # EVEN quarter turns (0, 180, 360, -180) are considered horizontal
    # ODD quarter turns (90, 270, -90, -270) are considered vertical
    if quarters % 2 == 0:
        bar_vertical = False
    else:
        bar_vertical = True
    
    return bar_vertical

# This function determines the dimensions of the relevant axis, in the user's desired units
def _config_bar_dim(ax, bar_vertical, bar_projection, bar_unit):
    
    # Literally just getting the figure for the passed axis
    fig = ax.get_figure()

    # First, finding the dimensions of the axis and the limits
    # get_window_extent() returns values in pixel coordinates
    # so dividing by dpi gets us the inches of the axis
    # Vertical scale bars are oriented against the y-axis (height)
    if bar_vertical==True:
        ax_inches = ax.patch.get_window_extent().height / fig.dpi
        min_lim, max_lim = ax.get_ylim()
    # Horizontal scale bars are oriented against the x-axis (width)
    else:
        ax_inches = ax.patch.get_window_extent().width / fig.dpi
        min_lim, max_lim = ax.get_xlim()
    # This calculates the range from max to min on the axis of interest
    ax_range = abs(max_lim - min_lim)


    # If the user is using one of the custom overrides, we can stop here, basically
    if bar_projection in ["px","pixel","pixels","pt","point","points","dx","custom","axis"]:
        # Enforcing an empty units label here
        units_label = ""
        if bar_unit is not None:
            warnings.warn(f"When bar['projection'] is set to '{bar_projection}', bar['unit'] will be ignored; you can set a custom label for the bar via the units argument, see documentation for details.")
        # If we're in pixels, just need to re-multiply ax_inches back out by fig.dpi
        if bar_projection in ["px","pixel","pixels"]:
            ax_units = ax_inches * fig.dpi
        # If we're in points, need to multiply by 72
        elif bar_projection in ["pt","point","points"]:
            ax_units = ax_inches * 72
        # If we're using the axis, then we can just use that directly!
        elif bar_projection in ["dx","custom","axis"]:
            ax_units = ax_range
    
    # Otherwise, we have more work to do!
    else:
        # Capturing the unit from the projection
        # (We use bar_vertical to index; 0 is for east-west axis, 1 is for north-south)
        units_proj = pyproj.CRS(bar_projection).axis_info[bar_vertical].unit_name
        # If the provided units are in degrees, we will convert ax_range to meters first
        if units_proj=="degree":
            warnings.warn(f"Provided CRS {bar_projection} uses degrees. An attempt will be made at conversion, but there will be accuracy issues: it is recommended that you use a projected CRS instead.")
            ylim = ax.get_ylim()
            xlim = ax.get_xlim()
            # Using https://github.com/seangrogan/great_circle_calculator/blob/master/great_circle_calculator/great_circle_calculator.py
            # If the bar is vertical, we use the midpoint of the longitude (x-axis) and the max and min of the latitude (y-axis)
            if bar_vertical==True:
                ax_range = distance_between_points(((xlim[0]+xlim[1])/2, ylim[0]), ((xlim[0]+xlim[1])/2, ylim[1]))
            # Otherwise, the opposite
            else:
                ax_range = distance_between_points((xlim[0], (ylim[0]+ylim[1])/2), (xlim[1], (ylim[0]+ylim[1])/2))
            # Setting units_proj to meters now
            units_proj = "m"
            
        # If a projected CRS is provided instead...
        else:
            # Standardizing the projection unit
            try:
                units_proj = sbt.units_standard[units_proj]
            except:
                warnings.warn(f"Units for specified projection ({units_proj}) are considered invalid; please use a different projection that conforms to an expected unit value (such as US survey feet or metres)")
                return None

        # Standardizing the units specified by the user
        # This means we will also handle conversion if necessary
        try:
            units_user = sbt.units_standard.get(bar_unit)
        except:
            warnings.warn(f"Desired output units selected by user ({bar_unit}) are considered invalid; please use one of the units specified in the units_standard dictionary in defaults.py")
            units_user = None

        # Converting
        # First, the case where the user doesn't provide any units
        # In this instance, we just use the units from the projection
        if units_user is None:
            units_label = units_proj
            # If necessary, scaling "small" units to "large" units
            # Meters to km
            if units_proj == "m" and ax_range > (1000*5):
                ax_units = ax_range / 1000
                units_label = "km"
            # Feet to mi
            elif units_proj == "ft" and ax_range > (5280*5):
                ax_units = ax_range / 5280
                units_label = "mi"
            # Otherwise, if no scaling is necessary...
            else:
                ax_units = ax_range

        # Otherwise, if the user supplied a unit of some sort, then handle conversion
        else:
            units_label = units_user
            # We only need to do so if the units are different, however!
            if units_user != units_proj:
                # This works by finding the ratios between the two units, using meters as the base
                ax_units = ax_range * (sbt.convert_dict[units_proj] / sbt.convert_dict[units_user])
            # Otherwise, if the units are the same
            else: 
                ax_units = ax_range
    
    return ax_inches, ax_units, units_label

# This function calculates the optimal length of the entire bar in inches and the user's units
def _config_bar_length(bar_max, bar_length, bar_major_mult, bar_major_div, ax_inches, ax_units, bar_projection):

    # First checking that the user is providing valid values
    if bar_length is not None and bar_max is not None:
        warnings.warn(f"Both bar['max'] and bar['length'] are provided; bar['length'] will be ignored. Please reference the documentation to understand why both may not be set at the same time.")
    elif (bar_max is not None or bar_length is not None) and bar_major_mult is not None:
        warnings.warn(f"Either bar['max'] or bar['length'] are provided, along with bar['major_mult']; bar['major_mult'] will be ignored. Please reference the documentation to understand why both may not be set at the same time.")
    elif bar_length is not None and bar_major_div is not None:
        warnings.warn(f"Both bar['length'] and bar['major_div'] are provided; bar['major_div'] will be ignored, and instead an optimal value will be calculated. Please reference the documentation to understand why both may not be set at the same time.")
    elif bar_length is not None and bar_length > ax_inches:
        warnings.warn(f"Provided bar length ({bar_length}) is greater than the axis length ({ax_inches} inches); setting bar length to default (25% of axis length).")
        bar_length = 0.25
    elif bar_projection in ["px","pixel","pixels","pt","point","points","dx","custom","axis"] and bar_length is not None:
        warnings.warn(f"Providing a bar length is incompatible with a bar['projection'] value of ${bar_projection}, please use either bar['max'] or bar['major_mult'] instead.")
    elif bar_major_mult is not None and bar_major_div is None:
        warnings.warn(f"bar['major_div'] must be supplied alongside bar['major_mult']. Reverting to default behavior (bar['length'] = 0.25).")
        bar_length = 0.25
    
    # Then, seeing if we need to use the default behavior (if everything is none)
    if bar_max is None and bar_length is None and bar_major_mult is None and bar_major_div is None:
        bar_length = 0.25
    
    # Deriving the length of the bar
    # First, with bar_max, if provided - it is the length of the bar in UNITS
    if bar_max is not None:
        # Only need to update the bar_length here, then
        bar_length = ax_inches * (bar_max / ax_units)
        
        # If we don't have a bar_major_div, set one
        if bar_major_div is None:
            if bar_max % 3 == 0:
                bar_major_div = 3
            elif bar_max % 2 == 0:
                bar_major_div = 2
            else:
                bar_major_div = 1
        # Same for minor
        if bar_major_div % 2 == 0:
            bar_minor_div = 2
        else:
            bar_minor_div = 1
    
    # Otherwise, if bar_length is provided - it is the length of the bar in INCHES
    elif bar_length is not None:
        # Converting, if bar length is expressed as a fraction of the axis
        if bar_length < 1:
            bar_length = ax_inches * bar_length
        
        # Calculating bar_max based on this length
        bar_max = ax_units * (bar_length / ax_inches)

        # We will also optimize it, so that it rounds to a "nice" number
        # Scaling the max down to just the important digits
        for units_mag in range(0,23):
            if bar_max / (10 ** (units_mag+1)) > 1.5:
                units_mag += 1
            else:
                break
        
        # Getting a list of "optimal" numbers we want to aim for
        preferred_maxes = list(sbt.preferred_divs.keys())
        # Finding the RMS/distance between each perferred max and our actual max
        max_rms = [math.sqrt((m - (bar_max/(10**units_mag)))**2) for m in preferred_maxes]
        # Sorting for the "best" number
        # Sorted() works on the first item in the tuple contained in the list
        # Note that we reverse m,r and r,m here, just to keep things confusing
        sorted_breaks = [(m,r) for r,m in sorted(zip(max_rms, preferred_maxes))]

        # Saving the values
        bar_max_best = sorted_breaks[0][0]
        bar_max = bar_max_best * 10**units_mag

        # Going back and re-calculating the length (it'll be slightly more/less now)
        bar_length = ax_inches * (bar_max / ax_units)

        # And finally picking out the major div from this
        bar_major_div, bar_minor_div = sbt.preferred_divs[bar_max_best]
    
    # Otherwise, if BOTH bar_major_mult and bar_major_div are provided, using that
    # bar_major_mult is expressed in UNITS
    elif bar_major_div is not None and bar_major_mult is not None:
        bar_max = bar_major_mult * bar_major_div
        bar_length = ax_inches * (bar_max / ax_units)
        # And we set bar_minor_div based on major_div
        if bar_major_div % 2 == 0:
            bar_minor_div = 2
        else:
            bar_minor_div = 1
    
    # Generic catch to throw a warning of any other situation
    else:
        warnings.warn("Error in calculating bar length, please re-check your values for bar['max'], bar['length'], bar['major_mult'], and/or bar['major_div']. If error persists when values appear correct, please file an issue on GitHub with a code sample.")
        return None

    # Another final check just to make sure our final calculations aren't too wonky     
    if ((bar_length / ax_inches) > 0.9) or (bar_max > (ax_units * 0.9)):
        warnings.warn(f"The auto-calculated dimensions of the bar are too large for the axis. This usually happens when the height or width of your map is ~1 to 2 miles or kilometres (depending on your selected unit). This will result in a bar close to or longer than your axis, extending beyond your frame. Consider either manually specifying a 'max' and 'major_div' value less than 2, or switching your units to feet/metres as necessary.")
    
    return bar_max, bar_length, bar_major_div, bar_minor_div

# This function handles the creation of the segments and their labels
# It is a doozy - needs to handle all the different inputs for minor_type and label_type
# The output of this function will be a list of dictionaries
# With each element in the list representing a segment with four keys:
# width (for the segment, in points), length (for the label, in points), value (numeric value in units), type (major or minor or spacer), and label (either the value (rounded if needed) or None if no label is required)
def _config_seg(bar_max, major_width, major_div, minor_div, minor_type, label_style, labels, format_str, format_int):
    segments = []
    ## SEGMENT WIDTHS ##
    # Starting with the minor boxes, if any
    # If you don't have minor divs, you only make boxes for the major divs, and you start at the zeroeth position
    if minor_div <= 1 or minor_type == "none":
        segments += [{"width":(major_width), "length":(major_width), "value":(d*(bar_max/major_div)), "type":"major"} for d in range(0,major_div+1)]
    else:
        if minor_div > 1:
            # If minor_type is first, we only need to append minor boxes for the first set of major divisions
            if minor_type == "first":
                # Minor
                segments += [{"width":(major_width/minor_div), "length":(major_width/minor_div), "value":(d*(bar_max/major_div/minor_div)), "type":"minor"} for d in range(0,minor_div)]
                # The edge between minor and major needs to have the width of a major div, but the lenght if a minor one
                segments += [{"width":(major_width), "length":(major_width/minor_div), "value":(bar_max/major_div), "type":"major"}]
                # After this we need to add a spacer! Otherwise our major divisions are offset
                # I figured out the ((minor_div-1)/2) part by trial and error, but it seems to work well enough for now
                segments += [{"width":(major_width/minor_div*((minor_div-1)/2)), "length":(major_width/minor_div*((minor_div-1)/2)), "value":-1, "type":"spacer", "label":None}]
                # All the major divs (if any) after this are normal
                if major_div > 1:
                    segments += [{"width":(major_width),"length":(major_width), "value":(d*(bar_max/major_div)), "type":"major"} for d in range(2,major_div+1)]
            # If minor_type is all, we append minor boxes for every major division, and no major boxes at all
            else:
                # Here, we have to do another correction for the minor divs that fall on what would be a major division
                segments += [{"width":(major_width/minor_div), "length":(major_width/minor_div), "value":(d*(bar_max/(major_div*minor_div))), "type":"major"} 
                                if ((d*(bar_max/(major_div*minor_div))) % (bar_max/major_div) == 0) else 
                            {"width":(major_width/minor_div), "length":(major_width/minor_div), "value":(d*(bar_max/(major_div*minor_div))), "type":"minor"} 
                                for d in range(0,(minor_div*major_div)+1)]
        
    # For all segments, we make sure that the first and last types are set to major
    segments[0]["type"] = "major"
    segments[-1]["type"] = "major"

    # Expanding all the widths
    for s in segments:
        s["width"] = s["width"]*72
        s["length"] = s["length"]*72

    ## LABELS ##
    # If we only have major labels, we only need to add labels to the major segments
    if label_style=="major":
        for s in segments:
            if s["type"] == "major":
                s["label"] = s["value"]
            else:
                s["label"] = None
    # If we only have the first and last labels
    elif label_style=="first_last":
        for i,s in enumerate(segments):
            if i == 0 or i == len(segments)-1:
                s["label"] = s["value"]
            else:
                s["label"] = None
    # If we only have the last label
    elif label_style=="last_only":
        for i,s in enumerate(segments):
            if i == len(segments)-1:
                s["label"] = s["value"]
            else:
                s["label"] = None
        # This is a custom override when specific conditions are met
        if major_div==1 and (minor_div==1 or minor_div==0):
            # We only need to keep the last segment
            segments[0] = segments[1]
            segments = segments[:1]
    # If we only have labels on the first minor segment, plus all the major segments
    elif label_style=="minor_first":
        apply_minor = True
        for i,s in enumerate(segments):
            if s["type"] == "major":
                s["label"] = s["value"]
            elif s["type"] == "minor" and apply_minor == True:
                s["label"] = s["value"]
                apply_minor = False
            else:
                s["label"] = None
    # If we have labels on all the minor segments, plus all the major segments
    elif label_style=="minor_all":
        for s in segments:
            if s["type"] != "spacer":
                s["label"] = s["value"]

    ## CUSTOM LABELS ##
    # If custom labels are passed, we will use this to simply overwrite the labels we have already calculated
    # Note that we also check the correct number of labels are passed
    if labels is not None:
        num_labels = len([s for s in segments if s["label"] is not None])
        if num_labels < len(labels):
            warnings.warn(f"More labels were provided ({len(labels)}) than needed. Only the first {num_labels} will be used.")
        elif num_labels > len(labels):
            warnings.warn(f"Fewer labels were provided ({len(labels)}) than needed ({num_labels}). The last {num_labels-len(labels)} will be set to None.")
        labels = _expand_list(labels, num_labels, "nfill")
        # Keeping track of how many labels we have applied
        # So we can map the labels list to the list of segments with labels
        i = 0
        for s in segments:
            if s["label"] is not None:
                if labels[i] == True or isinstance(labels[i], (int, float)):
                    s["label"] = _format_numeric(labels[i], format_str, format_int)
                elif labels[i] == False or labels[i] is None:
                    s["label"] = None
                else:
                    s["label"] = labels[i]
                i += 1
    else:
        # If no custom labels are passed, we will clean up the ones we generated
        for s in segments:
            if s["label"] is None:
                pass
            else:
                s["label"] = _format_numeric(s["label"], format_str, format_int)

    # Returning everything at the end
    return segments

# A small function for expanding a list a potentially uneven number of times
# Ex. ['black','white'] -> ['black','white','black','white''black']
def _expand_list(seq: list, length: int, how="cycle", convert=True):
    if type(seq) != list and convert == True:
        seq = [seq]
    # Cycle through the shorter list and add items repetitively
    if how == "cycle":
        # To hold the expanded list
        seq_expanded = []
        # To reach the desired length
        i = 0
        # While loop to pick colors until the desired length is reached
        while i < length:
            # This cycles the selection
            pick = i % len(seq)
            # Appending the selected color to our expanded list
            seq_expanded.append(seq[pick])
            i += 1
    # Fill the list with Nones
    elif how == "nfill":
        # Copying the shorter list
        seq_expanded = seq.copy()
        # Resetting the length
        i = len(seq_expanded)
        # Filling the rest of the list with nones
        seq_expanded += [None for i in range(i, length)]
    # Returning the longer list
    return seq_expanded

# A function to convert font sizes that are passed as a string to points
def _convert_font_size(font_size):
    if type(font_size) != str:
        return font_size
    else:
        # Getting the current default font size
        default_font_size = matplotlib.rcParams["font.size"]
        # Creating the mapping of string size to multiplier
        # See https://github.com/matplotlib/matplotlib/blob/v3.5.1/lib/matplotlib/font_manager.py#L51-L62
        font_scalings = matplotlib.font_manager.font_scalings
        # Confirming the string is in the mapping
        if font_size in font_scalings.keys():
            # Getting the multiplier
            multiplier = font_scalings[font_size]
            # Calculating the new size
            size_points = default_font_size * multiplier
            # Returning the new size
            return size_points
        # If the string is not in the mapping, return the default size, and raise a warnings
        else:
            warnings.warn(f"The string {font_size} is not a valid font size. Using the default font size of {default_font_size} points.")
            return default_font_size

# A function to format a numeric string as we desire
def _format_numeric(val, fmt, integer_override=True):
    # If the format is None, we return the string as is
    if fmt is None or fmt == "":
        return val
    # If the format is a string, we return a function that formats the string as desired
    else:
        if integer_override == True and type(val) == int or (type(val) == float and val % 1 == 0):
            return f"{int(val)}"
        else:
            return f"{val:{fmt}}"

# A small function for creating a temporary figure based on a provided axis
def _temp_figure(ax, axis=False, visible=False, dpi=None):
    # Getting the figure of the provided axis
    fig = ax.get_figure()
    # If no dpi is passed, fall back to the figure dpi
    if dpi is None:
        dpi = fig.dpi
    # Getting the dimensions of the axis
    ax_bbox = ax.patch.get_window_extent()
    # Converting to inches and rounding up
    ax_dim = math.ceil(max(ax_bbox.height, ax_bbox.width) / fig.dpi)
    # Creating a new temporary figure
    fig_temp, ax_temp = matplotlib.pyplot.subplots(1,1, figsize=(ax_dim*1.5, ax_dim*1.5), dpi=dpi)
    # Turning off the x and y labels if desired
    if axis == False:
        ax_temp.axis("off")
    # Turning off the backgrounds of the figure and axis
    if visible == False:
        fig_temp.patch.set_visible(False)
        ax_temp.patch.set_visible(False)
    # Returning
    return fig_temp, ax_temp

# A function to make a drawing area with a rectangle within it
# This is used pretty frequently when making spacers and major boxes
def _make_boxes(width, height, facecolor, edgecolor, linewidth):
    # First, a drawing area to store the rectangle, and a rectangle to color it
    area = matplotlib.offsetbox.DrawingArea(width=width, height=height, clip=False)
    rect = matplotlib.patches.Rectangle((0,0), width=width, height=height, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
    # Placing the rect in the drawing area
    area.add_artist(rect)
    # Returning the final drawing area
    return area

# A function to make a drawing area with all of the ticks involved in it: major, minor, and the base tick that constitutes the bar
# Unlike _make_boxes, we don't call this within the context of a for loop - it will go ahead and return a list
def _make_ticks(fig, segments, tick_loc, bar_max, bar_length, major_width, major_height, minor_height, bar_facecolors, bar_edgecolors, edgewidth):
    # Converting everything back to inches
    major_width = major_width/72
    major_height = major_height/72
    minor_height = minor_height/72
    # Filtering out any spacers in our segment
    segments = [s for s in segments if s["type"] != "spacer"]
    # Creating a ATB to scale everything in inches
    bar_ticks = matplotlib.offsetbox.AuxTransformBox(fig.dpi_scale_trans)
    # Establishing where each vertical tick should span
    # Each of these will be relative to x=0, which is where the horizontal line will be drawn
    if tick_loc == "below":
        y_major = (-major_height,0)
        y_minor = (-(minor_height),0)
    elif tick_loc == "middle":
        y_major = (-(major_height/2), (major_height/2))
        y_minor = (-(minor_height/2), (minor_height/2))
    else:
        y_major = (0,major_height)
        y_minor = (0,minor_height)

    # Now iterating through each segment and making the ticks
    # Note we split this in two: first doing the horizontal, then the vertical ticks
    # This is so they are drawn correctly (vertical on top of horizontal)
    # But also so that we can exclude the first (invisible) horizontal tick

    # This will help us keep track of the width of the bars
    x_pos = 0
    for s,f in zip(segments[1:], bar_facecolors):
        width = s["value"]/bar_max*bar_length
        bar_ticks.add_artist((matplotlib.lines.Line2D([x_pos,width],[0,0], color=f, linewidth=edgewidth, solid_capstyle="butt")))
        # Updating the x position for the next tick
        x_pos = width
    
    # Resetting the x_pos for the second iteration
    x_pos = 0
    for s,e in zip(segments, bar_edgecolors):
        x_pos = s["value"]/bar_max*bar_length
        if s["type"] == "major":
            bar_ticks.add_artist(matplotlib.lines.Line2D([x_pos,x_pos],y_major, color=e, linewidth=edgewidth, solid_capstyle="projecting"))
        elif s["type"] == "minor":
            bar_ticks.add_artist(matplotlib.lines.Line2D([x_pos,x_pos],y_minor, color=e, linewidth=edgewidth, solid_capstyle="projecting"))
        else:
            pass

    # Returning the ATB of ticks
    return bar_ticks

# A function, similar to above, but for adding text as well
# This is used pretty frequently when making spacers and major boxes
def _make_text(width, height, facecolor, edgecolor, linewidth, 
               text_label, text_x, text_y, text_va, text_ha, text_color, text_fontsize, 
               text_rotation=0, text_mode="anchor", stroke_width=0, stroke_color="none", **kwargs):
    # First, creating a path effect for the stroke, if needed
    if stroke_width > 0:
        text_stroke = [matplotlib.patheffects.withStroke(linewidth=stroke_width, foreground=stroke_color)]
    else:
        text_stroke = []
    # Then, calculating the height (if one wasn't provided)
    if height is None:
        height = text_fontsize + stroke_width*2
        if text_y is None and text_va=="center_baseline":
            text_y = height/2
    # Then, the drawing area
    area = _make_boxes(width, height, facecolor, edgecolor, linewidth)
    # Checking that the text is not None
    if text_label is not None:
        # Placing the text in the drawing area
        text = matplotlib.text.Text(x=text_x, y=text_y, text=text_label, va=text_va, ha=text_ha, color=text_color, fontsize=text_fontsize, 
                                    rotation=text_rotation, rotation_mode=text_mode, path_effects=text_stroke, **kwargs)
        area.add_artist(text)
    # Returning the final drawing area with text
    return area

# During testing, noticed some issues with odd/prime numbers of divs causing misalignment of the bars by ~1 pixel
# So this is intended to check for alignment
def _align_dual(ax, artist, bar_vertical, reverse):
    # First, making a temporary axis to render the image
    fig_temp, ax_temp = _temp_figure(ax=ax)
    # Then, rendering the image, and getting back a 2D array
    img_temp = _render_as_image(fig_temp, ax_temp, copy.deepcopy(artist), rotation=0, remove=True)
    # Getting the image as an array
    arr_temp = numpy.array(img_temp)
    # Now, comparing when the top and bottom bars (or left and right) start to each other
    # This is done by finding the midpoint of the image (should be symmetric), and then looking ~15 pixels up and down the image
    if bar_vertical == True:
        dim = 1
    else:
        dim = 0
    midpoint = arr_temp.shape[dim] // 2
    dim_top = int(midpoint + 15)
    dim_bot = int(midpoint - 15)
    
    # Now, for each row at the specified height (or each column at the specified width for vertical artists), 
    # find the first non-transparent pixel
    if bar_vertical == True:
        slice_top = arr_temp[:, dim_top, :].copy()
        slice_bot = arr_temp[:, dim_bot, :].copy()
    else:
        slice_top = arr_temp[dim_top, :, :].copy()
        slice_bot = arr_temp[dim_bot, :, :].copy()
    # We'll need to work backwards if reverse == True
    if reverse == True:
        slice_top = numpy.flip(slice_top, axis=dim)
        slice_bot = numpy.flip(slice_bot, axis=dim)
    # Now iterating through each slice to find the index of the first non-transparent pixel
    xtop = -1
    xbot = -1
    for it,pt in enumerate(slice_top):
        if pt[3] > 20:
            xtop = it
            break
    for ib,pb in enumerate(slice_bot):
        if pb[3] > 20:
            xbot = ib
            break
    # Finding the difference
    # If we weren't able to determine the right nudge amount, just return the original artist
    if xtop == -1 or xbot == -1 or xtop == xbot:
        return artist
    # Otherwise we are just calculating the difference in pixels,
    # Which is the number of blank rows/columns we need to add to align
    else:
        diff = xtop - xbot
    
    # Now, adding a row/column of blank pixels to create the alignment, as needed
    # Getting the child artist we need
    if diff < 0:
        child = artist.get_child().get_children()[1]
    else:
        child = artist.get_child().get_children()[0]
    # Creating the dimension of blank row/columns
    if bar_vertical == True:
        to_append = numpy.array([[[255,0,0,0]]*child.get_data().shape[1]]*abs(diff))
        axis_append = 0
    else:
        to_append = numpy.array([[[255,0,0,0]]*abs(diff)]*child.get_data().shape[0])
        axis_append = 1
    # Appending the blank row/column to the child artist
    if reverse == True:
        child.set_data(numpy.concatenate((child.get_data(), to_append), axis=axis_append))
    else:
        child.set_data(numpy.concatenate((to_append, child.get_data()), axis=axis_append))
    # Returning the new 2-bar artist
    return artist

# A function that handles invisibly rendering an artist and returning its image
def _render_as_image(fig, ax, artist, rotation, add=True, remove=True, close=True):
    # If needed, adding the artist to the axis
    if add == True:
        ax.add_artist(artist)
    # Render directly with Agg; a prior draw_without_rendering() can override
    # temporary figure DPI in some wrappers (e.g., UltraPlot), which makes
    # raster_dpi ineffective.
    canvas = FigureCanvasAgg(fig)
    # Draws the figure onto the canvas
    canvas.draw()
    # Converts the rendered figure to an RGBA(lpha) array
    rgba = numpy.asarray(canvas.buffer_rgba())
    # Converts the array to a PIL image object
    img = PIL.Image.fromarray(rgba)
    # Rotates the image
    img = img.rotate(rotation, expand=True)
    # Crops the transparent pixels out of the image
    img = img.crop(img.getbbox())
    # If needed, removing the artist from the axis
    if remove == True:
        artist.remove()
    # If needed, closing the figure, to ensure it doesn't render
    if close == True:
        matplotlib.pyplot.close(fig)
    # Returning the image
    return img


def _resolve_raster_dpi(bar, fig, renderer=None):
    """
    Resolve base raster DPI and raster scale for temporary rendering.
    """
    raster_dpi = bar.get("raster_dpi", None)
    if raster_dpi is None:
        raster_dpi = renderer.dpi if renderer is not None else fig.dpi
    raster_dpi_scale = bar.get("raster_dpi_scale", 1)
    return raster_dpi, raster_dpi_scale