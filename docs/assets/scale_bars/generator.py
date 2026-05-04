# Packages used by this tutorial
import geopandas # manipulating geographic data
import numpy # creating arrays
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

# Importing the main package
from matplotlib_map_utils import ScaleBar, scale_bar

#------------------------------------------------
# scale_bar_func.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").plot(ax=ax)
# Adding a scale_bar to the upper-right corner of the axis - note that bar['projection'] MUST be set for this to work
scale_bar(ax=ax, location="upper right", style="boxes", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"})

matplotlib.pyplot.savefig("./scale_bar_func.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# scale_bar_class.png
#------------------------------------------------

# Setting up a plot
fig, ax = new_map()
# Plotting a state (Georgia)
states.query("NAME=='Georgia'").plot(ax=ax)
# Creating a ScaleBar object that we want to place in the upper-right corner of the axis, 
# Note that here, we do not specify the axis
sb = ScaleBar(location="upper right", style="ticks", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"})
# The ScaleBar can then be added using add_artist(), which calls its built-in draw() function:
ax.add_artist(sb)

matplotlib.pyplot.savefig("./scale_bar_class.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# reuse_bar_ga.png
# reuse_bar_tx.png
#------------------------------------------------

# Setting up the scale bar artist 
sb = ScaleBar(location="upper right", style="boxes", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"})

# Setting up plots for both Georgia and Texas
ga_fig, ga_ax = new_map()
states.query("NAME=='Georgia'").plot(ax=ga_ax)
ga_ax.add_artist(sb.copy())
matplotlib.pyplot.savefig("./reuse_bar_ga.png", bbox_inches="tight")

tx_fig, tx_ax = new_map()
states.query("NAME=='Texas'").plot(ax=tx_ax)
tx_ax.add_artist(sb.copy())
matplotlib.pyplot.savefig("./reuse_bar_tx.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# custom_bar_class.png
#------------------------------------------------

shapes = ["Texas","Georgia","California","Louisiana"]
# What we'll be updating
families = ["serif", "cursive", "fantasy", "monospace"]
# Creating the initial bar
sb = ScaleBar(location="upper right", style="boxes", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"})
# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,s,f in zip(axs.flatten(), shapes, families):
	states.query(f"NAME=='{s}'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	sb.text = {"fontfamily":f}
	ax.add_artist(sb.copy())

matplotlib.pyplot.savefig("./custom_bar_class.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# custom_bar_func.png
#------------------------------------------------

shapes = ["Texas","Georgia","California","Louisiana"]
families = ["serif", "cursive", "fantasy", "monospace"]
# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,s,f in zip(axs.flatten(), shapes, families):
	states.query(f"NAME=='{s}'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="upper right", style="boxes", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"}, text={"fontfamily":f})

matplotlib.pyplot.savefig("./custom_bar_func.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# bar_length.png
#------------------------------------------------

# Creating three identical bars using the four different methods
# Grid of location options
# Note that the "center" options will feel slightly off: this is because the the center of the scale bar is of the entire artist, text included, not just the bar itself
bar_lengths = [
	{"length":0.5}, # this bar will be ~50% of the axis
	{"length":2}, # this bar will be ~2.5 inches
	{"max":300, "major_div":3}, # this bar will be 300 km (because EPSG:3857 is in meters)
	{"major_mult":100, "major_div":3}, # this bar will be 300 km (100 * 3 = 300)
]

fig, axs = new_map(1,4, figsize=(20,5))

for ax,l in zip(axs.flatten(), bar_lengths):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="boxes", bar={"projection":3857,"minor_type":"none"} | l, labels={"style":"first_last"})

matplotlib.pyplot.savefig("./bar_length.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# locations.png
#------------------------------------------------

# Do not worry about this: it is covered later, it is simply updating the default size of the scale bar to xs
# ScaleBar.set_size() is no longer needed — pass size= directly instead
# Grid of location options
# Note that the "center" options will feel slightly off: this is because the the center of the scale bar is of the entire artist, text included, not just the bar itself
locs = ["upper left", "upper center", "upper right", "center left", "center", "center right", "lower left", "lower center", "lower right"]
fig, axs = new_map(3,3, figsize=(9,9))
for ax,l in zip(axs.flatten(), locs):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, size="xs", location=l, style="boxes", bar={"projection":3857,"minor_type":"none"}, labels={"style":"first_last"})

matplotlib.pyplot.savefig("./locations.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# styles.png
#------------------------------------------------

# Just reverting the change I made above; again this is explained later, don't worry about it for now
# (No longer needed: we pass size= directly now)
# Modifying the styles
styles = ["boxes","ticks"]
# Creating 1x2 subplots
fig, axs = new_map(1,2, figsize=(10,5))
for ax,s in zip(axs.flatten(), styles):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style=s, 
				bar={"projection":3857,"minor_type":"none","length":0.5}, labels={"style":"first_last"})

matplotlib.pyplot.savefig("./styles.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# zorder.png
#------------------------------------------------

# An example to show changing zorders
zorders = [{"plot":5,"scale":10}, {"plot":10,"scale":5}]
# Creating four subplots
fig, axs = new_map(1,2, figsize=(10,5))
for ax,z in zip(axs.flatten(), zorders):
	states.query(f"NAME=='Georgia'").plot(ax=ax, zorder=z["plot"])
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="upper left", 
				bar={"projection":3857,"minor_type":"none","length":0.5}, labels={"style":"first_last"}, zorder=z["scale"])

matplotlib.pyplot.savefig("./zorder.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# bar.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{}, # default settings for comparison
	{"unit":"yd"}, # converting units
	{"rotation":90}, # making the bar vertical
	{"height":0.5}, # increasing the height
	{"reverse":True}, # reversing the order of the bar
	{"minor_type":"all"}, # adding minor divisions
	{"length":0.2}, # shortening the bar
	{"length":None,"max":400,"major_div":4,"minor_div":2,"minor_type":"first"}, # setting all the bar divisions
]
# Creating 2x4 subplots
fig, axs = new_map(2,4, figsize=(20,10))
for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="boxes", labels={"style":"first_last"},
			bar={"projection":3857,"minor_type":"none","length":0.5} | m) # this line just concatenates the two dictionaries together

matplotlib.pyplot.savefig("./bar.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# bar_boxes.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{}, # default settings for comparison
	{"facecolors":["red","blue"]}, # changing the colors of the divisions
	{"edgecolors":["red","yellow"]}, # changing the colors of the edges
	# NOTE: I do think this changes the length of the bar which I don't love, so large values not recommended (relative to plot size)
	{"edgewidth":5}, # changing the width of the edges 
]
# Creating 1x4 subplots
fig, axs = new_map(1,4, figsize=(20,5))
for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="boxes", labels={"style":"first_last"},
				bar={"projection":3857,"minor_type":"none","length":0.5} | m) # this line just concatenates the two dictionaries together

matplotlib.pyplot.savefig("./bar_boxes.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# bar_ticks.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{}, # default settings for comparison
	# Iterating through the three tick locations
	{"tick_loc":"above"},
	{"tick_loc":"below"},
	{"tick_loc":"middle"},
	# Iterating through the other settings
	{"minor_frac":0.25}, # the default value is 0.66
	{"basecolors":["red","blue"]}, # changing the colors of the divisions
	{"tickcolors":["red","yellow"]}, # changing the colors of the edges
	{"tickwidth":5}, # changing the width of the edges 
]
# Creating 2x4 subplots
fig, axs = new_map(2,4, figsize=(20,10))
for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="ticks", labels={"style":"first_last"},
				bar={"projection":3857,"minor_type":"all","length":0.5} | m) # this line just concatenates the two dictionaries together

matplotlib.pyplot.savefig("./bar_ticks.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# labels_style.png
#------------------------------------------------

# Creating 2x5 subplots
fig, axs = new_map(2,5, figsize=(25,10))
# Now we define the different label settings
modifications = [
	# Iterating through the label styles
	{"style":"major"},
	{"style":"first_last"},
	{"style":"last_only"},
	{"style":"minor_all"},
	{"style":"minor_first"},
]
# We'll first iterate through each of the two minor_types
for axc,t in zip(axs, ["all","first"]):
	for ax,m in zip(axc, modifications):
		states.query(f"NAME=='Georgia'").plot(ax=ax, color="white")
		ax.set_aspect(1, adjustable="datalim")
		scale_bar(ax=ax, location="center", style="ticks", labels={"fontsize":6} | m, 
						bar={"projection":3857,"max":500,"major_div":2,"minor_div":5,"minor_type":t})
		ax.set_title(m["style"])

matplotlib.pyplot.savefig("./labels_style.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# labels.png
#------------------------------------------------

# Creating 2x5 subplots
fig, axs = new_map(2,5, figsize=(25,10))
# Now we define the different label settings
modifications = [
	# Iterating through the label styles
	{"style":"major"},
	{"style":"first_last"},
	{"style":"last_only"},
	{"style":"minor_all"},
	{"style":"minor_first"},
]
# We'll first iterate through each of the two minor_types
for axc,t in zip(axs, ["all","first"]):
	for ax,m in zip(axc, modifications):
		states.query(f"NAME=='Georgia'").plot(ax=ax, color="white")
		ax.set_aspect(1, adjustable="datalim")
		scale_bar(ax=ax, location="center", style="ticks", labels={"fontsize":6} | m, 
						bar={"projection":3857,"max":500,"major_div":2,"minor_div":5,"minor_type":t})
		ax.set_title(m["style"])

matplotlib.pyplot.savefig("./labels_style.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# units_locations.png
#------------------------------------------------

# This block will show the different label locations
# Creating 1x3 subplots
fig, axs = new_map(1,3, figsize=(15,5))
# Now we define the different label settings
modifications = [
	# Iterating through the label locations
	{"loc":"bar"},
	{"loc":"text"},
	{"loc":"opposite"}, # this one looks best when bar["minor_type"] = "last_only"
]
# We'll first iterate through each of the two minor_types
for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax, color="white")
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="ticks", labels={"style":"first_last"}, units=m,
							bar={"projection":3857,"max":300,"major_div":3,"minor_div":1,"minor_type":"none"})
	ax.set_title(m["loc"])

matplotlib.pyplot.savefig("./units_locations.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# units.png
#------------------------------------------------

# Modifying other elements
modifications = [
    {}, # default for comparison
    {"label":"kilometer"},
    {"textcolor":"red"}, # changing the color of the units label, without affecting the other lables
    {"rotation":-45},
]

# Creating 1x4 subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="ticks", labels={"style":"major"}, units=m, # changed the style to major here
					bar={"projection":3857,"max":300,"major_div":3,"minor_div":1,"minor_type":"none"})

matplotlib.pyplot.savefig("./units.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# text.png
#------------------------------------------------

# Modifying specific elements
modifications = [
	{}, # default settings
	{"fontsize": 16}, # increased size
	{"fontweight": "bold"}, # different weight
	{"stroke_color": "black", "stroke_width":3, "textcolor": "white"}, # changing the mode, not a great example
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="center", style="ticks", labels={"style":"major"}, text=m,
					bar={"projection":3857,"max":300,"major_div":3,"minor_div":1,"minor_type":"none"})

matplotlib.pyplot.savefig("./text.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# aob.png
#------------------------------------------------

# Modifying specific elements

modifications = [
	{"facecolor": "lightgrey"}, # different facecolor
	{"edgecolor": "red"}, # different edgecolor; note that this automatically sets the facecolor to white
	# these two show the difference between pad and borderpad
	{"edgecolor": "red", "pad": 3}, # increased pad
	{"edgecolor": "red", "borderpad": 3}, # increased borderpad, which is "invisible" relative to where the edge is
]

# Creating four subplots
fig, axs = new_map(1,4, figsize=(20,5))

for ax,m in zip(axs.flatten(), modifications):
	states.query(f"NAME=='Georgia'").plot(ax=ax)
	ax.set_aspect(1, adjustable="datalim")
	scale_bar(ax=ax, location="upper right", style="ticks", labels={"style":"major"}, aob=m, # using location="upper right" to illustrate borderpad
					bar={"projection":3857,"max":300,"major_div":3,"minor_div":1,"minor_type":"none"})

matplotlib.pyplot.savefig("./aob.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# matplotlib_scalebar.png
#------------------------------------------------

fig, ax = new_map(1,1, figsize=(5,5))

# Plotting the a state
states.query(f"NAME=='Georgia'").plot(ax=ax)

# Setting up the scale bar
scale_bar(ax=ax, location="upper right", style="boxes",
			bar={"projection":3857,"max":100,"major_div":1,"minor_div":1,"minor_type":"none"},
			labels={"style":"last_only","loc":"below","fontsize":8}, units={"loc":"text"},
			aob={"facecolor":"whitesmoke","edgecolor":"none","pad":0.5,"borderpad":0.5})

matplotlib.pyplot.savefig("./matplotlib_scalebar.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# set_size.png
#------------------------------------------------

# For reference, this is 5 inches x 10 inches
fig, ax = new_map(1,1, figsize=(5,10))

# Plotting the a state
states.query(f"NAME=='California'").plot(ax=ax)

# Visualizing three different sizes at various positions
for s,l in zip(["sm","md","lg"], ["upper center", "center", "lower center"]):
	# Calling the function to update the defaults
	scale_bar(ax=ax, size=s, location=l, style="boxes", labels={"style":"major"}, 
					bar={"projection":3857,"max":900,"major_div":3,"minor_div":1,"minor_type":"none"})

# No need to reset sizes - the size= parameter handles it per-call

matplotlib.pyplot.savefig("./set_size.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# external_placement.png
#------------------------------------------------

fig, ax = new_map()

states.query("NAME=='Georgia'").plot(ax=ax)

scale_bar(ax=ax, location="upper center", style="boxes", labels={"style":"major"}, 
            bar={"projection":3857,"max":500,"major_div":5,"minor_div":1,"minor_type":"none"}, 
            aob={"bbox_to_anchor":(0.5,-0.01), "bbox_transform":ax.transAxes})

matplotlib.pyplot.savefig("./external_placement.png")
matplotlib.pyplot.close()

#------------------------------------------------
# dual_bars.png
#------------------------------------------------

# Using dual_bars()
from matplotlib_map_utils import dual_bars

fig, ax = new_map(1,1, figsize=(5,5))
_ = states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax)

# Note that this handles the flipping of the ticks and labels automatically!
dual_bars(ax=ax, draw=True, style="ticks", location="center", 
		# For these settings, the first item in the list will apply to the top bar, and the second to the bottom
		units_dual=["km","mi"], bar_maxes=[300,200], major_divs=[3,4], minor_divs=[1,1], # you could set bar_length=[x,y] here too
		# These settings are shared among all the bars
		bar={"projection":3520,"rotation":0,"reverse":False,"minor_type":"none"},
		labels={"style":"major"},
		units={"loc":"text"}, 
		text={"stroke_width":1,"stroke_color":"white","fontsize":"xx-small"},
		# These settings are for the V/HPacker (see the manual example)
		sep=1.5, pad=0)

matplotlib.pyplot.savefig("./dual_bars.png", bbox_inches="tight")
matplotlib.pyplot.close()

#------------------------------------------------
# dual_manual.png
#------------------------------------------------

# Manual version
import matplotlib.offsetbox

fig, ax = new_map(1,1, figsize=(5,5))
_ = states.query("NAME=='Georgia'").to_crs(3520).plot(ax=ax)

# First the bar showing kilomtres
km = scale_bar(ax=ax, draw=False, return_aob=False, style="ticks", location="center",
					bar={"projection":3520,"unit":"km","max":300,"major_div":3,"minor_div":1,
											"rotation":0,"reverse":False,"minor_type":"none"},
					labels={"style":"major"},
					units={"loc":"text"}, 
					text={"stroke_width":1,"stroke_color":"white","fontsize":"xx-small"})

# Then the bar showing miles
# Note that I have to MANUALLY change the location of the ticks and the lables
mi = scale_bar(ax=ax, draw=False, return_aob=False, style="ticks", location="center",
					bar={"projection":3520,"unit":"mi","max":200,"major_div":4,"minor_div":1,
											"rotation":0,"reverse":False,"minor_type":"none","tick_loc":"below"},
					labels={"style":"major","loc":"below"},
					units={"loc":"text"}, 
					text={"stroke_width":1,"stroke_color":"white","fontsize":"xx-small"})

# Now, placing each OffsetImage inside of a VPacker
pack = matplotlib.offsetbox.VPacker(children=[km,mi], align="left", pad=0, sep=1.5)
# And placing that into an AnchoredOffsetBox
aob = matplotlib.offsetbox.AnchoredOffsetbox(loc="center", child=pack, frameon=False)
# And drawing it onto the axis
_ = ax.add_artist(aob)

matplotlib.pyplot.savefig("./dual_manual.png", bbox_inches="tight")
matplotlib.pyplot.close()