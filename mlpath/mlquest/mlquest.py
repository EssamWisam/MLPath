'''
The main module of mlquest. It contains the mlquest class which is used to log the experiments.
'''
# pylint: skip-file
import time
import warnings
import json
import inspect
import re
from varname import  argname
import pickle
import os

class mlquest():
    '''
    mlpath is library to help you with logging machine and deep learning experiments.
    '''
    experiments = {}             # dictionary of experiments (e.g, one for each model) that contains a list of logs (runs)
    log = {}                     # dictionary of the current log (run)
    active = False               # is an mlquest already active
    start_time = None            # to compute the duration of the experiment later

    
    @staticmethod
    def start(exp_name):
       '''
        Start a new mlquest (run). This function must be called before any other function.
        
        :param exp_name: The name of the experiment this run belongs to (e.g, the name of the model in the current file)
        :type number: string
       '''
       # read the experiments file after checking if 'experiments.pkl' exists
       if 'experiments.pkl' in os.listdir():
            with open('experiments.pkl', 'rb') as f:
               mlquest.experiments = pickle.load(f)
       
       if mlquest.active == True: warnings.warn("Attempting to start a quest while another one is active may cause data overwrite")
       else:
         mlquest.active = True
         mlquest.log['info'] = {}
         mlquest.log['info']['name'] = exp_name
         mlquest.start_time = time.time()
         mlquest.log['info']['time'] =  time.strftime('%X') 
         mlquest.log['info']['date'] = time.strftime('%x')
         
   
    @staticmethod
    def clear():
       '''
        Clear the current mlquest (run).
       '''
       if mlquest.active == False: warnings.warn("Attempting to clear the current quest when no quest is active will do nothing")
       mlquest.log = {}
      
   
    @staticmethod
    def l(func, name=None):
       '''
       Log the parameters of a function. This function must be called on the function to be logged.
       
       :param func: The function to be logged
       :type func: function
       :param name: A custom name of the function to be logged. If not given, the name of the function will be used.
       :type name: string
       
       :return: The function wrapped with the logging functionality
       :rtype: function
       '''
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
                   values[param.name] = args[i]
                # the rest of the parameters are positional arguments given by name or defaults or kwargs
                
          # or are keyword arguments in **kwargs
          values.update(kwargs)
          values.update(defaults)
          
          # Now set the values in the log with the key being the name of the function
          if name:
             mlquest.log[name] = values
          else:
             mlquest.log[func.__name__] = values
          
          return func(*args, **kwargs)
       return wrapped
    
    @staticmethod
    def log_metrics(m1=None, m2=None, m3=None, m4=None, m5=None, m6=None, m7=None, m8=None, m9=None, m10=None, **kwargs):
       '''
         Log the metrics of the experiment. If the metrics are given as positional arguments, they will be logged with the
         name of the variable given to them. If they are given as keyword arguments, they will be logged with the name of
         the keyword.
         
         :param mi: The ith metric to be logged 
         :type mi: float or string
         
       '''
       mlquest.log['metrics'] = {}
       
       # See if any of m1-m10 are set and if so, add them to the log with the key being the vairable name
       for i in range(1, 11):
          if locals()[f'm{i}'] is not None:
             with warnings.catch_warnings():
                warnings.simplefilter("ignore")           # ignores a useless warning of the varname library
                mlquest.log['metrics'][argname(f'm{i}')] = locals()[f'm{i}']
                
       # Any kwargs are metrics with custom names, add them as well
       mlquest.log['metrics'].update(kwargs)
      
   
    @staticmethod
    def to_log(name, info):
       '''
       Log any other information you want to log. This information will be stored under the 'notes' key in the log
       '''
       mlquest.log['notes'] = {}
       mlquest.log['notes'][name] = info
       
    @staticmethod
    def merge_dicts(dict_list):
       '''
       Merges a list of dictionaries into one dictionary suitable for conversion into a table.
       
       :param dict_list: A list of dictionaries to be merged
       :type dict_list: list of dictionaries
      '''
       big_dict = {}
       # Get all keys in the top-level, they will be part of the final dict
       keys = set().union(*(d.keys() for d in dict_list))
       for key in keys:
         big_dict[key] = {}
         # Get all possible keys in the 2nd level under the top-level key (if not found, the empty set does nothing to union)
         subkeys = set().union(*(d.get(key, {}) for d in dict_list))
         for subkey in subkeys:
             values = [d.get(key, {}).get(subkey) for d in dict_list]    # None if not found
             big_dict[key][subkey] = values
       return big_dict
       
       
    @staticmethod
    def delete_experiment(exp_name):
       '''
       deletes an experiment (collection of runs) from the log
       :param exp_name: The name of the experiment to be deleted
       :type exp_name: string
       '''
       del mlquest.experiments[exp_name]
 
    @staticmethod
    def delete_run(exp_name, run_id):
       '''
       deletes a run from the log
       :param exp_name: The name of the experiment to be deleted
       :type exp_name: string
       :param run_id: The id of the run to be deleted
       :type run_id: int
       '''
       del mlquest.experiments[exp_name][run_id - 1]
       
    @staticmethod
    def runs_to_json(exp_name):
       '''
       converts the runs of an experiment to a json file
       :param exp_name: The name of the experiment to be converted
       :type exp_name: string
       '''
       runs = mlquest.experiments[exp_name]
       big_dict = mlquest.merge_dicts(runs)
       j = json.dumps(big_dict, indent=3)
       # save the json file
       with open(f'{exp_name}.json', 'w') as f:
          f.write(j)
    
    @staticmethod
    def save_experiments():
       '''
       Uses pickle to save the experiments object to a file.
       '''
       with open('experiments.pkl', 'wb') as f:
            pickle.dump(mlquest.experiments, f)
          
    @staticmethod
    def end():
       '''
       ends an active mlquest (run) and saves it to the log.
       '''
       if mlquest.active == False: warnings.warn('No active mlquest to end')
       else:
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
         if mlquest.log['info']['name'] in mlquest.experiments:
            exp_name = mlquest.log['info']['name']
            id = len(mlquest.experiments[exp_name]) + 1
            mlquest.log['info']['id'] = id
            mlquest.experiments[exp_name].append(mlquest.log)
         else:
            id = 1
            mlquest.log['info']['id'] = id
            exp_name = mlquest.log['info']['name']
            mlquest.experiments[exp_name] = [mlquest.log]
         mlquest.runs_to_json(exp_name)
         mlquest.active = False
         mlquest.log = {}
         mlquest.save_experiments()