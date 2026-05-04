# Packages used by this tutorial
import geopandas # manipulating geographic data
import shapely # manipulating geometries
import pygris # easily acquiring shapefiles from the US Census
import matplotlib.pyplot # visualization

# Downloading the state-level dataset from pygris
# states = pygris.states(cb=True, year=2022, cache=False).to_crs(3857)
states = geopandas.read_file("../../../matplotlib_map_utils/scratch/states.gpkg").to_crs(3857)

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

# Using the USA utility within this package to help filter data
from matplotlib_map_utils.utils import USA
usa = USA()
# Filtering based on FIPS codes
contiguous = states.query(f"GEOID in {usa.filter_contiguous(True)}")
puerto_rico = states.query(f"GEOID == '{usa.filter_abbr("PR")}'").to_crs(4437)
washington_dc = states.query(f"GEOID == '{usa.filter_abbr("DC")}'")
alaska = states.query(f"GEOID == '{usa.filter_abbr("AK")}'").to_crs(3467)
hawaii = states.query(f"GEOID == '{usa.filter_abbr("HI")}'").to_crs(4135)
# optional; just selecting the largest islands of Hawaii
hawaii.geometry = [shapely.MultiPolygon([g for g in hawaii.iloc[0].geometry.geoms if g.area>1e-3])]

from matplotlib_map_utils import InsetMap, inset_map, ExtentIndicator, indicate_extent, DetailIndicator, indicate_detail
from matplotlib_map_utils import config

#------------------------------------------------
# usa_w_alaska_func.png
#------------------------------------------------

# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA
contiguous.plot(ax=ax)

# Adding an inset map to the plot
iax = inset_map(ax, location="lower left", imsize=0.8, pad=0.1, xticks=[], yticks=[])
# Plotting alaska in the inset map
alaska.plot(ax=iax)

