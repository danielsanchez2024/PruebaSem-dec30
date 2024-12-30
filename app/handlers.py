import requests
import json
def get_country(country):
    Url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(Url)

    if response.status_code != 200:
        return {"message": "does not exist", "country": country}, 404
    
    json_data = response.json()
    translations = json_data[0] ['translations'] 
    spa = translations.get('spa', {})

    country_data = { 
        "nombre": spa.get('common', {}),
        "nombre_completo": spa.get('official', {}),
        "region": json_data[0]['region'],
        "subregion": json_data[0]['subregion'],
        "area": json_data[0]['area'],
        "bandera": json_data[0]['flags']['png'],
        "capital": ''.join(json_data[0]['capital'])   
    }
    return country_data