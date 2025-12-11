from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import xgboost as xgb
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for GitHub Pages to access the API

# Global variable to store the trained model
model = None

def train_model():
    """Train the XGBoost model using the dataset"""
    global model
    
    # Load the dataset
    csv_path = r"C:\Users\ichan\OneDrive\Desktop\total_rgb_Brix_Hardness_AC.csv"
    
    if not os.path.exists(csv_path):
        print(f"Warning: Dataset not found at {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    X = df.drop(columns=['Anti-oxidation'])
    y = df['Anti-oxidation']
    
    # Train on full dataset for production
    train_dmatrix = xgb.DMatrix(data=X, label=y)
    
    # Model parameters (same as in your Xgboost_AC.py)
    param = {
        "booster": "gbtree",
        "objective": "reg:squarederror",
        "max_depth": 4,
        "alpha": 10,
        "eta": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8
    }
    
    # Train the model
    model = xgb.train(params=param, dtrain=train_dmatrix, num_boost_round=100)
    print("Model trained successfully!")
    return model

def load_or_train_model():
    """Load existing model or train a new one"""
    global model
    model_path = "xgb_model.json"
    
    if os.path.exists(model_path):
        print(f"Loading model from {model_path}")
        model = xgb.Booster()
        model.load_model(model_path)
    else:
        print("Training new model...")
        model = train_model()
        if model:
            model.save_model(model_path)
            print(f"Model saved to {model_path}")

@app.route('/')
def home():
    """API documentation endpoint"""
    return jsonify({
        "message": "Anti-oxidation Prediction API",
        "version": "1.0",
        "endpoints": {
            "/predict": {
                "method": "POST",
                "description": "Predict anti-oxidation from RGB, Brix, and Hardness values",
                "parameters": {
                    "r": "Red value (0-255)",
                    "g": "Green value (0-255)",
                    "b": "Blue value (0-255)",
                    "brix": "Brix value (sugar content)",
                    "hardness": "Hardness value"
                },
                "example": {
                    "r": 200,
                    "g": 150,
                    "b": 100,
                    "brix": 12.5,
                    "hardness": 8.3
                }
            },
            "/health": {
                "method": "GET",
                "description": "Check API health status"
            }
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict anti-oxidation from input features"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['r', 'g', 'b', 'brix', 'hardness']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Extract and validate values
        r = float(data['r'])
        g = float(data['g'])
        b = float(data['b'])
        brix = float(data['brix'])
        hardness = float(data['hardness'])
        
        # Validate RGB ranges
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            return jsonify({
                "error": "RGB values must be between 0 and 255"
            }), 400
        
        # Create input DataFrame with correct column names
        # Adjust column names based on your dataset
        input_data = pd.DataFrame({
            'R': [r],
            'G': [g],
            'B': [b],
            'Brix': [brix],
            'Hardness': [hardness]
        })
        
        # Convert to DMatrix for prediction
        dmatrix = xgb.DMatrix(input_data)
        
        # Make prediction
        if model is None:
            return jsonify({
                "error": "Model not loaded. Please check server logs."
            }), 500
        
        prediction = model.predict(dmatrix)[0]
        
        # Return prediction
        return jsonify({
            "prediction": float(prediction),
            "input": {
                "r": r,
                "g": g,
                "b": b,
                "brix": brix,
                "hardness": hardness
            },
            "status": "success"
        })
        
    except ValueError as e:
        return jsonify({
            "error": f"Invalid input format: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Prediction failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting Anti-oxidation Prediction API...")
    print("Loading model...")
    load_or_train_model()
    
    if model is None:
        print("ERROR: Model could not be loaded or trained!")
        print("Please check that the dataset file exists.")
    else:
        print("Model ready!")
    
    # Run the Flask app
    print("Starting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
