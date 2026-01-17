import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

# GBIF Occurrence Search API
GBIF_API_URL = "https://api.gbif.org/v1/occurrence/search"

class SpeciesInfo(BaseModel):
    scientific_name: str
    kingdom: str
    risk_category: str  # e.g., "CR" (Critically Endangered)

class EcoData(BaseModel):
    is_sensitive_area: bool
    endangered_count: int
    nearby_species: List[SpeciesInfo]
    message: str

async def check_biodiversity_risk(lat: float, lon: float) -> EcoData:
    """
    Checks if the location is within a 'Biodiversity Hotspot' by searching
    for IUCN Red List 'Critically Endangered' (CR) species within ~5km.
    """
    # Create a rough bounding box (~0.05 degrees is approx 5km at equator)
    min_lat, max_lat = lat - 0.05, lat + 0.05
    min_lon, max_lon = lon - 0.05, lon + 0.05
    
    # Query GBIF:
    # - hasCoordinate=true (must have location)
    # - iucnRedListCategory=CR (Critically Endangered)
    # - limit=5 (We only need a few examples to prove sensitivity)
    params = {
        "decimalLatitude": f"{min_lat},{max_lat}",
        "decimalLongitude": f"{min_lon},{max_lon}",
        "iucnRedListCategory": "CR", 
        "hasCoordinate": "true",
        "limit": 5
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GBIF_API_URL, params=params)
            
            # GBIF returns 200 even for empty searches, but we check anyway
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="GBIF API error")
                
            data = response.json()
            count = data.get("count", 0)
            results = data.get("results", [])
            
            species_list = []
            seen_species = set()

            for record in results:
                name = record.get("scientificName", "Unknown Species")
                # Simple deduplication
                if name not in seen_species:
                    species_list.append(SpeciesInfo(
                        scientific_name=name,
                        kingdom=record.get("kingdom", "Unknown"),
                        risk_category="Critically Endangered"
                    ))
                    seen_species.add(name)

            is_sensitive = count > 0
            
            msg = "No immediate ecological concerns detected."
            if is_sensitive:
                msg = f"Eco-Alert: This area is a habitat for {count} critically endangered species occurrences."

            return EcoData(
                is_sensitive_area=is_sensitive,
                endangered_count=count,
                nearby_species=species_list,
                message=msg
            )

        except httpx.RequestError as e:
            print(f"GBIF Connection Error: {e}")
            # Fail safe: return clean data rather than crashing the dashboard
            return EcoData(
                is_sensitive_area=False, 
                endangered_count=0, 
                nearby_species=[], 
                message="Could not verify biodiversity data."
            )