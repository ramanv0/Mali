import numpy as np
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
import pandas as pd

def train_model():
    """
    Train the model from the EMBER dataset
    """
    filename = 'dataset/bodmas.npz'
    data = np.load(filename)

    X = data['X']  # all the feature vectors
    y = data['y']  # labels, 0 as benign, 1 as malicious
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    train_df = pd.DataFrame(X_train, columns=np.arange(X_train.shape[1]))
    train_df['label'] = y_train
    predictor = TabularPredictor(label = 'label', path = 'models/ag_test')
    predictor.fit(train_df)

    test_df = pd.DataFrame(X_test, columns=np.arange(X_test.shape[1]))
    test_df['label'] = y_test
    predictor.leaderboard(test_df)

    return predictor


if __name__ == "__main__":
    train_model()