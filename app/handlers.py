import requests
import os

api_url = os.getenv("API_URL", "https://restcountries.com/v3.1")

def get_country(country):
    
    url = f"{api_url}/name/{country}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"message": f"The country '{country}' does not exist"}, 404

    try:
        json_data = response.json()
        translations = json_data[0].get('translations', {})
        spa = translations.get('spa', {})

        country_data = { 
            "nombre": spa.get('common', "No disponible"),
            "nombre_completo": spa.get('official', "No disponible"),
            "region": json_data[0].get('region', "No disponible"),
            "subregion": json_data[0].get('subregion', "No disponible"),
            "area": json_data[0].get('area', "No disponible"),
            "bandera": json_data[0].get('flags', {}).get('png', "No disponible"),
            "capital": ', '.join(json_data[0].get('capital', ["No disponible"]))   
        }
        return country_data
    except (IndexError, KeyError) as e:
        return {"message": "Unexpected error occurred while processing country data"}, 500
