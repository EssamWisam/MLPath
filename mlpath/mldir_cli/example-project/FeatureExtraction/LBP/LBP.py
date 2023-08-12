import cv2
from skimage.feature import local_binary_pattern
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import os

def LBP(image, P=8, R=1, method="uniform"):
    '''
    given an image, return the LBP histogram of the image
    '''
    # apply LBP
    lbp = local_binary_pattern(image, P, R, method)
    # get the histogram
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, 8 + 3), range=(0, 8 + 2))
    # normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    # return the histogram of Local Binary Patterns
    return hist


def save_features(apply_LBP):
    ''' A decorator to the apply_LBP function that extends it so that:
    - it can take x_train and x_val simultaneously
    - it saves the features
    - it can still only take x_test when eval=True
    '''
    def apply_LBP_d(x_train, x_val, P=8, R=1, method="uniform", saved=False, eval=False):
        if eval: return apply_LBP(x_val, P, R, method)
        module_dir = os.path.dirname(__file__)
        if saved:
            with open(os.path.join(module_dir, '../../Saved/LBP.npy'), 'rb') as f:
                x_train = np.load(f, allow_pickle=True)
                x_val = np.load(f, allow_pickle=True)
            return x_train, x_val
        else:
            x_train = apply_LBP(x_train, P, R, method)
            x_val = apply_LBP(x_val, P, R, method)
            with open(os.path.join(module_dir, '../../Saved/LBP.npy'), 'wb') as f:
                np.save(f, x_train, allow_pickle=True)
                np.save(f, x_val, allow_pickle=True)
            return x_train, x_val
    return apply_LBP_d


# given a numpy array of images, return the LBP histogram of each as a numpy array
@save_features
def apply_LBP(x_data, P=8, R=1, method="uniform"):
    '''
    given a numpy array of images, return the LBP histogram of each as a numpy array
    '''
    x_data = np.array([LBP(image, P, R, method) for image in x_data])
    return x_data



def visualize(x_data, y_data):
    '''
    visualize the data by classes in a scatter plot
    '''
    # create a scatter plot of the data and color it blue or red based on the label
    plt.scatter(x_data[:, 0], x_data[:, 1], c=y_data, cmap=plt.cm.Paired)
    # show the plot
    plt.show()

# dimensionally reduce the data using PCA then visualize the data
def visualize_LBP(x_data, y_data, n_components=2):
    '''
    reduces dimensionality before visualization
    '''
    # dimensionally reduce the data
    x_data = PCA(n_components=n_components).fit_transform(x_data)
    # visualize the data
    visualize(x_data, y_data)
    

    