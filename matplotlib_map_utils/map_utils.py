# Importing other packages
import json
import re
import math
import os 
os.environ["USE_PYGOES"] = "0"
import requests
import geopandas 
import shapely 
import pandas 
import numpy
import matplotlib
import matplotlib.pyplot
import matplotlib.patches
import matplotlib.patheffects
import matplotlib_scalebar.scalebar
import mpl_toolkits.axes_grid1.axes_divider
import adjustText
import rasterio
import rasterio.mask
import rasterio.enums
import osgeo.gdal

# Start a normal map with a single plot
def init_map(subplots=(1,1), figsize=(10,15), dpi=300, ticks=False, bg="white"):
    # Starting the fig and ax
    fig, ax = matplotlib.pyplot.subplots(subplots[0], subplots[1], figsize=figsize, dpi=dpi)
    # Hiding ticks if we don't want them
    if ticks == False:
        ax.set_xticks([])
        ax.set_yticks([])
    if bg:
        fig.patch.set_facecolor(bg)
    # Returning the fig and the ax
    return fig, ax

# Start a normal map with multiple plots
# Subplots is in (rows, column) format, but figsize is in (width, length) :(
def init_maps(subplots=(2,2), figsize=(10,15), dpi=300, ticks=False, bg="white", sharex=False, sharey=False):
    # Starting the fig and ax
    fig, axs = matplotlib.pyplot.subplots(subplots[0], subplots[1], figsize=figsize, dpi=dpi, sharex=sharex, sharey=sharey)
    # Hiding ticks if we don't want them
    if ticks == False:
        for ax in axs.flatten():
            ax.set_xticks([])
            ax.set_yticks([])
    if bg:
        fig.patch.set_facecolor(bg)
    # Returning the fig and the ax
    return fig, axs

# Add a north arrow
# I THINK because we use ax.transAxes, loc is expressed in fraction of the axes (bottom left is 0,0 and top right is 1,1)
# AND radius is a fraction of the axis as well: so 0.05 would mean it is 5% of the axes "long" and "wide", leading to a given shape
# def north_arrow(ax, r, loc=(0.94,0.94), color="black", fontcolor="white", fontsize=8, zorder=99):
#     north_arrow = matplotlib.patches.RegularPolygon(loc, 3, radius=r, color="black", transform=ax.transAxes, zorder=zorder-1)
#     ax.add_patch(north_arrow)
#     ax.text(x=north_arrow.xy[0], y=north_arrow.xy[1], s='N', ha="center", va="center", fontsize=fontsize, color=fontcolor, transform=ax.transAxes, zorder=zorder)

# Add a scale bar
def scale_bar(ax, location="upper left", scale_format=None, **kwargs):
    if scale_format:
        ax.add_artist(matplotlib_scalebar.scalebar.ScaleBar(1, location=location, scale_formatter=lambda v,l: f"{v}{scale_format}", **kwargs))
    else:
        ax.add_artist(matplotlib_scalebar.scalebar.ScaleBar(1, location=location, **kwargs))

# Add an arbitrary colorbar
# TODO: work for arbitrary colormaps, not just named ones
# TODO: figure out how to do this for "left" or "right"?
# Seems that the main issue is when the figure still has room to grow in a given dimension
# Could also do like: https://matplotlib.org/stable/users/explain/axes/colorbar_placement.html#colorbar-placement
def color_bar(ax, fig, cmap, vmin, vmax, label, cax_kwargs):
    divider = mpl_toolkits.axes_grid1.axes_divider.make_axes_locatable(ax)
    cax = divider.append_axes("bottom", size="5%", pad=0.1)
    cax.set_axis_off()
    cmap = matplotlib.cm.get_cmap(cmap)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    fig.colorbar(matplotlib.cm.ScalarMappable(norm, cmap), ax=cax, location="bottom", label=label)

