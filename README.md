
# MLPath

MLPath is an MLOPs library on Python that makes tracking machine learning experiments and organizing machine learning projects easier. It consists of two subpackages so far, MLQuest for tracking and MLDir for directory structure.

Check this for <a href='https://essamwisam.github.io/MLPath/mlpath.html'>documentation</a>. It also has examples and notes that will help you further understand the library.

### Installation
```
pip install mlpath
```

<h1 text-align='center'> MLQuest </h1>
<img src="https://user-images.githubusercontent.com/49572294/218260658-846c1aab-fe57-44fa-baa6-5d988ff07e1b.png"></img>

### To get started

> This is your code without mlquest

```Python

# Preprocessing
x_data_p = Preprocessing(x_data=[1, 2, 3], alpha=1024, beta_param=7, c=12)

# Feature Extraction
x_data_f = FeatureExtraction(x_data_p, 14, 510, 4)  

# Model Initialization
model = RadialBasisNet(x_data_f, 12, 2, 3)

# Model Training
accuracy = train_model(model)
```
> This is your code with mlquest
```Python

from mlpath import mlquest as mlq
l = mlq.l

# Start a new quest, this corresponds to a table where every run of the Python file will be logged.
mlq.start_quest('Radial Basis Pipeline', log_defs=False)     

# Preprocessing
x_data_p = l(Preprocessing)(x_data=[1, 2, 3], alpha=1114, beta_param=2, c=925)

# Feature Extraction
x_data_f = l(FeatureExtraction)(x_data_p, 32, 50, 4)  # x_data_p is an array so it won't be logged.

# Model Initialization
model = l(RadialBasisNet)(x_data_f, 99, 19, 31)

# Model Training
accuracy = train_model(model)

# log the accuracy
mlq.log_metrics(accuracy)        # can also do mlq.log_metric(acc=accuracy) so its logged as acc

mlq.end_quest()

mlq.show_table('Radial Basis Pipeline', last_k=10)    # show the table for the last 10 runs

```
After the third run, this shows up under the Quests folder (and the notebook itself):
<table>
<tr>
<th colspan=4 style="text-align: center; vertical-align: middle;">info</th>
<th colspan=3 style="text-align: center; vertical-align: middle;">Preprocessing</th>
<th colspan=3 style="text-align: center; vertical-align: middle;">FeatureExtraction</th>
<th colspan=3 style="text-align: center; vertical-align: middle;">RadialBasisNet</th>
<th colspan=1 style="text-align: center; vertical-align: middle;">metrics</th>
</tr>
<th style="text-align: center; vertical-align: middle;">time</th>
<th style="text-align: center; vertical-align: middle;">date</th>
<th style="text-align: center; vertical-align: middle;">duration</th>
<th style="text-align: center; vertical-align: middle;">id</th>
<th style="text-align: center; vertical-align: middle;">alpha</th>
<th style="text-align: center; vertical-align: middle;">beta_param</th>
<th style="text-align: center; vertical-align: middle;">c</th>
<th style="text-align: center; vertical-align: middle;">x_param</th>
<th style="text-align: center; vertical-align: middle;">y_param</th>
<th style="text-align: center; vertical-align: middle;">z_param</th>
<th style="text-align: center; vertical-align: middle;">p_num</th>
<th style="text-align: center; vertical-align: middle;">k_num</th>
<th style="text-align: center; vertical-align: middle;">l_num</th>
<th style="text-align: center; vertical-align: middle;">accuracy</th>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">16:31:16</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">1.01 min</td>
<td style="text-align: center; vertical-align: middle;">1</td>
<td style="text-align: center; vertical-align: middle;">74</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">95</td>
<td style="text-align: center; vertical-align: middle;">13</td>
<td style="text-align: center; vertical-align: middle;">530</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">99</td>
<td style="text-align: center; vertical-align: middle;">99</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">50</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">16:32:40</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">4.91 ms</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">14</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">95</td>
<td style="text-align: center; vertical-align: middle;">132</td>
<td style="text-align: center; vertical-align: middle;">530</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">99</td>
<td style="text-align: center; vertical-align: middle;">19</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">70</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">16:32:57</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">4.93 ms</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">1114</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">925</td>
<td style="text-align: center; vertical-align: middle;">32</td>
<td style="text-align: center; vertical-align: middle;">50</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">99</td>
<td style="text-align: center; vertical-align: middle;">19</td>
<td style="text-align: center; vertical-align: middle;">31</td>
<td style="text-align: center; vertical-align: middle;">70</td>
</tr>
</table>

