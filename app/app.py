import handlers
from flask import Flask, request, jsonify 
import os
import psycopg2

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
    data = handlers.get_country(country_code)    
    return jsonify(data)

@app.route('/save/<string:country_code>', methods=['POST'])
def save_country(country_code):
    data = handlers.get_country(country_code)
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO countries (nombre, nombre_completo, region, subregion, area, bandera, capital) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['nombre'], data['nombre_completo'], data['region'], data['subregion'], data['area'], data['bandera'], data['capital'])
        )
        conn.commit()

        return jsonify({"message": "success"}, data), 201
    except Exception as e:
        return jsonify({"message": "error"}), 500

@app.route('/delete/<string:country_code>', methods=['DELETE'])
def delete_country(country_code):
    try:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM countries WHERE nombre = %s',
            (country_code)
        )
        conn.commit()
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": "error"}), 500

@app.route('/list', methods=['GET'])
def list_countries():
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM countries'
        )
        countries = cursor.fetchall()
        return jsonify(countries), 200
    except Exception as e:
        return jsonify({"message": "error"}), 500

@app.route('/detail/<string:country_code>', methods=['GET'])
def detail_country(country_code):
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM countries WHERE nombre = %s',
            (country_code)
        )
        country = cursor.fetchone()
        return jsonify(country), 200
    except Exception as e:
        return jsonify({"message": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)