matplotlib.pyplot.savefig("./usa_w_alaska_func.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# usa_w_hawaii_class.png
#------------------------------------------------

# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA
contiguous.plot(ax=ax)

# Creating an InsetMap object that we want to place in the lower-right corner of the axis, 
# Note that here, we do not specify the "parent" axis (ax)
# Note that we also tell it what data we are going to want to plot there, but this is optional!
im = InsetMap("lower left", imsize=0.8, pad=0.1, to_plot={"data":hawaii}, xticks=[], yticks=[])
# The InsetMap can then be added using create()
# Note that this is DIFFERENT than NorthArrow and ScaleBar objects, which rely on add_artist()!
iax = im.create(ax)

matplotlib.pyplot.savefig("./usa_w_hawaii_class.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# location_grid.png
#------------------------------------------------

# Grid of location options
locs = ["upper left", "upper center", "upper right", "center left", "center", "center right", "lower left", "lower center", "lower right"]
# Creating a 9x9 grid of maps
fig, axs = new_map(3,3, figsize=(9,9))
for ax,l in zip(axs.flatten(), locs):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim") # this is just making things square-ish for us
	ax.set_title(l)
	# Creating the inset map at our specified location
	inset_map(ax=ax, location=l, imsize=0.5, pad=0.05, xticks=[], yticks=[])

matplotlib.pyplot.savefig("./location_grid.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# size_padding.png
#------------------------------------------------

# Changing size and padding
modifications = [
	{"imsize":0.25,"pad":0},
	{"imsize":0.5,"pad":0},
	{"imsize":0.25, "pad":0.25},
]
fig, axs = new_map(1,3, figsize=(9,3))
for ax,l,m in zip(axs.flatten(), locs, modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim") # this is just making things square-ish for us
	ax.set_title(m, fontsize=10)
	inset_map(ax=ax, location="upper right", **m, xticks=[], yticks=[])

matplotlib.pyplot.savefig("./size_padding.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# zorder.png
#------------------------------------------------

# An example to show changing zorders
zorders = [{"plot":5,"inset":10}, {"plot":10,"inset":5}]
# Creating four subplots
fig, axs = new_map(1,2, figsize=(10,5))
for ax,z in zip(axs.flatten(), zorders):
	states.query(f"NAME=='Georgia'").plot(ax=ax, zorder=z["plot"])
	ax.set_aspect(1, adjustable="datalim")
	inset_map(ax=ax, location="upper left", imsize=1, pad=0.05, xticks=[], yticks=[], zorder=z["inset"])

matplotlib.pyplot.savefig("./zorder.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# locations.png
#------------------------------------------------

fig, axs = new_map(1,3, figsize=(9,3))
for ax,l,m in zip(axs.flatten(), locs, modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim") # this is just making things square-ish for us

# First, a default for comparison
inset_map(ax=axs[0], location="upper right", imsize=0.8, pad=0.05, xticks=[], yticks=[])
# Placing the upper right corner of the inset axes in the middle of the map
inset_map(ax=axs[1], location="upper right", imsize=0.8, pad=0.05, coords=(0.5,0.5), xticks=[], yticks=[])
# Placing the upper left corner of the inset axes on Atlanta, GA, using ax.transData
inset_map(ax=axs[2], location="upper left", imsize=0.8, pad=0.05, coords=(-9353446,4007500), transform=axs[2].transData, xticks=[], yticks=[])

matplotlib.pyplot.savefig("./locations.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# to_plot.png
#------------------------------------------------

# This block will show how to re-use and plot data on an inset map
# One common use-case for this would be displaying a map of the US as you plot multiple individual US states

# Defining the inset map
im = InsetMap("lower left", imsize=0.8, pad=0.05, xticks=[], yticks=[], 
							to_plot=[{"data":contiguous, "kwargs":{"facecolor":"red"}}])

# Creating 1x3 subplots
fig, axs = new_map(1,4, figsize=(15,3))
# Now we define the different states
state_names = ["Georgia","Texas","Pennsylvania","Illinois"]
# Iterating through
for ax,s in zip(axs, state_names):
	states.query(f"NAME=='{s}'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")

# I'm specifying this as a separate function call/loop to ensure the sizes of the inset maps are consistent
# Otherwise, the constant re-calculation makes different sizes for each one
for ax in axs:
	im.create(ax)

matplotlib.pyplot.savefig("./to_plot.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# kwargs.png
#------------------------------------------------

# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA
contiguous.plot(ax=ax)

# Adding an inset map to the plot with some kwargs for xticks, yticks, and facecolor
iax = inset_map(ax, location="lower left", imsize=0.8, pad=0.1, xticks=[], yticks=[], facecolor="red")
# Plotting alaska in the inset map
alaska.plot(ax=iax)

matplotlib.pyplot.savefig("./kwargs.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# multiple_insets.png
#------------------------------------------------

# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA
contiguous.plot(ax=ax)

# Adding multiple inset maps to the plot
# Also using facecolor so you can see which is which
iax = inset_map(ax, location="lower left", imsize=0.25, pad=0.1, xticks=[], yticks=[], facecolor="red") 
iax = inset_map(ax, location="lower right", imsize=0.25, pad=0.1, xticks=[], yticks=[], facecolor="blue")
iax = inset_map(ax, location="center right", imsize=0.25, pad=0.1, xticks=[], yticks=[], facecolor="green")

matplotlib.pyplot.savefig("./multiple_insets.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# usa_w_all.png
#------------------------------------------------

from matplotlib_map_utils import inset_usa

# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA
contiguous.plot(ax=ax)

# Creating all the axes at once
# Note that each of the 4 states can be turned off individually!
aax, hax, pax, dax = inset_usa(ax, alaska=True, hawaii=True, dc=True, puerto_rico=True, imsize=0.4, pad=0.05, xticks=[], yticks=[], box_aspect=1)

alaska.plot(ax=aax)
hawaii.plot(ax=hax)
puerto_rico.plot(ax=pax)
washington_dc.plot(ax=dax)

matplotlib.pyplot.savefig("./usa_w_all.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# inset_graph.png
#------------------------------------------------

import mapclassify
import matplotlib
# Setting up the main plot
fig, ax = new_map()
# Plotting the contiguous USA, and shading by land area
contiguous.plot(ax=ax, column="ALAND", edgecolor="black", linewidth=0.5, 
            cmap="Blues", scheme="fisherjenks", classification_kwds={"k":5})

# Adding an axis to handle a graph below
# Don't worry too much about this code, it is quite messy and could be done better, but it should illustrate what is possible
jenks_land = mapclassify.FisherJenks(contiguous["ALAND"], k=5)
gax = inset_map(ax, location="lower left", imsize=(1.1,0.3), pad=(0.25,0.5))
gax.tick_params(labelsize=4)
gax.bar(x=range(5), height=jenks_land.counts, color=matplotlib.colormaps["Blues"]([0,0.25,0.50,0.75,1]), 
    tick_label=["{:.0e}".format(b) for b in jenks_land.bins], edgecolor="black", linewidth=0.5)

matplotlib.pyplot.savefig("./inset_graph.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# set_size.png
#------------------------------------------------

# For reference, this is 5 inches x 10 inches
fig, ax = new_map(1,1, figsize=(10,5))
# Visualizing three different sizes at various positions
for s,l in zip(["xs","sm","md"], ["center left", "center", "center right"]):
	# Calling the function to update the defaults
	# Note the function exists on the CLASS, but impacts both the class and function
	inset_map(ax=ax, location=l, size=s, xticks=[], yticks=[])

# Resetting the sizes
config.DEFAULT_SIZE = "sm"

matplotlib.pyplot.savefig("./set_size.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# extent_indicator.png
#------------------------------------------------

# Defining the inset map
im = InsetMap("upper right", imsize=1, pad=0.05, xticks=[], yticks=[], to_plot=[{"data":contiguous}])

# Creating a plot of Georgia
fig, ax = new_map(1,1, figsize=(5,5))
states.query(f"NAME=='Georgia'").plot(ax=ax)

# Plotting the inset map
iax = im.create(ax)

# Creating the extent indicator, which appears by-default as a red square on the map
indicate_extent(iax, ax, 3857, 3857)

matplotlib.pyplot.savefig("./extent_indicator.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# extent_indicator_custom.png
#------------------------------------------------

# Setting up an inset map
im = InsetMap(location="upper right", imsize=0.75, pad=0.05, xticks=[], yticks=[], to_plot=[{"data":contiguous}])
# What will be changed for each extent indicator
modifications = [
	{}, # default for comparison
	{"facecolor":"black"},
	{"alpha":0}, # making the facecolor invisible
	{"pad":0.25}, # extra padding
	{"straighten":False}, # turning straighten off
]
fig, axs = new_map(1,5, figsize=(15,3))
for ax,m in zip(axs.flatten(), modifications):
	# Note that here I am intentionally plotting Colorado with an incorrect CRS, to show the effects of straighten
	states.query(f"NAME=='Colorado'").to_crs(2240).plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim") # this is just making things square-ish for us
	ax.set_title(m, fontsize=10)
	iax = im.create(ax) # creating the inset map
	indicate_extent(iax, ax, 3857, 2240, **m)

matplotlib.pyplot.savefig("./extent_indicator_custom.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# detail_indicator_extent.png
#------------------------------------------------

# Defining the inset map, which will be of Washington, DC (!)
im = InsetMap("lower right", imsize=0.5, pad=0.05, xticks=[], yticks=[], to_plot=[{"data":washington_dc}])

# Creating a plot of the contiguous US
fig, ax = new_map(1,1, figsize=(5,5))
contiguous.plot(ax=ax)

# Plotting the inset map
iax = im.create(ax)

# Creating the extent indicator, which appears by-default as a red square on the map
# note we've added some padding to make it more visible
indicate_extent(ax, iax, 3857, 3857, pad=3)

matplotlib.pyplot.savefig("./detail_indicator_extent.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# detail_indicator.png
#------------------------------------------------

# The code below is the same, except for the very last function
im = InsetMap("lower right", imsize=0.5, pad=0.05, xticks=[], yticks=[], to_plot=[{"data":washington_dc}])

fig, ax = new_map(1,1, figsize=(5,5))
contiguous.plot(ax=ax)

iax = im.create(ax)

# Creating the detail indicator, which appears slightly differently to an extent indicator
indicate_detail(ax, iax, 3857, 3857, pad=3)

matplotlib.pyplot.savefig("./detail_indicator.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# detail_indicator_custom.png
#------------------------------------------------

# Setting up an inset map
im = InsetMap("lower left", imsize=0.5, pad=0.05, xticks=[], yticks=[], to_plot=[{"data":states.query("NAME=='Georgia'")}])

# What will be changed for each extent indicator
modifications = [
	{}, # default for comparison
	{"facecolor":"black", "alpha":0.25},
	{"linecolor":"red"},
	{"linewidth":2},
]

fig, axs = new_map(1,4, figsize=(12,3))

for ax,m in zip(axs.flatten(), modifications):
	# Note that here I am intentionally plotting Colorado with an incorrect CRS, to show the effects of straighten
	contiguous.plot(ax=ax)
	ax.set_title(m, fontsize=10)
	iax = im.create(ax) # creating the inset map
	indicate_detail(ax, iax, 3857, 3857, **m)

matplotlib.pyplot.savefig("./detail_indicator.png", bbox_inches="tight")
matplotlib.pyplot.close()