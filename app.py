# app.py
from flask import Flask, request, jsonify, render_template
import json
import sqlite3

import sql_queries

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('data/sales_test.db')
    #conn.row_factory = sqlite3.Row
    return conn

@app.get('/query')
def test_query():
    conn = get_db_connection()
    cur = conn.cursor()
    posts = cur.execute('SELECT * FROM store_cities').fetchall()
    conn.close()
    return jsonify(posts);


def get_db_query(conn, request_json):
    json_dict = json.loads(request_json)
    print(json_dict)
    print(type(json_dict))

    # hierarchy1_id, date range -> total sales quantity and revenue
    if "hierarchy1_id" in json_dict :
        print("hierarchy request received")
        query = sql_queries.hier_rev.format(json_dict["hierarchy1_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        retString = {"Quantity": posts[0][0], "Revenue": posts[0][1]}

        return retString

    # city id, date range -> total sales quantity and revenue
    elif "city_id" in json_dict:
        print("city_id request received")
        query = sql_queries.city_rev.format(json_dict["city_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        retString = {"Quantity": posts[0][0], "Revenue": posts[0][1]}

        return retString

    # product_id, date range -> total volume
    elif "product_id" in json_dict:
        print("product_id request received")
        query = sql_queries.volume.format(json_dict["product_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        retString = {"TotalVolume": posts[0][0]}

        return retString

    # (2018 public holiday dates in Sweden -> total revenue)
    elif "country" in json_dict:
        print("city_id request received")
    else:
        print("No matching request type")
        return "Record not found", 400


@app.get('/query/<request_json>')
def json_query(request_json):
    print(request_json)

    conn = get_db_connection()
    response = get_db_query(conn, request_json)
    conn.close()
    return jsonify(response)


#@app.get('/countries/<country_id>')
#def hello(country_id):
#    return jsonify(countries[int(country_id)])
#
#
@app.get('/test/<json_string>')
def getJson(json_string):
    y = json.loads(json_string)

    # the result is a Python dictionary:
    the_id = y["id"]
    return jsonify({"idWas": the_id})
