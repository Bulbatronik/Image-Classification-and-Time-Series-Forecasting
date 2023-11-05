import os
import tensorflow as tf
import numpy as np
import random
import pandas as pd
import seaborn as sns

telescope = 864
window = 600

class model:
    def __init__(self, path):
        self.model = tf.keras.models.load_model(os.path.join(path, 'SubmissionModel'))

    def predict(self, X):
        # Insert your preprocessing here

        X = X.numpy()
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)

        future = X[-window:]
        future = (future - X_min) / (X_max - X_min)
        future = np.expand_dims(future, axis=0)

        out = self.model.predict(future)

        # Insert your postprocessing here
        out = out * (X_max - X_min) + X_min  # denormalize
        out = np.reshape(out, (864, 7))
        out = tf.convert_to_tensor(out)

        # check for NaN predictions
        assert not np.isnan(out).any()

        return out
