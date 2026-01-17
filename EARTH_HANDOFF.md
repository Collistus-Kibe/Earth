
# 🌍 EARTH: AI-Powered Planetary Intelligence Platform

## Project Vision
To create a singular, unified intelligence system that moves beyond simple data monitoring. "EARTH" is a proactive decision-support platform that fuses multi-domain data to predict and analyze interconnected environmental, health, and climate threats in real-time. It provides actionable, location-specific insights and alerts.

**Our Core Mantra:** "Show data relevant to the user." Fire risk for Norway is useless. We focus on regional relevance.

## 7-Point Data Plan
1.  **Hyperlocal Weather:** Temp, rain, wind, UV. (Done)
2.  **Air Quality & Health:** AQI, PM2.5. (Done)
3.  **Natural Disaster Risk (Regional):**
    * Wildfire Risk (Done)
    * Earthquake Probability (Done)
    * Flood Risk (Done)
4.  **Satellite Intelligence:** (Removed - Not a life-saving priority)
5.  **Pollution & Toxicity:** (Partially done with Crowdsourcing)
6.  **AI Predictive Modeling:** (Done - Proactive Alerts)
7.  **Personal Earth Safety Score:** (Done - Local Intelligence Widget)


## 📂 Final Project Structure

```
earth-project/
├── backend/
│   ├── app/
│   │   ├── api/v1/ (all 10 router files)
│   │   ├── models/ (all 4 model files)
│   │   ├── services/ (all 7 service files)
│   │   ├── helpers.py
│   │   ├── main.py
│   │   └── processing.py
│   ├── .env (LISTED BELOW)
│   ├── ca.pem
│   ├── firebase-service-account.json
│   └── requirements.txt
├── frontend/
│   ├── login.html
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── dashboard.js
│   └── serve.py
├── data/
│   ├── world_rivers.json
│   └── world_countries.json
└── create_handoff.py (This script)
```

## 🔑 Required Keys (.env) & Data Files

* `TIDB_CONNECTION_STRING`
* `FIREBASE_CREDENTIALS_PATH`
* `N2YO_API_KEY`
* `NASA_API_KEY`
* `Maps_API_KEY`
* `OPENAI_API_KEY`
* `data/world_rivers.json` (from Natural Earth)
* `data/world_countries.json` (from Natural Earth)

## 💻 Full Project Code

### `frontend/login.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EARTH - Login</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="login-page">

    <div class="login-container">
        <h1>🌍 EARTH</h1>
        <p>AI-Powered Planetary Intelligence</p>
        <button id="btn-login">Login with Google</button>
    </div>

    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-auth-compat.js"></script>
    <script type="module" src="app.js"></script>
</body>
</html>
```

### `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EARTH - Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="dashboard-page">

    <header class="dashboard-header">
        <h1>🌍 EARTH Dashboard</h1>
        <div class="user-profile">
            <span id="user-email-display">Loading...</span>
            <button id="btn-logout">Logout</button>
        </div>
    </header>

    <main id="dashboard-grid">

        <div class="widget-card" id="widget-local-intel">
            <h2><span class="icon">📍</span> Local Intelligence</h2>
            <p class="widget-description">A fused "Earth Safety Score" (0-100) based on live weather, air quality, and fire risk for your home.</p>
            
            <div class="widget-content" id="local-intel-loading">
                <p>Click the button to set your home location and load your local intelligence summary.</p>
                <button id="btn-set-home-location">Set My Home Location</button>
            </div>
            
            <div class="widget-content hidden" id="local-intel-data">
                <div class="safety-score-container">
                    <canvas id="safety-score-gauge"></canvas>
                    <div id="safety-score-label">--</div>
                </div>
                <div id="safety-score-risk" class="primary-risk">--</div>
                
                <div class="sub-metrics">
                    <div class="metric-box">
                        <span class="metric-label">AQI</span>
                        <span id="metric-aqi" class="metric-value">--</span>
                    </div>
                    <div class="metric-box">
                        <span class="metric-label">Temp</span>
                        <span id="metric-temp" class="metric-value">--°</span>
                    </div>
                    <div class="metric-box">
                        <span class="metric-label">Fire Risk</span>
                        <span id="metric-fire" class="metric-value">--</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="widget-card" id="widget-flood">
            <h2><span class="icon">🌊</span> Flood Probability</h2>
            <p class="widget-description">7-day flood risk based on rain forecast, soil saturation, and proximity to rivers.</p>
            <div class="widget-content">
                <div class="safety-score-container">
                    <canvas id="flood-gauge-chart"></canvas>
                    <div id="flood-gauge-label">--</div>
                </div>
                <div id="flood-risk-details" class="primary-risk">
                    Set home location to load risk
                </div>
            </div>
        </div>

        <div class="widget-card" id="widget-storm">
            <h2><span class="icon">⚡️</span> Storm Tracking</h2>
            <p class="widget-description">Real-time alerts for natural events (wildfires, storms, floods) within a 500km radius of your home.</p>
            <div class="widget-content">
                <button id="btn-fetch-nearby-events">Refresh Nearby Events</button>
                <div id="nearby-events-list-container">
                    <small id="nearby-events-status">Set home location to find events</small>
                    <ul id="nearby-events-list">
                        </ul>
                </div>
            </div>
        </div>

        <div class="widget-card" id="widget-weather">
            <h2><span class="icon">☀️</span> 7-Day Forecast</h2>
            <p class="widget-description">Hyperlocal weather forecast for your home location, powered by Open-Meteo.</p>
            <div class="widget-content">
                <div id="forecast-list-container">
                    <small id="forecast-status">Set home location to load forecast</small>
                    <ul id="forecast-list">
                        </ul>
                </div>
            </div>
        </div>
        
        <div class="widget-card" id="widget-seismic">
            <h2><span class="icon">🌋</span> Seismic Activity</h2>
            <p class="widget-description">Find the most recent significant earthquake (2.5+ Mag) closest to your home location.</p>
            <div class="widget-content">
                <p class="data-display" id="seismic-mag">--</p>
                <small id="seismic-details">Set home location to find quakes</small>
                <a id="seismic-link" href="#" target="_blank" class="hidden">View Event Details</a>
            </div>
        </div>
        
        <div class="widget-card" id="widget-alerts">
            <h2><span class="icon">🔔</span> Proactive Alerts</h2>
            <p class="widget-description">Click to run a full analysis of all predictive models (Fire, Flood, UV) for your home location.</p>
            <div class="widget-content">
                <button id="btn-check-alerts">Check for New Alerts</button>
                <div id="alerts-list-container">
                    <small id="alerts-status">Click button to check for alerts.</small>
                    <ul id="alerts-list">
                        </ul>
                </div>
            </div>
        </div>

    </main>

    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-auth-compat.js"></script>
    <script type="module" src="app.js"></script>
    <script type="module" src="dashboard.js"></script>
</body>
</html>
```

### `frontend/styles.css`

```css
/* --- Global Styles --- */
:root {
    --bg-color: #121212;
    --bg-light: #1e1e1e;
    --text-color: #e0e0e0;
    --text-muted: #aaa;
    --accent-color: #4CAF50;
    --accent-hover: #45a049;
    --border-color: #333;
    --warning-color: #f39c12; /* Orange */
    --danger-color: #e74c3c; /* Red */
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
}

button {
    background-color: var(--accent-color);
    color: white;
    border: none;
    padding: 10px 20px;
    margin: 10px 0;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s;
    width: 100%;
}

button:hover {
    background-color: var(--accent-hover);
}

button:disabled {
    background-color: #555;
    cursor: not-allowed;
}

/* --- Login Page Styles --- */
.login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.login-container {
    background-color: var(--bg-light);
    padding: 3rem 4rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    text-align: center;
    width: 90%;
    max-width: 400px;
}
.login-container h1 {
    color: var(--accent-color);
    margin-top: 0;
}

/* --- Dashboard Page Styles --- */
.dashboard-page {
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}
.dashboard-header {
    background-color: var(--bg-light);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--border-color);
    flex-shrink: 0;
}
.dashboard-header h1 {
    margin: 0;
    font-size: 1.5rem;
}
.user-profile {
    display: flex;
    align-items: center;
}
.user-profile span {
    margin-right: 1rem;
    color: var(--text-muted);
}
.user-profile button {
    width: auto;
    margin: 0;
    background-color: #c0392b;
}
.user-profile button:hover {
    background-color: #e74c3c;
}

/* --- Dashboard Grid Styles --- */
#dashboard-grid {
    flex-grow: 1;
    display: grid;
    /* --- UPDATED: 3-column grid --- */
    grid-template-columns: repeat(3, 1fr);
    grid-gap: 1.5rem;
    padding: 1.5rem;
    overflow-y: auto;
}

.widget-card {
    background-color: var(--bg-light);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    min-height: 250px; /* Give widgets a minimum height */
}

/* --- UPDATED: Local Intel spans 3 columns --- */
#widget-local-intel {
    grid-column: 1 / -1; /* Span all columns */
}
/* --- END UPDATE --- */

.widget-card h2 {
    margin-top: 0;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
}
.widget-card .icon {
    font-size: 1.5rem;
    margin-right: 10px;
}
.widget-description {
    font-size: 0.9rem;
    color: var(--text-muted);
    flex-grow: 1; /* Pushes content to bottom */
}
.widget-content {
    margin-top: 1rem;
    text-align: center;
}
.widget-content .data-display {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--accent-color);
    margin: 10px 0;
}
.widget-content small {
    color: var(--text-muted);
}
.widget-card .hidden {
    display: none;
}