Editors like VSCode support viewing markdown out-of-the-box. You may need to press `CTRL/CMD+Shift+V`

⦿ Besides of the markdown, you will also find a ```json``` folder in that directory with a config file that allows you to customize the columns to show in the markdown table.


### But you probably prefer a web interface

In the same level as the ```Quests``` folder run the command ```mlweb``` then open ```http://localhost:5000``` in your browser. You should see something like this:

<img width="1430" alt="image" src="https://user-images.githubusercontent.com/49572294/218263965-3e376645-e85f-4045-8cf2-20294832983f.png">


⦿ You can search for specific runs, an example would be ```metrics.accuracy>50``` (similar syntax to MLFlow)

⦿ You can customize the columns to show in the table by clicking on `columns` (in lieu of doing it through```json``` config file)

⦿ Choose which model (folder containing python files where you run quests) and which pipeline file (quest) using the bar on the left


### An example with Scikit-Learn


```python
from mlpath import mlquest as mlq

# We won't log defaults here but note that being aware of them and their values/impact is important.
mlq.start_quest('Fractal-GB', log_defs=False, table_dest='../../')

# read the data
x_train_i, x_val_i, y_train_i, y_val_i = read_data()

# preprocess the data
x_train_p, x_val_p = preprocess_data(x_train_i, x_val_i)

# extract fractal features
x_train_f, x_val_f = mlq.l(apply_SFTA)(x_train_p, x_val_p, deviation=10)

# initialize a GB model
model = mlq.l(GradientBoostingClassifier)(n_estimators=10, learning_rate=220, max_depth=110)

# train the model
model.fit(x_train_f, y_train_i)

# report the accuracy
accuracy = model.score(x_val_f, y_val_i).item()     # .item() so its a scalar that can be logged

mlq.log_metrics(acc=accuracy)

mlq.end_quest()

mlq.show_table('Fractal-GB', last_k=10)    # show the table for the last 10 runs
```
<table>
<tr>
<th colspan=4 style="text-align: center; vertical-align: middle;">info</th>
<th colspan=1 style="text-align: center; vertical-align: middle;">apply_SFTA</th>
<th colspan=3 style="text-align: center; vertical-align: middle;">GradientBoostingClassifier</th>
<th colspan=1 style="text-align: center; vertical-align: middle;">metrics</th>
</tr>
<th style="text-align: center; vertical-align: middle;">time</th>
<th style="text-align: center; vertical-align: middle;">date</th>
<th style="text-align: center; vertical-align: middle;">duration</th>
<th style="text-align: center; vertical-align: middle;">id</th>
<th style="text-align: center; vertical-align: middle;">deviation</th>
<th style="text-align: center; vertical-align: middle;">n_estimators</th>
<th style="text-align: center; vertical-align: middle;">learning_rate</th>
<th style="text-align: center; vertical-align: middle;">max_depth</th>
<th style="text-align: center; vertical-align: middle;">acc</th>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">17:26:34</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">2.33 min</td>
<td style="text-align: center; vertical-align: middle;">1</td>
<td style="text-align: center; vertical-align: middle;">30</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">50</td>
<td style="text-align: center; vertical-align: middle;">12</td>
<td style="text-align: center; vertical-align: middle;">0.5</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">17:29:08</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">344.98 ms</td>
<td style="text-align: center; vertical-align: middle;">2</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">50</td>
<td style="text-align: center; vertical-align: middle;">20</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">0.5</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">17:29:14</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">251.52 ms</td>
<td style="text-align: center; vertical-align: middle;">3</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">50</td>
<td style="text-align: center; vertical-align: middle;">20</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">0.5</td>
</tr>
<tr>
<td style="text-align: center; vertical-align: middle;">17:29:22</td>
<td style="text-align: center; vertical-align: middle;">02/11/23</td>
<td style="text-align: center; vertical-align: middle;">266.31 ms</td>
<td style="text-align: center; vertical-align: middle;">4</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">10</td>
<td style="text-align: center; vertical-align: middle;">220</td>
<td style="text-align: center; vertical-align: middle;">110</td>
<td style="text-align: center; vertical-align: middle;">0.5</td>
</tr>
</table>


### An example with PyTorch

A real example on a dummy dataset that demonstrates using the library on real models is provided in the MLDir examples mentioned below.

<h1 text-align='center'> MLDir </h1>

<img src="https://user-images.githubusercontent.com/49572294/218267208-c4f01847-4184-4732-aa10-bfe7f37b7005.png"></img>

