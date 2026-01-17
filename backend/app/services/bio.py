from pydantic import BaseModel

class BioRisk(BaseModel):
    risk_level: str   # Low, Moderate, High, Critical
    vector: str       # Mosquitoes, Bacteria (Cholera), Heat Stress
    message: str
    prevention: str   # "Sleep under nets", "Boil water"

async def analyze_biological_risk(temp: float, rain_7day: float):
    """
    The 'Bio-Shield' Logic:
    Correlates weather conditions with disease outbreak probability.
    """
    # 1. MALARIA / DENGUE (Mosquitoes)
    # Logic: Standing water (Rain > 20mm) + Warmth (> 23°C) = Breeding
    if rain_7day > 20 and temp > 23:
        return BioRisk(
            risk_level="HIGH",
            vector="Mosquito-Borne Disease",
            message="Conditions are optimal for mosquito breeding (Warm + Wet).",
            prevention="Use treated nets tonight. Clear standing water."
        )

    # 2. CHOLERA / TYPHOID (Waterborne)
    # Logic: Heavy floods (> 80mm) mix sewage with drinking water.
    if rain_7day > 80:
        return BioRisk(
            risk_level="CRITICAL",
            vector="Waterborne Contamination",
            message="Heavy rainfall may contaminate local wells and taps.",
            prevention="Boil ALL drinking water. Avoid raw vegetables."
        )

    # 3. HEAT STRESS (Human Biology)
    # Logic: Temp > 32°C affects cognitive function.
    if temp > 32:
        return BioRisk(
            risk_level="MODERATE",
            vector="Heat Stroke",
            message="Extreme heat affecting physical safety.",
            prevention="Hydrate immediately. Avoid midday sun."
        )

    # 4. DEFAULT (Safe)
    return BioRisk(
        risk_level="LOW",
        vector="None",
        message="Biological conditions are stable.",
        prevention="Maintain standard hygiene."
    )