/* Local Intelligence Widget */
.safety-score-container {
    position: relative;
    width: 100%;
    max-width: 250px;
    margin: 0 auto;
}
#safety-score-gauge {
    width: 100%;
    height: auto;
}
#safety-score-label {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-top: -15px;
    font-size: 3rem;
    font-weight: bold;
    color: #fff;
}
.primary-risk {
    font-size: 1.1rem;
    font-weight: bold;
    color: #FF4500; /* Default to red */
    margin-top: -30px; /* Pull it up under the gauge */
    margin-bottom: 20px;
}
.sub-metrics {
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-top: 1.5rem;
    border-top: 1px solid var(--border-color);
    padding-top: 1.5rem;
}
.metric-box {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.metric-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--text-color);
}

/* Flood Gauge Styles */
#flood-gauge-label {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-top: -15px;
    font-size: 3rem;
    font-weight: bold;
    color: #fff;
}
#flood-risk-details {
    font-size: 1.1rem;
    font-weight: bold;
    color: #FFD700; /* Yellow */
    margin-top: -30px;
    margin-bottom: 20px;
}

/* --- UPDATED: Storm Tracking Widget Styles --- */
#nearby-events-list-container {
    margin-top: 1rem;
    width: 100%;
    /* Set a max height so it becomes scrollable */
    max-height: 200px; 
    overflow-y: auto;
    background-color: var(--bg-color); /* Darker bg for the list area */
    border-radius: 5px;
    border: 1px solid var(--border-color);
    text-align: left;
}
#nearby-events-status {
    padding: 1rem;
    display: block; /* Make it a block to center it */
    text-align: center;
    color: var(--text-muted);
}
#nearby-events-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}
#nearby-events-list li {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
}
#nearby-events-list li:last-child {
    border-bottom: none;
}
#nearby-events-list li strong {
    color: var(--accent-color);
    margin-right: 8px;
}
#nearby-events-list li .event-details {
    font-size: 0.9rem;
    color: var(--text-muted);
}

/* Seismic Widget Styles */
#seismic-mag {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--warning-color); /* Orange for quakes */
    margin: 10px 0;
}
#seismic-details {
    font-size: 1rem;
    color: var(--text-muted);
    height: 3rem; /* Give it space */
}
#seismic-link {
    display: inline-block;
    background-color: var(--bg-light);
    border: 1px solid var(--accent-color);
    color: var(--accent-color);
    padding: 8px 15px;
    font-size: 0.9rem;
    text-decoration: none;
    width: auto; /* Don't make it full width */
    margin-top: 10px;
}
#seismic-link:hover {
    background-color: var(--accent-color);
    color: white;
}

/* Proactive Alert Widget Styles */
#alerts-list-container {
    margin-top: 1rem;
    width: 100%;
    max-height: 200px;
    overflow-y: auto;
    background-color: var(--bg-color);
    border-radius: 5px;
    border: 1px solid var(--border-color);
    text-align: left;
}
#alerts-status {
    padding: 1rem;
    display: block;
    text-align: center;
    color: var(--text-muted);
}
#alerts-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}
#alerts-list li {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-color);
    font-weight: bold;
}
#alerts-list li:last-child {
    border-bottom: none;
}
#alerts-list li.alert-critical {
    color: var(--danger-color);
    border-left: 4px solid var(--danger-color);
}
#alerts-list li.alert-warning {
    color: var(--warning-color);
    border-left: 4px solid var(--warning-color);
}
#alerts-list li.alert-health {
    color: var(--warning-color); /* Health is a warning */
    border-left: 4px solid var(--warning-color);
}
#alerts-list li.alert-safe {
    color: var(--accent-color);
    border-left: 4px solid var(--accent-color);
}
#forecast-list-container {
    margin-top: 1rem;
    width: 100%;
    max-height: 200px; /* Or adjust as needed */
    overflow-y: auto;
    text-align: left;
}

#forecast-status {
    padding: 1rem;
    display: block;
    text-align: center;
    color: var(--text-muted);
}

#forecast-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

#forecast-list li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0.5rem;
    border-bottom: 1px solid var(--border-color);
}

#forecast-list li:last-child {
    border-bottom: none;
}

.forecast-day {
    font-weight: bold;
    flex-basis: 25%;
}

.forecast-icon {
    font-size: 1.5rem;
    flex-basis: 20%;
    text-align: center;
}

.forecast-temps {
    flex-basis: 55%;
    text-align: right;
}

.forecast-temps .temp-high {
    font-weight: bold;
    color: var(--text-color);
}

.forecast-temps .temp-low {
    font-weight: normal;
    color: var(--text-muted);
}
```

### `frontend/app.js`

```javascript
// --- 1. Firebase Configuration ---
const firebaseConfig = {
  apiKey: "AIzaSyDX__F_8Y-E4IKXU1deMDloDDwQEfVcHcM",
  authDomain: "earth-aaa66.firebaseapp.com",
  projectId: "earth-aaa66",
  storageBucket: "earth-aaa66.firebasestorage.app",
  messagingSenderId: "619303358483",
  appId: "1:619303358483:web:039af3c04f766224552fe6",
  measurementId: "G-5H870QG1KJ"
};

// --- 2. Initialize Firebase ---
firebase.initializeApp(firebaseConfig);
export const auth = firebase.auth(); // Export auth object
const provider = new firebase.auth.GoogleAuthProvider();

// --- 3. Create a "Ready" Signal ---
// This Promise will resolve when Firebase confirms the user's auth state
export const whenAuthReady = new Promise((resolve) => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
        unsubscribe(); // Stop listening
        resolve(user);   // Send the user (or null) to whatever is waiting
    });
});

// --- 4. Get Current Page ---
const currentPage = window.location.pathname;

// --- 5. Auth Guard Logic ---
// We must wait for our "Ready" signal before checking auth
whenAuthReady.then((user) => {
    if (user) {
        // User is logged in
        if (currentPage.includes('login.html') || currentPage === '/') {
            // If on login page, redirect to dashboard
            window.location.href = '/index.html';
        } else if (currentPage.includes('index.html')) {
            // User is on the dashboard, populate user info
            const userEmailDisplay = document.getElementById('user-email-display');
            if (userEmailDisplay) {
                userEmailDisplay.textContent = user.email;
            }
        }
    } else {
        // User is not logged in
        if (currentPage.includes('index.html')) {
            // If on dashboard, redirect to login
            window.location.href = '/login.html';
        }
    }
});

// --- 6. Event Listeners (THE FIX) ---
// --- We now wait for the HTML to be fully loaded ---
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded. Attaching listeners.");
    
    // Listen for login button click
    if (currentPage.includes('login.html') || currentPage === '/') {
        const btnLogin = document.getElementById('btn-login');
        if (btnLogin) {
            console.log("Found login button, attaching listener.");
            btnLogin.addEventListener('click', () => {
                console.log("Login button clicked, signing in...");
                auth.signInWithPopup(provider)
                    .catch((error) => {
                        console.error("Login Error:", error);
                    });
            });
        } else {
            console.error("Could not find login button!");
        }
    }
    
    // Listen for logout button click
    if (currentPage.includes('index.html')) {
        const btnLogout = document.getElementById('btn-logout');
        if (btnLogout) {
            console.log("Found logout button, attaching listener.");
            btnLogout.addEventListener('click', () => {
                auth.signOut()
                    .catch((error) => {
                        console.error("Logout Error:", error);
                    });
            });
        }
    }
});
// --- END FIX ---
```

### `frontend/dashboard.js`

```javascript
// --- NEW: Import the auth object and "ready" signal ---
import { auth, whenAuthReady } from './app.js';

console.log("dashboard.js loaded. Waiting for DOM and auth...");

// --- 1. Global Helpers ---
const API_BASE_URL = 'http://localhost:8000/api/v1';

async function getAuthToken() {
    // We get the user from the 'auth' object we imported
    const user = auth.currentUser;
    if (!user) {
        console.error("User not logged in, redirecting...");
        window.location.href = '/login.html';
        throw new Error("User not authenticated");
    }
    return user.getIdToken();
}

// --- 2. Widget Refs (declared globally) ---
let localIntelLoading, localIntelData, safetyScoreLabel, safetyScoreRisk, metricAqi, metricTemp, metricFire, btnSetHomeLocation, safetyGauge;
let floodGaugeLabel, floodRiskDetails, floodGauge;
let forecastList, forecastStatus;
let btnFetchNearbyEvents, nearbyEventsList, nearbyEventsStatus;
let seismicMag, seismicDetails, seismicLink;
let btnCheckAlerts, alertsList, alertsStatus;

