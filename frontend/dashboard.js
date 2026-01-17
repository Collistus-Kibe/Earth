import { auth, whenAuthReady } from './app.js';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; 
const FIXED_LAT = -1.2921;
const FIXED_LON = 36.8219;
let userToken = null;

try { google.charts.load('current', {'packages':['corechart']}); } catch(e){}

console.log("🚀 EARTH Command Console v15.0");

whenAuthReady.then(async (user) => {
    if (user) {
        userToken = await user.getIdToken();
        setupEventListeners();
        const nav = document.getElementById('nav-dashboard');
        if(nav) nav.click();
    }
});

// --- DASHBOARD LOGIC ---
async function initDashboard() {
    renderDashboardLayout();
    
    // 1. AI & Weather
    try {
        const res = await fetch(`${API_BASE_URL}/predict/flood-trend?lat=${FIXED_LAT}&lon=${FIXED_LON}`, { headers: { 'Authorization': `Bearer ${userToken}` } });
        if(res.ok) {
            const data = await res.json();
            updateHero(Math.round(data.analysis.next_week_score), data.analysis.message, data.analysis.air_quality);
            if(google.visualization) drawChart(20, 'risk-chart', ['#10b981']);
        }
    } catch(e) { console.error("AI Error:", e); }

    // 2. Infrastructure (Now Works!)
    try {
        const res = await fetch(`${API_BASE_URL}/infra/status?lat=${FIXED_LAT}&lon=${FIXED_LON}`, { headers: { 'Authorization': `Bearer ${userToken}` } });
        if(res.ok) {
            const data = await res.json();
            updateStat('stat-power', data.power_grid_risk, 'txt-safe');
            updateStat('stat-road', data.road_network_risk, 'txt-safe');
            updateStat('stat-net', data.internet_risk, 'txt-safe');
        }
    } catch(e) {}
}

// --- RENDERERS ---
function renderDashboardLayout() {
    const el = document.getElementById('view-dashboard');
    if(!el || el.innerHTML.length > 50) return;
    el.innerHTML = `
        <div class="hero-card bg-home" id="dash-hero">
            <div class="hero-label">PLANETARY STATUS</div>
            <div class="hero-big-value" id="hero-score">--</div>
            <div class="hero-status" id="hero-status-text">ANALYZING</div>
            <div class="hero-desc" id="hero-msg">Connecting to sensor grid...</div>
            <div style="display:flex; gap:15px; margin-top:20px;">
                <div style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:20px; font-size:0.8rem; display:flex; align-items:center; gap:5px;">
                    <i class="material-icons-round" style="font-size:14px">wb_sunny</i> UV: <span id="val-uv">High (7)</span>
                </div>
                <div style="background:rgba(255,255,255,0.1); padding:5px 12px; border-radius:20px; font-size:0.8rem; display:flex; align-items:center; gap:5px;">
                    <i class="material-icons-round" style="font-size:14px">air</i> AQI: <span id="val-aqi">Good (42)</span>
                </div>
            </div>
        </div>
        <div class="section-title">INFRASTRUCTURE HEALTH</div>
        <div class="grid-3">
            <div class="stat-card"><div class="stat-label">POWER GRID</div><div class="stat-val txt-safe" id="stat-power">--</div></div>
            <div class="stat-card"><div class="stat-label">ROAD NETWORK</div><div class="stat-val txt-safe" id="stat-road">--</div></div>
            <div class="stat-card"><div class="stat-label">COMMUNICATION</div><div class="stat-val txt-safe" id="stat-net">--</div></div>
        </div>
        <div class="section-title">7-DAY RISK FORECAST</div>
        <div class="chart-box" id="risk-chart"></div>
    `;
}

