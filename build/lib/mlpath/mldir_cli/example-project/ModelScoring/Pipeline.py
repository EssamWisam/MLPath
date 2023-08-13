import sys
import numpy as np
import os
sys.path.append('../')
from DataPreparation.Preprocessing import preprocess_data
from FeatureExtraction.Fractal.Fractal import apply_SFTA
import pickle as pkl


def pipeline(x):
    '''
    This is the pipeline function that runs the whole project.
    '''
    # load the Fractal-GB Model
    module_dir = os.path.dirname(__file__)
    with open(os.path.join(module_dir, '../Saved/Fractal-GB.pkl'), 'rb') as f:
        model = pkl.load(f)
    # run the pipeline
    x_p = preprocess_data(None, x, eval=True)
    x_f = apply_SFTA(None, x_p, eval=True)
    y_pred = model.predict(x_f)
    
    return y_pred