// --- This function assigns the elements ---
function initializeElementRefs() {
    localIntelLoading = document.getElementById('local-intel-loading');
    localIntelData = document.getElementById('local-intel-data');
    safetyScoreLabel = document.getElementById('safety-score-label');
    safetyScoreRisk = document.getElementById('safety-score-risk');
    metricAqi = document.getElementById('metric-aqi');
    metricTemp = document.getElementById('metric-temp');
    metricFire = document.getElementById('metric-fire');
    btnSetHomeLocation = document.getElementById('btn-set-home-location');
    safetyGauge = null; 

    floodGaugeLabel = document.getElementById('flood-gauge-label');
    floodRiskDetails = document.getElementById('flood-risk-details');
    floodGauge = null;

    forecastList = document.getElementById('forecast-list');
    forecastStatus = document.getElementById('forecast-status');

    btnFetchNearbyEvents = document.getElementById('btn-fetch-nearby-events');
    nearbyEventsList = document.getElementById('nearby-events-list');
    nearbyEventsStatus = document.getElementById('nearby-events-status');

    seismicMag = document.getElementById('seismic-mag');
    seismicDetails = document.getElementById('seismic-details');
    seismicLink = document.getElementById('seismic-link');

    btnCheckAlerts = document.getElementById('btn-check-alerts');
    alertsList = document.getElementById('alerts-list');
    alertsStatus = document.getElementById('alerts-status');
}

// This function runs on page load and on location set
async function loadLocalIntelligence() {
    console.log("Attempting to load local intelligence...");
    try {
        const token = await getAuthToken();
        const prefsResponse = await fetch(`${API_BASE_URL}/preferences/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!prefsResponse.ok) {
            if (prefsResponse.status === 404) {
                console.log("No home location set. Waiting for user action.");
                localIntelLoading.classList.remove('hidden');
                localIntelData.classList.add('hidden');
                // Set default text for all widgets
                floodRiskDetails.textContent = "Set home location to load risk";
                forecastStatus.textContent = "Set home location to load forecast";
                nearbyEventsStatus.textContent = "Set home location to find events";
                seismicDetails.textContent = "Set home location to find quakes";
                alertsStatus.textContent = "Set home location to check for alerts.";
            }
            return; // Don't proceed
        }

        const prefs = await prefsResponse.json();
        const { latitude, longitude } = prefs;

        // --- We have a location! Load data for all widgets ---
        localIntelLoading.classList.add('hidden');
        localIntelData.classList.remove('hidden');
        initializeSafetyGauge();
        initializeFloodGauge(); 
        safetyScoreLabel.textContent = '...';
        floodGaugeLabel.textContent = '...';

        // Load widgets independently
        loadLocalSummary(token, latitude, longitude);
        loadFloodRisk(token);
        loadNearbyEvents(token);
        loadNearbyEarthquake(token);
        loadWeatherForecast(token);

    } catch (error) {
        console.error("Failed to get user preferences:", error);
    }
}

// --- Local Summary Widget ---
async function loadLocalSummary(token, latitude, longitude) {
    try {
        const summaryResponse = await fetch(
            `${API_BASE_URL}/intelligence/local-summary?lat=${latitude}&lon=${longitude}`,
            { headers: { 'Authorization': `Bearer ${token}` } }
        );
        if (!summaryResponse.ok) {
            const err = await summaryResponse.json();
            throw new Error(`Local Summary: ${err.detail}`);
        }
        const data = await summaryResponse.json();
        
        const aqiValue = data.air_quality.aqi;
        const aqiText = (aqiValue !== null && aqiValue !== undefined) ? aqiValue : 'N/A';

        // Populate Local Intelligence Widget
        updateSafetyGauge(data.safety_score);
        safetyScoreRisk.textContent = data.primary_risk;
        metricAqi.textContent = aqiText;
        metricTemp.textContent = `${Math.round(data.weather.temperature)}°`;
        metricFire.textContent = data.fire_risk;
        if(data.safety_score < 50) safetyScoreRisk.style.color = '#FF4500';
        else if (data.safety_score < 80) safetyScoreRisk.style.color = '#FFD700';
        else safetyScoreRisk.style.color = '#4CAF50';
        
    } catch (error) {
        console.error("Local Summary Widget Error:", error);
        safetyScoreLabel.textContent = 'Error';
    }
}

// --- Flood Risk Widget ---
async function loadFloodRisk(token) {
    try {
        const floodResponse = await fetch(
            `${API_BASE_URL}/risks/flood`,
            { headers: { 'Authorization': `Bearer ${token}` } }
        );
        if (!floodResponse.ok) {
            const err = await floodResponse.json();
            throw new Error(`${err.detail}`);
        }
        const floodData = await floodResponse.json();
        updateFloodGauge(floodData.flood_score);
    } catch (error) {
        console.error("Flood Risk Widget Error:", error);
        floodGaugeLabel.textContent = 'Error';
        floodRiskDetails.textContent = error.message;
    }
}

// --- Nearby Events Widget ---
async function loadNearbyEvents(token) {
    nearbyEventsList.innerHTML = ''; 
    nearbyEventsStatus.textContent = 'Finding nearby events...';
    nearbyEventsStatus.style.display = 'block';
    btnFetchNearbyEvents.disabled = true;
    try {
        const authToken = token || await getAuthToken();
        const response = await fetch(`${API_BASE_URL}/alerts/nearby-events`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail);
        if (data.event_count === 0) {
            nearbyEventsStatus.textContent = 'No events found within 500km. Your area is clear.';
        } else {
            nearbyEventsStatus.style.display = 'none';
            data.events.forEach(event => {
                const li = document.createElement('li');
                const eventType = event.categories[0].title;
                const distance = event.distance_km;
                li.innerHTML = `
                    <strong>${eventType}</strong>
                    <span class="event-details">${event.title} (${distance}km away)</span>
                `;
                nearbyEventsList.appendChild(li);
            });
        }
    } catch(error) {
        console.error("Fetch Nearby Events Error:", error);
        nearbyEventsStatus.textContent = `Error: ${error.message}`;
    } finally {
        btnFetchNearbyEvents.disabled = false;
    }
}

// --- Seismic Activity Widget ---
async function loadNearbyEarthquake(token) {
    seismicMag.textContent = '...';
    seismicDetails.textContent = 'Fetching quake data...';
    seismicLink.classList.add('hidden');
    try {
        const authToken = token || await getAuthToken();
        const response = await fetch(`${API_BASE_URL}/alerts/nearby-earthquake`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail);
        if (data.message) {
            seismicMag.textContent = 'Safe';
            seismicDetails.textContent = data.message;
        } else {
            seismicMag.textContent = data.mag.toFixed(1);
            seismicDetails.textContent = `${data.place} (${data.distance_km}km away)`;
            seismicLink.href = data.url;
            seismicLink.classList.remove('hidden');
        }
    } catch(error) {
        console.error("Fetch Nearby Quake Error:", error);
        seismicMag.textContent = 'Error';
        seismicDetails.textContent = error.message;
    }
}

// --- 7-Day Forecast Widget ---
async function loadWeatherForecast(token) {
    forecastList.innerHTML = '';
    forecastStatus.textContent = 'Loading forecast...';
    forecastStatus.style.display = 'block';
    
    try {
        const authToken = token || await getAuthToken();
        const response = await fetch(`${API_BASE_URL}/weather/forecast`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail);
        
        if (data.daily && data.daily.length > 0) {
            forecastStatus.style.display = 'none'; // Hide status
            data.daily.forEach(day => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="forecast-day">${formatDay(day.time)}</span>
                    <span class="forecast-icon">${getWeatherIcon(day.weather_code)}</span>
                    <span class="forecast-temps">
                        <span class="temp-high">${Math.round(day.temp_max)}°</span> /
                        <span class="temp-low">${Math.round(day.temp_min)}°</span>
                    </span>
                `;
                forecastList.appendChild(li);
            });
        } else {
            forecastStatus.textContent = "Forecast data unavailable.";
        }
    } catch(error) {
        console.error("Fetch 7-Day Forecast Error:", error);
        forecastStatus.textContent = `Error: ${error.message}`;
    }
}


// --- 3. Chart.js Logic ---
function initializeSafetyGauge() {
    const gaugeCtx = document.getElementById('safety-score-gauge').getContext('2d');
    if (safetyGauge) safetyGauge.destroy();
    safetyGauge = new Chart(gaugeCtx, {
        type: 'doughnut', data: { datasets: [{
            data: [0, 100], backgroundColor: ['#4CAF50', '#333'],
            borderColor: '#1e1e1e', borderWidth: 2, circumference: 180, rotation: 270,
        }]},
        options: { responsive: true, aspectRatio: 2, plugins: { tooltip: { enabled: false } }, cutout: '70%' }
    });
}
function updateSafetyGauge(score) {
    if (!safetyGauge) initializeSafetyGauge();
    const cappedScore = Math.min(Math.max(score, 0), 100);
    safetyGauge.data.datasets[0].data = [cappedScore, 100 - cappedScore];
    let color = '#4CAF50';
    if (cappedScore < 50) color = '#FF4500';
    else if (cappedScore < 80) color = '#FFD700';
    safetyGauge.data.datasets[0].backgroundColor[0] = color;
    safetyScoreLabel.textContent = cappedScore;
    safetyScoreLabel.style.color = color;
    safetyGauge.update('none');
}
function initializeFloodGauge() {
    const gaugeCtx = document.getElementById('flood-gauge-chart').getContext('2d');
    if (floodGauge) floodGauge.destroy();
    floodGauge = new Chart(gaugeCtx, {
        type: 'doughnut', data: { datasets: [{
            data: [0, 100], backgroundColor: ['#3498db', '#333'],
            borderColor: '#1e1e1e', borderWidth: 2, circumference: 180, rotation: 270,
        }]},
        options: { responsive: true, aspectRatio: 2, plugins: { tooltip: { enabled: false } }, cutout: '70%' }
    });
    floodGaugeLabel.textContent = '--';
    floodGaugeLabel.style.color = '#aaa';
}
function updateFloodGauge(score) {
    if (!floodGauge) initializeFloodGauge();
    const cappedScore = Math.min(Math.max(score, 0), 100);
    floodGauge.data.datasets[0].data = [cappedScore, 100 - cappedScore];
    let color = '#3498db';
    if (cappedScore > 40) color = '#FFD700';
    if (cappedScore > 70) color = '#FF4500';
    floodGauge.data.datasets[0].backgroundColor[0] = color;
    floodGaugeLabel.textContent = capped.score;
    floodGaugeLabel.style.color = color;
    if (cappedScore > 70) floodRiskDetails.textContent = "High Risk";
    else if (cappedScore > 40) floodRiskDetails.textContent = "Moderate Risk";
    else floodRiskDetails.textContent = "Low Risk";
    floodRiskDetails.style.color = color;
    floodGauge.update('none');
}

