import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import lightgbm as lgb
import numpy as np

# Get the project root directory (one level up from src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

# Define paths for data and model
train_file_path = os.path.join(project_root, 'data', 'train.csv')
model_file_path = os.path.join(project_root, 'models', 'model.pkl')

# Load the training data
train = pd.read_csv(train_file_path)

# Define features and target
X = train.drop(columns='MedHouseVal')  # Drop the target column to get features
y = train['MedHouseVal']               # Target variable

# Split data into training and validation sets (80% train, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------- RANDOM FOREST WITH HYPERPARAMETER TUNING -------------------

# Initialize Random Forest Regressor
rf = RandomForestRegressor(random_state=42)

# Define hyperparameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Perform GridSearchCV
print("Starting hyperparameter tuning for Random Forest...")
grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Get the best model from grid search
best_rf = grid_search.best_estimator_

# Predict on the validation set
y_pred_rf = best_rf.predict(X_val)

# Calculate and print the Mean Squared Error (MSE) on the validation set
mse_rf = mean_squared_error(y_val, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
print(f"Validation MSE (Random Forest): {mse_rf:.4f}")
print(f"Validation RMSE (Random Forest): {rmse_rf:.4f}")

# ---------------------------- LIGHTGBM MODEL ----------------------------

# Initialize LightGBM Regressor
print("Training LightGBM model...")
lgb_model = lgb.LGBMRegressor(random_state=42, n_estimators=1000, learning_rate=0.05, max_depth=10)

# Train LightGBM model with early stopping using callbacks
lgb_model.fit(
    X_train,
    y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='rmse',
    callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=10)]
)

# Predict on the validation set
y_pred_lgb = lgb_model.predict(X_val)

# Calculate and print the Mean Squared Error (MSE) on the validation set
mse_lgb = mean_squared_error(y_val, y_pred_lgb)
rmse_lgb = np.sqrt(mse_lgb)
print(f"Validation MSE (LightGBM): {mse_lgb:.4f}")
print(f"Validation RMSE (LightGBM): {rmse_lgb:.4f}")

# -------------------------- SAVE BEST MODEL --------------------------

# Ensure the 'models' directory exists
os.makedirs(os.path.dirname(model_file_path), exist_ok=True)

# Save the best model based on validation RMSE
if rmse_lgb < rmse_rf:
    with open(model_file_path, 'wb') as f:
        pickle.dump(lgb_model, f)
    print(f"Best model (LightGBM) saved at: {model_file_path}")
else:
    with open(model_file_path, 'wb') as f:
        pickle.dump(best_rf, f)
    print(f"Best model (Random Forest) saved at: {model_file_path}")
