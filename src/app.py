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
        risk_score = round(risk_raw, 1)

        # Risk level
        if   risk_score >= 80: risk_level = 'CRITICAL'
        elif risk_score >= 60: risk_level = 'HIGH'
        elif risk_score >= 45: risk_level = 'ELEVATED'
        elif risk_score >= 25: risk_level = 'MODERATE'
        else:                  risk_level = 'LOW'

        # Sail recommendation
        rcssize = str(data.get('rcssize', 'MEDIUM'))
        object_type = str(data.get('objtype', 'DEBRIS'))
        is_payload = (object_type == 'PAYLOAD')
        mult = {'LARGE':6, 'MEDIUM':12, 'SMALL':20}.get(rcssize, 10)

        if   risk_score < 25: pct, action = 0,   'MONITOR'
        elif risk_score < 45: pct, action = (10 if is_payload else 20),  'PREPARE'
        elif risk_score < 60: pct, action = (30 if is_payload else 50),  'DEPLOY_PARTIAL'
        elif risk_score < 80: pct, action = (60 if is_payload else 80),  'DEPLOY_HIGH'
        else:                 pct, action = 100, 'DEPLOY_FULL'

        sail_mult  = 1 + (mult - 1) * (pct / 100) if pct > 0 else 1
        sail_years = round(nat_years / sail_mult, 2)

        return jsonify({
            'success': True,
            'natural_deorbit_years': round(nat_years, 2),
            'risk_score': risk_score,
            'risk_level': risk_level,
            'sail_deployment_pct': pct,
            'action': action,
            'sail_deorbit_years': sail_years,
            'years_saved': round(nat_years - sail_years, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Starting Drag Sail AI Backend API...")
    app.run(port=5000, debug=True)
