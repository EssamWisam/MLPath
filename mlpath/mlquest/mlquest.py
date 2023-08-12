'''
This is the main module of mlquest. It contains the mlquest class which is used to log machine learning experiments.
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
import json
from IPython.display import display, Markdown, HTML

class mlquest():
    '''
    The mlquest class provides methods and attributes to log machine learning experiments.
    '''
    quests = {}             # dictionary of quests (e.g, one for each model) that contains a list of logs (runs)
    log = {}                     # dictionary of the current log (run)
    active = False               # is a quest already active
    start_time = None            # to compute the duration of the experiment later
    relative_path = ''           # the relative location for where to save the 'mlquests' folder
    curr_dir = None              # the name of the folder containing the current file (for saving purposes)
    non_default_log = {}         # contains the arguments actually passed to the function
    log_defs = False             # if true, default arguments are also logged
    quest_name = None            # the name of the quest (e.g, the name of the model in the current file)
    
    @staticmethod
    def start_quest(quest_name, log_defs=False, table_dest=''):
       '''
      Start a new run under the quest with quest_name. This function should be called before any other function with logging functionality.
        
      :param quest_name: The name of the experiment this run belongs to (e.g, the name of the model in the current file)
      :type number: string
      :param log_defs: Decides whether the next render of the experiments table should include the default arguments or not
      :type number: boolean
      :param table_dest: The relative path to the folder where the experiments table should be saved
      :type number: string
        
      :Example:
        
      The following would start a new quest called 'Naive-Bayes with the :samp:`Quests` folder that tracks your experiments being at :samp:`../`.
        
      >>> start_quest('Naive-Bayes', log_defs=True, '../')

      :Notes:
       
      - The :samp:`log_defs` parameter is used to decide whether the next render of the experiments table should include the default arguments or not. Default arguments are logged anyway.
      - The :samp:`table_dest` parameter is used to decide where the experiments table should be saved. If it's given as :samp:`../` then this means that the markdown file (experiments table) corresponding to this quest will be saved in the folder :samp:`../Quests/<ParentFolder>/<QuestName>/`.
       '''
       # get the name of the folder containing the current file
       mlquest.relative_path = table_dest
       mlquest.log_defs = log_defs
       mlquest.curr_dir = os.path.basename(os.getcwd())
       if not os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'):
          os.makedirs(mlquest.relative_path + 'Quests/' + mlquest.curr_dir + '/' + quest_name, exist_ok=True)
            
       if 'quests.mlq' in os.listdir(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'):
            with open(mlquest.relative_path + f'Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'rb') as f:
               mlquest.quests = pickle.load(f)
       
       mlquest.quest_name = quest_name
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
       
       - If you can later change the function definition then :samp:`MLQuest` may handle this by creating new columns that are empty for the previous runs.

       - :func:`mlq.l()` doesn't log collections to avoid having to deal with very large arrays. If your hyperparameter is a small array then you can still stringify it and log it using the :func:`mlq.to_log_ext()` method

       '''
       
       if mlquest.active == False: 
          warnings.warn("Attempting to log a function when no run is active will do nothing")
          return func

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
       Log any other information you want to log. This information will be stored under the 'notes' key (column) in the log.
       
       :param dict: A dictionary of the key (subcolumns), values to be logged under the 'notes' coumns
       :param kwargs: key value pairs to be logged under the 'notes' coumns notes (an alternative to dict)
       
       :Example:
       
       >>> mlq.to_log(modification="Changed the loss function to cross entropy", reason="...")
       
       This would log the modification and reason under the 'notes' column. Any previous runs will have empty values for these columns.
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
          for key, value in kwargs.items():
             mlquest.log[col_name][key] = value
             
    @staticmethod
    def save_quest(quest_name):
       '''
       Uses pickle to save the quests object to a file.
       '''
       # see if there is a 'mlquests' folder, if not, create it
       if not os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}'):
          os.makedirs(mlquest.relative_path + 'Quests/'  + mlquest.curr_dir, exist_ok=True)
       
       with open(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'wb') as f:
            pickle.dump(mlquest.quests, f)
          
    @staticmethod
    def end_quest():
       '''
       ends an active run and saves it to the log. This must called at the end of the experiment else it will not be logged.
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
            # get the id of the last experiment
            id = int(mlquest.quests[quest_name][-1]['info']['id'])+1
            mlquest.log['info']['id'] = id
            mlquest.quests[quest_name].append(mlquest.log)
         else:
            id = 1
            mlquest.log['info']['id'] = id
            quest_name = mlquest.log['info']['name']
            mlquest.quests[quest_name] = [mlquest.log]
         utils.runs_to_json(mlquest.relative_path, mlquest.curr_dir, mlquest.quests[quest_name], quest_name, mlquest.log_defs, mlquest.non_default_log)
         utils.json_to_html_table(mlquest.relative_path, mlquest.curr_dir, f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}.json',
                                  f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}-config.json',  quest_name, last_k=None, save=True)
         mlquest.active = False
         mlquest.log = {}
         mlquest.save_quest(quest_name)
         
   
    @staticmethod
    def show_logs(quest_name,  table_dest='', last_k=None):
      '''
      Shows the logs of a quest in a table.
      
      :param quest_name: The name of the quest to show the logs of
      :type quest_name: string
      :param log_defs: Whether to show the log defaults or not
      :type log_defs: bool
      :param table_dest: The destination of the Quests folder
      :type table_dest: string
      
      :Example:
      
      >>> mlq.show_logs('NaiveBayesExp')
      
      This would show the logs of the NaiveBayesExp quest as saved in :samp:`../Quests/<ParentFolder>/NaiveBayesExp/`
         
      '''
      # get the name of the folder containing the current file
      mlquest.relative_path = table_dest
      mlquest.curr_dir = os.path.basename(os.getcwd())
      assert os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'), f'Quest {quest_name} does not exist yet. Please start a quest with that name first.'
         
      if 'quests.mlq' in os.listdir(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'):
         with open(mlquest.relative_path + f'Quests/{mlquest.curr_dir}/{quest_name}/quests.mlq', 'rb') as f:
            mlquest.quests = pickle.load(f)
            
      # convert the file to html table
      table = utils.json_to_html_table(mlquest.relative_path, mlquest.curr_dir, f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}.json',
                                 f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}-config.json',  quest_name, last_k)
            
            
      # display the table
      display(HTML(table))
      
    @staticmethod
    def delete_runs(table_dest, quest_name, run_ids):
      '''
      permanently deletes runs that have ids in run_ids from the log.
      
      :param table_dest: The destination of the Quests folder
      :type table_dest: string
      :param quest_name: The name of the quest to delete the runs from
      :type quest_name: string
      :param run_ids: The ids (indecies) of the runs to be deleted
      :type run_ids: list of ints
      
      :Example:
      
      >>> mlq.delete_runs('../', 'NaiveBayesExp', [1, 2, 3])
      
      This would delete the runs with ids 1, 2, and 3 from the NaiveBayesExp quest found in :samp:`../Quests/<ParentFolder>/NaiveBayesExp/`
      
      :Notes:
      
      - You need not run :func:`mlq.end_quest()` or :func:`mlq.start_quest()` before calling the function
      - Calling it from the file that initiated the quest is recommended. Otherwise, make sure the current file is in the same parent folder as it.
      

      '''
      curr_dir = os.path.basename(os.getcwd())
      
      # read the mlq file from table_dest and quest_name
      with open(f'{table_dest}Quests/{curr_dir}/{quest_name}/quests.mlq', 'rb') as f:
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
      with open(f'{table_dest}Quests/{curr_dir}/{quest_name}/quests.mlq', 'wb') as f:
         pickle.dump(data, f)
         
      # update the json and html files
      utils.runs_to_json(table_dest, curr_dir, data[quest_name], quest_name, None, None)
      utils.json_to_html_table(table_dest, curr_dir, f'Quests/{curr_dir}/{quest_name}/json/{quest_name}.json', f'Quests/{curr_dir}/{quest_name}/json/{quest_name}-config.json',  quest_name, last_k=None, save=True)
         
         
    @staticmethod
    def get_col_logs(quest_name, col_name, sub_col_name, table_dest=''):
      '''
      Returns a list of values of a column in the log of a quest.
      
      :param quest_name: The name of the quest to get the column from
      :type quest_name: string
      :param col_name: The name of the column to get the values from
      :type col_name: string
      :param sub_col_name: The name of the sub-column to get the values from
      :type sub_col_name: string
      :param table_dest: The destination of the Quests folder
      :type table_dest: string
      
      :Example:
      
      >>> mlq.get_logs('NaiveBayesExp', 'metrics', 'accuracy')
      
      This would return a list of the accuracy values of the runs in the NaiveBayesExp quest found in :samp:`../Quests/<ParentFolder>/NaiveBayesExp/`
      
      '''
      # get the name of the folder containing the current file
      mlquest.relative_path = table_dest
      mlquest.curr_dir = os.path.basename(os.getcwd())
      assert os.path.exists(f'{mlquest.relative_path}Quests/{mlquest.curr_dir}/{quest_name}'), f'Quest {quest_name} does not exist yet. Please start a quest with that name first.'
         
      # get the data from the json file
      with open(mlquest.relative_path + f'Quests/{mlquest.curr_dir}/{quest_name}/json/{quest_name}.json', 'r') as f:
         table = json.load(f)
      
      # get the values of the column
      column = table[col_name][sub_col_name]
      
      return column