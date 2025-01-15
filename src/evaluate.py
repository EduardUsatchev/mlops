import os
import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error
import numpy as np

# Get the project root directory (one level up from src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Define paths for test data and the saved model
test_file_path = os.path.join(project_root, 'data', 'test.csv')
model_file_path = os.path.join(project_root, 'models', 'model.pkl')

# Load the test data
test = pd.read_csv(test_file_path)

# Define features and target
X_test = test.drop(columns='MedHouseVal')  # Drop the target column to get features
y_test = test['MedHouseVal']               # Target variable

# Load the saved model
with open(model_file_path, 'rb') as f:
    model = pickle.load(f)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"Test MSE: {mse:.4f}")
print(f"Test RMSE: {rmse:.4f}")
