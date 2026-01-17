import os

# --- 1. Configuration ---

# The name of the new file we will create
output_filename = "EARTH_HANDOFF.md"

# List of all files to include in the handoff
# This ensures we only get our code and not venv, pycache, etc.
files_to_include = [
    # Frontend Files
    'frontend/login.html',
    'frontend/index.html',
    'frontend/styles.css',
    'frontend/app.js',
    'frontend/dashboard.js',
    'frontend/serve.py',

    # Backend App Files
    'backend/app/main.py',
    'backend/app/helpers.py',
    'backend/app/processing.py',
    
    # Backend Models
    'backend/app/models/database.py',
    'backend/app/models/preference.py',
    'backend/app/models/pollutant.py',
    'backend/app/models/user.py',

    # Backend Services
    'backend/app/services/ai_services.py',
    'backend/app/services/firebase_auth.py',
    'backend/app/services/google_maps.py',
    'backend/app/services/nasa_eonet.py',
    'backend/app/services/open_meteo.py',
    'backend/app/services/usgs.py',

    # Backend API Routers
    'backend/app/api/v1/alerts.py',
    'backend/app/api/v1/ai.py',
    'backend/app/api/v1/disasters.py',
    'backend/app/api/v1/general.py',
    'backend/app/api/v1/intelligence.py',
    'backend/app/api/v1/pollutants.py',
    'backend/app/api/v1/preferences.py',
    'backend/app/api/v1/risks.py',
    'backend/app/api/v1/weather.py',

    # Root Files
    'backend/requirements.txt',
]

# This is the high-level context for the new AI
# It will be written to the top of the .md file
project_vision = """
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
"""

# Helper to get the correct markdown language for code blocks
def get_language(filepath):
    if filepath.endswith('.py'):
        return 'python'
    if filepath.endswith('.js'):
        return 'javascript'
    if filepath.endswith('.css'):
        return 'css'
    if filepath.endswith('.html'):
        return 'html'
    if filepath.endswith('.txt'):
        return 'text'
    return ''

# --- 2. The Script ---

def create_handoff_file():
    print(f"Starting handoff... Will create '{output_filename}'")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        # 1. Write the Project Vision
        f.write(project_vision + "\n\n")

        # 2. Write the File Structure (a simplified tree)
        f.write("## 📂 Final Project Structure\n\n")
        f.write("```\n")
        f.write("earth-project/\n")
        f.write("├── backend/\n")
        f.write("│   ├── app/\n")
        f.write("│   │   ├── api/v1/ (all 10 router files)\n")
        f.write("│   │   ├── models/ (all 4 model files)\n")
        f.write("│   │   ├── services/ (all 7 service files)\n")
        f.write("│   │   ├── helpers.py\n")
        f.write("│   │   ├── main.py\n")
        f.write("│   │   └── processing.py\n")
        f.write("│   ├── .env (LISTED BELOW)\n")
        f.write("│   ├── ca.pem\n")
        f.write("│   ├── firebase-service-account.json\n")
        f.write("│   └── requirements.txt\n")
        f.write("├── frontend/\n")
        f.write("│   ├── login.html\n")
        f.write("│   ├── index.html\n")
        f.write("│   ├── styles.css\n")
        f.write("│   ├── app.js\n")
        f.write("│   ├── dashboard.js\n")
        f.write("│   └── serve.py\n")
        f.write("├── data/\n")
        f.write("│   ├── world_rivers.json\n")
        f.write("│   └── world_countries.json\n")
        f.write("└── create_handoff.py (This script)\n")
        f.write("```\n\n")
        
        # 3. Write the .env and Data requirements
        f.write("## 🔑 Required Keys (.env) & Data Files\n\n")
        f.write("* `TIDB_CONNECTION_STRING`\n")
        f.write("* `FIREBASE_CREDENTIALS_PATH`\n")
        f.write("* `N2YO_API_KEY`\n")
        f.write("* `NASA_API_KEY`\n")
        f.write("* `Maps_API_KEY`\n")
        f.write("* `OPENAI_API_KEY`\n")
        f.write("* `data/world_rivers.json` (from Natural Earth)\n")
        f.write("* `data/world_countries.json` (from Natural Earth)\n")
        f.write("\n")

        # 4. Write all the file contents
        f.write("## 💻 Full Project Code\n\n")
        
        for filepath in files_to_include:
            print(f"Adding '{filepath}'...")
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    lang = get_language(filepath)
                    
                    f.write(f"### `{filepath}`\n\n")
                    f.write(f"```{lang}\n")
                    f.write(content + "\n")
                    f.write("```\n\n")
                    
            except FileNotFoundError:
                print(f"  WARNING: File not found, skipping: {filepath}")
            except Exception as e:
                print(f"  ERROR reading {filepath}: {e}")

    print("-" * 30)
    print(f"✅ Success! Handoff file created: {output_filename}")
    print("You can now open this file, copy its entire contents, and paste it into a new chat.")
    print("-" * 30)

if __name__ == "__main__":
    # Ensure the script is running from the 'earth-project' root
    if not os.path.exists('frontend') or not os.path.exists('backend'):
        print("ERROR: This script must be run from the root 'earth-project' folder.")
    else:
        create_handoff_file()