# Create legend elements
# Expects a LIST of dictionaries with 3 values: label, type (patch or point or line), and kwargs to format it
# example: [{"type":"s", "label":"Example Label", "kwargs":{"color":"tab:blue"}}]
def legend(ax, elements):
    for_legend = []
    for e in elements:
        if e["type"] == "patch" or e["type"] == "s":
            ele = matplotlib.patches.Patch(label=e["label"], **e["kwargs"])
        elif e["type"] == "point" or e["type"] == "p":
            ele = matplotlib.lines.Line2D([0], [0], color="none", label=e["label"], **e["kwargs"])
        elif e["type"] == "line" or e["type"] == "l":
            ele = matplotlib.lines.Line2D([0], [0], label=e["label"], **e["kwargs"])
        else:
            print("Error: invalid type")
            ele = matplotlib.patches.Patch(label=e["label"])
        for_legend.append(ele)
    return for_legend

# Add text labels
def label_points(ax, gdf, col, wrap=None, size=None, format={}, color="white", stroke="black", alignment=("center","center"), shift=(0,0), override=None, mask=False, adjust=False, adjust_kwargs={}):
    # List to hold all of our eventual text objects
    texts = []
    if mask:
        xmin,xmax = ax.get_xlim()
        ymin,ymax = ax.get_ylim()
        bbox = shapely.box(xmin, ymin, xmax, ymax)
        gdf_to_label = gdf.cx[xmin:xmax, ymin:ymax].copy()
        gdf_to_label["geometry"] = gdf_to_label.intersection(bbox).copy()
    else:
        gdf_to_label = gdf.copy()
    # Iterating through each provided point
    for i,r in gdf_to_label.iterrows():
        x = r["geometry"].centroid.x + shift[0]
        y = r["geometry"].centroid.y + shift[1]
        label = r[col]
        # If we want to wrap our labels (only a certain # of words per line)
        if wrap:
            words = label.split(" ")
            label = ""
            for j,w in enumerate(words):
                label += w
                if j+1 == len(words):
                    pass
                elif ((j+1) % wrap == 0):
                    label += "\n"
                else:
                    label += " "
        # If we need to manually override the text in a label (can pass empty dict to hide it)
        if override and r[col] in override.keys():
            label = override.get(r[col])

        # Making the actual text
        texts.append(ax.text(x, y, f"{format}".format(label), fontsize=size,
                            color=color, path_effects=[matplotlib.patheffects.withStroke(linewidth=math.floor(size/2), foreground=stroke)],
                            ha=alignment[0], va=alignment[1]))
    
    # Final adjustment
    if adjust:
        adjustText.adjust_text(texts, **adjust_kwargs)

# Rename legend labels with a list of custom text
def replace_legend_items(ax, labels):
    for t,l in zip(ax.get_legend().texts, labels):
        t.set_text(l)

# Adding a patch to a currently-existing legend
# STILL BEING WORKED ON!
def add_patch(ax, patch, label):
    legend = ax.get_legend()

    handles = ax.get_legend().legendHandles
    # This interestingly returns a Text object or array of some sort?
    labels = ax.get_legend().texts
    print(handles, labels)
    handles.append(patch)
    labels.append(label)

    legend._legend_box = None
    legend._init_legend_box(handles, labels)
    legend._set_loc(legend._loc)
    # This doesn't work, but this does: ax.get_legend().get_title().get_text()
    legend.set_title(legend.get_title().get_text())

