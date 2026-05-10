import re

with open('E:/My Codes/compitition/COSMIC/src/templates/drag_sail_ai_app.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find('async function runModel() {')
idx_end = text.find('function resetApp() {')

if idx_start != -1 and idx_end != -1:
    clean_runModel = """async function runModel() {
    const inp = getInputs();
    
    if (!inp.periapsis || !inp.apoapsis || !inp.meanmotion) {
      alert('Please fill in all required fields');
      return;
    }
    
    setStep(2);
    showPanel('step2');
    await delay(1000); // Wait for prediction
    
    let natYears, risk, riskLevel, sailPct, action, sailYears, timeSaved;
    
    try {
      const apiUrl = window.location.protocol === 'file:' ? 'http://127.0.0.1:5000/predict' : '/predict';
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(inp)
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          natYears = data.natural_deorbit_years;
          risk = data.risk_score;
          riskLevel = data.risk_level;
          sailPct = data.sail_deployment_pct;
          action = data.action;
          sailYears = data.sail_deorbit_years;
          timeSaved = data.years_saved;
        } else {
          throw new Error(data.error);
        }
      } else {
        throw new Error("Backend API /predict failed.");
      }
    } catch (error) {
      alert("⚠️ CONNECTION ERROR: Cannot connect to the ML Backend! Check if your Flask server (app.py) is running on port 5000.");
      console.warn("Backend unavailable or failed.", error);
      return;
    }
  
    setStep(3);
    showPanel('step3');
    
    const rc = getRiskColor(risk);
    
    const needleAngle = (risk / 100) * 180 - 90;
    document.getElementById('gaugeNeedle').style.transform = `translateX(-50%) rotate(${needleAngle}deg)`;
    
    await delay(300);
    document.getElementById('gaugeScore').textContent = risk;
    document.getElementById('gaugeScore').style.color = rc;
    document.getElementById('gaugeLevel').textContent = riskLevel;
    document.getElementById('gaugeLevel').style.color = rc;
    
    setStep(4);
    showPanel('step4');
    
    const sailColor = sailPct >= 80 ? 'var(--red)' : sailPct >= 50 ? 'var(--orange)' : sailPct >= 20 ? 'var(--yellow)' : sailPct > 0 ? 'var(--cyan)' : 'var(--green)';
    
    const segs = Array.from({length:10},(_,i) => {
      const filled = (i+1)*10 <= sailPct;
      const col = filled ? sailColor : 'rgba(255,255,255,0.06)';
      return `<div class="sail-seg" style="background:${col}"></div>`;
    }).join('');
    
    document.getElementById('sailSection').innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
        <div>
          <div style="font-size:12px;color:var(--muted)">ACTION PLAN</div>
          <div style="font-size:18px;font-weight:700;letter-spacing:1px;color:${sailColor}">${action}</div>
        </div>
        <div style="text-align:right">
          <div style="font-size:12px;color:var(--muted)">DEPLOYMENT TARGET</div>
          <div style="font-size:24px;font-weight:800;font-variant-numeric:tabular-nums">${sailPct}%</div>
        </div>
      </div>
      <div class="sail-vis">${segs}</div>
      
      <div style="margin-top:24px;display:flex;gap:12px">
        <div class="data-box" style="flex:1;border-color:var(--muted)">
          <div class="db-lbl">Natural Deorbit</div>
          <div class="db-val" style="color:var(--muted)">${natYears >= 100 ? '>100' : Math.round(natYears*10)/10} <span>yr</span></div>
        </div>
        <div class="data-box" style="flex:1;border-color:${sailColor}">
          <div class="db-lbl">With Drag Sail</div>
          <div class="db-val" style="color:${sailColor}">${sailYears >= 100 ? '>100' : Math.round(sailYears*10)/10} <span>yr</span></div>
        </div>
      </div>
      ${timeSaved > 0 ? `
      <div style="margin-top:12px;font-size:12px;color:var(--green);text-align:center;padding:12px;background:rgba(34,215,135,0.08);border-radius:6px;border:1px solid rgba(34,215,135,0.2)">
        ⭐ Sail deployment saves <strong>${timeSaved >= 100 ? '>100' : Math.round(timeSaved*10)/10} years</strong> in orbit.
      </div>
      ` : `
      <div style="margin-top:12px;font-size:12px;color:var(--muted);text-align:center;padding:12px;background:rgba(255,255,255,0.03);border-radius:6px;">
        No sail intervention recommended. Risk is low or object decays naturally.
      </div>
      `}
    `;
    
    document.getElementById('resetBar').style.display = 'block';
  }

"""
    new_text = text[:idx_start] + clean_runModel + text[idx_end:]
    with open('E:/My Codes/compitition/COSMIC/src/templates/drag_sail_ai_app.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Fixed!")
else:
    print("Failed to find boundaries")
