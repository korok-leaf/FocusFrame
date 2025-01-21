import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
from getScreenTime import get_screen_time_data
from getAppName import get_app_name
import os

def convertNp(data, apps):
    # ...code from prototype...
    len_data = len(data)
    len_apps = len(apps)

    X_test = np.zeros((len_data, 4))
    Y_test = np.zeros((len_data,))

    for i in range(len_data):
        x = data[i][1]
        y = data[i][0]

        X_test[i][0] = x[1]/12
        X_test[i][1] = x[2]/24
        X_test[i][2] = x[3]/60
        X_test[i][3] = x[5]/6

        if y not in apps:
            Y_test[i] = 1
        else:
            ind = apps.index(y)
            Y_test[i] = ind/len_apps
    return X_test, Y_test

def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(4, activation='relu'),
        tf.keras.layers.Dense(30, activation='relu'),
        tf.keras.layers.Dense(70, activation='relu'),
        tf.keras.layers.Dense(100, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model(X_train, Y_train, epochs=20):
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

    default_time = 725780000 # jan 1 2024
    max_length_data = 32920000 # around 16 days

    default_time = max(default_time, test_end-max_length_data)

    data = get_screen_time_data(default_time, test_end) # jan 1 - January 16 2025 6:16:40 PM
    apps = get_app_name(default_time, test_end)
    print(len(data))
    X_train, Y_train = convertNp(data, apps)

    # Build and train
    model = train_model(X_train, Y_train, epochs=3)
    save_model(model, model_path)

if __name__ == '__main__':
    make_new_model(758700000)