# Centering the map on a given object
def center_map(ax, geo=None, bounds=None, incr=(0.1, 0.1), square=False):
    if geo is not None:
        # Get the bounds of the geo we want to center on
        minx, miny, maxx, maxy = geo.total_bounds
    elif bounds is not None:
        minx, miny, maxx, maxy = bounds 
    else:
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
    # Get the range of each boundary
    rangex = maxx-minx
    rangey = maxy-miny
    # Will we increment by the same amount in each direction?
    if square==True:
        rangemax = max(rangex, rangey)
        incrementx = rangemax * incr[0]
        incrementy = rangemax * incr[1]
        midx = (maxx+minx)/2
        midy = (maxy+miny)/2
        ax.set_xlim(midx-incrementx, midx+incrementx)
        ax.set_ylim(midy-incrementy, midy+incrementy)
    else:
        # Find the amount we want to increment on
        incrementx = rangex * incr[0]
        incrementy = rangey * incr[1]
        # Set new x and y limits for the axis
        ax.set_xlim(minx-incrementx, maxx+incrementx)
        ax.set_ylim(miny-incrementy, maxy+incrementy)

### RASTER UTILS ###
# Stolen from: https://rasterio.readthedocs.io/en/stable/topics/reproject.html
def reproject_raster(raster, crs, output, return_open=False):
    # Renaming the CRS
    if type(crs) == int:
        new_crs = f"EPSG:{str(crs)}"
    else:
        new_crs = crs
    # Calculating how the new projection is warped from the base
    transform, width, height = rasterio.warp.calculate_default_transform(raster.crs, new_crs, 
                                                                         raster.width, raster.height, 
                                                                         *raster.bounds)
    # Updating the metadata of the source raster
    kwargs = raster.meta.copy()
    kwargs.update({
        'crs': new_crs,
        'transform': transform,
        'width': width,
        'height': height})
    # Saving the file
    with rasterio.open(output, "w", **kwargs) as reproj:
        # Reprojecting each band
        for i in range(1, raster.count + 1):
            rasterio.warp.reproject(
                source=rasterio.band(raster, i),
                destination=rasterio.band(reproj, i),
                src_transform=raster.transform,
                src_crs=raster.crs,
                dst_transform=transform,
                dst_crs=new_crs,
                resampling=rasterio.warp.Resampling.nearest)
    if return_open:
        # Returning the reporjected raster
        return rasterio.open(output)
    else:
        return output    

# TODO: allow this to read an already-existing raster to use as input
# TODO: allow this to work for non-categorical data
# TODO: allow this to work for non-integer data
# vector should be dissolved beforehand
# ref_path is a string
# ras_path is a string
# res is a tuple of (x,y) values
# col is the numeric column you want to retain as an attribute value
# coltype is a tuple of (numpy.dtype, rasterio.dtype)
# all_touched=False sets cell assignment based on which shape contains the centroid
def rasterize_vector(vector, ref_path, ras_path, res, col=None, coltype=None, all_touched=False):
    ### FIRST: SETTING UP A REFERENCE RASTER ###
    # Setting bounds of the vector
    xmin, ymin, xmax, ymax = vector.total_bounds
    # These should be in whatever units your crs is in (meters, feet, etc.)
    xres = res[0]
    yres = -1*res[1] # we make this negative because GDAL expects (0,0) to be the TOP LEFT, not the BOTTOM LEFT
    # Setting the spatial reference to be the same as the file we want to rasterize
    spatial_ref = vector.crs.to_wkt()
    # Calculating the size of the raster in pixels
    xsize = abs(int(((xmax-xmin)/xres)))
    ysize = abs(int(((ymax-ymin)/yres)))

    # Initializing the gdal driver for geotiffs
    driver = osgeo.gdal.GetDriverByName("GTiff")

    # Creating the raster
    ds = driver.Create(ref_path, xsize, ysize, 1, osgeo.gdal.GDT_Int16, options=["COMPRESS=LZW", "TILED=YES"]) # 1 is the number of bands we made
    # Setting the projection
    ds.SetProjection(spatial_ref)
    # Transforming the geometry (do not understand this fully)
    # I do know that the 3rd and 5th parameters (being 0) mean that the map is oriented "up"
    # See: https://stackoverflow.com/questions/27166739/description-of-parameters-of-gdal-setgeotransform
    ds.SetGeoTransform([xmin, xres, 0, ymax, 0, yres])
    # Filling in the raster band with 0
    ds.GetRasterBand(1).Fill(0)
    ds.GetRasterBand(1).SetNoDataValue(-1)
    # Cleaning up the memory
    ds.FlushCache()
    ds = None

    ### NEXT: RASTERIZING ###
    # Creating tuples that pair the geometry with the code
    if col:
        geom_value = ((geom,value) for geom,value in zip(vector["geometry"], vector[col]))
        nd = coltype[0]
        rd = coltype[1]
    else:
        geom_value = ((geom,value) for geom,value in zip(vector["geometry"], range(0,len(vector))))
    # Now actually rasterizing the vector using the properties of the empty raster we made above^
    with rasterio.open(ref_path) as template_raster:
        rasterized_vector = rasterio.features.rasterize(geom_value,
                                                        out_shape = template_raster.shape,
                                                        transform = template_raster.transform,
                                                        all_touched = all_touched,
                                                        fill = -1, #background value
                                                        merge_alg = rasterio.enums.MergeAlg.replace, # .add is also an option
                                                        dtype = nd)
        # Saving the raster
        with rasterio.open(ras_path, "w", driver="GTiff",
                            crs=template_raster.crs, transform=template_raster.transform, count=1, # count refers to the number of bands
                            dtype=rd, width=template_raster.width, height=template_raster.height) as raster_save:
            raster_save.write(rasterized_vector, indexes=1)  

    return ras_path

