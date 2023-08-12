import numpy as np
import cv2
import os
from FeatureExtraction.Fractal.utils import get_fractal_dimension, TTBD


def SFTA(img, deviation=70):                         
    '''
    Applies segmentation-based fractal analysis on the image and returns a feature vector.
    '''
    silhouettes = []
    opt_t,_ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    T = [ opt_t - deviation,opt_t, opt_t + deviation ]
    T.append(np.amax(img))
    for t1, t2 in zip(T, T[1:]):         # Apply two-threshold binary decomposition on the image using each two consequtive thresholds.
        silhouettes.append(TTBD(img, t1, t2))

    if len(T) > 2:
        T.pop()
        for t in T:                         # Apply two-threshold binary decomposition on the image using each threshold and the max value
            silhouettes.append(TTBD(img, t, np.amax(img)))

    fractal_vector = [ get_fractal_dimension(sil) for sil in silhouettes ]      # 2*len(T) Binary Images => Fractal Dimension for each.
    mean_vector = [np.mean(sil) for sil in silhouettes]                         # Get mean of each as well
    
    return fractal_vector + mean_vector

def save_features(apply_SFTA):
    ''' A decorator to the apply_SFTA function that extends it so that:
    - it can take x_train and x_val simultaneously
    - it saves the features
    - it can still only take x_test when eval=True
    '''
    def apply_SFTA_d(x_train, x_val, deviation=70, saved=False, eval=False):
        if eval: return apply_SFTA(x_val, deviation)
        module_dir = os.path.dirname(__file__)
        if saved:
            with open(os.path.join(module_dir, '../../Saved/Fractal.npy'), 'rb') as f:
                x_train = np.load(f, allow_pickle=True)
                x_val = np.load(f, allow_pickle=True)
            return x_train, x_val
        else:
            x_train = apply_SFTA(x_train, deviation)
            x_val = apply_SFTA(x_val, deviation)
            with open(os.path.join(module_dir, '../../Saved/Fractal.npy'), 'wb') as f:
                np.save(f, x_train, allow_pickle=True)
                np.save(f, x_val, allow_pickle=True)
            return x_train, x_val
    return apply_SFTA_d


@save_features
def apply_SFTA(x_data, deviation=70):
    '''
    Applies fractal analysis on the images and returns the feature vectors.
    '''
    x_data = np.array([SFTA(image, deviation) for image in x_data])
    return x_data