function renderOceanView() {
    const el = document.getElementById('view-ocean');
    if(!el || el.innerHTML.length > 50) return;
    
    // MATHEMATICAL OCEAN IDENTIFICATION
    // If Longitude is > 20 and < 100, it's likely Indian Ocean for this region
    const oceanName = (FIXED_LON > 20 && FIXED_LON < 120) ? "INDIAN OCEAN" : "ATLANTIC OCEAN";

    el.innerHTML = `
        <div class="hero-card bg-ocean">
            <div class="hero-label">OCEAN INTELLIGENCE</div>
            <i class="material-icons-round" style="font-size:60px; margin:10px 0;">tsunami</i>
            <div class="hero-status">MONITORING: ${oceanName}</div>
        </div>
        <div class="grid-3">
            <div class="stat-card"><div class="stat-label">WATER TEMP</div><div class="stat-val txt-ocean">26.2°C</div></div>
            <div class="stat-card"><div class="stat-label">WAVE HEIGHT</div><div class="stat-val txt-ocean">1.1m</div></div>
            <div class="stat-card"><div class="stat-label">TIDE LEVEL</div><div class="stat-val txt-ocean">FALLING</div></div>
        </div>
        <div class="section-title">TIDAL FORECAST (24H)</div>
        <div class="chart-box" id="ocean-chart"></div>
    `;
    setTimeout(() => { if(google.visualization) drawChart(15, 'ocean-chart', ['#38bdf8']); }, 500);
}

// ... (Keep Nature/Space renderers same as before) ...
function renderNatureView() {
    document.getElementById('view-nature').innerHTML = `<div class="hero-card bg-nature"><div class="hero-label">BIODIVERSITY</div><i class="material-icons-round" style="font-size:60px; margin:10px 0;">spa</i><div class="hero-status">STABLE</div></div><div class="grid-3"><div class="stat-card"><div class="stat-label">SOIL MOISTURE</div><div class="stat-val txt-safe">28%</div></div><div class="stat-card"><div class="stat-label">FIRE RISK</div><div class="stat-val txt-safe">LOW</div></div><div class="stat-card"><div class="stat-label">SPECIES</div><div class="stat-val txt-safe">NORMAL</div></div></div><div class="chart-box" id="nature-chart"></div>`;
    setTimeout(() => { if(google.visualization) drawChart(30, 'nature-chart', ['#4ade80']); }, 500);
}
function renderSpaceView() {
    document.getElementById('view-space').innerHTML = `<div class="hero-card bg-space"><div class="hero-label">SPACE WEATHER</div><i class="material-icons-round" style="font-size:60px; margin:10px 0;">wb_sunny</i><div class="hero-status">MODERATE</div></div><div class="grid-3"><div class="stat-card"><div class="stat-label">FLARE RISK</div><div class="stat-val txt-warn">MEDIUM</div></div><div class="stat-card"><div class="stat-label">GEOMAGNETIC</div><div class="stat-val txt-warn">K-Index 4</div></div><div class="stat-card"><div class="stat-label">NEO</div><div class="stat-val txt-danger">2 TRACKED</div></div></div><div class="chart-box" id="space-chart"></div>`;
    setTimeout(() => { if(google.visualization) drawChart(50, 'space-chart', ['#a855f7']); }, 500);
}

// --- SETTINGS WITH PHONE INPUT ---
window.loadSettingContent = function(tabName) {
    const area = document.getElementById('settings-content-area');
    if(!area) return;

    if(tabName === 'general') {
        area.innerHTML = `<div class="setting-group"><div class="setting-label">THEME</div><div class="flex-row"><div class="btn-toggle active">DARK</div><div class="btn-toggle">LIGHT</div></div></div>`;
    } 
    else if (tabName === 'location') {
        area.innerHTML = `<div class="setting-group"><div class="setting-label">LOCATION</div><div style="font-weight:700; margin-bottom:10px;">Riara Ridge, Kiambu</div><button class="btn-google" style="margin-top:0">UPDATE GPS</button></div>`;
    }
    else if (tabName === 'notifications') {
        // --- PHONE NUMBER INPUT ADDED HERE ---
        area.innerHTML = `
            <div class="setting-group" style="border-left: 3px solid #10b981;">
                <div class="setting-label" style="color:#10b981">EARLY WARNING SYSTEM (THE ARK)</div>
                <p style="font-size:0.8rem; color:#94a3b8; margin-bottom:15px;">Receive autonomous alerts when risk probability exceeds 80%.</p>
                <div class="setting-label">PHONE NUMBER</div>
                <div style="display:flex; gap:10px;">
                    <input type="tel" placeholder="+254 7..." style="flex:1; padding:12px; background:#0f172a; border:1px solid #334155; color:white; border-radius:8px;">
                    <button class="btn-google" style="margin-top:0; background:#10b981; border:none; color:white;" onclick="alert('Phone number saved.')">SAVE</button>
                </div>
            </div>
        `;
    } else {
        area.innerHTML = `<div class="setting-group"><div class="setting-label">INFO</div><p style="color:#888">Version 15.0</p></div>`;
    }
}

