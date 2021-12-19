# app.py
from flask import Flask, request, jsonify
import json



app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
def get_countries():
    return jsonify(countries)


@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415


@app.get('/countries/<country_id>')
def hello(country_id):
    return jsonify(countries[int(country_id)])


@app.get('/query/<json_string>')
def getJson(json_string):
    y = json.loads(json_string)

    # the result is a Python dictionary:
    the_id = y["id"]
    return jsonify(countries[int(the_id)])
