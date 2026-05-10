/* ============================================================
   Drag Sail AI — Frontend Logic
   ============================================================ */

'use strict';

// ── Preset test cases (from notebook cell_verify_code) ────────────────────────
const PRESETS = {
  critical: {
    periapsis: 702.7, apoapsis: 824.4, bstar: 0.000083,
    mean_motion_dot: 0.00000218, eccentricity: 0.00852, inclination: 98.76,
    period: 98.5, mean_motion: 14.62, object_type: 'DEBRIS', rcs_size: 'MEDIUM'
  },
  payload: {
    periapsis: 547, apoapsis: 563, bstar: 0.00022,
    mean_motion_dot: 0.0000018, eccentricity: 0.00115, inclination: 53.0,
    period: 95.5, mean_motion: 15.08, object_type: 'PAYLOAD', rcs_size: 'SMALL'
  },
  rocket: {
    periapsis: 800, apoapsis: 830, bstar: 0.000056,
    mean_motion_dot: 0.0000008, eccentricity: 0.00220, inclination: 82.5,
    period: 100.8, mean_motion: 14.28, object_type: 'ROCKET BODY', rcs_size: 'LARGE'
  },
  low: {
    periapsis: 388, apoapsis: 410, bstar: 0.00098,
    mean_motion_dot: 0.00012, eccentricity: 0.00156, inclination: 51.6,
    period: 92.3, mean_motion: 15.60, object_type: 'DEBRIS', rcs_size: 'SMALL'
  }
};

// ── Risk level meta ────────────────────────────────────────────────────────────
const RISK_META = {
  LOW:      { color: '#00e676', gaugeColor: '#00e676', badgeClass: 'level-low' },
  MODERATE: { color: '#ffd600', gaugeColor: '#ffd600', badgeClass: 'level-moderate' },
  ELEVATED: { color: '#ff9100', gaugeColor: '#ff9100', badgeClass: 'level-elevated' },
  HIGH:     { color: '#ff5252', gaugeColor: '#ff5252', badgeClass: 'level-high' },
  CRITICAL: { color: '#ff1744', gaugeColor: '#ff1744', badgeClass: 'level-critical' }
};

// ── Action CSS class map ───────────────────────────────────────────────────────
const ACTION_CLASS = {
  MONITOR:        'action-monitor',
  PREPARE:        'action-prepare',
  DEPLOY_PARTIAL: 'action-deploy-par',
  DEPLOY_HIGH:    'action-deploy-high',
  DEPLOY_FULL:    'action-deploy-full'
};

// ── Gauge geometry (r=90, circumference = 2π*90 ≈ 565.49) ─────────────────────
const GAUGE_CIRC = 2 * Math.PI * 90;   // 565.49

// ── DOM refs ───────────────────────────────────────────────────────────────────
const form        = document.getElementById('predict-form');
const analyzeBtn  = document.getElementById('analyze-btn');
const btnText     = analyzeBtn.querySelector('.btn-text');
const btnLoader   = document.getElementById('btn-loader');

const resultsEmpty  = document.getElementById('results-empty');
const resultsError  = document.getElementById('results-error');
const resultsBody   = document.getElementById('results-body');
const errorMsg      = document.getElementById('error-msg');

const gaugeArc      = document.getElementById('gauge-arc');
const gaugeNumber   = document.getElementById('gauge-number');
const riskBadge     = document.getElementById('risk-level-badge');
const actionBadge   = document.getElementById('action-badge');

const natYears      = document.getElementById('nat-years');
const sailYears     = document.getElementById('sail-years');
const savingsTag    = document.getElementById('savings-tag');

const deployFill    = document.getElementById('deploy-fill');
const deployPctLbl  = document.getElementById('deploy-pct-label');
const deployActLbl  = document.getElementById('deploy-action-label');

const qsType        = document.getElementById('qs-type');
const qsZone        = document.getElementById('qs-zone');
const qsRcs         = document.getElementById('qs-rcs');

const rsNat         = document.getElementById('rs-nat');
const rsScore       = document.getElementById('rs-score');
const rsLevel       = document.getElementById('rs-level');
const rsDeploy      = document.getElementById('rs-deploy');
const rsSail        = document.getElementById('rs-sail');
const rsSaved       = document.getElementById('rs-saved');

// ── Star field animation ───────────────────────────────────────────────────────
(function initStars() {
  const canvas = document.getElementById('stars-canvas');
  const ctx    = canvas.getContext('2d');
  let stars    = [];

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function mkStar() {
    return {
      x:   Math.random() * canvas.width,
      y:   Math.random() * canvas.height,
      r:   Math.random() * 1.4 + 0.2,
      a:   Math.random(),
      da:  (Math.random() - 0.5) * 0.006
    };
  }

  function init() {
    resize();
    stars = Array.from({ length: 180 }, mkStar);
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    stars.forEach(s => {
      s.a  = Math.max(0.05, Math.min(1, s.a + s.da));
      if (s.a <= 0.05 || s.a >= 1) s.da *= -1;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(205,214,244,${s.a * 0.7})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); stars = Array.from({ length: 180 }, mkStar); });
  init();
  draw();
})();

