import numpy as np
import cv2
import torch
import os
from torch.utils.data import TensorDataset, DataLoader


## For classical machine learning algorithms
def save_data(preprocess_data):
    ''' A decorator to the preprocess_data function that extends it so that:
    - it can take x_train and x_val simultaneously
    - it saves the features
    - it can still only take x_test when eval=True
    Its better to do this as a decorator to isolate this from the preprocessing logic.
    '''
    def preprocess_data_d(x_train, x_val, saved=False, eval=False):
        if eval: return preprocess_data(x_val)
        module_dir = os.path.dirname(__file__)
        if saved:
            with open(os.path.join(module_dir, '../Saved/prep.npy'), 'rb') as f:
                x_train = np.load(f, allow_pickle=True)
                x_val = np.load(f, allow_pickle=True)
            return x_train, x_val
        else:
            x_train = preprocess_data(x_train)
            x_val = preprocess_data(x_val)
            with open(os.path.join(module_dir, '../Saved/prep.npy'), 'wb') as f:
                np.save(f, x_train, allow_pickle=True)
                np.save(f, x_val, allow_pickle=True)
            return x_train, x_val
    return preprocess_data_d

@save_data
def preprocess_data(x_data, new_size=(500, 500), crop_size=(400, 400), crop_offset=(100, 100)):
    ''''
    Apply preprocessing on each image in x_data
    '''
    resized_data = []
    # resize all the images to 500x500
    for i in range(len(x_data)):
        resized_data.append(cv2.resize(x_data[i], new_size))

    img_data = []
    # take a center crop of 400x400
    for i in range(len(resized_data)):
        img_data.append(resized_data[i][crop_offset[0]:crop_offset[0] + crop_size[0], crop_offset[1]:crop_offset[1] + crop_size[1]])

    x_data = np.array(img_data)       
    return x_data


## For deep learning
def two_loaders(deep_data_loader):
    '''
    A decorator to the deep_data_loader function that extends it so that:
    - it can take x_train and x_val simultaneously
    - it can still only take x_test when eval=True
    - its not often needed to save the data loaders
    '''
    def deep_data_loader_d(x_train, y_train, x_val, y_val, batch_size=2, eval=False):
        if eval: return deep_data_loader(x_val, y_val, batch_size)
        train_loader = deep_data_loader(x_train, y_train, batch_size)
        val_loader = deep_data_loader(x_val, y_val, batch_size)
        return train_loader, val_loader
    return deep_data_loader_d
    

@two_loaders
def deep_data_loader(x_data, y_data, batch_size=2):
    '''
    For PyTorch deep learning models, we further need a function that creates a data loader out of the data.
    '''
    x_data = np.array([np.vstack(x[:,:]).astype(np.float32) for x in x_data])
    # introduce a new dimension for the channels
    x_data = np.array([x.reshape(1, *x.shape) for x in x_data])
    print(x_data.shape)
    # Create dataset and data loaders
    data = TensorDataset(torch.from_numpy(x_data), torch.from_numpy(y_data))
    data_loader = DataLoader(data, batch_size=batch_size, shuffle=True)
    # check dimensionality of a data item
    print(next(iter(data_loader))[0].shape)
    return data_loader
