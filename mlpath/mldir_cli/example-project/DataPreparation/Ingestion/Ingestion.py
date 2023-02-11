import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
from sklearn.model_selection import train_test_split


def read_data(saved=False, eval=False):
    '''
    reads the dataset from the folder and returns the train, validation and test sets
    '''
    if saved:
        with open('../../Saved/DataPreparation/Ingestion/data.npy', 'rb') as f:
            x_data = np.load(f, allow_pickle=True)
            y_data = np.load(f, allow_pickle=True)
        
    else:
        x_data, y_data= [], []
        
        #load golden retriever images
        for filename in tqdm(sorted(glob.glob('../../DataFiles/Dataset/Golden/*.jpeg'))):
            try:
                img = cv2.imread(filename, 0)                           # 0 to read in grayscale
                x_data.append(img)
                y_data.append(1)
            except:
                print("corrupted image detected.")
            

        ## load swedish elkhound images
        for filename in tqdm(sorted(glob.glob('../../DataFiles/Dataset/Swedish/*.jpeg'))):
            try:
                img = cv2.imread(filename, 0)
                x_data.append(img)
                y_data.append(0)
            except:
                print("corrupted image detected.") 

        x_data,  y_data = np.array(x_data), np.array(y_data)
        


        with open('../../Saved/DataPreparation/Ingestion/data.npy', 'wb') as f:
            np.save(f, x_data, allow_pickle=True)
            np.save(f, y_data, allow_pickle=True)

    # Split into training, validation and test sets
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.4, random_state=42)
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)


    if eval:        return x_test, y_test
    
    return x_train, x_val, y_train, y_val


def read_sample(path):
    '''
    A read_sample function for when the model is deployed
    '''
    x_data = []         
    img = np.array(cv2.imread(path, 0))
    x_data.append(img)
    return np.array(x_data)     # By putting in a numpy array, we can use the same pipeline as the test data


def visualize_data(x_data, y_data, num_images=3):
    """
    show num_images next to each other
    """
    fig, axs = plt.subplots(1, num_images, figsize=(15, 15))
    for i in range(num_images):
        axs[i].imshow(x_data[i], cmap='gray')
        axs[i].set_title('Golden Retriever' if y_data[i] == 1 else 'Swedish Elkhound')
        axs[i].axis('off')

    plt.show()