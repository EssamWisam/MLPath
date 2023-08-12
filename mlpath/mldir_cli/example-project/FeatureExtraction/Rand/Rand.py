import numpy as np
import os

# lets sample random pixels from the image to create a feature vector
def rand(img, num_samples=100):
    '''
    Takes an image and returns a feature vector of length num_samples
    '''
    # get the dimensions of the image
    height, width = img.shape

    # create a feature vector
    feature_vector = []

    # sample random pixels
    for i in range(num_samples):
        # get a random x coordinate
        x = int(np.random.random_integers(0, width-1))

        # get a random y coordinate
        y = int(np.random.random_integers(0, height-1))

        # get the color of the pixel at (x, y)
        pixel = img[y, x]

        # add the pixel to the feature vector
        feature_vector.append(pixel)
    # return the feature vector
    feature_vector = np.array(feature_vector)
    
    return np.squeeze(feature_vector)



def save_features(apply_rand):
    ''' A decorator to the apply_rand function that extends it so that:
    - it can take x_train and x_val simultaneously
    - it saves the features
    - it can still only take x_test when eval=True
    '''
    module_dir = os.path.dirname(__file__)
    def apply_rand_d(x_train, x_val, num_samples=100, saved=False, eval=False):
        if eval: return apply_rand(x_val, num_samples)
        if saved:
            with open(os.path.join(module_dir, '../../Saved/Rand.npy'), 'rb') as f:
                x_train = np.load(f, allow_pickle=True)
                x_val = np.load(f, allow_pickle=True)
            return x_train, x_val
        else:
            x_train = apply_rand(x_train, num_samples)
            x_val = apply_rand(x_val, num_samples)
            with open(os.path.join(module_dir, '../../Saved/Rand.npy'), 'wb') as f:
                np.save(f, x_train, allow_pickle=True)
                np.save(f, x_val, allow_pickle=True)
            return x_train, x_val
    return apply_rand_d


@save_features
def apply_rand(x_data, num_samples=100):
    '''
    Simply applies the rand function to each image in x_data
    '''
    x_data = np.array([rand(x, num_samples) for x in x_data])
    return x_data

