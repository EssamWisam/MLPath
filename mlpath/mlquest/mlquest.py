'''
The main module of mlquest. It contains the mlquest class which is used to log the experiments.
'''
import mlpath.mlquest.utils as utils

# pylint: skip-file
import time
import warnings
import inspect
from varname import  argname
from copy import copy
import pickle
import os

class mlquest():
    '''
    mlpath is library to help you with logging machine and deep learning experiments (quests).
    '''
    quests = {}             # dictionary of quests (e.g, one for each model) that contains a list of logs (runs)
    log = {}                     # dictionary of the current log (run)
    active = False               # is a quest already active
    start_time = None            # to compute the duration of the experiment later
    relative_path = ''           # the relative location for where to save the 'mlquests' folder
    curr_dir = None              # the name of the folder containing the current file (for saving purposes)
    non_default_log = {}         # contains the arguments actually passed to the function
    log_defs = False             # if true, default arguments are also logged

    @staticmethod
    def start_quest(quest_name, log_defs=False, table_dest=''):
       '''
        Start a new run under the quest with quest_name. This function should be called before any other function with logging functionality.
        
        :param quest_name: The name of the experiment this run belongs to (e.g, the name of the model in the current file)
        :type number: string
       '''
       # get the name of the folder containing the current file
       mlquest.relative_path = table_dest
       mlquest.log_defs = log_defs
       mlquest.curr_dir = os.path.basename(os.getcwd())
       if not os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'):
          os.makedirs(mlquest.relative_path + 'Quests/' + mlquest.curr_dir + '/' + quest_name)
            
       if 'quests.mlq' in os.listdir(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'):
            with open(mlquest.relative_path + f'Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'rb') as f:
               mlquest.quests = pickle.load(f)
       
       if mlquest.active == True: warnings.warn("Attempting to start a run while another one is active may cause data overwrite")
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
        Clear the log record of the current run.
       '''
       if mlquest.active == False: warnings.warn("Attempting to clear the current run when no run is active will do nothing")
       mlquest.log = {}
       
    
   
    @staticmethod
    def l(func, name=None):
       '''
       Log the scalar parameters of a function that aren't None. This function must be called on the function to be logged.
       
       :param func: The function to be logged
       :type func: function
       :param name: A custom name of the function to be logged. If not given, the name of the function will be used.
       :type name: string
       
       :return: The function wrapped with the logging functionality
       :rtype: function
       '''
       assert mlquest.active, " You can't start logging before starting a run"

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
         be logged with the name of the keyword.
         
         :param mi: The ith metric to be logged 
         :type mi: scalar
       '''
       assert mlquest.active, " You can't start logging before starting a run"
       mlquest.log['metrics'] = {}
       
       # See if any of m1-m10 are set and if so, add them to the log with the key being the vairable name
       for i in range(1, 11):
          if locals()[f'm{i}'] is not None:
             with warnings.catch_warnings():
                warnings.simplefilter("ignore")           # ignores a useless warning of the varname library
                data = utils.stringify(locals()[f'm{i}'])
                if data is not None:
                  mlquest.log['metrics'][argname(f'm{i}')] = locals()[f'm{i}']
                
       # Any kwargs are metrics with custom names, add them as well
       for key, value in kwargs.items():
          data = utils.stringify(value)
          if data is not None:
             mlquest.log['metrics'][key] = value
          else:
             print(data)
             warnings.warn(f"Metric {key} is either None or not a scalar and thus can't be logged")
      
   
    @staticmethod
    def to_log(dict=None,**kwargs):
       '''
       Log any other information you want to log. This information will be stored under the 'notes' key in the log.
       
       :param dict: A dictionary of the key, values to be logged under notes
       :param kwargs: key value pairs to be logged under notes (an alternative to dict)
       '''
       
       if dict is not None:
            mlquest.log['notes'] = dict   
       else:
          # check if mlquest.log['notes'] exists, if not, create it
         if 'notes' not in mlquest.log:
             mlquest.log['notes'] = {}
         for key, value in kwargs.items():
            mlquest.log['notes'][key] = value
       
    @staticmethod
    def to_log_ext(col_name, dict=None, **kwargs):
       '''
       Grants logging with extensive access to the log. 
       
       :param dict: A dictionary of the key, values to be logged under notes
       :param kwargs: key value pairs to be logged under notes (an alternative to dict)
       '''
       if dict is not None:
            mlquest.log[col_name] = dict
       else:
          # check if mlquest.log[col_name] exists, if not, create it
          if col_name not in mlquest.log:
             mlquest.log[col_name] = {}
          for key, value in kwargs.items():
             mlquest.log[col_name][key] = value
          
       
    @staticmethod
    def delete_quest(quest_name):
       '''
       deletes a quest (collection of runs) from the log
       
       :param quest_name: The name of the experiment to be deleted
       :type quest_name: string
       '''
       del mlquest.quests[quest_name]
 
    @staticmethod
    def delete_run(quest_name, run_id):
       '''
       deletes a run under quest_name from the log
       
       :param quest_name: The name of the experiment to be deleted
       :type quest_name: string
       :param run_id: The id of the run to be deleted
       :type run_id: int
       '''
       del mlquest.quests[quest_name][run_id - 1]
       

    @staticmethod
    def save_quest(quest_name):
       '''
       Uses pickle to save the quests object to a file.
       '''
       # see if there is a 'mlquests' folder, if not, create it
       if not os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}'):
          os.makedirs(mlquest.relative_path + 'Quests/'  + mlquest.curr_dir)
       
       with open(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'wb') as f:
            pickle.dump(mlquest.quests, f)
          
    @staticmethod
    def end_quest():
       '''
       ends an active run and saves it to the log.
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
         if mlquest.log['info']['name'] in mlquest.quests:
            quest_name = mlquest.log['info']['name']
            id = len(mlquest.quests[quest_name]) + 1
            mlquest.log['info']['id'] = id
            mlquest.quests[quest_name].append(mlquest.log)
         else:
            id = 1
            mlquest.log['info']['id'] = id
            quest_name = mlquest.log['info']['name']
            mlquest.quests[quest_name] = [mlquest.log]
         utils.runs_to_json(mlquest.relative_path, mlquest.curr_dir, mlquest.quests[quest_name], quest_name, mlquest.log_defs, mlquest.non_default_log)
         utils.json_to_html_table(mlquest.relative_path, mlquest.curr_dir, f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}.json',
                                  f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}-config.json',  quest_name)
         mlquest.active = False
         mlquest.log = {}
         mlquest.save_quest(quest_name)