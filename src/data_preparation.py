import os
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

# Get the absolute path of the project root (one level up from src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Set the path for the 'data' directory in the root directory
data_dir = os.path.join(project_root, 'data')

# Ensure the 'data' directory exists
os.makedirs(data_dir, exist_ok=True)

# Load the California housing dataset
housing = fetch_california_housing(as_frame=True)
df = housing.frame
print(f"Dataset shape: {df.shape}")
print(df.head())

# Split into train and test sets
train, test = train_test_split(df, test_size=0.2, random_state=42)
print(f"Train shape: {train.shape}")
print(f"Test shape: {test.shape}")

# Save train.csv and test.csv with high precision and without index
train_file_path = os.path.join(data_dir, 'train.csv')
test_file_path = os.path.join(data_dir, 'test.csv')

train.to_csv(train_file_path, index=False, float_format="%.10g")
test.to_csv(test_file_path, index=False, float_format="%.10g")

print(f"Train data saved at: {train_file_path}")
print(f"Test data saved at: {test_file_path}")

# Read back train.csv and test.csv
train_read = pd.read_csv(train_file_path)
test_read = pd.read_csv(test_file_path)

def is_approx_equal(df1, df2, tol=1e-6):
    """Check if two DataFrames are approximately equal within a given tolerance."""
    return np.allclose(df1.values, df2.values, atol=tol)

if is_approx_equal(train, train_read):
    print("Train data saved and verified successfully.")
else:
    print("Error: Train data verification failed.")

if is_approx_equal(test, test_read):
    print("Test data saved and verified successfully.")
else:
    print("Error: Test data verification failed.")

print("Data preparation completed!")
