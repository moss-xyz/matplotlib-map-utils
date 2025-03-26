import re
import json
import warnings
from importlib import resources
from typing import List, Literal, Union

# Literal lists, for intellisense
regions = Literal["Midwest", "Northeast", "South", "West", 
                  "Inhabited Territory", "Uninhabited Territory", "Sovereign State"]

divisions = Literal["East North Central", "East South Central", "Mid-Atlantic", "Mountain", 
                    "New England", "Pacific", "South Atlantic", "West North Central", "West South Central",
                    "Commonwealth", "Compact of Free Association", "Incorporated and Unorganized", 
                    "Unincorporated and Unorganized", "Unincorporated and Organized"] 

ombs = Literal["Region I", "Region II", "Region III", "Region IV", "Region IX", "Region V", 
               "Region VI", "Region VII", "Region VIII", "Region X",
               "Inhabited Territory", "Uninhabited Territory", "Sovereign State"]

beas = Literal["Far West", "Great Lakes", "Mideast", "New England", "Plains", 
               "Rocky Mountain", "Southeast", "Southwest",
               "Inhabited Territory", "Uninhabited Territory", "Sovereign State"]

returns = Literal["fips","name","abbr","object","dict"]

class USA:
    # No arguments need to pass on initialization really
    def __init__(self):
        self._jurisdictions = self._load_json()

    # This is just for loading the JSON
    def _load_json(self):
        with resources.files("matplotlib_map_utils.utils").joinpath("usa.json").open("r") as f:
            usa_json = json.load(f)
        return usa_json
    
    # Getter for all jurisdictions, VALID OR NOT
    @property 
    def _all(self):
        return self._jurisdictions

    # Getter for all valid jurisdictions
    @property
    def jurisdictions(self):
        return self.filter_valid(True, self._all, "object")
    
    # Getter for all valid states
    @property
    def states(self):
        return self.filter_state(True, self.jurisdictions, "object")
    
    # Getter for all valid territories
    @property
    def territories(self):
        return self.filter_territory(True, self.jurisdictions, "object")
    
    # Getters to generate distinct values for Region, Division, OMB, and BEA
    # which are useful if you can't recall which options are valid
    # First, the function that will get the distinct values
    def _distinct_options(self, key):
        # First getting all the available options from the list
        options = [j[key] for j in self.jurisdictions if j[key] is not None]
        # Creating the distinct set
        options_set = set(options)
        # Returning the set (but as a list)
        # this will also be alphabetically sorted
        options = list(options_set)
        options.sort()
        return options
    
    # The getters are now just calls to the properties
    @property 
    def regions(self):
        return self._distinct_options("region")
    
    @property 
    def divisions(self):
        return self._distinct_options("division")
    
    @property 
    def omb(self):
        return self._distinct_options("omb")
    
    @property 
    def bea(self):
        return self._distinct_options("bea")
    
    # Main filter function
    # Each filter step will follow the same process
    ## Check that there is a non-None filter
    ## Normalize the input to be in a list (if not already)
    ## Perform the filter step
    # Each step is also available as its own independent function, as needed
    def filter(self, valid: bool | None=True, 
               fips: str | int | None=None, 
               name: str | None=None, 
               abbr: str | None=None, 
               state: bool | None=None, 
               contiguous: bool | None=None, 
               territory: bool | None=None, 
               region: Union[regions, List[regions]]=None, 
               division: Union[divisions, List[divisions]]=None, 
               omb: Union[ombs, List[ombs]]=None,
               bea: Union[beas, List[beas]]=None,
               to_return: Union[returns, List[returns]]="fips"):
        
        # Getting a copy of our jurisdictions, which will be filtered each time
        filter_juris = self.jurisdictions.copy()

        # Starting with an initial valid filtering
        # Which will drop invalid FIPS codes 03, 07, 14, 43, and 52
        if (valid is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_valid(valid, filter_juris, to_return="_ignore")

        # Going through each step
        if (fips is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_fips(fips, filter_juris, to_return="_ignore")
        
        if (name is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_name(name, filter_juris, to_return="_ignore")
        
        if (abbr is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_abbr(abbr, filter_juris, to_return="_ignore")
        
        if (state is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_state(state, filter_juris, to_return="_ignore")
        
        if (contiguous is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_contiguous(contiguous, filter_juris, to_return="_ignore")
        
        if (territory is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_territory(territory, filter_juris, to_return="_ignore")
        
        if (region is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_region(region, filter_juris, to_return="_ignore")
        
        if (division is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_division(division, filter_juris, to_return="_ignore")
        
        if (omb is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_omb(omb, filter_juris, to_return="_ignore")
        
        if (bea is not None) and (len(filter_juris) > 0):
            filter_juris = self.filter_bea(bea, filter_juris, to_return="_ignore")
        
        # Final step is to process the input based on to_return
        # and then return it!
        return self._process_return(filter_juris, to_return)
    
    # Filtering bool values (valid, state, contiguous, territory)
    # Will accept either true or false
    def _filter_bool(self, value, key, to_filter=None, to_return="_ignore"):
        # If nothing is passed to to_filter, getting the jurisdictions list
        to_filter = self.jurisdictions.copy() if to_filter is None else to_filter
        if not isinstance(value, bool):
            warnings.warn(f"Invalid {key} filter: {value}. Only boolean values (True/False) are considered valid, see documentation for details.")
        else:    
            # Performing the filter
            filtered = [j for j in to_filter if j[key] == value]
            # And returning the values
            return self._process_return(filtered, to_return)

    # Shortcuts for filtering based on valid, state, contiguous, and territory
    def filter_valid(self, valid: bool, to_filter=None, to_return="fips"):
        return self._filter_bool(valid, "valid", to_filter, to_return)
    
    def filter_state(self, state: bool, to_filter=None, to_return="fips"):
        return self._filter_bool(state, "state", to_filter, to_return)
    
    def filter_contiguous(self, contiguous: bool, to_filter=None, to_return="fips"):
        return self._filter_bool(contiguous, "contiguous", to_filter, to_return)
    
    def filter_territory(self, territory: bool, to_filter=None, to_return="fips"):
        return self._filter_bool(territory, "territory", to_filter, to_return)

    # Filtering FIPS
    # Will accept an integer or a two-digit string as an input
    # If a longer string is inserted, will truncate to only the first two characters
    def filter_fips(self, fips: str | List[str], to_filter=None, to_return="abbr"):
        # If nothing is passed to to_filter, getting the jurisdictions list
        to_filter = self.jurisdictions.copy() if to_filter is None else to_filter
        # Normalizing the fips value being passed
        fips = self._normalize_input(fips)
        # This will store the cleaned-up fips codes
        fips_clean = []
        for f in fips:
            # If the input is an integer, convert it to a two-digit string
            if isinstance(f, int):
                fips_clean.append(str(f).zfill(2)[:2])
            # If the input is already a string, get the first two characters
            elif isinstance(f, str):
                fips_clean.append(f.zfill(2)[:2])
            # Otherwise, throw a *warning*
            else:
                warnings.warn(f"Invalid FIPS filter: {f}. Only integers and strings are considered valid, see documentation for details.")
        # Now can use the clean fips to actually filter
        filtered = [j for j in to_filter if j["fips"] in fips_clean]
        # And returning the values
        return self._process_return(filtered, to_return)
    
    # Filtering name
    # Will accept strings
    # Will normalize the string first (trim, case, special characters), before checking
    # Some states also have an alias available for checking against (Washington, D.C. and District of Columbia are equivalent)
    def filter_name(self, name: str | List[str], to_filter=None, to_return="fips"):
        # If nothing is passed to to_filter, getting the jurisdictions list
        to_filter = self.jurisdictions.copy() if to_filter is None else to_filter
        # Normalizing the name input being passed
        name = self._normalize_input(name)
        # This will store the cleaned-up name input
        name_clean = []
        for n in name:
            # If the input is a string, clean it
            if isinstance(n, str):
                name_clean.append(self._normalize_string(n, case="lower"))
            else:
                warnings.warn(f"Invalid name filter: {n}. Only strings are considered valid, see documentation for details.")
        # Now we can use the clean name to filter
        # Note that we also normalize the names and aliases in our to_filter list!
        filtered = [j for j in to_filter if ((self._normalize_string(j["name"], case="lower") in name_clean) or 
                                             (j["alias"] is not None and self._normalize_string(j["alias"], case="lower") in name_clean))]
        # And returning the values
        return self._process_return(filtered, to_return)

    # Filtering abbr
    # Will accept strings
    # Will normalize the string first (trim, case, special characters), before checking
    # If a string longer than two characters is passed, will only look at the first two characters!
    def filter_abbr(self, abbr: str | List[str], to_filter=None, to_return="fips"):
        # If nothing is passed to to_filter, getting the jurisdictions list
        to_filter = self.jurisdictions.copy() if to_filter is None else to_filter
        # Normalizing the input being passed
        abbr = self._normalize_input(abbr)
        # This will store the cleaned-up input
        abbr_clean = []
        for a in abbr:
            # If the input is a string, clean it
            if isinstance(a, str):
                abbr_clean.append(self._normalize_string(a, case="lower"))
            else:
                warnings.warn(f"Invalid abbr filter: {a}. Only strings are considered valid, see documentation for details.")
        # Now we can use the clean input to filter
        filtered = [j for j in to_filter if (j["abbr"] is not None and self._normalize_string(j["abbr"], case="lower")[:2] in abbr_clean)]
        # And returning the values
        return self._process_return(filtered, to_return)

    # Filtering for categorical values (region/division/omb/bea)
    # Will get the list of acceptable values and compare inputs to it
    # while also warning if an invalid filter is requested
    def _filter_categorical(self, input, key, to_filter=None, to_return="_ignore"):
        # If nothing is passed to to_filter, getting the jurisdictions list
        to_filter = self.jurisdictions.copy() if to_filter is None else to_filter
        # Normalizing the input being passed
        input = self._normalize_input(input)
        # This has the acceptable inputs we want to compare against
        accepted_inputs = self._distinct_options(key)
        # This will store the cleaned-up input
        input_clean = []
        for i in input:
            # If the input is not a string, warn
            if not isinstance(i, str):
                warnings.warn(f"Invalid {key} filter: {i}. Only strings are considered valid, see documentation for details.")
            # If the input is not in our list, warn the user
            elif i not in accepted_inputs:
                warnings.warn(f"Invalid {key} filter: {i}. Only the following inputs are considered valid: {accepted_inputs}.")
            # Otherwise, add it to our list
            else:
                input_clean.append(i)
        # Now we can use the clean input to filter
        filtered = [j for j in to_filter if j[key] in input_clean]
        # And returning the values
        return self._process_return(filtered, to_return)
    
    # Iterations for each categorical filter based on their respective inputs
    def filter_region(self, region: Union[regions, List[regions]], to_filter=None, to_return="fips"):
        return self._filter_categorical(region, "region", to_filter, to_return)
    
    def filter_division(self, division: Union[divisions, List[divisions]], to_filter=None, to_return="fips"):
        return self._filter_categorical(division, "division", to_filter, to_return)
    
    def filter_omb(self, omb: Union[ombs, List[ombs]], to_filter=None, to_return="fips"):
        return self._filter_categorical(omb, "omb", to_filter, to_return)
    
    def filter_bea(self, bea: Union[beas, List[beas]], to_filter=None, to_return="fips"):
        return self._filter_categorical(bea, "bea", to_filter, to_return)

    # Function that processes the returning of a filtered jurisdiction
    def _process_return(self, filter_juris, to_return):
        # If the length is zero, warn!
        if filter_juris is None or len(filter_juris) == 0:
            warnings.warn(f"No matching entities found. Please refer to the documentation and double-check your filters.")
            return None
        if to_return is None:
            to_return == "_ignore"
        # Available options for to_return include fips, name, and abbr
        elif to_return.lower() == "fips":
            juris_return = [j["fips"] for j in filter_juris]
        elif to_return.lower() == "name":
            juris_return = [j["name"] for j in filter_juris]
        elif to_return.lower() == "abbr":
            juris_return = [j["abbr"] for j in filter_juris]
        # Can also request that the entire object be returned, in which case nothing is done
        # This will also happen if an invalid return object is passed
        elif to_return.lower() not in ["object","dict","_ignore"]:
            warnings.warn(f"Invalid to_return request: {to_return}. The entire object will be returned.")
            juris_return = filter_juris.copy()
        else:
            juris_return = filter_juris.copy()
        
        # Now, also processing the return request based on the length of the returned list
        # If the length is zero, warn!
        if len(juris_return) == 0:
            warnings.warn(f"No matching entities found. Please refer to the documentation and double-check your filters.")
            return None
        # If only one element is returned, return the element itself, not a list
        elif len(juris_return) == 1 and to_return != "_ignore":
            return juris_return[0]
        # Otherwise return the whole thing
        else:
            return juris_return

    # Utility function to normalize a string that is passed to it
    def _normalize_string(self, string, case="keep", nan="", spaces="_"):
        string = string.strip()
        if case == "lower":
            string = string.lower()
        string = re.sub(r"\W\S",nan,string)
        string = re.sub(r"\s",spaces,string)
        return string
    
    # Utility function to convert a relevant non-list input to a list
    def _normalize_input(self, input):
        if not isinstance(input, (list, tuple)):
            return [input]
        else:
            return input