import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import joblib
from getScreenTime import get_screen_time_data
from getAppName import get_app_name

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

def evaluate_model(model, X_test, Y_test):
    test_loss, test_acc = model.evaluate(X_test, Y_test)
    return test_loss, test_acc

def run_production_flow():
    # Retrieve data
    data = get_screen_time_data(758099000, 758700000)
    apps = get_app_name(758099000, 758700000)
    X_train, Y_train = convertNp(data, apps)

    # Build and train
    model = train_model(X_train, Y_train, epochs=20)

    # Testing
    testing_data_x = get_screen_time_data(758700000, 758990000)
    testing_data_y = get_app_name(758700000, 758990000)
    testing_x, testing_y = convertNp(testing_data_x, testing_data_y)

    test_loss, test_acc = evaluate_model(model, testing_x, testing_y)
    print("test accuracy:", test_acc)

if __name__ == '__main__':
    run_production_flow()
