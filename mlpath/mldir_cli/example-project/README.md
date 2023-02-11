## 📜 The MLDir Manifesto
➜ Each stage in the ML pipeline should be a separate directory.

➜ If that stage is further broken down into sub-stages, each sub-stage should be a separate directory.

➜ For any pipeline stage, each alternative that implements that stage should be in a separate directory within that stage's folder.

➜ Any implementation of a stage is a set of functions.

➜ Functions are defined only in .py files not in notebooks.

➜ Notebooks are only for testing or running entire pipelines (e.g., training and hyperparameter tuning). They import the needed functions from pipeline stages.



### 📜 A more fine-grained version of the MLDir Manifesto also specifies

➜ In the implementation of any stage, any logic not specifically related to the stage's implementation such as saving or visualizion should be in a seperate function in the file.

➜ Call the training, validation and testing data x_train, x_val and x_test respectively. x_val is x_val even if x_test doesn't exist (yet). The variable name may be appended with an _{letter} to indicate the stage of the pipeline that resulted in it.

➜ Any function that takes x_train and x_val should be also able to take x_test only.

➜ Once the experimentation phase is over (converged on a pipeline with fixed hyperparameters), the pipeline should be implemented in a single .py file with a single pipeline function. The project, except for this file can be archived at this point (along with a requirements.txt).

### 📜 Which also has the following extension

➜ If a pipeline stage takes time then provide a way to save its results and load them later.

➜ If a pipeline stage may benefit from visualizion then provide a method for that.

➜ Logging should be implemented for every pipeline.


## This directory structure is an attempt to implement the above manifesto.

⦿ It assumes a pipeline with the following stages:

1. Data Preparation (Ingestion and Preprocessing)           
2. Feature Extraction
3. Model Implementation
4. Model Pipeline Composition
5. Model Scoring
6. Model Serving (Production)

In summary, different preprocessing methods are implemented in the first stage. Different feature extraction methods are implemented in the second stage. Different model implementations are implemented in the third stage. Then the fourth stage implements different pipelines for each model (a combination of preprocessing and feature extraction methods).

Once, the best pipeline (composing a preprocessing method, a feature extraction method and a model) is found, the fifth stage implements the scoring of the model. The sixth stage implements the deployment of the model by plugging in a single pipeline function in the ready-made Flask app.

⦿ The structure is further explained in each .py file

Besides the pipeline stages, there are three other directories:
1. DataFiles - contains the datasets for the project
2. References - contains the references for the project (e.g., papers, books, etc.)
3. Saved - contains the saved results of the pipeline stages

There is also a Sandbox.ipynb which is used for debugging (e.g. coopying a function over when a pipeline decides to break)

⦿ For a live example on a dummy dataset consider running
```
mldir --example
```
and don't forget to follow that up with ```pip install -r requirements.txt```

Side note: The fact that this does not seperate the data preparation stage into ingestion and preprocessing is in itself a violation. Its important to note that your team doesn't have to follow everything in the manifesto; if everyone agrees that something should be done differently, then do it differently. The manifesto is just a reference.

This was intuitive in our case since the ingestion stage will seldom have different methods so having its own folder seems unnecessary. 
