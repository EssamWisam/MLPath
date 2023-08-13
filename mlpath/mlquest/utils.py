'''
Utility functions for mlquest
'''
# pylint: skip-file

import os
import json
import warnings
from mlpath.mlquest import mlquest

def merge_dicts(dict_list):
   '''
   Merges a list of dictionaries into one dictionary suitable for conversion into a table.
   
   :param dict_list: A list of dictionaries to be merged
   :type dict_list: list of dictionaries
   
   :meta private:
   '''
   def unique(sequence):
      seen = set()
      return [x for x in sequence if not (x in seen or seen.add(x))]
   big_dict = {}
   # Get all keys in the top-level, they will be part of the final dict
   keys = [(list(d.keys())) for d in dict_list]
   # reverse keys
   keys = list(reversed(keys))
   # flatten keys
   keys = [item for sublist in keys for item in sublist]
   keys = unique(keys)
   # remove duplicates without changing the order
   for key in keys:
      big_dict[key] = {}
      # Get all possible keys in the 2nd level under the top-level key (if not found, the empty set does nothing to union)
      #subkeys = set().union(*(d.get(key, {}) for d in dict_list))
      subkeys = [list(d.get(key, {})) for d in dict_list]
      subkeys = list(reversed(subkeys))
      subkeys = [item for sublist in subkeys for item in sublist]
      subkeys = unique(subkeys)
      for subkey in subkeys:
            values = [d.get(key, {}).get(subkey) for d in dict_list]    # None if not found
            big_dict[key][subkey] = values
   return big_dict




def stringify(item):
   '''
   Puts a given item into a suitable format for logging.
   
   :meta private:
   '''
   if item is None: return None
   # To log it, must not be any sort of collection
   try:
      if not hasattr(item, "__len__") and not hasattr(item, "__iter__") and not hasattr(item, "__getitem__") or isinstance(item, str):
         # So we can convert it into string, it must also not be too long
         # lets round it if it is a float
         if isinstance(item, float): item = round(item, 3)
         string_item = str(item)
         if len(string_item) > 60:
            string_item = string_item[:60] + "..."
         return string_item
      else:
         return None
   except:
      warnings.warn(f"An error has occured while checking that {item} is a scalar with a __str__ method. It will thus be skipped.")
      return None