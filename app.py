import pickle as pkl
from flask import Flask, request
import numpy as np
from autogluon.tabular import TabularPredictor
from features import predict_sample
import pandas as pd

app = Flask(__name__)
model = None

def load_model():
    global model
    model = TabularPredictor.load('./models/ag_test')

@app.route('/')
def home_endpoint():
    return 'Mali: A malware classification tool.'

@app.route('/predict', methods=['POST'])
def get_prediction():
    if request.method == 'POST':
        file_data = request.files['file'].read()
        score, sha256 = predict_sample(model, file_data)
        if score == 0:
            return 'Benign'
        else:
            family_data = pd.read_csv("dataset/bodmas_malware_category.csv")
            malware_msg = 'Malware'
            if (family_data['sha256'].str.contains(sha256)):
               return malware_msg + "Identified malware family: " + family_data.loc[family_data['sha256'] == sha256, 'category']
            return malware_msg

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5000)