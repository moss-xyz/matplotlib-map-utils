# Default packages
import warnings
# Geo packages
import pyproj
# matplotlib's useful validation functions
import matplotlib.rcsetup

### VALIDITY CHECKS ###
# Functions and variables used for validating inputs for classes
# All have a similar form, taking in the name of the property (prop), the value (val)
# some parameters to check against (min/max, list, type, etc.),
# and whether or not None is acceptable value

def _validate_list(prop, val, list, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value in this list: {list}")
    elif none_ok==True and val is None:
        return val
    elif not val in list:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value in this list: {list}")
    return val

def _validate_range(prop, val, min, max=None, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif none_ok==True and val is None:
        return val
    elif type(val) != int and type(val) != float:
        raise ValueError(f"The supplied type is not valid for {prop}, please provide a float or integer between {min} and {max}")
    elif max is not None:
        if not val >= min and not val <= max:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value between {min} and {max}")
    elif max is None:
        if not val >= min:
            raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a value greater than {min}")
    return val

def _validate_type(prop, val, match, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {match}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==match:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {match}")
    return val

def _validate_types(prop, val, matches, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {matches}")
    elif none_ok==True and val is None:
        return val
    elif not type(val) in matches:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {matches}")
    return val

def _validate_coords(prop, val, numpy_type, dims, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif none_ok==True and val is None:
        return val
    elif not type(val)==numpy_type:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide an object of type {numpy_type}")
    elif not val.ndim==dims:
        raise ValueError(f"'{val}' is not a valid value for {prop}, please provide a numpy array with {dims} dimensions")
    return val

def _validate_tuple(prop, val, length, types, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif none_ok==True and val is None:
        return val
    elif not isinstance(val, (tuple, list)):
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    elif len(val)!=length:
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a tuple of length {length} instead")
    else:
        for item in val:
            if type(item) not in types:
                raise ValueError(f"{type(item)} is not a valid value for the items in {prop}, please provide a value of one of the following types: {types}")
    return val

def _validate_color_or_none(prop, val, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a color string acceptable to matplotlib instead")
    elif none_ok==True and val is None:
        return val
    else:
        matplotlib.rcsetup.validate_color(val)
    return val

# NOTE: This one is a bit messy, particularly with the rotation module, but I can't think of a better way to do it...
def _validate_crs(prop, val, rotation_dict, none_ok=False):
    degrees = rotation_dict.get("degrees",None)
    crs = rotation_dict.get("crs",None)
    reference = rotation_dict.get("reference",None)
    coords = rotation_dict.get("coords",None)
    
    if degrees is None:
        if reference == "center":
            if crs is None:
                raise ValueError(f"If degrees is set to None, and reference is 'center', then a valid crs must be supplied")
        else:
            if crs is None or reference is None or coords is None:
                raise ValueError(f"If degrees is set to None, then crs, reference, and coords cannot be None: please provide a valid input for each of these variables instead")
    elif (type(degrees)==int or type(degrees)==float) and (crs is not None or reference is not None or coords is not None):
            warnings.warn(f"A value for degrees was supplied; values for crs, reference, and coords will be ignored")
            return val
    else:
        if none_ok==False and val is None:
            raise ValueError(f"If degrees is set to None, then {prop} cannot be None: please provide a valid CRS input for PyProj instead")
        elif none_ok==True and val is None:
            return val
    # This happens if (a) a value for CRS is supplied and (b) a value for degrees is NOT supplied
    if type(val)==pyproj.CRS:
        pass
    else:
        try:
            val = pyproj.CRS.from_user_input(val)
        except:
            raise Exception(f"Invalid CRS supplied ({val}), please provide a valid CRS input that PyProj can use instead")
    return val

# A simpler validation function for CRSs
def _validate_projection(prop, val, none_ok=False):
    if type(val)==pyproj.CRS:
        pass
    else:
        try:
            val = pyproj.CRS.from_user_input(val)
        except:
            raise Exception(f"Invalid CRS supplied ({val}) for {prop}, please provide a valid CRS input that PyProj can use instead")
    return val    

# This is specifically to apply another validation function to the items in a list 
# Ex. if we want to validate a LIST of colors instead of a single color
def _validate_iterable(prop, val, func, kwargs=None):
    # Making sure we wrap everything in a list
    if not isinstance(val, (tuple, list)):
        val = [val]
    # Then, we apply our validation func with optional kwargs to each item in said list, relying on it to return an error value
    if kwargs is not None:
        for v in val:
            v = func(prop=prop, val=v, **kwargs)
        return val
    # The matplotlib built-in functions DON'T have that, and only ever take the one value
    else:
        for v in val:
            v = func(v)
        return val
    
# This is to check for the structure of a dictionary-like object 
def _validate_keys(prop, val, keys, none_ok=False):
    if none_ok==False and val is None:
        raise ValueError(f"None is not a valid value for {prop}, please provide a dictionary with keys {keys} instead")
    elif none_ok==True and val is None:
        return val
    elif not isinstance(val, (dict)):
        raise ValueError(f"{val} is not a valid value for {prop}, please provide a dictionary with keys {keys} instead")
    else:
        for k in val.keys():
            if k not in keys:
                raise ValueError(f"{k} is not a valid key for the items in {prop}, please provide a dictionary with keys {keys} instead")
    return val

# This is to apply multiple validation functions to a value, if needed - only one needs to pass
# Ex. If an item can be a string OR a list of strings, we can use this to validate it
def _validate_or(prop, val, funcs, kwargs):
    success = False
    # Simply iterate through each func and kwarg
    for f,k in zip(funcs,kwargs):
        # We wrap the attempts in a try block to suppress the errors
        try:
            val = f(prop=prop, val=val, **k)
             # If we pass, we can stop here and return the value
            success = True 
            break
        except:
            pass
    if success == False:
        # If we didn't return a value and exit the loop yet, then the passed value is incorrect, as we raise an error
        raise ValueError(f"{val} is not a valid value for {prop}, please check the documentation")
    else:
        return val

# This is the same, but ALL need to pass
def _validate_and(prop, val, funcs, kwargs):
    success = True
    # Simply iterate through each func and kwarg
    for f,k in zip(funcs,kwargs):
        # We wrap the attempts in a try block to suppress the errors
        try:
            val = f(prop=prop, val=val, **k)
        except:
             # If we fail, we can stop here and return the value
            success = False
            break
    if success == False:
        # If we didn't return a value and exit the loop yet, then the passed value is incorrect, as we raise an error
        raise ValueError(f"{val} is not a valid value for {prop}, please check the documentation")
    else:
        return val

# This final one is used for keys that are not validated
def _skip_validation(val, none_ok=False):
    return val


### MORE VALIDITY FUNCTIONS ###
# These are more customized, and so are separated from the _validate_* functions above
# Mainly, they can process the input dictionaries wholesale, as well as the individual functions in it
def _validate_dict(input_dict, default_dict, functions, to_validate=None, return_clean=False, parse_false=True):
    if input_dict == False:
        if parse_false == True:
            return None
        else:
            return False
    elif input_dict is None or input_dict == True:
        return default_dict
    elif type(input_dict) != dict:
        raise ValueError(f"A dictionary (NoneType) must be provided, please double-check your inputs")
    else:
        values = default_dict | input_dict
        # Pre-checking that no invalid keys are passed
        invalid = [key for key in values.keys() if key not in functions.keys() and key not in ["bbox_to_anchor", "bbox_transform"]]
        if len(invalid) > 0:
            print(f"Warning: Invalid keys detected ({invalid}). These will be ignored.")
        # First, trimming our values to only those we need to validate
        if to_validate == "input":
            values = {key: val for key, val in values.items() if (key in input_dict.keys() and key in functions.keys())} # have to check against both here
            functions = {key: val for key, val in functions.items() if key in values.keys()}
        elif to_validate is not None:
            values = {key: val for key, val in values.items() if key in to_validate}
            functions = {key: val for key, val in functions.items() if key in values.keys()}
        else:
            values = {key: val for key, val in values.items() if key in functions.keys()}
            functions = {key: val for key, val in functions.items() if key in values.keys()}
        # Now, running the function with the necessary kwargs
        for key,val in values.items():
            fd = functions[key]
            func = fd["func"]
            # NOTE: This is messy but the only way to get the rotation value to the crs function
            if key=="crs":
                _ = func(prop=key, val=val, rotation_dict=values, **fd["kwargs"])
            # NOTE: This is messy but the only way to check the projection dict without keywords
            elif key=="projection":
                _ = func(prop=key, val=val)
            # Our custom functions always have this dictionary key in them, so we know what form they take
            elif "kwargs" in fd:
                _ = func(prop=key, val=val, **fd["kwargs"])
            # The matplotlib built-in functions DON'T have that, and only ever take the one value
            else:
                _ = func(val)
        if return_clean==True:
            return values

# This function can process the _VALIDATE dictionaries we established above, but for single variables at a time
def _validate(validate_dict, prop, val, return_val=True, kwargs={}):
    fd = validate_dict[prop]
    func = fd["func"]
    # Most of our custom functions always have this dictionary key in them, so we know what form they take
    if "kwargs" in fd:
        val = func(prop=prop, val=val, **(fd["kwargs"] | kwargs))
    # The matplotlib built-in functions DON'T have that, and only ever take the one value
    else:
        val = func(val)
    if return_val==True:
        return val