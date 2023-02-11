# pylint: skip-file
import time
import os
from flask import Flask, render_template, request

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
    Defines what the browser should 
    ''' 
    # We can't proceed if the post request doesn't have the file or the file was not selected.
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('model.html', err_msg='No File Selected!')
    
    # Okay, so we have it
    file = request.files['file']
    # You can check if the filetype is correct here, we skippped that for simplicity.

    # Save the file in the uploads folder so the 
    path = os.path.join(os.getcwd() + UPLOADS_FOLDER, file.filename)
    file.save(path)

    # call the model on it
    pipeline = lambda file: 'This is my prediction'     # You will import your trained model from ModelScoring.Pipeline
    time.sleep(3)                                       # As if the model is taking time to run.               
    model_output = pipeline(file)

    #display the model's output
    return render_template('model.html', err_msg='', model_output=model_output)
        
 



if __name__ == '__main__':
    app.run(debug=True)