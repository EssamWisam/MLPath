'''
Utility functions for mlquest
'''
# pylint: skip-file

import os
import json
import warnings

def merge_dicts(dict_list):
   '''
   Merges a list of dictionaries into one dictionary suitable for conversion into a table.
   
   :param dict_list: A list of dictionaries to be merged
   :type dict_list: list of dictionaries
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

       
       
def json_to_html_table(relative_path, curr_dir, json_path, config_path, quest_name):
   '''
      Makes an html table from a nested json file. 
      
      :param json_path: The path to the json file
      :type json_path: string
      
      :param quest_name: The name of the quest to be converted
      :type quest_name: string
   '''
   # read json file from path as dict
   with open(relative_path + json_path, 'rb') as JSON:
      json_obj = json.load(JSON)
   with open(relative_path + config_path, 'rb') as JSON:
      config_obj = json.load(JSON)
   
   # convert to html table
   table = '<table>\n'
   # make a header row
   table += '<tr>\n'
   # for each key in the top-level dict make a column with colspan being the number of subkeys
   for key in json_obj.keys():
      # the length of the colspan is the number of subkeys with value 'true' in the config file
      length = [config_obj[key][subkey] for subkey in config_obj[key].keys()].count('true')
      if length > 0 : 
         table += f'<th colspan={length} style="text-align: center; vertical-align: middle;">{key}</th>\n'
   table += '</tr>\n'
   # for each subkey of the top-level dict, make a subheader row
   for key in json_obj.keys():
      for subkey in json_obj[key].keys():
         if config_obj[key][subkey] == 'true':
            table += f'<th style="text-align: center; vertical-align: middle;">{subkey}</th>\n'
   table += '</tr>\n'
   # get the number of ids to infer the number of rows
   num_rows = len(json_obj['info']['id'])
   for i in range(num_rows):
      table += '<tr>\n'
      for key in json_obj.keys():
         for subkey in json_obj[key].keys():
            if config_obj[key][subkey] == 'true':
               value = json_obj[key][subkey][i] if json_obj[key][subkey][i] is not None else ''
               table += f'<td style="text-align: center; vertical-align: middle;">{value}</td>\n'
      table += '</tr>\n'


   # save the html file
   if not os.path.exists(f'{relative_path}Quests/{curr_dir}/{quest_name}'):
      os.makedirs(f'{relative_path}Quests/{curr_dir}/{quest_name}')
   with open(relative_path + f'Quests/{curr_dir}/{quest_name}/{quest_name}.md', 'w') as f:
      f.write(table)
   
      
    
def runs_to_json(relative_path, curr_dir, runs, quest_name, log_defs, non_default_log):
   '''
   converts the runs of a quest to a json file
   :param quest_name: The name of the quest to be converted
   :type quest_name: string
   '''
   if not os.path.exists(f'{relative_path}Quests/{curr_dir}/{quest_name}/json'):
      os.makedirs(f'{relative_path}Quests/{curr_dir}/{quest_name}/json')
   
   big_dict = merge_dicts(runs)
   # remove ['info]['name'] from the dict
   del big_dict['info']['name']
   # now convert to json
   j = json.dumps(big_dict, indent=4)
   # save the json file
   with open(relative_path + f'Quests/{curr_dir}/{quest_name}/json/{quest_name}.json', 'w') as f:
      f.write(j)
   
   if log_defs is not None and non_default_log is not None:
      # Now lets make a version of big_dict called config_dict that replaces all the leaf values with 'true'
      if log_defs:
         config_dict = {}
         for key in big_dict.keys():
            config_dict[key] = {}
            for subkey in big_dict[key].keys():
               config_dict[key][subkey] = 'true'
      else:
         # let's get the set of subkeys that are in the non_default_log
         config_dict = {}
         for key in big_dict.keys():
            config_dict[key] = {}
            for subkey in big_dict[key].keys():
               if key in non_default_log.keys():
                  if subkey in non_default_log[key].keys():
                     config_dict[key][subkey] = 'true'
                  else:
                     config_dict[key][subkey] = 'false'
               else:
                  config_dict[key][subkey] = 'true'

      # let's see if there is a version of the config file already
      if os.path.exists(relative_path + f'Quests/{curr_dir}/{quest_name}/json/{quest_name}-config.json'):
         # if there is, we will merge the two dicts
         with open(relative_path + f'Quests/{curr_dir}/{quest_name}/json/{quest_name}-config.json', 'r') as f:
            old_config = json.load(f)
            # get false values from the old_config before overwriting with the new one!
            for key in old_config.keys():
               if key in config_dict.keys():
                  for subkey in old_config[key].keys():
                     if old_config[key][subkey]!='true' and subkey in config_dict[key].keys():
                        config_dict[key][subkey] = 'false'
                        if log_defs:
                           if key in non_default_log.keys():
                              if subkey not in non_default_log[key].keys():      # it must be a default and we want to log it!
                                 config_dict[key][subkey] = 'true'
                              else:
                                 config_dict[key][subkey] = 'false'
                     
      # convert to json      
      c = json.dumps(config_dict, indent=4)
      # save the json file
      with open(relative_path + f'Quests/{curr_dir}/{quest_name}/json/{quest_name}-config.json', 'w') as f:
         f.write(c)



def stringify(item):
   '''
   Puts a given item into a suitable format for logging.
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