import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.utils.data as utils
import matplotlib.pyplot as plt
import numpy as np 
from tqdm import tqdm
import cv2


# Convolutional neural network with one hidden layer
class ConvNet(nn.Module):
    '''
    CNN Definition
    '''
    def __init__(self, hidden_size, output_size, kernel_dim, in_channels, mid_channels, out_channels,
                 pool_dim=2, pool_stride=2):
        super(ConvNet, self).__init__()
        self.feature_extraction= nn.Sequential(
        nn.Conv2d(in_channels, mid_channels, kernel_dim), nn.ReLU(), nn.MaxPool2d(pool_dim, pool_stride),
        nn.Conv2d(mid_channels, out_channels, kernel_dim), nn.ReLU(), nn.MaxPool2d(pool_dim, pool_stride),
        nn.Flatten()
        )
        self.feed_forward = nn.Sequential(
        nn.LazyLinear(hidden_size), nn.ReLU(),
        nn.Linear(hidden_size, int(hidden_size/2)), nn.ReLU(),
        nn.Linear(int(hidden_size/2), output_size)
        ) 
        

    def forward(self, x):
        '''
        Forward method to pass a given input batch to the model
        '''
        x = self.feature_extraction(x)
        x = self.feed_forward(x)
        return x



def train_model(model, num_epochs, train_loader, criterion, optimizer, device):
    '''
    Training method to train the model for a given number of epochs
    '''
    for epoch in range(num_epochs):
        for  (images, labels) in tqdm(train_loader):  #each batch is a tuple of images and their corresponding labels.
            
            images, labels = images.to(device), labels.to(device)    
            
            # Forward pass
            logits = model(images)                          # Propagate the batch: gives output [batch_size, K] 
            loss = criterion(logits, labels)          # Calculate the loss (uses Softmak on the outputs along the way)
            
            # Backward Pass
            optimizer.zero_grad()                     # Clear the gradients for all network parameters (e.g. due to a previous batch)
            loss.backward()                           # Accumulate all the gradients due to the current batch
            optimizer.step()                          # Update the network's weights and biases
            
    

def validate_model(model, test_loader, device):
    '''
    Validation method to test the model on the test set
    '''
    with torch.no_grad():
        n_correct = 0
        n_correct_rand = 0
        for test_images, test_labels in test_loader:
            test_images, test_labels = test_images.to(device), test_labels.to(device)  
            logits = model(test_images)                                 # Propagate the test batch
            predicted = logits.argmax(1)                    
            n_correct += (predicted == test_labels).sum().item()

            random_guess = torch.from_numpy(np.random.randint(0,2,len(predicted)))
            n_correct_rand += (random_guess == test_labels).sum().item()
            
        batch_size = test_images.shape[0]
        acc = 100.0 * n_correct / (len(test_loader) * batch_size)
        acc_rand = 100.0 * n_correct_rand / (len(test_loader) * batch_size)
        print(f'Model Accuracy is at {acc} and Random Guessing Accuracy is at {acc_rand} %')
    return acc, acc_rand

def save_model(model, path):
    '''
    Save method to save the model
    '''
    torch.save(model.state_dict(), path)
    
    
def load_model(model, path):
    '''
    Load method to load the model
    '''
    model.load_state_dict(torch.load(path))
