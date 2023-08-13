MLQuest Quick Start
-------------------

Some Example Functions
^^^^^^^^^^^^^^^^^^^^^^

Suppose we have any set of functions such as the following and we
interesed in running a Python file or notebook that calls them multiple
times with different arguments and we would like to keep track of the
arguments that they take and their corresponding outputs for each run.
This problem is exactly what this package attempts to solve.

In this example, we will try to demonstrate the high-level features of
the package. For a more detailed explanation of the package, please
refer to the
`documentation <https://essamwisam.github.io/MLPath/mlpath.html>`__. You
can also run this notebook firsthand by simply downloading it from the
Github repo
`here <https://github.com/EssamWisam/MLPath/blob/main/Example.ipynb>`__.

.. code:: ipython3

    ### Define some functions with default and non-default parameters
    def Preprocessing(x_data, alpha, beta_param, c=0, depth_ratio=4, a_num=5, b_gum=7, c_hum=12):
        return [2, 3, 4]
    
    def FeatureExtraction(x_data, x_param, y_param, z_param, a_num=5, b_gum=7, c_hum=12, **kwargs):
        return [3, 4, 5]
    
    def RadialBasisNet(x_data, p_num, k_num, l_num, a_num=5, b_gum=7, c_hum=12, **kwargs):
        return None
    
    def train_model(model):
        return 701

Imports
^^^^^^^

The main functions responsible for logging functions is simply called
``l`` and is defined under the class ``mlquest``. You can ignore the
second line and use ``mlq.l`` to log your functions.

.. code:: ipython3

    from mlpath import mlquest as mlq
    l = mlq.l

Starting a Quest
^^^^^^^^^^^^^^^^

A quest simply corresponds to a table where each row is an experiment
corresponding to a run of the file. When you call ``mlq.start_quest`` it
simply creates an empty table or loads it if it was created already
already.

.. code:: ipython3

    # Start a new quest, this corresponds to a table where every run will be logged.
    mlq.start_quest('Radial Basis Pipeline')     

Core Pipeline
^^^^^^^^^^^^^

Suppose the following is our pipeline, we can log the input to each
function by simple using ``l(func)(args)`` instead of ``func(args)``.
This logs the arguments regardless to whether they are given by name or
not and even if they are default arguments. Note that non-scalar
arguments are always ignored by ``l()``. We will later see how the log
looks like.

.. code:: ipython3

    # Preprocessing
    x_data_p = l(Preprocessing)(x_data=[1, 2, 3], alpha=14, beta_param=9)
    
    # Feature Extraction
    x_data_f = l(FeatureExtraction)(x_data_p, 20, 340, 10)
    
    # Model Initialization
    model = l(RadialBasisNet)(x_data_f, 55, 25, 26)
    
    # Model Training
    accuracy = train_model(model)  + 15

Model Evaluation
^^^^^^^^^^^^^^^^

To log a metric we use the ``log_metrics`` function. If you pass it
variables with scalar context directly then a column will be created
with that variable’s name to log a variable with a different name you
can pass it as a keyword argument.

.. code:: ipython3

    # log the accuracy
    mlq.log_metrics(accuracy)        # can also do mlq.log_metric(acc=accuracy) if want to log it as acc

Extra Logging
^^^^^^^^^^^^^

Suppose we have another piece of information that we would like to log.
We can use the ``to_log`` function. The first argument it takes is the
column header and the rest are any number of key value pairs passed as
keyword arguments where a column under the column header will be created
for each key.

.. code:: ipython3

    mlq.to_log('New Column', User="Malzahar", Ult="Yes")

Save and Display Logs
^^^^^^^^^^^^^^^^^^^^^

Once the quest is ended with ``mlq.end_quest``, the run is converted to
a row and logged to a table and saved. The first argument is where we
would like to save the markdown corresponding to the quest, the second
argument specifies whether to show or hide the default arguments of
functions and the third helps blacklist further arguments

.. code:: ipython3

    mlq.end_quest('./', log_defs=True, blacklist=['alpha'])

We can use ``mlq.show_logs`` to show the logs of the last ``last_k``
below the notebook cell that calls it. To see it, please consider
running the notebook.

.. code:: ipython3

    mlq.show_logs(last_k=5)                     # higlight color assumes dark theme and can be changed




Server
^^^^^^

We can also view the table in a server using ``mlq.run_server``. There
further filtering can be easily done to show specific rows of the table.

.. code:: ipython3

    mlq.run_server()


Deleting Runs
^^^^^^^^^^^^^

Deleting runs using their id is easily possible using
``mlq.delete_runs``

.. code:: ipython3

    mlq.delete_runs([2,3])
    mlq.show_logs(last_k=9)



Converting to DF
^^^^^^^^^^^^^^^^

The table can be easily converted to a pandas DataFrame to later be used
for plotting or other analysis. The key step here is to use
``mlq.get_flat_dict()`` to get the equivalent flat dictionary.

.. code:: ipython3

    import pandas as pd
    
    my_dict = mlq.get_flat_dict()
    df = pd.DataFrame.from_dict(my_dict)
    df


