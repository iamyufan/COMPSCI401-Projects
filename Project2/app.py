import json
import pickle
import urllib.request
import pandas as pd
from flask import Flask, request, jsonify
import os
import numpy as np

from flask import Flask

# Creation of the Flask app
app = Flask(__name__)

model_url = 'https://github.com/iambrucez/COMPSCI401-Project2/raw/main/model.pkl'
model_filename, headers = urllib.request.urlretrieve(model_url, filename = "model.pkl")

app.model = pickle.load(open(model_filename, 'rb'))
    
@app.route('/api/american', methods = ['POST'])
def prediction():
    content = request.get_json(force=True)
    text = np.array([content['text']])        
    prediction = app.model['model'].predict(text)

    return jsonify({"is_american": str(prediction[0]), 
                    "version": app.model['model_version'], 
                    "model_date": app.model['model_date']})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5016")