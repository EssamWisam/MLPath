import sys
sys.path.append('../')
from DataPreparation.Ingestion import read_data, read_sample
from ModelScoring.Pipeline import pipeline
import pickle as pkl
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

def score():
    '''
    This is the pipeline function that runs the whole project.
    '''
    # run the pipeline
    x_test_i, y_test_i = read_data(eval=True)
    y_pred = pipeline(x_test_i)
    # save the predictions in this folder as a csv
    df = pd.DataFrame({'y_pred': y_pred, 'y_test': y_test_i})
    df.to_csv('./results.csv', index=False)
    
    # print the accuracy
    print('Accuracy: ', accuracy_score(y_test_i, y_pred))
    return y_pred

if __name__ == '__main__':
    score()
