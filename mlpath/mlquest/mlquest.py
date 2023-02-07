'''
The main module of mlquest. It contains the mlquest class which is used to log the experiments.
'''
import mlpath.mlquest.utils as utils

# pylint: skip-file
import time
import warnings
import json
import inspect
from varname import  argname
import pickle
import os
from collections import OrderedDict

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
       if not os.path.exists('mlquests'): os.mkdir('mlquests')
            
       if 'experiments.mlq' in os.listdir('mlquests'):
            with open('mlquests/experiments.mlq', 'rb') as f:
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
       assert mlquest.active, " You can't start logging before starting a quest"

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
       assert mlquest.active, " You can't start logging before starting a quest"
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
    def save_experiments():
       '''
       Uses pickle to save the experiments object to a file.
       '''
       # see if there is a 'mlquests' folder, if not, create it
       if not os.path.exists('mlquests'): os.mkdir('mlquests')
       
       with open('mlquests/experiments.mlq', 'wb') as f:
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
         utils.runs_to_json(mlquest.experiments[exp_name], exp_name)
         utils.json_to_html_table(f'mlquests/{exp_name}.json',f'mlquests/{exp_name}_config.json',  exp_name)
         mlquest.active = False
         mlquest.log = {}
         mlquest.save_experiments()