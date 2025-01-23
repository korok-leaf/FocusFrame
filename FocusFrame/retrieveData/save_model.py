import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
import os

from ScreenTime import ScreenTime




def convertNp(data, apps):
    len_data = len(data)

    X_test = np.zeros((len_data, 3))
    Y_test = np.zeros((len_data, 20))

    for i in range(len_data):
        x = data[i][1]
        y = data[i][0]

        X_test[i][0] = x[1]/12 # divide to squish it 
        X_test[i][1] = x[2]/24
        X_test[i][2] = x[5]/6

        if y not in apps:
            ind = apps.index("off")
            Y_test[i][ind] = 1
        else:
            ind = apps.index(y)
            Y_test[i][ind] = 1
    return X_test, Y_test

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(3,)),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(20, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model(X_train, Y_train, epochs=10):
    model = build_model()
    model.fit(X_train, Y_train, epochs=epochs)
    return model

def save_model(model, path):
    model.save(path)

def evaluate_model(model, X_test, Y_test):
    test_loss, test_acc = model.evaluate(X_test, Y_test)
    return test_loss, test_acc

def make_new_model(test_end):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'FocusFrameModel.keras')
    # Retrieve data

    default_time = 757480000 # jan 1 2025
    max_length_data = 32920000 # around 16 days

    default_time = max(default_time, test_end-max_length_data)

    screen = ScreenTime(default_time, test_end)

    data = screen.get_screen_time_data() # jan 1 - January 16 2025 6:16:40 PM
    apps = screen.get_app_names()
    print(len(data))
    X_train, Y_train = convertNp(data, apps)

    # Build and train
    model = train_model(X_train, Y_train, epochs=3)
    save_model(model, model_path)

if __name__ == '__main__':
    make_new_model(758700000)
