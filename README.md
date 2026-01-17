# 🌍 EARTH: The Planetary Intelligence Platform

![License](https://img.shields.io/badge/license-GPLv3-blue.svg) ![Python](https://img.shields.io/badge/python-3.11-yellow.svg) ![Status](https://img.shields.io/badge/status-Prototype-green.svg)

> **"We don't just show you the weather; we tell you how to survive it."**

**EARTH** is a mission-critical intelligence system designed to bridge the gap between scientific data and human safety. While standard apps display raw numbers, EARTH fuses **Atmospheric**, **Oceanographic**, and **Space Weather** data into a single, actionable risk score for protecting power grids, road networks, and vulnerable communities.

---

## 🆚 Why EARTH is Different (The "Action Gap")

Most weather apps are passive. EARTH is active. Here is how we lead the market:

| Feature 🚀 | Standard Weather Apps ☁️ | EARTH Platform 🛡️ |
| :--- | :--- | :--- |
| **Data Logic** | Displays raw numbers (e.g., "40km/h Wind") | **Infrastructure Oracle**: Translates numbers into physical risks (e.g., "Grid Stress Warning") |
| **Offline Access** | ❌ Fails without Internet (Blank Screen) | ✅ **Ark Protocol**: Auto-switches to SMS alerts when internet fails |
| **Data Scope** | Single Domain (Atmosphere only) | **Multi-Domain Fusion**: Atmosphere + Ocean + Space Weather + Land (GEE) |
| **User Focus** | General Public (Passive) | **Decision Makers**: Utility Managers, Disaster Response, & At-Risk Communities |
| **Resilience** | Crashes on weak connections | **Zero-Fail Architecture**: Loads in <2s on 2G networks |

---

## ⚡ Key Features

### 1. 🧠 The Infrastructure Oracle
We moved beyond "forecasts." Our proprietary logic engine (`infra.py`) continuously cross-references meteorological thresholds against physical infrastructure limits.
* **Grid Watch:** Predicts power line failures by analyzing Heat + Wind stress.
* **Road Guard:** correlates soil moisture saturation with rainfall to predict flash floods *before* rain hits the ground.

### 2. 📡 The Ark Protocol (Offline Equity)
Disasters don't wait for Wi-Fi.
* **Dead Man's Switch:** If the system detects a high-probability threat (>80%) and the user is offline, it bypasses the app entirely.
* **SMS Fallback:** Delivers critical text-only warnings via a low-bandwidth gateway.

### 3. 🛰️ Planetary Data Fusion
We break down scientific silos. EARTH aggregates:
* **Space Weather:** Solar flare tracking for GPS/Radio safety.
* **Ocean Intelligence:** Wave physics and "Sea State" safety scores.
* **Google Earth Engine:** Real-time Vegetation Health Index (VHI) analysis.

---

## 🛠️ Tech Stack & Architecture

We built a **Microservices-First** architecture designed for chaos.

* **Brain (Backend):** Python 3.11, FastAPI (Async/Await for parallel fetching).
* **Eyes (Satellite Analysis):** Google Earth Engine (GEE) Python API.
* **Face (Frontend):** Vanilla JavaScript (ES6+), HTML5, CSS3 (Optimized for low-bandwidth).
* **Security:** Firebase Authentication & Environment Variable Isolation.

---

## 🚀 How to Run Locally

Follow these steps to deploy the "Situation Room" on your local machine.

### Prerequisites
* Python 3.10+
* A Google Earth Engine Account
* Firebase Project Credentials

### 1. Clone the Repo
```bash
git clone [https://github.com/Collistus-Kibe/Earth.git](https://github.com/Collistus-Kibe/Earth.git)
cd Earth
