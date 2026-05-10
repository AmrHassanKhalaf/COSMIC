# 🚀 COSMIC TEAM — Drag Sail AI
### Impact of Drag Sail on Satellite Orbital Decay

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Machine Learning](https://img.shields.io/badge/AI-RandomForest-green)
![Flask](https://img.shields.io/badge/Backend-Flask-black)
![Deployment](https://img.shields.io/badge/Deploy-Render-success)
![IEEE AESS](https://img.shields.io/badge/IEEE-AESS-orange)

---

# 🌌 Live Demo

🔗 **Web Application:**  
https://cosmic-6jw8.onrender.com

---

# 📌 Project Overview

**Drag Sail AI** is an AI-powered orbital sustainability platform developed by **COSMIC TEAM** for the **IEEE AESS Sustainability Hackathon 2026**.

The project predicts:
- 🛰️ Natural orbital decay time
- ⚠️ Space debris collision risk
- 🌍 Sustainability impact
- 🚀 Optimal drag sail deployment strategy

using real orbital mechanics data and machine learning models.

The goal is to support safer and cleaner Low Earth Orbit (LEO) operations through intelligent deorbit recommendations.

---

# 🌍 Problem Statement

Space debris is one of the fastest-growing threats to future space missions.

Currently orbiting Earth:
- **37,000+ tracked debris objects**
- **100+ million small fragments**
- Thousands of inactive satellites and rocket bodies

Even tiny debris travels at:
- ~7–8 km/s
- Faster than a bullet

This creates major risks for:
- Operational satellites
- Space stations
- Future launches
- Astronaut safety

Without mitigation, orbital congestion may trigger the **Kessler Syndrome**, where collisions generate more debris and make orbit unusable.

---

# 🧠 Proposed Solution

Drag Sail AI combines:
- Orbital mechanics
- Feature engineering
- Machine learning
- Sustainability-focused decision systems

to estimate:

| Output | Description |
|---|---|
| `natural_deorbit_years` | Estimated natural orbital lifetime |
| `risk_score` | Predicted orbital collision risk |
| `risk_level` | LOW → CRITICAL classification |
| `recommended_action` | Suggested drag sail action |
| `sail_deorbit_years` | Lifetime after sail deployment |
| `years_saved` | Reduction in orbital lifetime |

---

# 🛰️ System Architecture

```text
Space-Track Orbital Data
            ↓
 Feature Engineering Layer
            ↓
 AI Prediction Models
 ├── Model A → Deorbit Time
 └── Model B → Risk Score
            ↓
 Decision Engine
            ↓
 Drag Sail Recommendation
            ↓
 Interactive GUI Dashboard
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
- Space-Track / TLE Data
- Drag & Atmospheric Decay Modeling

## 🌐 GUI & Deployment
- Flask
- HTML / CSS / JavaScript
- Render Cloud Deployment

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
| `ecc_periapsis` | Orbit-shape interaction |
| `in_critical_zone` | Detects dangerous orbital regions |
| `delta_altitude` | Measures orbit variation |

---

# 🛰️ Drag Sail Decision Logic

| Risk Level | Recommended Action |
|---|---|
| LOW | MONITOR |
| MODERATE | PREPARE |
| ELEVATED | DEPLOY_PARTIAL |
| HIGH | DEPLOY_HIGH |
| CRITICAL | DEPLOY_FULL |

The deployment percentage depends on:
- Object type
- Orbital risk
- Atmospheric drag
- Sustainability impact
- Orbital lifetime

---

# 🧪 Simulation Features

The project includes:
- Orbital decay simulation
- Drag sail deployment modeling
- Satellite re-entry visualization
- MATLAB orbital animation
- Burn-up and disappearance simulation

---

# 💻 Interactive GUI

The deployed web application allows users to:
- Enter TLE-derived orbital parameters
- Analyze orbital risk instantly
- Predict deorbit lifetime
- Receive drag sail recommendations
- Visualize sustainability impact

---

# ▶️ How to Run Locally

## 1️⃣ Clone Repository

```bash
git clone https://github.com/AmrHassanKhalaf/COSMIC.git
cd COSMIC
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Flask Application

```bash
python app.py
```

---

## 4️⃣ Open Browser

```text
http://127.0.0.1:5000
```

---

# 📥 Example Input

```python
{
    "PERIAPSIS": 700,
    "APOAPSIS": 824,
    "BSTAR": 0.000083,
    "ECCENTRICITY": 0.00852,
    "MEAN_MOTION": 14.62,
    "MEAN_MOTION_DOT": 0.00000218,
    "INCLINATION": 98.76,
    "PERIOD": 98.5,
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

The proposed system significantly reduces:
- Orbital congestion
- Long-term debris accumulation
- Satellite collision exposure
- Future sustainability risks

---

# ⚠️ Assumptions & Limitations

- Models are focused mainly on Low Earth Orbit (LEO).
- Atmospheric density changes are simplified.
- Solar activity effects are approximated.
- Predictions are research-oriented and not flight-certified.
- Risk scores are AI-estimated values and not official aerospace safety metrics.

---

# 🤖 AI Usage Disclosure

AI-assisted tools were used for:
- Documentation drafting
- Research organization
- README refinement
- GUI planning assistance
- Presentation structuring

However:
- Model development
- Orbital calculations
- Feature engineering
- Decision logic
- Validation and testing

were manually reviewed and validated by the COSMIC TEAM.

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
- IADC Space Debris Mitigation Guidelines
- Orbital Mechanics for Engineering Students
- IEEE AESS Sustainability References

---

# 🌌 Final Vision

> “Making Earth Orbit Safer Through Intelligent Sustainable Deorbiting.”

COSMIC TEAM aims to combine AI and aerospace sustainability to support safer future space operations and reduce long-term orbital debris accumulation.

---