# Masking a raster with a vector
# TODO: rewrite this with numpy arrays?
def mask_raster(original, new, gdf, crop=True, nodata=-1, all_touched=False, filled=True):
    with rasterio.open(original) as og_raster:
        mask, transform = rasterio.mask.mask(og_raster, gdf["geometry"], crop=crop, nodata=nodata, all_touched=all_touched, filled=filled)
        # return mask
        with rasterio.open(new, "w", driver="GTiff",
                        crs=og_raster.crs, transform=transform, count=1,
                        dtype=og_raster.dtypes[0], width=mask.shape[2], height=mask.shape[1]) as raster_save:
            
            raster_save.write(mask)
    
    return new

# Changing the resolution of a raster
# New res needs to be a tuple of (x,y) resolutions
def resample_raster(original, new, new_res, resample=rasterio.enums.Resampling.nearest):
    # Opening the original raster
    with rasterio.open(original) as og:
        xscale = og.res[0]/new_res[0]
        yscale = og.res[1]/new_res[1]
        # Storing the transformation and other data
        new_profile = og.profile.copy()
        # Resampling the data
        new_data = og.read(out_shape=(og.count, int(og.height * yscale), int(og.width * xscale)), resampling=resample)
        # Scaling the transformation
        new_transform = og.transform * og.transform.scale((1/xscale), (1/yscale))
        # Updating the output profile
        new_profile.update({"height":new_data.shape[-2],"width":new_data.shape[-1],"transform":new_transform})
    # Writing the new information
    with rasterio.open(new, "w", **new_profile) as nr:
        nr.write(new_data)
    # Returning the string path for the new raster
    return new

