import handlers
from flask import Flask, jsonify
import os
import psycopg2.extras

PG_HOST = os.environ['PG_HOST']
PG_PORT = int(os.environ['PG_PORT'])
PG_USER = os.environ['PG_USER']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_DB = os.environ['PG_DB']

conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    database=PG_DB
)


app = Flask(__name__)

@app.route('/search/<string:country_code>', methods=['GET'])
def country(country_code):
    try:
        data = handlers.get_country(country_code)
        
        if isinstance(data, tuple) and data[1] == 404:
            return jsonify({"message": f"The country '{country_code}' does not exist"}), 404
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500


@app.route('/save/<string:country_code>', methods=['POST'])
def save_country(country_code):
    try:
        data = handlers.get_country(country_code)

        if isinstance(data, tuple) and data[1] == 404:
            return jsonify({"message": f"The country '{country_code}' does not exist"}), 404

        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO countries 
            (nombre, nombre_completo, region, subregion, area, bandera, capital) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''',
            (
                data.get('nombre', 'No disponible'),
                data.get('nombre_completo', 'No disponible'),
                data.get('region', 'No disponible'),
                data.get('subregion', 'No disponible'),
                data.get('area', 0),
                data.get('bandera', 'No disponible'),
                data.get('capital', 'No disponible')
            )
        )
        conn.commit()

        return jsonify({"message": "Country saved successfully", "data": data}), 201
    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500


@app.route('/delete/<string:country_code>', methods=['DELETE'])
def delete_country(country_code):
    try:
        cursor = conn.cursor()
        
        cursor.execute(
            'DELETE FROM countries WHERE nombre = %s',
            (country_code,)  
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": f"The country '{country_code}' does not exist"}), 404

        return jsonify({"message": f"The country '{country_code}' was successfully deleted"}), 200
    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500





@app.route('/list', methods=['GET'])
def list_countries():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  
        cursor.execute('SELECT * FROM countries')
        countries = cursor.fetchall()

        if not countries:
            return jsonify([]), 200

        formatted_countries = [
            {
                "nombre": country["nombre"],
                "nombre_completo": country["nombre_completo"],
                "region": country["region"],
                "subregion": country["subregion"],
                "area": country["area"],
                "bandera": country["bandera"],
                "capital": country["capital"]
            }
            for country in countries
        ]

        return jsonify(formatted_countries), 200

    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500



@app.route('/detail/<string:country_code>', methods=['GET'])
def detail_country(country_code):
    try:

        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            'SELECT * FROM countries WHERE nombre = %s',
            (country_code,)
        )
        country = cursor.fetchone()

        if country is None:
            return jsonify({"message": f"Country {country_code} not found"}), 404

        country_data = {
            "nombre": country.get("nombre", ""),
            "nombre_completo": country.get("nombre_completo", ""),
            "region": country.get("region", ""),
            "subregion": country.get("subregion", ""),
            "area": country.get("area", ""),
            "bandera": country.get("bandera", ""),
            "capital": country.get("capital", "")
        }

        return jsonify(country_data), 200
    except Exception as e:
        return jsonify({"message": "error", "details": str(e)}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)