// --- 4. Event Listener Attachment Function ---
function attachAllListeners() {
    btnSetHomeLocation.addEventListener('click', () => {
        btnSetHomeLocation.disabled = true;
        btnSetHomeLocation.textContent = 'Fetching Location...';
        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            btnSetHomeLocation.disabled = false;
            return;
        }
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                try {
                    await saveHomeLocation(lat, lon);
                    await loadLocalIntelligence(); // This now loads ALL widgets
                } catch (error) {
                    console.error("Failed to update location/intelligence:", error);
                }
            },
            (error) => {
                console.error("Geolocation Error:", error);
                alert("Could not get your location. Please allow location access.");
                btnSetHomeLocation.disabled = false;
                btnSetHomeLocation.textContent = 'Set My Home Location';
            }
        );
    });

    // Nearby Events Button
    btnFetchNearbyEvents.addEventListener('click', async () => {
        loadNearbyEvents(); // This button just re-runs the load function
    });

    // Proactive Alerts Button
    btnCheckAlerts.addEventListener('click', async () => {
        alertsList.innerHTML = '';
        alertsStatus.textContent = 'Checking all models...';
        alertsStatus.style.display = 'block';
        btnCheckAlerts.disabled = true;

        try {
            const token = await getAuthToken();
            const response = await fetch(`${API_BASE_URL}/alerts/run-check`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.detail);

            if (data.alerts && data.alerts.length > 0) {
                alertsStatus.style.display = 'none';
                data.alerts.forEach(alertText => {
                    const li = document.createElement('li');
                    if (alertText.startsWith("CRITICAL")) li.className = 'alert-critical';
                    else if (alertText.startsWith("WARNING")) li.className = 'alert-warning';
                    else if (alertText.startsWith("HEALTH")) li.className = 'alert-health';
                    else li.className = 'alert-safe';
                    li.textContent = alertText;
                    alertsList.appendChild(li);
                });
            } else {
                alertsStatus.textContent = "Error: No alerts returned.";
            }

        } catch(error) {
            console.error("Fetch Proactive Alerts Error:", error);
            alertsStatus.textContent = `Error: ${error.message}`;
        } finally {
            btnCheckAlerts.disabled = false;
        }
    });
}


// --- 5. Function to save home location ---
async function saveHomeLocation(lat, lon, zoom = 10) {
    console.log(`Saving home location: ${lat}, ${lon}`);
    try {
        const token = await getAuthToken();
        const response = await fetch(`${API_BASE_URL}/preferences/me`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ latitude: lat, longitude: lon, zoom: zoom })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Failed to save location");
        }
        console.log("Home location saved successfully.");
    } catch (error) {
        console.error("Failed to save home location:", error);
        alert(`Could not save home location: ${error.message}`);
    }
}

// --- 7. Page Load Initialization ---
// --- THIS IS THE FIX ---
// We wait for the HTML (DOM) to be loaded FIRST.
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded. Now waiting for auth...");
    
    // THEN we wait for the auth signal from app.js
    whenAuthReady.then((user) => {
        if (user) {
            // Auth is ready AND user is logged in.
            // It is NOW safe to find elements and add listeners.
            console.log("Auth is ready. Initializing dashboard.");
            
            // 1. Find all elements on the page
            initializeElementRefs();
            
            // 2. Attach all button click listeners
            attachAllListeners();
            
            // 3. Load the initial data for all widgets
            loadLocalIntelligence();
            
        } else {
            // User is not logged in (on login page)
            console.log("Auth is ready. User is not logged in.");
        }
    });
});
// --- END FIX ---


// --- 8. Helper Functions ---
function formatDay(dateString) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    // Add 'T00:00:00' to ensure it's parsed as local time, not UTC
    const date = new Date(dateString + 'T00:00:00');
    return days[date.getDay()];
}

function getWeatherIcon(code) {
    // WMO Weather interpretation codes
    const icons = {
        0: '☀️', // Clear sky
        1: '🌤️', // Mainly clear
        2: '🌥️', // Partly cloudy
        3: '☁️', // Overcast
        45: '🌫️', // Fog
        48: '🌫️', // Depositing rime fog
        51: '🌦️', // Drizzle: Light
        53: '🌦️', // Drizzle: Moderate
        55: '🌦️', // Drizzle: Dense
        61: '🌧️', // Rain: Slight
        63: '🌧️',R // Rain: Moderate
        65: '🌧️', // Rain: Heavy
        80: '🌧️', // Showers: Slight
        81: '🌧️', // Showers: Moderate
        82: '🌧️', // Showers: Violent
        95: '⛈️', // Thunderstorm: Slight or moderate
        96: '⛈️', // Thunderstorm with slight hail
        99: '⛈️', // Thunderstorm with heavy hail
    };
    return icons[code] || '❓'; // Return icon or a question mark
}
```

### `frontend/serve.py`

```python
import http.server
import socketserver

PORT = 8001

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # --- THIS IS THE CHANGE ---
        # If the user requests the root, serve login.html
        if self.path == '/':
            self.path = '/login.html'
        # --- END CHANGE ---
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Serving frontend at http://localhost:{PORT}")
print("Go to this address in your browser.")
print("Your backend should be running on http://localhost:8000")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
```

### `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import json

# Load environment variables FIRST
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# --- All other app imports now go AFTER load_dotenv() ---
from app.api.v1 import general as general_router
from app.api.v1 import disasters as disasters_router
from app.api.v1 import pollutants as pollutants_router
from app.api.v1 import ai as ai_router
from app.api.v1 import risks as risks_router
from app.api.v1 import preferences as prefs_router
from app.api.v1 import alerts as alerts_router
from app.api.v1 import intelligence as intel_router
from app.api.v1 import weather as weather_router # <-- NEW
from app.services.firebase_auth import initialize_firebase

# Import our DB Base and engine
from app.models.database import Base, engine
# Import all models so Base.metadata knows about them
from app.models.user import User
from app.models.pollutant import PollutantSource
from app.models.preference import UserPreference
# -----------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Starting up EARTH backend...")
    
    initialize_firebase()
    
    try:
        print("Initializing database and creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created (if they didn't exist).")
    except Exception as e:
        print(f"CRITICAL: Failed to connect to TiDB or create tables. Error: {e}")
    
    # Load GeoJSON data from the correct root 'data' folder
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(base_dir, 'data')
        rivers_file_path = os.path.join(data_dir, 'world_rivers.json')
        
        print(f"Loading rivers data from {rivers_file_path}...")
        with open(rivers_file_path, 'r', encoding='utf-8') as f:
            app.state.rivers_data = json.load(f)
        print(f"Successfully loaded {len(app.state.rivers_data['features'])} river features.")
    except Exception as e:
        print(f"CRITICAL: Failed to load 'world_rivers.json'. Flood model will fail. Error: {e}")
        app.state.rivers_data = None
    
    yield
    
    # Code to run on shutdown
    print("Shutting down EARTH backend...")