### DATA UTILS ###
# Querying the ACS API for data
# geo should be a dictionary along the lines of {"for":"RG:*", "in":["FG1:*","FG2:*"]}
# Where RG is the geo you want data returned at the level of
# And FG# are the filtering geos you want to filter by
# See here for examples and detail: https://api.census.gov/data/2022/acs/acs5/profile/examples.html
# Also here: https://api.census.gov/data/2022/acs/acs5/geography.html
# NOTE: probably best if "in" is always a list of values, even if you only have one
# NOTE: can filter by multiple geos if comma separated, like 1,2,3
def get_acs(table, geo, year=2022, acs="acs5", pivot=True, drop_margin=True):
    table = table.upper()
    # Adding the necessary code for DP tables
    if table[:2] == "DP":
        acs = acs + "/profile"
    elif table[:1] == "S":
        acs = acs + "/subject"
    # elif table[:1] == "C":
        # acs = acs + "/cprofile"
    # Constructing the geo filter
    geo_filter = f"for={geo['for']}"
    if "in" in geo:
        if type(geo['in']) == list:
            geo_filter += "&in="
            for i,f in enumerate(geo['in']):
                geo_filter += f
                if i+1 < len(geo['in']):
                    geo_filter += "+"
        else:
            geo_filter += f"&in={geo['in']}"
    # Setting up the census url
    key = "d1244ae231dc81cf92fefca3ae8467caf62b0dfa" # NOTE: MY PERSONAL API KEY
    acs_url = f"https://api.census.gov/data/{year}/acs/{acs}?get=group({table})&{geo_filter}&key={key}"
    # Retrieving the data and doing some light cleaning
    df_acs = pandas.DataFrame(requests.get(acs_url).json())
    df_acs = df_acs.rename(columns=df_acs.iloc[0]).drop(df_acs.index[0]).reset_index(drop=True)
    
    # If pivot is true, then we want to relabel the data with useful column description instead
    if pivot:
        json_vars = requests.get(f"https://api.census.gov/data/{year}/acs/{acs}/variables.json").json()
        df_vars = pandas.DataFrame.from_dict(json_vars["variables"], orient="index").reset_index()
        ## Cleaning up the Label column
        ### Our ultimate vision is to split this into groups to make for a flat hierarchy
        #### TODO: Need to create a "type" column that splits out Estimate vs Percent!
        df_vars["label_clean"] = df_vars["label"].str.replace("Estimate!!","")
        df_vars["label_clean"] = df_vars["label_clean"].str.replace("[^\w\s!]","",regex=True)
        ## Cleaning up the Concept column
        df_vars["concept_clean"] = df_vars["concept"].str.replace(" \\(.+\\)", "",regex=True)
        df_vars["concept_clean"] = df_vars["group"] + " " + df_vars["concept_clean"]
        ## Renaming the index column to variable
        df_vars = df_vars.rename(columns={"index":"variable"})
        
        # Now applying this variable names to our original dataframe
        # First getting the full list of geos we need to preserve
        if "in" in geo:
            geo_melt = [re.search(r"(.+)\:",g).group(1) for g in geo["in"]]
        else:
            geo_melt = []
        geo_melt.append(re.search(r"(.+)\:",geo["for"]).group(1))
        # Now melting on those variables (pivoting wide -> long)
        df_acs = df_acs.melt(id_vars=["GEO_ID","NAME"] + geo_melt)
        ## dropping non-numeric columns
        if drop_margin:
            df_acs = df_acs.drop(df_acs.loc[df_acs["variable"].str.contains("EA$|M$|MA$")].index)
        else:
            df_acs = df_acs.drop(df_acs.loc[df_acs["variable"].str.contains("EA$|MA$")].index)
        # merging clean variable info
        # TODO: this could be made more efficient: need to unpivot on the "attributes" column for each estimated variable, and then append new label_l# column for ESTIMATE vs MARGIN OF ERROR
        df_acs = df_acs.merge(df_vars.loc[:,["variable","label_clean"]], how="left", on="variable")
        # Splitting the label_clean column by the double exclamation point
        names = df_acs["label_clean"].str.split("!!", expand=True)
        # Renaming the columns to something useable
        names.columns = ["label_l"+str(i) for i in range(0, names.shape[1])]
        # Rejoining our new column info on to the data
        df_acs = df_acs.merge(names, how="inner", left_index=True, right_index=True)
        # Dropping the label_clean column
        df_acs = df_acs.drop(columns="label_clean")
        # Moving the value column to the end 
        df_acs = df_acs[[c for c in df_acs if c not in ["value"]] + ["value"]]
        # Table is now cleaned!
    
    
    return df_acs
