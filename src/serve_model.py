import os
import pickle
import pandas as pd
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import logging

# Initialize the Flask app and set the static folder
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
app = Flask(__name__, static_folder=os.path.join(project_root, 'static'))
CORS(app)  # Enable CORS for all routes

# Define the path to the saved model
model_file_path = os.path.join(project_root, 'models', 'model.pkl')

# Load the saved model
try:
    with open(model_file_path, 'rb') as f:
        model = pickle.load(f)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

# Define expected feature names and their types
expected_features = [
    'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude'
]

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions. Expects a JSON payload with feature values.
    Returns predictions or an error message if the request is invalid.
    """
    logging.info("Received request for prediction")

    # Parse the incoming JSON request
    data = request.get_json()

    # Check if 'features' key is present in the request
    if 'features' not in data:
        logging.error("Missing 'features' key in request")
        return jsonify({"error": "Missing 'features' key in request"}), 400

    features = data['features']

    # Validate the length of features
    if len(features) != len(expected_features):
        logging.error(f"Invalid number of features. Expected {len(expected_features)}, got {len(features)}")
        return jsonify({
            "error": f"Invalid number of features. Expected {len(expected_features)}, got {len(features)}"
        }), 400

    # Validate feature types (ensure all are numeric)
    if not all(isinstance(f, (int, float)) for f in features):
        logging.error("All features must be numeric (int or float).")
        return jsonify({
            "error": "All features must be numeric (int or float)."
        }), 400

    # Convert features to DataFrame
    df = pd.DataFrame([features], columns=expected_features)
    logging.info(f"Input features: {df.to_dict(orient='records')}")

    # Make prediction
    try:
        prediction = model.predict(df)
        logging.info(f"Prediction: {prediction}")
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500

    # Return the prediction as a JSON response
    return jsonify({
        "prediction": prediction.tolist(),
        "message": "Prediction successful. House price is in units of $100,000."
    })


@app.errorhandler(404)
def page_not_found(e):
    """Custom error handler for 404 - Not Found."""
    logging.error("404 Error: Endpoint not found")
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    """Custom error handler for 500 - Internal Server Error."""
    logging.error("500 Error: Internal server error")
    return jsonify({"error": "An internal error occurred"}), 500


# -------------------- Swagger/OpenAPI Documentation --------------------

SWAGGER_URL = '/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Path to the Swagger JSON file

# Create a Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={'app_name': "House Price Prediction API"}
)

# Register the Swagger UI blueprint with the Flask app
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# ------------------------ Run the Flask app ------------------------

if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
