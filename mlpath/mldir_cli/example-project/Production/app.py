# pylint: skip-file
import sys
import time
import os
from flask import Flask, render_template, request
sys.path.append('../')
from DataPreparation.Ingestion import read_sample
from ModelScoring.Pipeline import pipeline
from ModelScoring.Scoring import score

UPLOADS_FOLDER = '/static/uploads/'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    '''
    The browser will render home.html when it visits '/' (the root of the web app)
    '''
    return render_template('home.html')


@app.route('/model', methods=['GET'])
def models_page():
    '''
    The browser will render model.html when it visits '/model'
    '''
    return render_template('model.html')


@app.route('/model', methods=['POST'])
def model_page():
    '''
    Defines what the browser should do when a post request (e.g. upload) is done on /model 
    '''
    if request.method == 'POST':
        
        # We can't proceed if the post request doesn't have the file or the file was not selected.
        if 'file' not in request.files or request.files['file'].filename == '':
            return render_template('model.html', err_msg='No File Selected!')
        
        # Okay, so we have it
        file = request.files['file']
        # You can check if the filetype is correct here, we skippped that for simplicity.
        path = os.path.join(os.getcwd() + UPLOADS_FOLDER, file.filename)
        # Save the file in the uploads folder so the 
        file.save(path)

        # call the model on it
        x = read_sample(path)
        model_output = pipeline(x)[0].item()
        
        if model_output == 1:
            model_output = 'Golden Retriever'
        else:
            model_output = 'Swedish Elkhound'

        #display the model's output
        return render_template('model.html', err_msg='', model_output=model_output)
        
 



if __name__ == '__main__':
    app.run(debug=True, port=5001)