# Initialize the FastAPI app
app = FastAPI(
    title="EARTH: AI-Powered Planetary Intelligence Platform",
    description="Backend API for EARTH project.",
    version="1.0.0", # <-- Version 1.0!
    lifpan=lifespan
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
app.include_router(general_router.router, prefix="/api/v1", tags=["General"])
app.include_router(disasters_router.router, prefix="/api/v1/disasters", tags=["Disasters"])
app.include_router(pollutants_router.router, prefix="/api/v1/pollutants", tags=["Pollutants"])
app.include_router(ai_router.router, prefix="/api/v1/ai", tags=["AI Engine"])
app.include_router(risks_router.router, prefix="/api/v1/risks", tags=["Risk Models"])
app.include_router(prefs_router.router, prefix="/api/v1/preferences", tags=["Preferences"])
app.include_router(alerts_router.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(intel_router.router, prefix="/api/v1/intelligence", tags=["Intelligence"])
app.include_router(weather_router.router, prefix="/api/v1/weather", tags=["Weather"]) # <-- NEW

# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the EARTH API (v1.0.0). See /docs for documentation."}
```

### `backend/app/helpers.py`

```python
import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on the
    earth (specified in decimal degrees) in kilometers.
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert decimal degrees to radians
    rad_lat1 = math.radians(lat1)
    rad_lon1 = math.radians(lon1)
    rad_lat2 = math.radians(lat2)
    rad_lon2 = math.radians(lon2)
    
    # Differences
    dlon = rad_lon2 - rad_lon1
    dlat = rad_lat2 - rad_lat1
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    
    return distance
```

### `backend/app/processing.py`

```python
import math
from typing import List
from .helpers import haversine_distance
from .services.usgs import QuakeData # Import the Pydantic model

def calculate_fwi(temp_c: float, humidity_rh: float, wind_kmh: float, rain_mm: float) -> float:
    """
    Calculates a simplified Fire Weather Index (FWI) score (0-100).
    This is a conceptual model based on FWI inputs, not the full CFFDRS.
    """
    
    # 1. Drought Factor (based on rain)
    # More rain = less drought.
    if rain_mm > 10:
        drought_factor = 0.1 # Very wet
    elif rain_mm > 5:
        drought_factor = 0.5
    elif rain_mm > 1:
        drought_factor = 0.8
    else:
        drought_factor = 1.0 # Very dry

    # 2. Temperature Factor
    # Higher temp = higher risk. Clamp at 0.
    temp_factor = max(0, temp_c - 10) / 10.0 
    
    # 3. Humidity Factor
    # Lower humidity = higher risk.
    humidity_factor = max(0, (70 - humidity_rh)) / 20.0

    # 4. Wind Factor
    # More wind = higher risk.
    wind_factor = 1.0 + (wind_kmh / 20.0)

    # Combine factors
    # This is a conceptual weighted product
    raw_score = (temp_factor * 1.5 + humidity_factor * 1.0) * wind_factor * drought_factor * 20
    
    # Normalize and clamp the score
    final_score = max(0, min(100, raw_score))
    
    return final_score


def calculate_safety_score(
    fire_risk: float, 
    aqi: int | None
) -> dict:
    """
    Calculates a "Personal Earth Safety Score" (0-100)
    and provides a primary risk factor.
    
    Score: 100 = Perfectly Safe, 0 = Extreme Danger
    """
    
    # Start with a perfect score of 100
    total_score = 100.0
    primary_risk = "Low"
    
    # 1. Deduct points for Fire Risk
    # This is the biggest penalty
    if fire_risk > 75:
        total_score -= 70
        primary_risk = "Extreme Fire Risk"
    elif fire_risk > 50:
        total_score -= 40
        primary_risk = "High Fire Risk"
    elif fire_risk > 20:
        total_score -= 15
        primary_risk = "Moderate Fire Risk"

    # 2. Deduct points for Air Quality
    if aqi is not None:
        if aqi > 150:
            total_score -= 25 # Unhealthy
            if total_score > 50: # Only set if fire isn't worse
                primary_risk = "Poor Air Quality"
        elif aqi > 100:
            total_score -= 15 # Unhealthy for sensitive groups
            if total_score > 70:
                primary_risk = "Poor Air Quality"
        elif aqi > 50:
            total_score -= 5 # Moderate
            if total_score > 85:
                primary_risk = "Moderate Air Quality"

    # Clamp the final score
    final_score = max(0, min(100, total_score))
    
    return {
        "score": round(final_score),
        "primary_risk": primary_risk
    }


def calculate_flood_risk(
    user_lat: float,
    user_lon: float,
    precipitation_forecast_7d: float,
    soil_moisture_current: float,
    rivers_data: dict  # This is the loaded world_rivers.json
) -> float:
    """
    Calculates a Flood Probability Score (0-100) by fusing
    rain forecast, soil moisture, and proximity to rivers.
    """
    base_risk = 0.0

    # 1. Rain Factor (Primary Driver)
    if precipitation_forecast_7d > 100: # Over 100mm in 7 days
        base_risk += 40
    elif precipitation_forecast_7d > 50:
        base_risk += 20
    elif precipitation_forecast_7d > 25:
        base_risk += 10
        
    # 2. Soil Moisture Factor (Risk Multiplier)
    # soil_moisture is in m³/m³ (e.g., 0.1 to 0.5)
    soil_multiplier = 1.0
    if soil_moisture_current > 0.4: # Very saturated
        soil_multiplier = 2.0
    elif soil_moisture_current > 0.3:
        soil_multiplier = 1.5
    
    # Apply multiplier
    base_risk = base_risk * soil_multiplier

    # 3. Proximity to River Factor (Risk Adder)
    # This is your Naivasha logic.
    min_dist_to_river = 99999 # Start with a huge distance
    
    if rivers_data:
        for feature in rivers_data.get("features", []):
            try:
                # A river is a LineString (list of points)
                for coords in feature.get("geometry", {}).get("coordinates", []):
                    river_lon, river_lat = coords[0], coords[1] # Take first point
                    dist = haversine_distance(user_lat, user_lon, river_lat, river_lon)
                    if dist < min_dist_to_river:
                        min_dist_to_river = dist
            except Exception:
                continue # Skip malformed river data

    # Add risk based on distance
    if min_dist_to_river < 10: # < 10km from a major river/lake
        base_risk += 30
    elif min_dist_to_river < 25:
        base_risk += 15
    elif min_dist_to_river < 50:
        base_risk += 5

    # 4. Final clamping
    final_score = max(0, min(100, base_risk))
    
    return round(final_score)


def find_closest_quake(
    user_lat: float,
    user_lon: float,
    quake_data: QuakeData
) -> dict | None:
    """
    Finds the closest significant earthquake to the user.
    """
    closest_quake = None
    min_distance = float('inf')

    for quake in quake_data.features:
        distance = haversine_distance(user_lat, user_lon, quake.lat, quake.lon)
        if distance < min_distance:
            min_distance = distance
            closest_quake = quake
            
    if closest_quake:
        return {
            "mag": closest_quake.mag,
            "place": closest_quake.place,
            "time": closest_quake.time,
            "url": closest_quake.url,
            "distance_km": round(min_distance, 2)
        }
    
    return None


def generate_proactive_alerts(
    fire_risk: float,
    flood_risk: float,
    uv_index: float | None
) -> List[str]:
    """
    Checks all risk scores and generates a list of human-readable
    alert messages for the user.
    """
    alerts = []

    # 1. Check Flood Risk (Your Naivasha example)
    if flood_risk > 75:
        alerts.append("CRITICAL: FLOODING MAY OCCUR IN YOUR AREA. EVACUATE LOW-LYING AREAS.")
    elif flood_risk > 50:
        alerts.append("WARNING: High flood probability detected. Monitor local river levels.")
    
    # 2. Check Fire Risk
    if fire_risk > 75:
        alerts.append("CRITICAL: Extreme Fire Risk detected. Be ready to evacuate.")
    elif fire_risk > 50:
        alerts.append("WARNING: High Fire Risk detected. Avoid all outdoor burning.")

    # 3. Check UV Index (Your Nairobi example)
    if uv_index is not None:
        if uv_index >= 11:
            alerts.append("HEALTH: Extreme UV Index (11+) forecast. Avoid sun exposure.")
        elif uv_index >= 8:
            alerts.append("HEALTH: Very High UV Index (8-10) forecast. Stay indoors or seek shade.")

    # 4. If no risks, return a safe message
    if not alerts:
        alerts.append("All Clear: No immediate environmental threats detected for your area.")
        
    return alerts
```

### `backend/app/models/database.py`

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# --- TiDB Connection String & SSL ---
TIDB_CONNECTION_STRING = os.getenv("TIDB_CONNECTION_STRING")

# We need the full path to ca.pem
# This file is in .../backend/app/models/
# We need to go up 3 levels to get to the 'backend' folder
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CA_CERT_PATH = os.path.join(BACKEND_DIR, "ca.pem")

# This is a robust way to add the ssl_ca param to your connection string
# It will add it if it's missing, or overwrite it if it's already there
# This ensures it always points to the correct ca.pem file
try:
    parsed_url = urlparse(TIDB_CONNECTION_STRING)
    query_params = parse_qs(parsed_url.query)
    query_params['ssl_ca'] = [CA_CERT_PATH]
    
    new_query = urlencode(query_params, doseq=True)
    new_url_parts = parsed_url._replace(query=new_query)
    FULL_CONNECTION_STRING = urlunparse(new_url_parts)
    
except Exception as e:
    print(f"Error parsing TiDB connection string: {e}")
    print("Please ensure TIDB_CONNECTION_STRING is set correctly in your .env file.")
    print(f"Example: mysql+mysqlconnector://user:pass@host.tidbcloud.com:4000/dbname")
    FULL_CONNECTION_STRING = ""

# --- SQLAlchemy Setup ---
engine = create_engine(
    FULL_CONNECTION_STRING,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- Database Dependency ---
def get_db():
    """
    FastAPI dependency to get a database session.
    Yields a session and closes it automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `backend/app/models/preference.py`

```python
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    # Link this to the user's UID from the 'users' table
    user_uid = Column(String(128), ForeignKey("users.uid"), primary_key=True)
    
    home_latitude = Column(Float, nullable=True)
    home_longitude = Column(Float, nullable=True)
    default_zoom = Column(Integer, default=10, nullable=False)
    
    # Track when these settings were last updated
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreference(user_uid='{self.user_uid}')>"
```

### `backend/app/models/pollutant.py`

```python
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class PollutantSource(Base):
    __tablename__ = "pollutant_sources"

    id = Column(String(36), primary_key=True, index=True) # A unique ID, e.g., UUID
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Optional: A user-provided description
    description = Column(String(500), nullable=True)
    
    # Link this report to the user who submitted it
    submitted_by_uid = Column(String(128), ForeignKey("users.uid"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Establish the relationship to the User model (optional but good practice)
    submitter = relationship("User")

    def __repr__(self):
        return f"<PollutantSource(lat={self.latitude}, lon={self.longitude})>"
```

### `backend/app/models/user.py`

```python
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String(128), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(uid='{self.uid}', email='{self.email}')>"
```

### `backend/app/services/ai_services.py`

```python
import os
from openai import AsyncOpenAI
from fastapi import HTTPException
from pydantic import BaseModel

# --- Initialize OpenAI Client ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("CRITICAL: OPENAI_API_KEY not set. AI Report will fail.")
    client = None
else:
    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        print("OpenAI client initialized.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize OpenAI: {e}")
        client = None

# --- NEW: Pydantic model for our local data ---
class LocalSummaryData(BaseModel):
    safety_score: int
    primary_risk: str
    aqi: int | None
    temperature: float
    fire_risk: int

async def get_local_insight(summary: LocalSummaryData) -> str:
    """
    Generates a high-level LOCAL insight using the OpenAI API based on
    the user's complete local intelligence summary.
    """
    if not client:
        raise HTTPException(status_code=500, detail="OpenAI service is not configured.")

    # This prompt is now much smarter and more personal
    prompt = f"""
    You are an expert risk analyst for the 'EARTH' platform.
    A user's local intelligence summary is as follows:
    - Overall Safety Score: {summary.safety_score}/100 (100 is safe, 0 is dangerous)
    - Primary Risk Factor: "{summary.primary_risk}"
    - Air Quality Index (AQI): {summary.aqi or 'N/A'}
    - Max Temperature: {summary.temperature}°C
    - Fire Risk Score: {summary.fire_risk}/100

    Write a single, concise, and helpful sentence (max 30 words) for the user.
    If the risk is high, be direct. If it's low, be reassuring.
    
    Example (High Risk): "Your personal safety score is very low due to extreme fire risk; avoid outdoor activity and stay alert."
    Example (Low Risk): "Your local conditions are stable, with a high safety score and no immediate environmental risks detected."
    Example (AQI Risk): "Your safety score is moderate; while fire risk is low, be mindful of poor air quality today."
    """

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=60,
            temperature=0.7
        )
        
        if chat_completion.choices:
            return chat_completion.choices[0].message.content.strip()
        else:
            return "No insight could be generated at this time."
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=503, detail=f"AI service request failed: {e}")
```

### `backend/app/services/firebase_auth.py`

```python
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os

# --- Import DB and User Model ---
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
# -------------------------------

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILE_NAME_FROM_ENV = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-service-account.json")
SERVICE_ACCOUNT_FILE = os.path.join(BACKEND_DIR, FILE_NAME_FROM_ENV)

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    """
    try:
        firebase_admin.get_app()
    except ValueError:
        print(f"Initializing Firebase with cert: {SERVICE_ACCOUNT_FILE}")
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)  # <-- ADDED DATABASE DEPENDENCY
):
    """
    Dependency to:
    1. Verify Firebase ID token.
    2. Get or Create the user in the TiDB database.
    3. Return the user's token data.
    """
    try:
        decoded_token = auth.verify_id_token(token)
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")

    # --- ADDED: TiDB User Sync Logic ---
    uid = decoded_token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token: No UID found")

    try:
        # Check if user exists in our DB
        db_user = db.query(User).filter(User.uid == uid).first()

        if not db_user:
            # User is new, create them in our TiDB
            print(f"New user detected. Creating user {uid} in TiDB.")
            new_user = User(
                uid=uid,
                email=decoded_token.get("email"),
                display_name=decoded_token.get("name")
            )
            db.add(new_user)
            db.commit()
        else:
            # Optional: Update user info if it has changed
            if db_user.display_name != decoded_token.get("name") or db_user.email != decoded_token.get("email"):
                db_user.display_name = decoded_token.get("name")
                db_user.email = decoded_token.get("email")
                db.commit()
                
    except Exception as e:
        # Don't fail the request if DB fails, but log it
        print(f"CRITICAL: Failed to sync user {uid} to TiDB. Error: {e}")
        # In a production app, you might want to handle this more gracefully
        # For now, we'll just log and continue.
    
    # --- END: TiDB User Sync Logic ---

    return decoded_token
```

### `backend/app/services/google_maps.py`

```python
import httpx
from fastapi import HTTPException
import os
from pydantic import BaseModel

# Get the Google Maps API Key you added to your .env file
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
AIR_QUALITY_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup"

if not API_KEY:
    print("WARNING: GOOGLE_MAPS_API_KEY is not set. Air Quality API will fail.")

class AirQualityData(BaseModel):
    """Holds the parsed Air Quality Index (AQI)"""
    aqi: int
    display_name: str

async def get_air_quality(lat: float, lon: float) -> AirQualityData | None:
    """
    Fetches the current Air Quality Index (AQI) from the Google Air Quality API.
    """
    if not API_KEY:
        # Don't fail the whole request, just return None
        print("Cannot fetch AQI: GOOGLE_MAPS_API_KEY is missing.")
        return None

    client = httpx.AsyncClient()
    try:
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "extraComputations": ["LOCAL_AQI"],
            "languageCode": "en"
        }
        
        headers = {
            'Content-Type': 'application/json'
        }

        response = await client.post(f"{AIR_QUALITY_URL}?key={API_KEY}", json=payload, headers=headers)
        
        response.raise_for_status() # Raise for 4xx/5xx errors
        
        data = response.json()

        # Parse the response to find the local AQI
        # We look for the "uaqi" (Universal AQI)
        for index in data.get("indexes", []):
            if index.get("code") == "uaqi":
                return AirQualityData(
                    aqi=index.get("aqi"),
                    display_name=index.get("displayName")
                )
        
        # If no uaqi is found, return None
        return None

    except httpx.HTTPStatusError as e:
        print(f"Google Air Quality HTTP Error: {e.response.text}")
        # Don't fail the whole request, just log and return None
        return None
    except Exception as e:
        print(f"Error processing Google Air Quality data: {e}")
        return None
    finally:
        await client.aclose()
```

### `backend/app/services/nasa_eonet.py`

```python
import httpx
from fastapi import HTTPException

# EONET API v3 endpoint for events
EONET_API_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

async def fetch_open_events():
    """
    Fetches the 20 most recent "open" natural events from NASA EONET.
    """
    params = {
        "status": "open",
        "limit": 20,
        "days": 30  # Look at events from the last 30 days
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(EONET_API_URL, params=params)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching data from NASA EONET: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, # Service Unavailable
                detail=f"Error connecting to NASA EONET: {e}"
            )
```

### `backend/app/services/open_meteo.py`

```python
import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

# --- This is the robust /forecast endpoint ---
METEO_API_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherData(BaseModel):
    """A Pydantic model to hold the parsed weather data."""
    temp_max: float
    humidity_min: float
    wind_max: float
    precipitation: float

async def get_raw_weather_data(lat: float, lon: float) -> WeatherData:
    """
    Fetches the raw weather components needed to calculate FWI.
    (Temp, Humidity, Wind, Precipitation)
    """
    
    # We ask for today's max temp, min humidity, max wind, and precip sum
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,relative_humidity_2m_min,wind_speed_10m_max,precipitation_sum",
        "forecast_days": 1,
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(METEO_API_URL, params=params)
            data = response.json()
            
            if data.get("error"):
                raise ValueError(data.get("reason", "Unknown Open-Meteo error"))

            response.raise_for_status()
            
            # --- Parse the 4 values ---
            daily_data = data.get("daily", {})
            
            temp_max = daily_data.get("temperature_2m_max", [None])[0]
            humidity_min = daily_data.get("relative_humidity_2m_min", [None])[0]
            wind_max = daily_data.get("wind_speed_10m_max", [None])[0]
            precipitation = daily_data.get("precipitation_sum", [None])[0]
            
            if any(v is None for v in [temp_max, humidity_min, wind_max, precipitation]):
                raise ValueError("Incomplete weather data received from Open-Meteo.")
                
            return WeatherData(
                temp_max=temp_max,
                humidity_min=humidity_min,
                wind_max=wind_max,
                precipitation=precipitation
            )
            
        except httpx.HTTPStatusError as e:
            print(f"Open-Meteo HTTP Error: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Open-Meteo: {e.response.text}"
            )
        except (httpx.RequestError, ValueError, KeyError) as e:
            print(f"Open-Meteo processing error: {e}") 
            raise HTTPException(
                status_code=503,
                detail=f"Weather data processing error: {e}"
            )


class FloodData(BaseModel):
    """A Pydantic model for flood-related data."""
    precipitation_forecast_7d: float  # 7-day sum
    soil_moisture_current: float    # Top-level soil moisture
    uv_index_tomorrow: float | None

async def get_flood_data(lat: float, lon: float) -> FloodData:
    """
    Fetches 7-day precipitation forecast, current soil moisture,
    and tomorrow's max UV index.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["precipitation_sum", "uv_index_max"],
        "forecast_days": 7,
        "current": "soil_moisture_0_1cm",
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(METEO_API_URL, params=params)
            data = response.json()
            
            if data.get("error"):
                raise ValueError(data.get("reason", "Unknown Open-Meteo error"))
            response.raise_for_status()

            soil_moisture = data.get("current", {}).get("soil_moisture_0_1cm", None)
            precip_list = data.get("daily", {}).get("precipitation_sum", [])
            precip_sum = sum(precip_list) if precip_list else 0.0
            uv_list = data.get("daily", {}).get("uv_index_max", [None, None])
            uv_tomorrow = uv_list[1] if len(uv_list) > 1 else None

            if soil_moisture is None:
                raise ValueError("Incomplete flood data received (soil moisture).")
                
            return FloodData(
                precipitation_forecast_7d=precip_sum,
                soil_moisture_current=soil_moisture,
                uv_index_tomorrow=uv_tomorrow
            )

        except (httpx.RequestError, ValueError, KeyError, httpx.HTTPStatusError) as e:
            print(f"Open-Meteo flood data processing error: {e}") 
            raise HTTPException(
                status_code=503,
                detail=f"Weather data processing error for flood model: {e}"
            )

# --- NEW FUNCTION FOR 7-DAY FORECAST ---

class DailyForecast(BaseModel):
    time: str
    weather_code: int
    temp_max: float
    temp_min: float

class ForecastData(BaseModel):
    daily: List[DailyForecast]

async def get_7_day_forecast(lat: float, lon: float) -> ForecastData:
    """
    Fetches the 7-day forecast: max/min temp and weather code.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "forecast_days": 7,
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(METEO_API_URL, params=params)
            data = response.json()
            
            if data.get("error"):
                raise ValueError(data.get("reason", "Unknown Open-Meteo error"))
            response.raise_for_status()

            daily_data = data.get("daily", {})
            
            forecast_list = []
            for i in range(len(daily_data.get("time", []))):
                forecast_list.append(
                    DailyForecast(
                        time=daily_data["time"][i],
                        weather_code=daily_data["weather_code"][i],
                        temp_max=daily_data["temperature_2m_max"][i],
                        temp_min=daily_data["temperature_2m_min"][i]
                    )
                )
            
            if not forecast_list:
                raise ValueError("No forecast data returned.")
                
            return ForecastData(daily=forecast_list)

        except (httpx.RequestError, ValueError, KeyError, httpx.HTTPStatusError) as e:
            print(f"Open-Meteo 7-day forecast error: {e}") 
            raise HTTPException(
                status_code=503,
                detail=f"Weather forecast processing error: {e}"
            )
```

### `backend/app/services/usgs.py`

```python
import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional

# USGS API endpoint for significant earthquakes in the past 24 hours
USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"
# Let's use 2.5+ magnitude for the past day for more data
USGS_API_URL_ALL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"


class QuakeFeature(BaseModel):
    """A Pydantic model for a single earthquake feature."""
    mag: float
    place: str
    time: int
    url: str
    lat: float
    lon: float

class QuakeData(BaseModel):
    """A Pydantic model for the full API response."""
    features: List[QuakeFeature]

async def get_significant_earthquakes() -> QuakeData:
    """
    Fetches all earthquakes with a magnitude of 2.5+ in the last 24 hours.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(USGS_API_URL_ALL)
            response.raise_for_status() # Raise for 4xx/5xx errors
            
            data = response.json()
            
            # Parse the features
            features_list = []
            for item in data.get("features", []):
                properties = item.get("properties", {})
                geometry = item.get("geometry", {}).get("coordinates", [])
                
                if not properties or len(geometry) < 2:
                    continue

                features_list.append(
                    QuakeFeature(
                        mag=properties.get("mag", 0.0),
                        place=properties.get("place", "Unknown location"),
                        time=properties.get("time", 0),
                        url=properties.get("url", ""),
                        lon=geometry[0], # Lon is first in GeoJSON
                        lat=geometry[1]
                    )
                )
            
            return QuakeData(features=features_list)

        except httpx.HTTPStatusError as e:
            print(f"USGS HTTP Error: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching data from USGS: {e.response.text}"
            )
        except (httpx.RequestError, ValueError, KeyError) as e:
            print(f"USGS processing error: {e}") 
            raise HTTPException(
                status_code=503,
                detail=f"Earthquake data processing error: {e}"
            )
```

### `backend/app/api/v1/alerts.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Request # <-- ADD Request
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.firebase_auth import get_current_user
from app.models.preference import UserPreference
from app.services import nasa_eonet
from app.helpers import haversine_distance

from app.services import usgs
from app import processing

# --- NEW IMPORT ---
from app.services import open_meteo
# -------------------

router = APIRouter()

@router.get("/nearby-events")
async def get_nearby_events(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    radius_km: int = 500
):
    # ... (existing function, no changes) ...
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set. Please set your location first.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    try:
        all_events_data = await nasa_eonet.fetch_open_events()
        all_events = all_events_data.get("events", [])
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch NASA EONET data: {e}")
    nearby_events = []
    for event in all_events:
        try:
            geom = event.get("geometry", [])[0]
            if geom.get("type") == "Point":
                event_lon, event_lat = geom.get("coordinates")
            else:
                event_lon, event_lat = geom.get("coordinates")[0][0]
            distance = haversine_distance(user_lat, user_lon, event_lat, event_lon)
            if distance <= radius_km:
                event['distance_km'] = round(distance, 2)
                nearby_events.append(event)
        except Exception as e:
            print(f"Skipping event {event.get('id')}: could not parse coordinates. Error: {e}")
    return {
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "search_radius_km": radius_km,
        "event_count": len(nearby_events),
        "events": nearby_events
    }

@router.get("/nearby-earthquake")
async def get_nearby_earthquake(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    # ... (existing function, no changes) ...
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    try:
        quake_data = await usgs.get_significant_earthquakes()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch USGS data: {e}")
    closest_quake = processing.find_closest_quake(user_lat, user_lon, quake_data)
    if not closest_quake:
        return { "message": "No significant earthquakes found in the last 24 hours." }
    return closest_quake

# --- NEW "PROACTIVE ALERT" ENDPOINT ---

@router.get("/run-check")
async def run_proactive_alert_check(
    request: Request, # To access app.state
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Simulates the "daily check" by running all models for the user.
    Returns a list of human-readable alert strings.
    """
    user_uid = user.get("uid")

    # 1. Get user's home location
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    
    print(f"Running proactive alert check for user {user.get('email')}...")

    try:
        # 2. Fetch all raw data in parallel
        flood_model_data = await open_meteo.get_flood_data(user_lat, user_lon)
        fire_model_data = await open_meteo.get_raw_weather_data(user_lat, user_lon)
        rivers_data = request.app.state.rivers_data
        
        # 3. Run all processing models
        flood_risk = processing.calculate_flood_risk(
            user_lat=user_lat,
            user_lon=user_lon,
            precipitation_forecast_7d=flood_model_data.precipitation_forecast_7d,
            soil_moisture_current=flood_model_data.soil_moisture_current,
            rivers_data=rivers_data
        )
        
        fire_risk = processing.calculate_fwi(
            temp_c=fire_model_data.temp_max,
            humidity_rh=fire_model_data.humidity_min,
            wind_kmh=fire_model_data.wind_max,
            rain_mm=fire_model_data.precipitation
        )
        
        uv_index = flood_model_data.uv_index_tomorrow

        # 4. Generate alert messages
        alerts = processing.generate_proactive_alerts(
            fire_risk=fire_risk,
            flood_risk=flood_risk,
            uv_index=uv_index
        )
        
        return {"alerts": alerts}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in alert-check endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate alerts: {e}")
```

### `backend/app/api/v1/ai.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.firebase_auth import get_current_user

# Import our new function and data model
from app.services import ai_services
from app.services.ai_services import LocalSummaryData

router = APIRouter()

# --- This endpoint is CHANGED from GET to POST ---
@router.post("/local-insight")
async def get_ai_local_insight(
    summary_data: LocalSummaryData, # <-- Receives data from frontend
    user: dict = Depends(get_current_user)
):
    """
    Generates a single-sentence AI insight based on the user's
    local intelligence summary.
    """
    print(f"User {user.get('email')} is requesting an AI local insight.")
    
    try:
        # 1. Pass the local data to the AI service
        insight = await ai_services.get_local_insight(summary_data)
        
        # 2. Return the result
        return {
            "insight": insight
        }
        
    except HTTPException as e:
        # Re-raise HTTPExceptions from services
        raise e
    except Exception as e:
        print(f"Error in local-insight endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI insight.")
```

### `backend/app/api/v1/disasters.py`

```python
from fastapi import APIRouter, Depends
from app.services.firebase_auth import get_current_user
from app.services import nasa_eonet

router = APIRouter()

@router.get("/eonet-events")
async def get_eonet_events(
    user: dict = Depends(get_current_user)
):
    """
    Secure endpoint to fetch the latest open natural events from NASA EONET.
    """
    print(f"User {user.get('email')} is requesting EONET data.")
    events = await nasa_eonet.fetch_open_events()
    return events
```

### `backend/app/api/v1/general.py`

```python
from fastapi import APIRouter, Depends
from typing import Dict
from app.services.firebase_auth import get_current_user

router = APIRouter()

@router.get("/health")
async def get_health():
    """
    Public endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "EARTH Backend is running!"}


@router.get("/protected-data", response_model=Dict[str, str])
async def get_protected_data(
    user: dict = Depends(get_current_user)
):
    """
    A secure endpoint that requires a valid Firebase auth token.
    It returns a welcome message using the user's name from the token.
    """
    user_name = user.get("name", "User")
    user_email = user.get("email", "no-email@example.com")
    
    print(f"Access granted for user: {user_email}")
    
    return {
        "message": f"Hello, {user_name}! Welcome to the secure EARTH API.",
        "your_email": user_email,
        "your_uid": user.get("uid")
    }
```

### `backend/app/api/v1/intelligence.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.firebase_auth import get_current_user

# Import all our services and models
from app.services import open_meteo
from app.services import google_maps
from app import processing

router = APIRouter()

@router.get("/local-summary")
async def get_local_intelligence_summary(
    lat: float = Query(..., description="User's latitude", ge=-90, le=90),
    lon: float = Query(..., description="User's longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    This is the new fusion endpoint for the "Local Intelligence" widget.
    It combines weather, air quality, and fire risk into a single score.
    """
    print(f"User {user.get('email')} requesting local intelligence for ({lat}, {lon})")
    
    try:
        # 1. Get Raw Weather Data
        weather_data = await open_meteo.get_raw_weather_data(lat, lon)
        
        # 2. Get Air Quality Data
        aqi_data = await google_maps.get_air_quality(lat, lon)
        
        # 3. Calculate Fire Risk
        fire_risk = processing.calculate_fwi(
            temp_c=weather_data.temp_max,
            humidity_rh=weather_data.humidity_min,
            wind_kmh=weather_data.wind_max,
            rain_mm=weather_data.precipitation
        )
        
        # 4. Calculate Final Safety Score
        aqi_value = aqi_data.aqi if aqi_data else None
        safety_score_data = processing.calculate_safety_score(fire_risk, aqi_value)
        
        # 5. Return the complete package
        return {
            "safety_score": safety_score_data["score"],
            "primary_risk": safety_score_data["primary_risk"],
            "weather": {
                "temperature": weather_data.temp_max,
                "precipitation": weather_data.precipitation
            },
            "air_quality": {
                "aqi": aqi_value,
                "display_name": aqi_data.display_name if aqi_data else "N/A"
            },
            "fire_risk": round(fire_risk)
        }
        
    except Exception as e:
        print(f"Error in local-summary endpoint: {e}")
        # This will catch errors from get_raw_weather_data if it fails
        raise HTTPException(status_code=500, detail=f"Failed to generate local summary: {e}")
```

### `backend/app/api/v1/pollutants.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid # To generate unique IDs
from datetime import datetime

# Import DB and auth dependencies
from app.models.database import get_db
from app.services.firebase_auth import get_current_user

# Import our new model
from app.models.pollutant import PollutantSource

router = APIRouter()

# --- Pydantic Models for Data Validation ---

class PollutantSourceCreate(BaseModel):
    """Data model for creating a new source."""
    latitude: float
    longitude: float
    description: str | None = None

class PollutantSourcePublic(BaseModel):
    """Data model for returning a source to the client."""
    id: str
    latitude: float
    longitude: float
    description: str | None
    submitted_by_uid: str
    created_at: datetime

    class Config:
        orm_mode = True # Allows mapping from SQLAlchemy model


@router.get("", response_model=list[PollutantSourcePublic])
async def get_all_pollutant_sources(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user) # Secure this endpoint
):
    """
    Fetches all pollutant sources from the database.
    """
    try:
        sources = db.query(PollutantSource).all()
        return sources
    except Exception as e:
        print(f"Error fetching pollutant sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pollutant sources.")

@router.post("", response_model=PollutantSourcePublic) # <-- THIS LINE IS FIXED
async def create_pollutant_source(
    source_data: PollutantSourceCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user) # Get user info from token
):
    """
    Creates a new pollutant source in the database from a user's click.
    """
    user_uid = user.get("uid")
    if not user_uid:
        raise HTTPException(status_code=401, detail="Could not verify user UID from token.")

    try:
        # Create a new PollutantSource object
        new_source = PollutantSource(
            id=str(uuid.uuid4()), # Generate a new unique ID
            latitude=source_data.latitude,
            longitude=source_data.longitude,
            description=source_data.description,
            submitted_by_uid=user_uid
        )
        
        db.add(new_source)
        db.commit()
        db.refresh(new_source) # Get the created object back from the DB
        
        print(f"New pollutant source added by user {user_uid} at ({new_source.latitude}, {new_source.longitude})")
        return new_source
        
    except Exception as e:
        db.rollback()
        print(f"Error creating pollutant source: {e}")
        raise HTTPException(status_code=500, detail="Failed to save pollutant source.")
```

### `backend/app/api/v1/preferences.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.database import get_db
from app.services.firebase_auth import get_current_user
from app.models.preference import UserPreference

router = APIRouter()

class PreferenceUpdate(BaseModel):
    latitude: float
    longitude: float
    zoom: int = 10

@router.get("/me", response_model=PreferenceUpdate)
async def get_my_preferences(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Get the current user's saved home location and zoom.
    """
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="User preferences not found.")
    
    return PreferenceUpdate(
        latitude=prefs.home_latitude,
        longitude=prefs.home_longitude,
        zoom=prefs.default_zoom
    )

@router.post("/me")
async def update_my_preferences(
    prefs_data: PreferenceUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Create or update the user's home location and zoom.
    """
    user_uid = user.get("uid")
    
    # Try to get existing preferences
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    
    if prefs:
        # Update existing
        prefs.home_latitude = prefs_data.latitude
        prefs.home_longitude = prefs_data.longitude
        prefs.default_zoom = prefs_data.zoom
    else:
        # Create new
        prefs = UserPreference(
            user_uid=user_uid,
            home_latitude=prefs_data.latitude,
            home_longitude=prefs_data.longitude,
            default_zoom=prefs_data.zoom
        )
        db.add(prefs)
        
    try:
        db.commit()
        return {"message": "Preferences updated successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
```

### `backend/app/api/v1/risks.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query, Request # <-- ADD Request
from sqlalchemy.orm import Session # <-- ADD Session
from app.services.firebase_auth import get_current_user

# --- UPDATED IMPORTS ---
from app.services import open_meteo
from app import processing
from app.models.database import get_db # <-- ADD get_db
from app.models.preference import UserPreference # <-- ADD UserPreference
# -----------------------

router = APIRouter()

@router.get("/fire-weather")
async def get_fire_weather_risk(
    lat: float = Query(..., description="User's latitude", ge=-90, le=90),
    lon: float = Query(..., description="User's longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    Calculates the Fire Weather Index (FWI) risk for a specific location
    by fetching raw data and running it through the processing model.
    """
    print(f"User {user.get('email')} requesting fire risk for ({lat}, {lon})")
    
    try:
        # 1. Fetch the raw weather data
        weather_data = await open_meteo.get_raw_weather_data(lat, lon)
        
        # 2. Run data through our local processing model
        fwi_score = processing.calculate_fwi(
            temp_c=weather_data.temp_max,
            humidity_rh=weather_data.humidity_min,
            wind_kmh=weather_data.wind_max,
            rain_mm=weather_data.precipitation
        )
        
        # 3. Return the calculated score
        return {
            "fwi_score": fwi_score,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "raw_data": weather_data.dict() # Send raw data for debugging
        }
        
    except HTTPException as e:
        # Re-raise HTTPExceptions from services
        raise e
    except Exception as e:
        print(f"Error in fire-weather endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate fire risk insight.")

# --- NEW FLOOD RISK ENDPOINT ---

@router.get("/flood")
async def get_flood_risk(
    request: Request, # To access app.state
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Calculates the Flood Probability risk for the user's
    saved home location.
    """
    user_uid = user.get("uid")

    # 1. Get user's home location from TiDB
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set. Please set your location first.")
        
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude

    print(f"User {user.get('email')} requesting flood risk for ({user_lat}, {user_lon})")

    try:
        # 2. Get flood-related weather data
        flood_data = await open_meteo.get_flood_data(user_lat, user_lon)
        
        # 3. Get river data from app state
        rivers_data = request.app.state.rivers_data
        if not rivers_data:
            raise HTTPException(status_code=500, detail="River data not loaded on server.")
        
        # 4. Run data through our processing model
        flood_score = processing.calculate_flood_risk(
            user_lat=user_lat,
            user_lon=user_lon,
            precipitation_forecast_7d=flood_data.precipitation_forecast_7d,
            soil_moisture_current=flood_data.soil_moisture_current,
            rivers_data=rivers_data
        )

        # 5. Return the score
        return {
            "flood_score": flood_score,
            "location": { "latitude": user_lat, "longitude": user_lon },
            "debug_data": flood_data.dict()
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in flood-risk endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate flood risk: {e}")
```

### `backend/app/api/v1/weather.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.firebase_auth import get_current_user

from app.models.database import get_db
from app.models.preference import UserPreference
from app.services import open_meteo

router = APIRouter()

@router.get("/forecast")
async def get_weather_forecast(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Gets the 7-day weather forecast for the user's saved home location.
    """
    user_uid = user.get("uid")
    
    # 1. Get user's home location
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set.")
        
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    
    print(f"User {user.get('email')} requesting 7-day forecast for ({user_lat}, {user_lon})")

    # 2. Fetch the 7-day forecast
    try:
        forecast_data = await open_meteo.get_7_day_forecast(user_lat, user_lon)
        return forecast_data
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in /forecast endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate forecast: {e}")
```

### `backend/requirements.txt`

```text
fastapi
uvicorn[standard]
python-dotenv
firebase-admin
python-jose[cryptography]
passlib[bcrypt]
sqlalchemy
mysql-connector-python
httpx
google-generativeai
openai
```

