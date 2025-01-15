import os
import pandas as pd

# Create a small dummy dataset
data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
df_original = pd.DataFrame(data)

# Define the test file path
test_file_path = os.path.join(os.getcwd(), 'data', 'test_output.csv')

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

# Save the dummy dataset to a CSV file
df_original.to_csv(test_file_path, index=False)

# Read the dataset back from the CSV file
df_read = pd.read_csv(test_file_path)

# Check if the written and read data match
if df_original.equals(df_read):
    print("Test passed: Data was successfully written to and read from the CSV file.")
else:
    print("Test failed: Data mismatch between written and read CSV files.")
