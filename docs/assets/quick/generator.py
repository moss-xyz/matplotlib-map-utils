import pygris
import geopandas
import shapely 
import pyproj
import matplotlib.pyplot
from matplotlib_map_utils.core import north_arrow, scale_bar, ScaleBar, inset_map, indicate_detail, indicate_extent
from matplotlib_map_utils.utils import USA

# This is just a function to create a new, blank map with matplotlib, with our default settings
def new_map(rows=1, cols=1, figsize=(5,5), dpi=150, ticks=False):
    # Creating the plot(s)
    fig, ax = matplotlib.pyplot.subplots(rows,cols, figsize=figsize, dpi=dpi)
    # Turning off the x and y axis ticks
    if ticks==False:
        if rows > 1 or cols > 1:
            for a in ax.flatten():
                a.set_xticks([])
                a.set_yticks([])
        else:
            ax.set_xticks([])
            ax.set_yticks([])
    # Returning the fig and ax
    return fig, ax

# states = pygris.states(cb=True, year=2022, cache=False).to_crs(3857)
states = geopandas.read_file("../../../matplotlib_map_utils/scratch/states.gpkg").to_crs(3857)
usa = USA()
contiguous = states.query(f"GEOID in {usa.filter_contiguous(True)}")
georgia = states.query(f"GEOID == '{usa.filter_abbr("GA")}'")

#------------------------------------------------
# north_arrow_generic.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Adding a north arrow to the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
north_arrow(ax=ax, location="upper right", rotation={"degrees":0})

matplotlib.pyplot.savefig("./north_arrow_generic.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# north_arrow_customised.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Adding a more customized north arrow
north_arrow(
	ax,
	location = "upper right", # accepts a valid string from the list of locations
	scale = 0.5, # accepts a valid positive float or integer
	# each of the follow accepts arguments from a customized style dictionary
	base = {"facecolor":"green"},
	fancy = False,
	label = {"text":"North"},
	shadow = {"alpha":0.8},
	pack = {"sep":6},
	aob = {"pad":1},
	rotation = {"degrees": 35}
)

matplotlib.pyplot.savefig("./north_arrow_customised.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# north_arrow_rotated.png
#------------------------------------------------

states = pygris.states(cb=True, year=2022, cache=False).to_crs(3857)
# Setting up a plot
fig, ax = new_map()
# Plotting a state (Texas)
states.query("NAME=='Texas'").to_crs(3520).plot(ax=ax)
# Adding a north arrow to the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
north_arrow(ax=ax, location="upper right", rotation={"crs":3520, "reference":"center"})

matplotlib.pyplot.savefig("./north_arrow_rotated.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# scale_bar_generic.png
#------------------------------------------------

fig, ax = new_map(1,2, figsize=(10,5))
# Changing the size
ScaleBar.set_size("sm")
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax[0])
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax[1])
# Adding a scale bar to the upper-right corner of the axis, in the same projection as whatever geodata you plotted
scale_bar(ax=ax[0], location="upper right", style="boxes", bar={"projection":3520})
scale_bar(ax=ax[1], location="upper right", style="ticks", bar={"projection":3520})

matplotlib.pyplot.savefig("./scale_bar_generic.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# scale_bar_customised.png
#------------------------------------------------

fig, ax = new_map(1,1, figsize=(5,5))
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax)
# Adding a scale bar to the upper-right corner of the axis, in the same projection as whatever geodata you plotted
scale_bar(ax=ax, location="lower left", style="boxes",
	# each of the follow accepts arguments from a customized style dictionary
		bar = {"projection":3520, "unit":"mi", "length":1.75}, # converting the units to miles, and changing the length of the bar (in inches)
		labels = {"style":"major", "loc":"below"}, # placing a label on each major division, and moving them below the bar
		units = {"loc":"text"}, # changing the location of the units text to the major division labels
		text = {"fontfamily":"monospace"}, # changing the font family of all the text to monospace)
)

matplotlib.pyplot.savefig("./scale_bar_customised.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# inset_map_generic.png
#------------------------------------------------

fig, ax = new_map(1,1, figsize=(5,5))
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax)
# Adding an inset map to the upper-right corner of the axis
iax = inset_map(ax=ax, location="upper right", size=0.75, pad=0.25, xticks=[], yticks=[])

matplotlib.pyplot.savefig("./inset_map_generic.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# inset_map_indicators.png
#------------------------------------------------

fig, ax = new_map(1,2, figsize=(10,5))
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax[0])
states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax[1])
# Adding an inset map to the upper-right corner of the axis
iax0 = inset_map(ax=ax[0], location="upper right", size=1, pad=0.25, xticks=[], yticks=[])
iax1 = inset_map(ax=ax[1], location="upper right", size=0.75, pad=0.25, xticks=[], yticks=[])
# Adding an extent indicator for the map on the left
contiguous.plot(ax=iax0, facecolor="none", edgecolor="black", linewidth=0.5)
indicate_extent(iax0, ax[0], 3857, 3520, pad=0.25)

# Adding a detail indicator for the plot on the left
atl_centroid = shapely.Point(pyproj.Transformer.from_crs(4326, 3520, always_xy=True).transform(-84.40123859860549, 33.75203795433787))
atl_buffer = atl_centroid.buffer(20000)
geopandas.GeoSeries(atl_buffer).plot(ax=iax1, facecolor="none", edgecolor="black")
indicate_detail(ax[1], iax1, 3520, 3520)

matplotlib.pyplot.savefig("./inset_map_indicators.png", bbox_inches="tight")
matplotlib.pyplot.close()