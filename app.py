"""
Drag Sail AI — Flask Backend
Inference logic ported exactly from drag_sail_ml_notebook_v2.ipynb
"""
import os
import json
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Model paths ───────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'src', 'models')

# ── Load models once at startup ───────────────────────────────────────────────
def _load():
    with open(os.path.join(MODEL_DIR, 'model_nat_deorbit.pkl'), 'rb') as f:
        nat = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'model_risk_score.pkl'), 'rb') as f:
        risk = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'encoders.pkl'), 'rb') as f:
        enc = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'model_card.json'), 'r') as f:
        card = json.load(f)
    return nat, risk, enc['le_type'], enc['le_rcs'], card

nat_model, risk_model, le_type, le_rcs, model_card = _load()

# Fallback feature order (matches model_card.json → selected_features)
FALLBACK_FEATURES = [
    'PERIAPSIS', 'APOAPSIS', 'BSTAR', 'ECCENTRICITY',
    'MEAN_MOTION', 'MEAN_MOTION_DOT'
]

def _feature_order(model):
    """Use sklearn's stored feature names if available (sklearn >= 1.0)."""
    if hasattr(model, 'feature_names_in_'):
        return list(model.feature_names_in_)
    return FALLBACK_FEATURES


def _build_features(periapsis, apoapsis, bstar, mean_motion_dot, eccentricity,
                    inclination, period, mean_motion, object_type, rcs_size):
    """
    Build feature dict — mirrors _build_feature_row() from the notebook.
    All engineered features included so both 6-feature and 20-feature
    variants of the model are handled automatically.
    """
    bstar_abs = abs(bstar)
    return {
        # Raw orbital elements
        'PERIAPSIS':        periapsis,
        'APOAPSIS':         apoapsis,
        'BSTAR':            bstar,
        'MEAN_MOTION_DOT':  mean_motion_dot,
        'MEAN_MOTION_DDOT': 0.0,
        'SEMIMAJOR_AXIS':   0.0,
        'PERIOD':           period,
        'MEAN_MOTION':      mean_motion,
        'ECCENTRICITY':     eccentricity,
        'INCLINATION':      inclination,
        # Engineered features (notebook Step 4.1)
        'altitude_mean':    (periapsis + apoapsis) / 2,
        'delta_altitude':   apoapsis - periapsis,
        'drag_exposure':    bstar_abs * (1.0 / max(period, 80)),
        'decay_urgency':    mean_motion_dot * period,
        'bstar_log':        float(np.log10(max(bstar_abs, 1e-7))),
        'in_critical_zone': int(550 <= periapsis <= 800),
        'in_upper_leo':     int(800 < periapsis <= 1000),
        'ecc_periapsis':    eccentricity * periapsis,
        # Encoded categoricals (notebook Step 4.2)
        'obj_type_enc': int(le_type.transform([object_type])[0]),
        'rcs_enc':      int(le_rcs.transform([rcs_size])[0]),
    }


def run_inference(periapsis, apoapsis, bstar, mean_motion_dot, eccentricity,
                  inclination, period, mean_motion, object_type, rcs_size):
    """
    Full inference pipeline — mirrors predict() from notebook cell_verify_code.
    Returns dict with all fields needed by the frontend.
    """
    feat = _build_features(
        periapsis, apoapsis, bstar, mean_motion_dot, eccentricity,
        inclination, period, mean_motion, object_type, rcs_size
    )

    # ── Model A: Natural deorbit time ─────────────────────────────────────────
    order_nat  = _feature_order(nat_model)
    X_nat      = np.array([[feat[f] for f in order_nat]])
    nat_years  = float(np.clip(nat_model.predict(X_nat)[0], 0.01, 100))

    # ── Model B: Risk score ───────────────────────────────────────────────────
    order_risk = _feature_order(risk_model)
    X_risk     = np.array([[feat[f] for f in order_risk]])
    risk_score = round(float(np.clip(risk_model.predict(X_risk)[0], 0, 100)), 1)

    # ── Risk level (notebook output_logic.risk_levels) ───────────────────────
    if   risk_score >= 80: risk_level = 'CRITICAL'
    elif risk_score >= 60: risk_level = 'HIGH'
    elif risk_score >= 45: risk_level = 'ELEVATED'
    elif risk_score >= 25: risk_level = 'MODERATE'
    else:                  risk_level = 'LOW'

    # ── Sail deployment (notebook sail_action + sail_pct_map) ─────────────────
    is_payload = (object_type == 'PAYLOAD')
    mult_map   = {'LARGE': 6, 'MEDIUM': 12, 'SMALL': 20}
    mult       = mult_map.get(rcs_size, 10)

    if   risk_score < 25: pct, action = 0,   'MONITOR'
    elif risk_score < 45: pct, action = (10 if is_payload else 20),  'PREPARE'
    elif risk_score < 60: pct, action = (30 if is_payload else 50),  'DEPLOY_PARTIAL'
    elif risk_score < 80: pct, action = (60 if is_payload else 80),  'DEPLOY_HIGH'
    else:                 pct, action = 100, 'DEPLOY_FULL'

    sail_mult   = 1 + (mult - 1) * (pct / 100) if pct > 0 else 1
    sail_years  = round(nat_years / sail_mult, 2)
    years_saved = round(nat_years - sail_years, 2)

    # ── Altitude zone description ─────────────────────────────────────────────
    if   periapsis < 400:        zone = "Very Low LEO (< 400 km)"
    elif periapsis < 550:        zone = "Low LEO (400–550 km)"
    elif periapsis <= 800:       zone = "Critical Belt (550–800 km) ⚠️"
    elif periapsis <= 1000:      zone = "Upper LEO (800–1000 km)"
    else:                        zone = "High LEO (> 1000 km)"

    return {
        'natural_deorbit_years': round(nat_years, 2),
        'risk_score':            risk_score,
        'risk_level':            risk_level,
        'sail_deployment_pct':   pct,
        'action':                action,
        'sail_deorbit_years':    sail_years,
        'years_saved':           years_saved,
        'altitude_zone':         zone,
        'object_type':           object_type,
        'rcs_size':              rcs_size,
        'periapsis':             periapsis,
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', model_card=model_card)


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        d = request.get_json(force=True)
        result = run_inference(
            periapsis=       float(d['periapsis']),
            apoapsis=        float(d['apoapsis']),
            bstar=           float(d['bstar']),
            mean_motion_dot= float(d['mean_motion_dot']),
            eccentricity=    float(d['eccentricity']),
            inclination=     float(d['inclination']),
            period=          float(d['period']),
            mean_motion=     float(d['mean_motion']),
            object_type=     str(d['object_type']),
            rcs_size=        str(d['rcs_size']),
        )
        return jsonify({'status': 'ok', 'result': result})
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f'Missing field: {e}'}), 400
    except ValueError as e:
        return jsonify({'status': 'error', 'message': f'Invalid value: {e}'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/model_info')
def model_info():
    return jsonify(model_card)


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'models_loaded': True})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
