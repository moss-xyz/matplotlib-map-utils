import pygris
import geopandas
import pyproj
import shapely
import contextily
import matplotlib.pyplot
from matplotlib_map_utils.core import north_arrow, scale_bar, ScaleBar, inset_map, indicate_detail, indicate_extent, dual_bars
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

# Making a map of Georgia
fig, ax = new_map(figsize=(10,10))
georgia.buffer(75000).plot(ax=ax, facecolor="none", edgecolor="none") # this helps us "zoom out" a bit
georgia.plot(ax=ax, edgecolor="black", facecolor="none")

# Creating an inset map and extent indicator for the USA
cax = inset_map(ax, "lower right", size=1.75, pad=0.1, xticks=[], yticks=[])
contiguous.plot(ax=cax, facecolor="none", edgecolor="black", linewidth=0.5)
indicate_extent(cax, ax, 3857, 3857)

# Creating an inset map and detail indicator for Atlanta, GA
atl_centroid = shapely.Point(pyproj.Transformer.from_crs(4326, 3857, always_xy=True).transform(-84.40123859860549, 33.75203795433787))
atl_buffer = atl_centroid.buffer(20000)
aax = inset_map(ax, "upper right", size=1.75, pad=0.25, xticks=[], yticks=[])
geopandas.GeoSeries(atl_buffer).plot(ax=aax, facecolor="none", edgecolor="none")
indicate_detail(ax, aax, 3857, 3857, linecolor="cornflowerblue")

# Creating a north arrow
na = north_arrow(ax=ax, location="upper left", scale=0.5, rotation={"degrees":0})

# Creating a scale bar
# sb = scale_bar(ax=ax, style="boxes", location="lower left", bar={"length":2, "projection":3857}, text={"fontsize":8})
db = dual_bars(ax=ax, style="boxes", location="lower left", 
               bar={"rotation":0, "reverse":False, "projection":3857}, 
							 text={"fontsize": 8}, units={"loc":"text"})

# Adding contextily basemaps
contextily.add_basemap(ax, attribution="", source=contextily.providers.CartoDB.Voyager)
contextily.add_basemap(cax, attribution="", source=contextily.providers.CartoDB.VoyagerNoLabels)
contextily.add_basemap(aax, attribution="", source=contextily.providers.CartoDB.Voyager)

matplotlib.pyplot.savefig("./bigmap_w_elements.png", bbox_inches="tight")