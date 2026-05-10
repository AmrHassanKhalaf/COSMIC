# 🚀 COSMIC TEAM — Drag Sail AI
### Impact of Drag Sail on Satellite Orbital Decay

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/AI-RandomForest-green)
![Space Sustainability](https://img.shields.io/badge/IEEE-AESS-orange)
![Status](https://img.shields.io/badge/Status-Research%20Prototype-success)

---

# 📌 Project Overview

**Drag Sail AI** is an AI-powered orbital sustainability project developed by **COSMIC TEAM** for the **IEEE AESS Sustainability Hackathon 2026**.

The project focuses on predicting:
- 🛰️ Natural satellite deorbit time
- ⚠️ Orbital collision risk
- 🌌 Optimal drag sail deployment strategy

using real orbital mechanics data and machine learning models.

The system helps reduce the growing danger of **space debris** in Low Earth Orbit (LEO) by recommending intelligent drag sail deployment actions for satellites and debris objects.

---

# 🌍 Problem Statement

Space debris is becoming one of the biggest threats to future space missions.

More than:
- **37,000+ tracked objects**
- **100+ million small fragments**

currently orbit Earth at extremely high velocities.

Without active mitigation:
- Collision probability increases
- Satellite operations become unsafe
- Kessler Syndrome risk rises dramatically

Our solution introduces an intelligent AI-assisted drag sail recommendation system to accelerate safe orbital decay.

---

# 🧠 Proposed Solution

The project combines:
- Orbital mechanics
- Feature engineering
- Machine learning
- Sustainability-focused decision logic

to estimate:

| Output | Description |
|---|---|
| `natural_deorbit_years` | Estimated orbital lifetime |
| `risk_score` | Collision & sustainability risk |
| `risk_level` | LOW → CRITICAL |
| `recommended_action` | Suggested drag sail action |
| `sail_deorbit_years` | Lifetime after drag sail deployment |
| `years_saved` | Reduction in orbital lifetime |

---

# 🛰️ System Architecture

```text
Space-Track Dataset
        ↓
Orbital Feature Engineering
        ↓
AI Prediction Models
 ├── Model A → Deorbit Time
 └── Model B → Risk Score
        ↓
Decision Engine
        ↓
Smart Drag Sail Recommendation
```

---

# 📂 Repository Structure

```text
COSMIC/
│
├── README.md
├── requirements.txt
│
├── models/
│   ├── deorbit_model.pkl
│   ├── risk_model.pkl
│   └── encoders.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── prediction.py
│   └── decision_engine.py
│
├── simulation/
│   ├── orbital_decay_simulation.py
│   └── matlab_simulation/
│
├── gui/
│   ├── app.py
│   ├── templates/
│   └── static/
│
├── results/
│   ├── evaluation_metrics.csv
│   ├── feature_importance.png
│   └── sample_outputs/
│
├── docs/
│   ├── concept_document.pdf
│   ├── presentation.pdf
│   └── architecture_diagrams/
│
└── assets/
    ├── images/
    └── demo_video/
```

---

# ⚙️ Technologies & Tools Used

## 🧠 AI & Data Science
- Python
- Scikit-learn
- Random Forest Regressor
- Pandas
- NumPy

## 🌌 Space & Simulation
- Orbital Mechanics
- MATLAB Simulation
- TLE / Space-Track Data
- Drag & Decay Modeling

## 🌐 GUI & Deployment
- Flask
- HTML / CSS / JavaScript
- Render Deployment

## 📊 Visualization
- Matplotlib
- Seaborn

---

# 📈 Model Performance

| Model | Task | R² Score | MAE |
|---|---|---|---|
| Model A | Deorbit Prediction | 0.9935 | 1.234 years |
| Model B | Risk Prediction | 0.9701 | 1.756 points |

---

# 🔬 Important Engineered Features

| Feature | Purpose |
|---|---|
| `decay_urgency` | Measures orbital instability |
| `bstar_log` | Atmospheric drag influence |
| `ecc_periapsis` | Combined orbit-shape effect |
| `in_critical_zone` | Detects dangerous orbital regions |
| `delta_altitude` | Orbit variation |

---

# 🛰️ Drag Sail Decision Logic

| Risk Level | Action |
|---|---|
| LOW | MONITOR |
| MODERATE | PREPARE |
| ELEVATED | DEPLOY_PARTIAL |
| HIGH | DEPLOY_HIGH |
| CRITICAL | DEPLOY_FULL |

The deployment percentage depends on:
- Object type
- Risk score
- Orbital lifetime
- Sustainability impact

---

# 🧪 Simulation

The project includes:
- Orbital decay simulations
- MATLAB-based re-entry visualization
- Drag sail deployment modeling
- Satellite burn-up animation

---

# ▶️ How to Run the Project

## 1️⃣ Clone Repository

```bash
git clone https://github.com/AmrHassanKhalaf/COSMIC.git
cd COSMIC
```

---

## 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Flask GUI

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# 📥 Example Input

```python
{
    "PERIAPSIS": 700,
    "APOAPSIS": 720,
    "BSTAR": 0.00012,
    "ECCENTRICITY": 0.002,
    "MEAN_MOTION": 14.8,
    "MEAN_MOTION_DOT": 0.00008,
    "OBJECT_TYPE": "DEBRIS",
    "RCS_SIZE": "MEDIUM"
}
```

---

# 📤 Example Output

```python
{
    "natural_deorbit_years": 28.4,
    "risk_score": 74.6,
    "risk_level": "HIGH",
    "recommended_action": "DEPLOY_HIGH",
    "sail_deployment_pct": 80,
    "sail_deorbit_years": 4.1,
    "years_saved": 24.3
}
```

---

# 📊 Sustainability Impact

| Scenario | Orbital Lifetime |
|---|---|
| Natural Decay | 25+ years |
| With Drag Sail | ~3.4 years |

The proposed solution significantly reduces orbital congestion and improves long-term space sustainability.

---

# ⚠️ Assumptions & Limitations

- Current models are trained primarily on LEO objects.
- Atmospheric density variations are simplified.
- Risk score is AI-estimated and not an official aerospace safety metric.
- Solar activity effects are approximated.
- Simulation outputs are research-oriented and not flight-certified.

---

# 🤖 AI Usage Disclosure

This project used AI-assisted tools during:
- Research organization
- README drafting
- Documentation refinement
- GUI planning assistance
- Feature engineering discussions

However:
- All orbital logic
- Model training
- Feature engineering
- Sustainability analysis
- Final validation

were reviewed, modified, and validated manually by the COSMIC TEAM.

---

# 👨‍🚀 Team — COSMIC TEAM

- Rahma Ramadan
- Amr Hassan
- Haneen Taha
- Farah Ali
- Evram Ashraf
- Rofida Abdellattef

---

# 📚 References

- NASA Orbital Debris Program
- Space-Track.org
- IADC Space Debris Guidelines
- Orbital Mechanics for Engineering Students
- IEEE AESS Sustainability References

---

# 🌌 Final Vision

> “Making Earth Orbit Safer Through Intelligent Sustainable Deorbiting.”

COSMIC TEAM aims to combine AI and aerospace sustainability to support safer future space operations and reduce long-term orbital debris accumulation.

---
