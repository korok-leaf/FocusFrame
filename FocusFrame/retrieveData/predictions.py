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

from save_model import make_new_model, convertNp, evaluate_model


# make_new_model(758700000)


# Testing

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FocusFrameModel.keras')
model = tf.keras.models.load_model(model_path)
    
testing_data_x = get_screen_time_data(758700000, 758990000)
testing_data_y = get_app_name(758700000, 758990000)
testing_x, testing_y = convertNp(testing_data_x, testing_data_y)

test_loss, test_acc = evaluate_model(model, testing_x, testing_y)
print("test accuracy:", test_acc)