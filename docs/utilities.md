---
title: Utilities
icon: lucide/wrench
---

This guide will provide a tutorial for using the sole utility class available in the `utils` module: `USA`.

### **USA**

The `USA` class within `utils` is intended to help users (a) quickly isolate subsets of states they want to include in their maps, and (b) enrich their data with additional characteristics (such as state abbreviations, regional/divisional groupings, and the like)

#### **Set-Up**


```python
# Packages used by this tutorial
import geopandas # manipulating geographic data
import numpy # creating arrays
import pygris # easily acquiring shapefiles from the US Census
import matplotlib.pyplot # visualization

# Importing the main package
from matplotlib_map_utils.utils import USA

# Downloading the state-level dataset from pygris
states = pygris.states(cb=True, year=2022, cache=False).to_crs(3857)

# Creating a usa object
usa = USA() # this will load the data from ./utils/usa.json
```

The `USA` class contains a list of all [states](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States) and [territories](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Territories) for the USA in a list of dictionary objects. The included states and territories are based upon [this Wikipedia page](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code) listing all the available FIPS codes.

Each state and territory has the following attributes available for it:

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `fips` | Two-char `string` | Represents [the FIPS code](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code#FIPS_state_codes). *Note that both FIPS 5-1 and FIPS 5-2 codes are included, but 5-1 Territory codes are marked as "invalid" (ex. FIPS code 66 is preferred over code 14 for Guam).* |
| `name` | `string` | Represents the name of the state or territory, with proper capitalisation and punctuation. Generally follows the name provided in the FIPS code table (above), with some minor modifications (`Washington, D.C.` is used instead of `District of Columbia`). |
| `abbr` | Two-char `string` | Represents the [proper abbreviation](https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations) (or "alpha code") for the state or territory. *Note that all states have abbreviations, but not all territories do*. |
| `valid` | `boolean` | Represents if the given entry is *valid* according to **FIPS 5-2**. "Invalid" entries (for territories such as Guam, American Samoa, and the like) are retained for backwards compatibility with older datasets, but should be superseded by "valid" entires for these territories (usually, with a higher FIPS value). |
| `state` | `boolean` | Represents if the given entry is a *state*, per [this list](https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States). Note that `Washington, D.C.` is *not* a state. |
| `contiguous` | `boolean` | Represents if the given entry is part of the *contiguous United States*, also referred to as the "lower 48" or *CONUS*, per [this list](https://en.wikipedia.org/wiki/Contiguous_United_States). Note that `Washington, D.C.` *is* included in this list. |
| `territory` | `boolean` | Represents if the given entry is a *territory*, per [this list](https://en.wikipedia.org/wiki/Territories_of_the_United_States). Note that `Washington, D.C.` is *not* included in this list. |
| `region` | `string` | For states and Washington, D.C., this will be their [Census designated *region*](https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States#Census_Bureau%E2%80%93designated_regions_and_divisions) (`Northeast`, `Midwest`, `South`, or `West`). For territories, this will be either `Inhabited Territory`, `Uninhabited Territory`, or `Sovereign State` (for Palau, Micronesia, and Marshall Islands). |
| `division` | `string` | For states and Washington, D.C., this will be their [Census designated *division*](https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States#Census_Bureau%E2%80%93designated_regions_and_divisions) (such as `New England`, `West North Central`, `Mountain`, or `Pacific`). For territories, this will be either `Commonwealth`, `Compact of Free Association`, `Incorporated and Unorganized`, `Unincorporated and Unorganized`, `Unincorporated and Organized`, per [this list](https://en.wikipedia.org/wiki/Territories_of_the_United_States). |
| `omb` | `string` | For states and Washington, D.C., this will be their [OMB administrative region](https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States#Agency_administrative_regions) (such as `Region I` or `Region IX`). For territories, this will have the same value has `region`. |
| `bea` | `string` | For states and Washington, D.C., this will be their [Bureau of Economic Analysis region](https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States#Bureau_of_Economic_Analysis_regions) (such as `Great Lakes` or `Far West`). For territories, this will have the same value has `region`. |
| `alias` | List of `string` | This field is only filled in if an entry has a common second name, such as `District of Columbia` instead of `Washington, D.C.`, and `Virgin Islands of the U.S.` instead of `U.S. Virgin Islands`. For most, it is `None`. |

Example:
```python
# Looking at a single example
usa.jurisdictions[0]
```

Returns:
```py
{'fips': '01',
 'name': 'Alabama',
 'abbr': 'AL',
 'valid': True,
 'state': True,
 'contiguous': True,
 'territory': False,
 'region': 'South',
 'division': 'East South Central',
 'omb': 'Region IV',
 'bea': 'Southeast',
 'alias': None}
```

#### **Filtering**

All entries are available through entry points such as `usa.jurisdictions` (all *valid* entries), `usa.states` (all states), and `usa.territories` (all territories), for users to iterate over the list-of-dicts as desired. However, a convenience `filter()` function is also provided for the `USA` class, which allows users to easily apply layered filters.

The arguments for `filter()` mirror the properties available for each state/territory, except for *alias* (see below), and they can accept either single values or lists-of-values.

The final argument of `filter()` is `to_return`, which tells the function what value you want to return:

* `fips` (default), `name`, or `abbr` will return *just that field* for each returned entry.

* `object` or `dict` will return the full list-of-dicts that passes the filter

Some notes:

* Filters are applied "top-to-bottom" in the order they are shown-above, and act as "and" filters

* If only a single entry is going to be returned, it will be removed from the list and returned as a single value

* The `name` filter compares against both the `name` and `alias` fields

=== "Single-Value Filter"
	```python
	usa.filter(abbr="CA", to_return="name")
	```
	Returns:
	```python
	# Note that it is not returned as a list
	'California'
	```

=== "Multi-Value Filter"
	```python
	# Filtering based on a list of FIPS codes
	usa.filter(fips=["01","02","10","11"], to_return="name")
	```
	Returns:
	```python
	['Alabama', 'Alaska', 'Delaware', 'Washington, D.C.']
	```

=== "Multi-Field Filter"
	```python
	# Filtering for Pacific contiguous states
	# Each option is applied as an "AND"
	usa.filter(division="Pacific", contiguous=True, to_return="abbr")
	```
	Returns:
	```python
	['CA', 'OR', 'WA']
	```

=== "Invalid Filter"
	```python
	# If no entries are returned, a warning will show
	usa.filter(territory=True, state=True)
	```
	Returns:
	```python
	UserWarning: No matching entities found. Please refer to the documentation and double-check your filters.
	```

??? tip "Single-Dimension Filtering"

	`filter()` is intended to be easy-to-use whether filtering based on a single dimension, or multiple. However, each property also has its own filter available as a standalone function, following the form `filter_FIELD()`: `filter_valid()`, `filter_fips()`, `filter_region()`, and so on.

	Each of these standalone functions accepts the same three arguments:

	* The `value` you want to filter by

	* (Optional) The list-of-dicts you want to filter (if left blank, will filter all valid states/territories)

	* `to_return`, which accepts the same arguments that `filter()` does

	Using this, you can build your own processing pipeline to filter the jurisdictions as you prefer.


	```python
	# Getting all valid states
	valid = usa.filter_valid(True, to_return="object")
	# Filtering that for all contiguous states
	contiguous = usa.filter_contiguous(True, valid, "object")
	# Filtering that for all Southern states
	south = usa.filter_region("South", contiguous, "name")
	south
	```

	Returns:
	```py
		['Alabama',
		'Arkansas',
		'Delaware',
		'Washington, D.C.',
		'Florida',
		'Georgia',
		'Kentucky',
		'Louisiana',
		'Maryland',
		'Mississippi',
		'North Carolina',
		'Oklahoma',
		'South Carolina',
		'Tennessee',
		'Texas',
		'Virginia',
		'West Virginia']
	```

#### **Pandas**

The original impetus for this utility class was to help filter/enrich DataFrames and GeoDataFrames with additional data for each state/territory, which can be quite useful for plotting.

For example, let's say you had an incomplete GeoDataFrame, that just contained the FIPS Code (STATEFP):

```python
gdf = states[["STATEFP","geometry"]].copy()
gdf.head()
```

| index | STATEFP | geometry |
|:---:|:---|:---|
| **0** | 35 | POLYGON ((-12139410.211 3695244.95, -12139373.... |
| **1** | 46 | POLYGON ((-11583670.355 5621144.876, -11582880... |
| **2** | 06 | MULTIPOLYGON (((-13202983.627 3958997.68, -132... |
| **3** | 21 | MULTIPOLYGON (((-9952591.899 4373541.269, -995... |
| **4** | 01 | MULTIPOLYGON (((-9802056.717 3568885.452, -980... |

If we want to add the name of each state corresponding to the FIPS code, we can call `.apply()` on a single column, which is pretty straightforward:

```python
gdf["NAME"] = gdf["STATEFP"].apply(lambda x: usa.filter_fips(x, to_return="name"))
gdf.head()
```

| index | STATEFP | geometry | NAME |
|:---:|:---|:---|:---|
| **0** | 35 | POLYGON ((-12139410.211 3695244.95, -12139373.... | New Mexico |
| **1** | 46 | POLYGON ((-11583670.355 5621144.876, -11582880... | South Dakota |
| **2** | 06 | MULTIPOLYGON (((-13202983.627 3958997.68, -132... | California |
| **3** | 21 | MULTIPOLYGON (((-9952591.899 4373541.269, -995... | Kentucky |
| **4** | 01 | MULTIPOLYGON (((-9802056.717 3568885.452, -980... | Alabama |

If you want to return a non-standard column, you can set `to_return` to `object` and then access the values of the returned dictionary as required:

```python
# When using .apply() on an entire DF, need to state the axis of transformation (0 for rows, 1 for columns)
gdf["BEA_REGION"] = gdf.apply(lambda x: usa.filter_fips(x["STATEFP"], to_return="object")["bea"], axis=1)
gdf.head()
```

| index | STATEFP | geometry | NAME | BEA_REGION |
|:---:|:---|:---|:---|:---|
| **0** | 35 | POLYGON (...) | New Mexico | Southwest |
| **1** | 46 | POLYGON (...) | South Dakota | Plains |
| **2** | 06 | MULTIPOLYGON (...) | California | Far West |
| **3** | 21 | MULTIPOLYGON (...) | Kentucky | Southeast |
| **4** | 01 | MULTIPOLYGON (...) | Alabama | Southeast |