// ── Preset buttons ─────────────────────────────────────────────────────────────
document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const p = PRESETS[btn.dataset.preset];
    if (!p) return;
    Object.entries(p).forEach(([k, v]) => {
      const el = document.getElementById(k);
      if (el) el.value = v;
    });
  });
});

// ── Form submit ────────────────────────────────────────────────────────────────
form.addEventListener('submit', async e => {
  e.preventDefault();
  if (!form.checkValidity()) { form.reportValidity(); return; }

  setLoading(true);

  const payload = {
    periapsis:       +document.getElementById('periapsis').value,
    apoapsis:        +document.getElementById('apoapsis').value,
    bstar:           +document.getElementById('bstar').value,
    mean_motion_dot: +document.getElementById('mean_motion_dot').value,
    eccentricity:    +document.getElementById('eccentricity').value,
    inclination:     +document.getElementById('inclination').value,
    period:          +document.getElementById('period').value,
    mean_motion:     +document.getElementById('mean_motion').value,
    object_type:      document.getElementById('object_type').value,
    rcs_size:         document.getElementById('rcs_size').value,
  };

  try {
    const resp = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const json = await resp.json();

    if (json.status === 'ok') {
      renderResults(json.result);
    } else {
      showError(json.message || 'Unknown error');
    }
  } catch (err) {
    showError('Could not reach the server. Please try again.');
  } finally {
    setLoading(false);
  }
});

// ── Loading state ──────────────────────────────────────────────────────────────
function setLoading(on) {
  analyzeBtn.disabled = on;
  btnText.style.display  = on ? 'none' : '';
  btnLoader.style.display = on ? '' : 'none';
}

// ── Show error ─────────────────────────────────────────────────────────────────
function showError(msg) {
  resultsEmpty.style.display = 'none';
  resultsBody.style.display  = 'none';
  resultsError.style.display = '';
  errorMsg.textContent = msg;
}

// ── Render results ─────────────────────────────────────────────────────────────
function renderResults(r) {
  resultsEmpty.style.display = 'none';
  resultsError.style.display = 'none';
  resultsBody.style.display  = '';

  const meta = RISK_META[r.risk_level] || RISK_META.LOW;

  // ── Gauge ──────────────────────────────────────────────────────────────────
  const score   = r.risk_score;
  const offset  = GAUGE_CIRC * (1 - score / 100);
  gaugeArc.style.strokeDashoffset = offset;
  gaugeArc.style.stroke           = meta.gaugeColor;
  animateNumber(gaugeNumber, 0, score, 1100, v => v.toFixed(1));

  // ── Risk badge ─────────────────────────────────────────────────────────────
  riskBadge.textContent = r.risk_level;
  riskBadge.className   = `risk-badge ${meta.badgeClass}`;

  // ── Action badge ───────────────────────────────────────────────────────────
  actionBadge.textContent = r.action.replace(/_/g, ' ');
  actionBadge.className   = `action-badge ${ACTION_CLASS[r.action] || ''}`;

  // ── Quick stats ────────────────────────────────────────────────────────────
  qsType.textContent = r.object_type;
  qsZone.textContent = r.altitude_zone;
  qsRcs.textContent  = r.rcs_size;

  // ── Timeline ───────────────────────────────────────────────────────────────
  animateNumber(natYears,  0, r.natural_deorbit_years, 1100, v => v.toFixed(1));
  animateNumber(sailYears, 0, r.sail_deorbit_years,    1100, v => v.toFixed(1));
  savingsTag.textContent = `saves ${r.years_saved.toFixed(1)} yrs`;

  // ── Deployment bar ─────────────────────────────────────────────────────────
  deployFill.style.width   = `${r.sail_deployment_pct}%`;
  deployPctLbl.textContent = `${r.sail_deployment_pct} %`;
  deployActLbl.textContent = r.action.replace(/_/g, ' ');

  // ── Summary table ──────────────────────────────────────────────────────────
  rsNat.textContent    = `${r.natural_deorbit_years.toFixed(2)} years`;
  rsScore.textContent  = `${r.risk_score} / 100`;
  rsLevel.textContent  = r.risk_level;
  rsDeploy.textContent = `${r.sail_deployment_pct}%`;
  rsSail.textContent   = `${r.sail_deorbit_years.toFixed(2)} years`;
  rsSaved.textContent  = `${r.years_saved.toFixed(2)} years`;
}

// ── Animated number counter ────────────────────────────────────────────────────
function animateNumber(el, from, to, duration, format) {
  const start = performance.now();
  function step(now) {
    const p = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);   // ease-out cubic
    const val  = from + (to - from) * ease;
    el.textContent = format ? format(val) : val.toFixed(0);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
