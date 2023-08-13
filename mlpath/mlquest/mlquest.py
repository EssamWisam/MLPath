'''
This is the main module of mlquest. It contains the mlquest class which is used to log machine learning experiments.
'''
import mlpath.mlquest.utils as utils
from mlpath.mldir_cli.web.app import run_server

# pylint: skip-file
import time
import warnings
import inspect
from varname import  argname
from copy import copy
import pickle
import os
import json
from IPython.display import display, HTML
import shutil
from collections import OrderedDict

class mlquest():
    '''
    The mlquest class provides methods and attributes to log machine learning experiments.
    '''
    quests = OrderedDict({})                  # dictionary of quests (e.g, one for each model) that contains a list of logs (runs)
    log = OrderedDict({})                     # dictionary of the current log (run)
    active = False                            # is a quest already active
    start_time = None                         # to compute the duration of the experiment later
    relative_path = ''                        # the relative location for where to save the 'mlquests' folder
    curr_dir = None                           # the name of the folder containing the current file (for saving purposes)
    non_default_log = OrderedDict({})         # contains the arguments actually passed to the function
    log_defs = False                          # if true, default arguments are also logged
    quest_name = None                         # the name of the quest (e.g, the name of the model in the current file)
    
    @staticmethod
    def get_quests_folder():
       return f'{mlquest.relative_path}/Quests/{mlquest.curr_dir}'
    
    @staticmethod
    def get_quest_folder():  
       return f'{mlquest.relative_path}/Quests/{mlquest.curr_dir}/{mlquest.quest_name}'  
    
    @staticmethod
    def get_quest_json_folder():
         return f'{mlquest.get_quest_folder()}/json'
    
    @staticmethod
    def get_quest_json_file():
         return f'{mlquest.get_quest_folder()}/json/{mlquest.quest_name}.json'
    
    @staticmethod
    def get_quest_json_config_file():
         return f'{mlquest.get_quest_folder()}/json/{mlquest.quest_name}-config.json'
    
    @staticmethod
    def start_quest(quest_name, **kwargs):
       '''
      Start a new run under the quest with quest_name. This function should be called before any other function with logging functionality.
        
      :param quest_name: The name of the experiment this run belongs to (e.g, the name of the model in the current file)
      :type number: string
        
      :Example:
        
      The following would start a new quest called 'Naive-Bayes'
        
      >>> start_quest('Naive-Bayes')
       
       '''
       # 1. get the quest folder or make it if it doesn't exist
       mlquest.relative_path = os.path.dirname(os.path.abspath(__file__))
       mlquest.curr_dir = os.path.basename(os.getcwd())
       mlquest.quest_name = quest_name
       quest_folder = mlquest.get_quest_folder()
       
       if not os.path.exists(quest_folder):
          os.makedirs(quest_folder, exist_ok=True)

       # 2. load the quests dictionary from the file if it exists
       if 'quests.mlq' in os.listdir(quest_folder):
            with open(quest_folder + '/quests.mlq', 'rb') as f:
               mlquest.quests = pickle.load(f)
       
       # 3. Initiate the attributes of the new quest to be added to quests later
       if mlquest.active == True: 
          warnings.warn("Attempting to start a run while another one is active may cause data overwrite")
       else:
         mlquest.active = True
         mlquest.log['info'] = {}
         mlquest.log['info']['name'] = quest_name
         mlquest.start_time = time.time()
         mlquest.log['info']['time'] =  time.strftime('%X') 
         mlquest.log['info']['date'] = time.strftime('%x')
   
   
    @staticmethod
    def clear():
       '''
        Clear the log record of the current run. You may use it while handling exceptions or debugging.
       '''
       if mlquest.active == False: warnings.warn("Attempting to clear the current run when no run is active will do nothing")
       mlquest.log = {}
       
    
   
    @staticmethod
    def l(func, name=None):
       '''
       Log the scalar parameters of a function. This function should be called on any function that you want to log the parameters of.
       
       :param func: The function to be logged
       :type func: function
       :param name: A custom name of the function to be logged. If not given, the name of the function will be used.
       :type name: string
       
       :return: The function wrapped with the logging functionality
       
       :Example:
       
       The following would log the parameters of the function NaiveBayesFit in the current run log
       
       >>> accuracy = mlq.l(NaiveBayesFit)(alpha=1024, beta_param=7, c=12, )
       
       :Notes:
       
       - It doesn't matter whether the argument is given through a variable or as a value, it doesn't matter if its given as a named argument or not. :func:`mlq.l()` will log the values under the column corresponding to the name as in the function's signature.

       - :func:`mlq.l()` always tracks all scalar arguments given to a function that have a name using the function's signature
       
       - If you later make a new function then :samp:`MLQuest` may handle this by creating new columns that are empty for the previous runs (rows).
       
      - Likewise, deleting a function will make the corresponding columns empty for the future runs (rows).

       - :func:`mlq.l()` doesn't log collections to avoid having to deal with very large arrays. If your hyperparameter is a small array then you can still stringify it and log it using the :func:`mlq.to_log_ext()` method

       '''
       
       if mlquest.active == False: 
          warnings.warn("Attempting to log a function when no run is active will do nothing")
          return func

      # wrap the function in a more generic version with logging functionality
       def wrapped(*args, **kwargs):
          signature = inspect.signature(func)
          
          # Get the parameters of the function
          params = signature.parameters.values()
          
          # the default values of the parameters
          defaults = {param.name: param.default \
             for param in params \
                if param.default != inspect._empty and kwargs.get(param.name) is None}
          
          # will have all the set values of the parameters
          values = {}
          for i, param in enumerate(params):
                # positional arguments not given as keyword arguments must be here
                if i < len(args):          
                     data = utils.stringify(args[i]) 
                     if data is not None:   values[param.name] = data
                   
                # the rest of the parameters are positional arguments given by name or defaults or kwargs
                
          # or are keyword arguments in **kwargs
          for key, value in kwargs.items():
               data = utils.stringify(value)
               if data is not None: values[key] = data
          
          non_def_values = copy(values)
          
          for key, value in defaults.items():
               data = utils.stringify(value)
               if data is not None: values[key] = data
          
          # Now set the values in the log with the key being the name of the function
          if name:
             mlquest.log[name] = values
             mlquest.non_default_log[name] = non_def_values
          else:
             mlquest.log[func.__name__] = values
             mlquest.non_default_log[func.__name__] = non_def_values
             
         
          
          return func(*args, **kwargs)
       return wrapped
    
    @staticmethod
    def log_metrics(m1=None, m2=None, m3=None, m4=None, m5=None, m6=None, m7=None, m8=None, m9=None, m10=None, **kwargs):
       '''
         Log the metrics of the experiment. As an experimental feature, if the metrics are given as positional arguments, 
         they will be logged with the name of the variable given to them. If they are given as keyword arguments, they will 
         be logged with the name as the keyword.
         
         :param mi: The ith metric to be logged 
         :type mi: scalar
         
         :example:
         
         >>> acc = mlq.l(NaiveBayes)(alpha=1024, beta_param=7, c=12, )
         >>> mlq.log_metrics(acc)
         
         This would log the accuracy of the NaiveBayes under the column 'acc'. To provide a different name than that of the variable
         you can use the keyword argument syntax:
         
         >>> mlq.log_metrics(accuracy=acc)
         
         :Notes:
         
         - Your metric should be a scalar. You may need to convert a Numpy array into a scalar by using the :samp:`metric.item()`.
         - You can log multiple metrics at once using this function
         
       '''
       if mlquest.active == False: 
          warnings.warn("Attempting to log a metric when no run is active will do nothing")
          
       mlquest.log['metrics'] = {}
       mlquest.non_default_log['metrics'] = {}

       # See if any of m1-m10 are set and if so, add them to the log with the key being the vairable name
       for i in range(1, 11):
          if locals()[f'm{i}'] is not None:
             with warnings.catch_warnings():
                warnings.simplefilter("ignore")           # ignores a useless warning of the varname library
                data = utils.stringify(locals()[f'm{i}'])
                if data is not None:
                  mlquest.log['metrics'][argname(f'm{i}')] = data
                  mlquest.non_default_log['metrics'][argname(f'm{i}')] = data
                  
       # Any kwargs are metrics with custom names, add them as well
       for key, value in kwargs.items():
          data = utils.stringify(value)
          if data is not None:
             mlquest.log['metrics'][key] = data
             mlquest.non_default_log['metrics'][key] = data
          else:
             print(data)
             warnings.warn(f"Metric {key} is either None or not a scalar and thus can't be logged")
      
   
       
    @staticmethod
    def to_log(col_name, dict=None, **kwargs):
       '''
       Grants logging with extensive access to the log. 
       
       :param col_name: The name of the column to log to
       :type col_name: string
       :param dict: A dictionary of the key (subcolumns), values to be logged under col_name column
       :param kwargs: key value pairs to be llogged under col_name column (an alternative to dict)
       
       :Example:
       
       >>> mlq.to_log_ext('graphs', Scatterplot='../plots/plt21.jpg', Histogram='../plots/plt22.jpg')
       
       This would log the Scatterplot and Histogram under the 'graphs' column. Any previous runs will have empty values for these columns.
       '''
       if dict is not None:
            mlquest.log[col_name] = dict
       else:
          # check if mlquest.log[col_name] exists, if not, create it
          if col_name not in mlquest.log:
             mlquest.log[col_name] = {}
             mlquest.non_default_log[col_name] = {}
          for key, value in kwargs.items():
             mlquest.log[col_name][key] = value
             mlquest.non_default_log[col_name][key] = value
             
    @staticmethod
    def save_quest():
       '''
       Uses pickle to save the quests object to a file.
       '''
       quest_folder = mlquest.get_quest_folder()
       quests_folder = mlquest.get_quests_folder()
       # see if there is a 'mlquests' folder, if not, create it
       if not os.path.exists(quests_folder):
          os.makedirs(quests_folder, exist_ok=True)
       
       with open(quest_folder + '/quests.mlq', 'wb') as f:
            pickle.dump(mlquest.quests, f)
      
      
    @staticmethod
    def save_logs(save_path='./'):
      '''
      Saves the logs of a quest in a table.
      
      :param save_path (optional): The path to save the logs to. Defaults to the current directory
      :type save_path: string
      
      :Example:
      >>> mlq.save_logs('./NaiveBayes', 'BlueFeats-NB')
      '''
      quest_folder = mlquest.get_quest_folder()
      quest_name = mlquest.quest_name
      # copy the quests table to the desired location
      shutil.copyfile(quest_folder + f'/{quest_name}.md', f'{save_path}/{quest_name}.md')
        
          
    @staticmethod
    def end_quest(save_ext=None, log_defs=False, blacklist=[]):
       '''
       ends an active run and internally saves it to the log. This must called at the end of the experiment else it will not be logged.
       
      :param save_ext (optional): Where to save the log externally. Defaults to not saving externally at all (None).
       '''
       if mlquest.active == False: warnings.warn('No active mlquest to end')
       else:
         mlquest.log_defs = log_defs
         
         duration = time.time() - mlquest.start_time
         # set the duration of the experiment with the appropriate unit
         if duration < 1:
            mlquest.log['info']['duration'] = f'{duration * 1000:.2f} ms'
         elif duration < 60:
            mlquest.log['info']['duration'] = f'{duration:.2f} s'
         elif duration > 60:
            mlquest.log['info']['duration'] = f'{duration / 60:.2f} min'
         elif duration > 3600:
            mlquest.log['info']['duration'] = f'{duration / 3600:.2f} h'
            
         # check if the experiment already exists and set its name and id
         if mlquest.log['info']['name'] in mlquest.quests:
            quest_name = mlquest.log['info']['name']
            # get the id of the last experiment
            id = int(mlquest.quests[quest_name][-1]['info']['id'])+1
            mlquest.log['info']['id'] = id
            mlquest.quests[quest_name].append(mlquest.log)
         else:
            id = 1
            mlquest.log['info']['id'] = id
            quest_name = mlquest.log['info']['name']
            mlquest.quests[quest_name] = [mlquest.log]
                  
         runs_to_json(mlquest.quests[quest_name], mlquest.log_defs, mlquest.non_default_log, blacklist)
         json_to_html_table(last_k=None, save=True)
                  
         if save_ext is not None:   mlquest.save_logs(save_ext)
         
         mlquest.active = False
         mlquest.log = {}
         mlquest.save_quest()
         

    @staticmethod
    def show_logs(*args, last_k=None, highlight='yellow',  **kwargs):
      '''
      Shows the logs of a quest in a table that can be rendered in a jupyter notebook.
      
      :param quest_name: The name of the quest to show the logs of
      :type quest_name: string
      :param last_k (optional): The number of (most recent) experiments to show. Defaults to all experiments.
      :type last_k: int
      
      :Example:
      
      >>> mlq.show_logs('NaiveBayesExp')
               
      '''
      # get the name of the folder containing the current file
      quest_name = mlquest.quest_name
      mlquest.curr_dir = os.path.basename(os.getcwd())
      assert os.path.exists(f'{mlquest.relative_path}/Quests/{mlquest.curr_dir}/{quest_name}'),\
         f'Quest {quest_name} does not exist yet. Please start a quest with that name first.'
         
      if 'quests.mlq' in os.listdir(f'{mlquest.relative_path}/Quests/{mlquest.curr_dir}/{quest_name}'):
         with open(mlquest.relative_path + f'/Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'rb') as f:
            mlquest.quests = pickle.load(f)
            
      # convert the file to html table
      table = json_to_html_table(last_k=last_k, color=highlight)
            
      # display the table
      display(HTML(table))
   
   
    @staticmethod
    def run_server():
      '''
      Runs the server to display the logs of the quests in a web browser. This includes all the quests in this directory.
      '''
      run_server()
   
      
    @staticmethod
    def delete_runs(run_ids):
      '''
      permanently deletes runs that have ids in run_ids from the log.
      
      :param run_ids: The ids (indecies) of the runs to be deleted
      :type run_ids: list of ints
      
      :Example:
      
      >>> mlq.delete_runs('../', 'NaiveBayesExp', [1, 2, 3])
      
      This would delete the runs with ids 1, 2, and 3 from the NaiveBayesExp quest.
            
      '''
      quest_name = mlquest.quest_name
      quest_folder = mlquest.get_quest_folder()

      # read the mlq file from table_dest and quest_name
      with open(quest_folder + '/quests.mlq', 'rb') as f:
         data = dict(pickle.load(f))
         
      for run_id in run_ids:
         # loop on the runs and delete the run with the given id
         for i, run in enumerate(data[quest_name]):
            if run['info']['id'] == run_id:
               del data[quest_name][i]
               break
            if i == len(data[quest_name])-1:
               warnings.warn(f"Run id {run_id} does not exist; failed to delete")
      
      # save the data to the mlq file
      with open(quest_folder + '/quests.mlq', 'wb') as f:
         pickle.dump(data, f)
         
      # update the json and html files
      runs_to_json(data[quest_name], None, None, [])
      json_to_html_table(last_k=None, save=True)
         
         
         
    @staticmethod
    def get_flat_dict(show_all=False):
      '''
       Convert the quests table to a flat dictionary. This is helpful if the table is needed in a csv or dataframe format.
       
      :param show_all: If True, the dictionary will contain all the columns in the table. If False, it will obey the blacklist and log_defs sent to end_quest.
      '''
      # read the json file
      json_file = mlquest.get_quest_json_file()
      json_config_file = mlquest.get_quest_json_config_file()
      with open(json_file, 'r') as f:
         j = json.load(f)
      with open(json_config_file, 'r') as f:
         config = json.load(f)
      
      # now lets flatten the dict
      flat_dict = {}
      for key in j.keys():
         for subkey in j[key].keys():
            if show_all:
               flat_dict[f'{subkey}'] = j[key][subkey]
            else:
               if config[key][subkey] == 'true':
                  flat_dict[f'{subkey}'] = j[key][subkey]
      return flat_dict
   
    @staticmethod
    def delete_quest(quest_name):
      relative_path = os.path.dirname(os.path.abspath(__file__))
      curr_dir = os.path.basename(os.getcwd())
      quest_folder = f'{relative_path}/Quests/{curr_dir}/{quest_name}'
      shutil.rmtree(quest_folder)
         

def remove_duplicate_rows(json_obj):
   '''
      Removes duplicate rows from the given nested json_obj which is expected to be a
      two-level nested dictionary where the values are lists representing column values.      
   '''
   # read json file from path as dict
   num_rows = len(json_obj['info']['id'])
   rows_to_remove = []
   old_row_values, new_row_values = [], []
   for i in range(num_rows):
      for key in json_obj.keys():
         for subkey in json_obj[key].keys():
            value = json_obj[key][subkey][i]
            # if the key is not info then append the value to the list
            if key != 'info':     new_row_values.append(value)
      
      if new_row_values == old_row_values:
         rows_to_remove.append(i)
         
      old_row_values = new_row_values
      new_row_values = []
   
   # remove the duplicate rows
   for i in range(len(rows_to_remove)-1, -1, -1):
      k = rows_to_remove[i]
      for key in json_obj.keys():
         for subkey in json_obj[key].keys():
            json_obj[key][subkey].pop(k)
            
   return json_obj
      

def get_path_mask(json_obj):
   '''
   Given a json_obj return a mask_obj of the same structure (two level dictionary of keys and subkeys
   and where values are lists) this returns a mask of the same shape as the json_obj but where if a value
   is different from the previous row then it is a 1, otherwise it is a 0.
   '''
   # make mask obj of the same structure as json_obj
   mask_obj = {}
   for key in json_obj.keys():
      mask_obj[key] = {}
      for subkey in json_obj[key].keys():
         mask_obj[key][subkey] = []
         
   num_rows = len(json_obj['info']['id'])
   for i in range(num_rows):
      for key in json_obj.keys():
         for subkey in json_obj[key].keys():
            value = json_obj[key][subkey][i]
            if key != 'info':
               if i != 0:
                  if value != json_obj[key][subkey][i-1]:
                     mask_obj[key][subkey].append(1)
                  else :
                     mask_obj[key][subkey].append(0)
               else:
                  mask_obj[key][subkey].append(0)
            else:
               mask_obj[key][subkey].append(0)
   return mask_obj
            


def runs_to_json(runs, log_defs, non_default_log, blacklist):
   '''
   converts the runs of a quest to a json file
   :param quest_name: The name of the quest to be converted
   :type quest_name: string
   '''
   json_folder = mlquest.get_quest_json_folder()
   json_file = mlquest.get_quest_json_file()
   json_config_file = mlquest.get_quest_json_config_file()
   
   if not os.path.exists(json_folder):
      os.makedirs(json_folder, exist_ok=True)
   
   big_dict = utils.merge_dicts(runs)
   # remove ['info]['name'] from the dict
   del big_dict['info']['name']
   # now convert to json
   j = json.dumps(big_dict, indent=4)
   # save the json file
   with open(json_file, 'w') as f:
      f.write(j)
   
   if log_defs is not None and non_default_log is not None:
      # Now lets make a version of big_dict called config_dict that replaces all the leaf values with 'true'
      config_dict = {}
      if log_defs==True:
         for key in big_dict.keys():
            config_dict[key] = {}
            for subkey in big_dict[key].keys():
               if subkey not in blacklist:
                  config_dict[key][subkey] = 'true'
               else:
                  config_dict[key][subkey] = 'false'
      else:
         # let's get the set of subkeys that are in the non_default_log
         for key in big_dict.keys():
            config_dict[key] = {}
            for subkey in big_dict[key].keys():
               if key in non_default_log.keys():
                  if subkey not in non_default_log[key].keys() or subkey in blacklist:
                     config_dict[key][subkey] = 'false'
                  else:
                     config_dict[key][subkey] = 'true'
               else:
                     config_dict[key][subkey] = 'false'

      for item in blacklist:
         if '.' in item:
            key, subkey = item.split('.')
            config_dict[key][subkey] = "false"


      # convert to json      
      c = json.dumps(config_dict, indent=4)
      
      # save the json file
      with open(json_config_file, 'w') as f:
         f.write(c)




def json_to_html_table(last_k, color='yellow', save=False):
   '''
      Makes an html table from a nested json file. 
      
      :param json_path: The path to the json file
      :type json_path: string
      
      :param quest_name: The name of the quest to be converted
      :type quest_name: string
   '''
   json_path = mlquest.get_quest_json_file()
   config_path = mlquest.get_quest_json_config_file()
   quest_path = mlquest.get_quest_folder()
   
   # read json file from path as dict
   with open(json_path, 'rb') as JSON:
      json_obj = json.load(JSON)
   with open(config_path, 'rb') as JSON:
      config_obj = json.load(JSON)
   
   json_obj = remove_duplicate_rows(json_obj)
   mask_obj = get_path_mask(json_obj)
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
   if last_k is None:      last_k = num_rows
   if last_k > num_rows:     last_k = num_rows
   
   
   for i in range(num_rows - last_k, num_rows):
      table += '<tr>\n'
      for key in json_obj.keys():
         for subkey in json_obj[key].keys():
            if config_obj[key][subkey] == 'true':
               html_color = color if mask_obj[key][subkey][i] and color else ''
               value = json_obj[key][subkey][i] if json_obj[key][subkey][i] is not None else ''
               table += f'<td style="text-align: center; vertical-align: middle;"> <font color={html_color}>{value}</font></td>\n'
      table += '</tr>\n'

   # save the html file
   if save:
      if not os.path.exists(quest_path):
         os.makedirs(quest_path, exist_ok=True)
      with open(quest_path + f'/{mlquest.quest_name}.md', 'w') as f:
         f.write(table)
   
   # return the html table
   return table