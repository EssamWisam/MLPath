
# MLPath

MLPath is an MLOPs library on Python that makes tracking machine learning experiments and organizing machine learning projects easier. It consists of two subpackages so far, MLQuest for tracking and MLDir for directory structure.

Check this for <a href='https://essamwisam.github.io/MLPath/mlpath.mlquest.html#module-mlpath.mlquest.mlquest'>documentation</a>.
### 💻 Installation
```
pip install mlpath
```

<h1 text-align='center'> MLQuest </h1>
<img src="https://user-images.githubusercontent.com/49572294/218260658-846c1aab-fe57-44fa-baa6-5d988ff07e1b.png"></img>

### 🚀 Quick Start

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

# 1. Import the Package
from mlpath import mlquest as mlq
l = mlq.l

# 2. Start a new quest, this simply create a table or loads an existing one to log your next run
mlq.start_quest('Radial Basis Pipeline', log_defs=False)     

# 3. Wrap function calls to be logged with `l()`

# Preprocessing
x_data_p = l(Preprocessing)(x_data=[1, 2, 3], alpha=1114, beta_param=2, c=925)

# Feature Extraction
x_data_f = l(FeatureExtraction)(x_data_p, 32, 50, 4)  # x_data_p is an array so it won't be logged.

# Model Initialization
model = l(RadialBasisNet)(x_data_f, 99, 19, 31)

# Model Training
accuracy = train_model(model)

# 4. log any metrics if needed
mlq.log_metrics(accuracy)        # can also do mlq.log_metric(acc=accuracy) so its logged as acc

# 5. End the quest to push the experiment to the table and save as markdown at './'
mlq.end_quest('./')

# 6. View the table (only for notebooks)
mlq.show_logs(last_k=10)         # show the table for the last 10 runs

```
This results in the following after three runs shown below the cell in the notebook or the separate markdown file.
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

Editors like VSCode support viewing markdown out-of-the-box. You may need to press `CTRL/CMD+Shift+V`. You can see a fuller version of this quick start in the [documentation](https://essamwisam.github.io/MLPath/Example.html) which corresponds to the `Full-Example` notebook found here which you can also run locally.



### <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png" width=30> An example with Scikit-Learn

Check `Example.ipynb` or equivalently the following [Colab notebook](https://drive.google.com/file/d/1OcNfL1mxQM5lr9LI9PFheD7gI5Rdphw8/view?usp=sharing).


### <img src="https://creazilla-store.fra1.digitaloceanspaces.com/icons/3254256/pytorch-icon-sm.png" width=20> An Example with PyTorch

More examples with `sci-kit learn` and an example with `PyTorch` could be found by running `mldir --example` as will be illustrated down below.

### 🌐 A Web Interface is also Supported

Simply run `mlq.run_server()` after `mlq.end_quest`

<img width="1430" alt="image" src="https://user-images.githubusercontent.com/49572294/218263965-3e376645-e85f-4045-8cf2-20294832983f.png">


⦿ You can search for specific runs, an example would be ```metrics.accuracy>50``` (similar syntax to MLFlow)

⦿ You can customize the columns to show in the table by clicking on `columns` (in lieu of doing it through```json``` config file)

<h1 text-align='center'> MLDir </h1>

<img src="https://user-images.githubusercontent.com/49572294/218267208-c4f01847-4184-4732-aa10-bfe7f37b7005.png"></img>

MLDir is a simple CLI that creates a standard directory structure for your machine learning project. It provides a folder structure that is comprehensive, highly scalable (development-wise) and apt for collaboration.

#### Note of caution

⦿ Although it integrates well with MLQuest, neither MLQuest nor MLDir require the other to function.

⦿ Suppose your project has very few people working on it (only you) or does not require trying many models with many other preprocessing methods and features, then you may not really need MLDir. A notebook and MLQuest should be enough. Otherwise use MLDir to prevent your directory from becoming a spaghetti soup of Python files.


### 📜 The MLDir Manifesto
The directory structure generated by MLDir complies with the MLDir manifesto ( a set of 'soft' standards) which attempts to enforce seperation of concerns among different stages of the machine learning pipeline and among writing code and running experiments (hyperparameter tuning). We recommend that you read more about the manifesto [here](https://github.com/EssamWisam/MLPath/tree/main/mlpath/mldir_cli/project).

### To get started

MLDir is part of MLPath. So you don't need to install it separately. To create a simple folder structure, run:
```bash
mldir --name <project_name>
```
⦿ If mldir is ran without a name, it uses the name 'Project'

This generates the following folder structure (with dummy names for features and models):

```
.
├── DataPreparation
│   ├── Ingestion.py
│   └── Preprocessing.py
├── FeatureExtraction
│   ├── BoW
│   │   └── BoW.py
│   ├── GLCM
│   │   └── GLCM.py
│   └── OneHot
│       └── OneHot.py
├── GIT-README.md
├── ModelPipelines
│   ├── GRU
│   │   └── OneHot-GRU.ipynb
│   ├── GradientBoost
│   │   ├── BoW-GB.ipynb
│   │   └── GLCM-GB.ipynb
│   └── SVM
│       └── BoW-SVM.ipynb
├── ModelScoring
│   ├── Pipeline.py
│   └── Scoring.py
├── README.md
└── Sandbox.ipynb
```
The file in each folder has instructions on how to use it. These are all grouped in the `README.md` for a more detailed explanation.

### Other important options

```bash
mldir --name<project-name> --full
```
⦿ The --full option generates an even more comprehensive folder structure. Including folders such as ```ModelImplementations```, ```References``` and most importantly ```Production```.

⦿ The ```Production``` folder contains a Flask app that can be used to serve your model as an API. All you need is only to import your final model into app.py and replace the dummy model with it. The Flask app assumes that your model takes a file via path and returns a prediction but it can be easilt extended otherwise to suit your needs

<img width="1430" alt="image" src="https://user-images.githubusercontent.com/49572294/218269358-d2db4974-c5a1-4531-a696-69e842f7bb55.png">


## 🚢 Complete Example (MLQuest + MLDir)
```bash
mldir --name <project-name>  --example
```
⦿ The --example option generates a complete example on a tiny dataset (and real models) that should be helpful for you to understand more about the folder structure and how to use it (e.g., you can use it as a template for your own project). 

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
