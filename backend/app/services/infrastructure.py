from pydantic import BaseModel

class InfraStatus(BaseModel):
    power_grid_risk: str  # "Stable", "High Risk", "CRITICAL"
    road_network_risk: str
    internet_risk: str
    message: str

async def analyze_vital_lines(wind_speed: float, rain_sum: float, soil_moisture: float, solar_kp: float):
    """
    Predicts infrastructure failure based on environmental stress.
    """
    # 1. POWER GRID (Vulnerable to High Wind & Trees)
    power = "Stable"
    if wind_speed > 90: power = "CRITICAL (Line Collapse)"
    elif wind_speed > 60: power = "High Risk (Tree Fall)"
    
    # 2. ROAD NETWORK (Vulnerable to Rain + Saturated Soil)
    roads = "Clear"
    # If soil is wet (>0.35) AND rain is heavy (>30mm), floods happen fast
    if soil_moisture > 0.35 and rain_sum > 30: 
        roads = "CRITICAL (Flash Floods)"
    elif rain_sum > 50: 
        roads = "High Risk (Hydroplaning)"
    elif rain_sum > 15: 
        roads = "Moderate (Slippery)"

    # 3. INTERNET/GPS (Vulnerable to Solar Storms)
    net = "Optimal"
    if solar_kp >= 7: net = "Blackout (Satellite Loss)"
    elif solar_kp >= 5: net = "Degraded (GPS Drift)"

    # Summary Message
    msg = "All vital systems operational."
    if "CRITICAL" in power:
        msg = "URGENT: Power grid failure imminent. Charge devices now."
    elif "CRITICAL" in roads:
        msg = "URGENT: Roads may become impassable. Avoid travel."
    elif "High" in power or "High" in roads:
        msg = "Infrastructure stress detected. Prepare for outages."
    
    return InfraStatus(
        power_grid_risk=power,
        road_network_risk=roads,
        internet_risk=net,
        message=msg
    )