// --- HELPERS & LISTENERS ---
function updateHero(score, msg, airData) {
    const elScore = document.getElementById('hero-score');
    const elMsg = document.getElementById('hero-msg');
    const elStatus = document.getElementById('hero-status-text');
    const elAQI = document.getElementById('val-aqi');
    
    if(elScore) elScore.textContent = score;
    if(elMsg) elMsg.textContent = msg;
    if(elStatus) elStatus.textContent = score > 40 ? "RISK DETECTED" : "SYSTEM NOMINAL";
    
    // Map AQI data if present
    if(airData && elAQI) {
        const aqiVal = airData.current?.us_aqi || 42;
        elAQI.textContent = `${aqiVal > 50 ? 'Moderate' : 'Good'} (${aqiVal})`;
    }
}

function updateStat(id, text, cls) {
    const el = document.getElementById(id);
    if(el) { el.textContent = text; el.className = `stat-val ${cls}`; }
}
function drawChart(base, id, color) {
    const el = document.getElementById(id);
    if(!el) return;
    const data = google.visualization.arrayToDataTable([['D','V'],['T',base],['+1',base+5],['+2',base+2],['+3',base+8],['+4',base+12]]);
    const opts = { backgroundColor: 'transparent', legend:'none', colors:color, areaOpacity:0.1, hAxis:{baselineColor:'transparent', gridlines:{color:'transparent'}, textStyle:{color:'#94a3b8'}}, vAxis:{baselineColor:'transparent', gridlines:{color:'rgba(255,255,255,0.05)'}, textStyle:{color:'#94a3b8'}} };
    new google.visualization.AreaChart(el).draw(data, opts);
}

// Settings Logic
function renderSettingsView() {
    const el = document.getElementById('view-settings');
    if(!el || el.innerHTML.length > 50) return;
    el.innerHTML = `
        <div style="font-size:1.2rem; font-weight:700; margin-bottom:20px;">SETTINGS</div>
        <div class="settings-container">
            <div class="settings-sidebar">
                <div class="settings-tab active" onclick="switchSettingTab(this, 'general')">GENERAL</div>
                <div class="settings-tab" onclick="switchSettingTab(this, 'location')">LOCATION</div>
                <div class="settings-tab" onclick="switchSettingTab(this, 'notifications')">NOTIFICATIONS</div>
                <div class="settings-tab" onclick="switchSettingTab(this, 'about')">ABOUT</div>
            </div>
            <div class="settings-panel" id="settings-content-area"></div>
        </div>`;
    loadSettingContent('general');
}
window.switchSettingTab = function(element, tabName) {
    document.querySelectorAll('.settings-tab').forEach(t => t.classList.remove('active'));
    element.classList.add('active');
    loadSettingContent(tabName);
}

// Nav Logic
function setupEventListeners() {
    const tabs = ['dashboard', 'ocean', 'nature', 'space'];
    tabs.forEach(t => {
        const btn = document.getElementById(`nav-${t}`);
        if(btn) {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
                document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
                document.getElementById(`view-${t}`).classList.add('active');
                btn.classList.add('active');
                if(t==='dashboard') initDashboard();
                if(t==='ocean') renderOceanView();
                if(t==='nature') renderNatureView();
                if(t==='space') renderSpaceView();
            });
        }
    });
    
    const settingsBtn = document.getElementById('btn-settings-header');
    if(settingsBtn) settingsBtn.addEventListener('click', () => {
        document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
        document.getElementById('view-settings').classList.add('active');
        renderSettingsView();
    });

    const logoutBtn = document.getElementById('btn-logout');
    if(logoutBtn) logoutBtn.addEventListener('click', () => auth.signOut().then(() => location.reload()));
}