MLDir is a simple CLI that creates a standard directory structure for your machine learning project. It provides a folder structure that is comprehensive, highly scalable (development-wise) and apt for collaboration.

#### Note of caution

⦿ Although it integrates well with MLQuest, neither MLQuest nor MLDir require the other to function.

⦿ Suppose your project has very few people working on it (only you) or does not require trying many models with many other preprocessing methods and features, then you may not really need MLDir. A notebook and MLQuest should be enough. Otherwise use MLDir to prevent your directory from becoming a spaghetti soup of Python files.


### 📜 The MLDir Manifesto
The directory structure generated by MLDir complies with the MLDir manifesto ( a set of 'soft' standards) which attempts to enforce seperation of concerns among different stages of the machine learning pipeline and among writing code and running experiments (hyperparameter tuning). It specifies:

➜ Each stage in the ML pipeline should be a separate directory.

➜ If that stage is further broken down into sub-stages, each sub-stage should be a separate directory (in the top level)

➜ For any pipeline stage, each alternative that implements that stage should be in a separate directory within that stage's folder.

➜ Any implementation of a stage is a set of functions.

➜ Functions are defined only in .py files not in notebooks.

➜ Notebooks are only for testing or running entire pipelines (e.g., training and hyperparameter tuning). They import the needed functions from pipeline stages.

You can also read more about the manifesto [here](https://github.com/EssamWisam/MLPath/tree/main/mlpath/mldir_cli/project).

### To get started

MLDir is part of MLPath. So you don't need to install it separately. To create a simple folder structure, run:
```bash
mldir --name <project_name>
```
⦿ If mldir is ran without a name, it uses the name 'Project'

This generates the following folder structure:

```
.
├── DataFiles
│   ├── Dataset 1
│   └── Dataset 2
├── DataPreparation
│   ├── Ingestion
│   └── Preprocessing
├── FeatureExtraction
│   ├── BoW
│   ├── GLCM
│   └── OneHot
├── ModelPipelines
│   ├── GRU
│   ├── GradientBoost
│   └── SVM
├── ModelScoring
│   ├── Pipeline
│   └── Scoring
├── README.md
├── Sandbox.ipynb
│   ├── DataPreparation
│   ├── FeatureExtraction
│   └── ModelsPipelines
└── Sandbox.ipynb
```
The file in each folder has instructions on how to use it. These are all grouped in the README for a more detailed explanation.

### Other important options

```bash
mldir --name<project-name> --full
```
⦿ The --full option generates an even more comprehensive folder structure. Including folders such as ```ModelImplementations```, ```References``` and most importantly ```Production```.

⦿ The ```Production``` folder contains a Flask app that can be used to serve your model as an API. All you need is only to import your final model into app.py and replace the dummy model with it. The Flask app assumes that your model takes a file via path and returns a prediction but it can be easilt extended otherwise to suit your needs

<img width="1430" alt="image" src="https://user-images.githubusercontent.com/49572294/218269358-d2db4974-c5a1-4531-a696-69e842f7bb55.png">

### A note on the Flask app
⦿ Even if you have never used Flask (and need to do more than just plug in your model), notice that the app is composed of a templates folder that stores the HTML of the pages and a static folder that stores CSS/JS and other assets. Lastly, the app.py file contains the code that runs the app by rendering the right HTML page and passing the right parameters to it according to your request (visiting a URL, submitting a file,...)

### A complete example
```bash
mldir --name <project-name>  --example
```
⦿ The --example option generates a complete example on a dummy dataset (but real models) that should be helpful for you to understand more about the folder structure and how to use it (or you can use it as a template for your own project). The example also uses 

## Credits

Thanks to [Abdullah](https://github.com/abdullahalshawafi) for all his startling work on the mlweb module and for all the time he spent with me to discuss or test the library.

Thanks to [Jimmy](https://github.com/Hero2323) for all his help in testing the library.
### Collaborators
<table>
<tr>
    <td align="center">
        <a href="https://github.com/EssamWisam">
            <img src="https://avatars.githubusercontent.com/u/49572294?v=4" width="100;" alt="EssamWisam"/>
            <br />
            <sub><b>Essam Wisam</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/abdullahalshawafi">
            <img src="https://avatars.githubusercontent.com/u/53022307?v=4" width="100;" alt="AhmedNossir"/>
            <br />
            <sub><b>Abdullah Adel</b></sub>
        </a>
    </td>
</tr>
</table>
