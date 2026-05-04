# Packages used by this tutorial
import geopandas # manipulating geographic data
import numpy # creating arrays
import pygris # easily acquiring shapefiles from the US Census
import matplotlib.pyplot # visualization

# Downloading the state-level dataset from pygris
states = pygris.states(cb=True, year=2022, cache=False).to_crs(3857)

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

# Importing the main package
from matplotlib_map_utils import NorthArrow, north_arrow

#------------------------------------------------
# north_arrow_func.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").plot(ax=ax)
# Adding a north arrow to the upper-right corner of the axis, without any rotation (see Rotation under Formatting Components for details)
north_arrow(ax=ax, location="upper right", rotation={"degrees":0})

matplotlib.pyplot.savefig("./north_arrow_func.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# north_arrow_class.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").plot(ax=ax)
# Creating a NorthArrow object that we want to place in the upper-right corner of the axis, 
# without any rotation (see Rotation under Formatting Components for details)
# Note that here, we do not specify the axis
na = NorthArrow(location="upper right", rotation={"degrees":0})
# The NorthArrow can then be added using add_artist(), which calls its built-in draw() function:
ax.add_artist(na)

matplotlib.pyplot.savefig("./north_arrow_class.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# reuse_arrow_ga.png
# reuse_arrow_tx.png
#------------------------------------------------

# Setting up the north arrow artist 
na = NorthArrow(location="upper right", rotation={"degrees":0})

# Setting up plots for both Georgia and Texas
# Note we have to call .copy() EACH TIME
ga_fig, ga_ax = new_map()
states.query("NAME=='Georgia'").plot(ax=ga_ax)
ga_ax.add_artist(na.copy())
matplotlib.pyplot.savefig("./reuse_arrow_ga.png", bbox_inches="tight")

tx_fig, tx_ax = new_map()
states.query("NAME=='Texas'").plot(ax=tx_ax)
tx_ax.add_artist(na.copy())
matplotlib.pyplot.savefig("./reuse_arrow_tx.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# custom_arrow_class.png
#------------------------------------------------

shapes = ["Texas","Georgia","California","Louisiana"]
labels = ["First","Second","Third","Fourth"]
# Creating the initial arrow
na = NorthArrow(location="upper right", rotation={"degrees":0})
# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,s,l in zip(axs.flatten(), shapes, labels):
	states.query(f"NAME=='{s}'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	na.label = {"text":l}
	ax.add_artist(na.copy())

matplotlib.pyplot.savefig("./custom_arrow_class.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# custom_arrow_func.png
#------------------------------------------------

shapes = ["Texas","Georgia","California","Louisiana"]
labels = ["First","Second","Third","Fourth"]
# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,s,l in zip(axs.flatten(), shapes, labels):
	states.query(f"NAME=='{s}'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", label={"text":l}, rotation={"degrees":0})

matplotlib.pyplot.savefig("./custom_arrow_func.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# locations.png
#------------------------------------------------

# Grid of location options
locs = ["upper left", "upper center", "upper right", "center left", "center", "center right", "lower left", "lower center", "lower right"]
fig, axs = new_map(3,3, figsize=(9,9))
for ax,l in zip(axs.flatten(), locs):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location=l, rotation={"degrees":0})

matplotlib.pyplot.savefig("./locations.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# scales.png
#------------------------------------------------

# Modifying the scale
# Recommend looking at the "Setting Size" section of "Tips and Tricks" for another way to do this!
scales = [0.25, 0.5, 1, 2]
# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,s in zip(axs.flatten(), scales):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, scale=s)

matplotlib.pyplot.savefig("./scales.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# zorder.png
#------------------------------------------------

# An example to show changing zorders
zorders = [{"plot":5,"arrow":10}, {"plot":10,"arrow":5}]
# Creating four subplots
fig, axs = new_map(1,2, figsize=(10,5))
for ax,z in zip(axs.flatten(), zorders):
	states.query(f"NAME=='Georgia'").plot(ax=ax, zorder=z["plot"])
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper left", rotation={"degrees":0}, zorder=z["arrow"])

matplotlib.pyplot.savefig("./zorder.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# base.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{"facecolor":"cyan"}, # changing the color
	{"edgecolor":"red"}, # changing the color
	{"linewidth":6}, # changing the stroke
	False # hiding it entirely - note that the shadow is hidden here too, as it is dependent on the base artist for visibility
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, base=m)

matplotlib.pyplot.savefig("./base.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# fancy.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	True, # normal patch
	{"coords":numpy.array([(0.50, 0.85), (0.35, 0.50), (0.50, 0.55), (0.65, 0.50), (0.50, 0.85)])}, # changing the shape
	{"facecolor":"blue"}, # changing the color
	False # hiding it entirely
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, fancy=m)

matplotlib.pyplot.savefig("./fancy.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# label.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{"text": "North"}, # changing the text
	{"position": "left"}, # changing the position
	{"fontsize": 30}, # changing the size
	{"fontfamily": "cursive"}, # changing the family
	{"color": "cyan"}, # changing the color of the text
	{"stroke_width": 5, "stroke_color": "red"}, # changing the stroke size and color
	{"rotation": 30}, # changing the rotation
	False # hiding it entirely
]

# Creating eight subplots
fig, axs = new_map(2,4, figsize=(20,10))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, label=m)

matplotlib.pyplot.savefig("./label.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# shadow.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{"offset": (4, -4)}, # changing the offset
	{"offset": (4, 4)}, # changing the offset
	{"offset": (-4, 4)}, # changing the offset
	{"offset": (-4, -4)}, # changing the offset
	{"alpha": 0.2}, # changing the transparency
	{"alpha": 0.8}, # changing the transparency
	{"shadow_rgbFace": "red"}, # changing the color
	False # hiding it entirely
]
# Creating eight subplots
fig, axs = new_map(2,4, figsize=(20,10))
for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, shadow=m)

matplotlib.pyplot.savefig("./shadow.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# pack.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	None, # default settings
	{"sep": 15}, # increased separation between items
	{"align": "left"}, # changing the alignment of items
	{"width": 100, "height": 200, "mode": "expand"}, # changing the mode, not a great example
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, pack=m)

matplotlib.pyplot.savefig("./pack.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# aob.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{"facecolor": "black"}, # different facecolor
	{"edgecolor": "red"}, # different edgecolor
	# these two show the difference between pad and borderpad
	{"edgecolor": "red", "pad": 3}, # increased pad
	{"edgecolor": "red", "borderpad": 3}, # increased borderpad
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	north_arrow(ax=ax, location="upper right", rotation={"degrees":0}, aob=m)

matplotlib.pyplot.savefig("./aob.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# set_size.png
#------------------------------------------------

# Creating an empty plot - for reference, this is 10 inches x 5 inches
fig, ax = new_map(1,1, figsize=(10,5))

# Visualizing the different sizes at various positions
for l,s in zip([0.1, 0.2, 0.35, 0.55, 0.85], ["xs","sm","md","lg","xl"]):
	# Using the size parameter to set the size directly
	north_arrow(ax=ax, size=s, location="center", label={"text":s}, rotation={"degrees":0}, aob={"bbox_to_anchor":(l, 0.5), "bbox_transform":ax.transAxes})

matplotlib.pyplot.savefig("./set_size.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# external_placement.png
#------------------------------------------------

fig, ax = new_map()
states.query("NAME=='Georgia'").plot(ax=ax)
north_arrow(ax=ax, size="sm", location="upper left", rotation={"degrees":0}, aob={"bbox_to_anchor":(1.05,1), "bbox_transform":ax.transAxes})

matplotlib.pyplot.savefig("./external_placement.png")
matplotlib.pyplot.close()