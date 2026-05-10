from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

SAVE_DIR = os.path.join(os.path.dirname(__file__), 'drag_sail_models')

# Load models and encoders
with open(f'{SAVE_DIR}/model_nat_deorbit.pkl', 'rb') as f:
    loaded_nat = pickle.load(f)

with open(f'{SAVE_DIR}/model_risk_score.pkl', 'rb') as f:
    loaded_risk = pickle.load(f)

with open(f'{SAVE_DIR}/encoders.pkl', 'rb') as f:
    enc = pickle.load(f)
    loaded_le_type = enc['le_type']
    loaded_le_rcs  = enc['le_rcs']

# Expected feature order for this RF model
FEATURE_ORDER = [
    'PERIAPSIS', 'APOAPSIS', 'BSTAR', 'ECCENTRICITY', 'MEAN_MOTION', 'MEAN_MOTION_DOT'
]

@app.route('/', methods=['GET'])
def index():
    return render_template('drag_sail_ai_app.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        periapsis = float(data['periapsis'])
        apoapsis = float(data['apoapsis'])
        bstar = float(data['bstar'])
        mmdot = float(data['mmdot'])
        eccentricity = float(data['eccentricity'])
        mean_motion = float(data['meanmotion'])
        
        # Build features array exactly as the model expects
        features = np.array([[
            periapsis,
            apoapsis,
            bstar,
            eccentricity,
            mean_motion,
            mmdot
        ]])
        
        # Predict using loaded .pkl models
        nat_years = float(np.clip(loaded_nat.predict(features)[0], 0.01, 100))
        risk_raw = float(np.clip(loaded_risk.predict(features)[0], 0, 100))
        
        # Apply the sail logic natively in the frontend to keep it interactive
        # Or we can return the exact numbers here
        return jsonify({
            'success': True,
            'natural_deorbit_years': nat_years,
            'risk_score': risk_raw,
            'features_used': FEATURE_ORDER
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Drag Sail AI Backend API...")
    app.run(port=5000, debug=True)
