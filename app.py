# rest_app/app.py
from flask import Flask, jsonify
import json
import sqlite3
import get_public_holidays
import sql_queries

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('data/sales.db')
    # conn.row_factory = sqlite3.Row
    return conn


def query_db(conn, request_json):
    json_dict = json.loads(request_json)
    print(json_dict)
    print(type(json_dict))

    # TODO: Refactor the below code to reduce duplicate code.

    # hierarchy1_id, date range -> total sales quantity and revenue
    if "hierarchy1_id" in json_dict:
        print("hierarchy request received")
        query = sql_queries.hier_rev.format(json_dict["hierarchy1_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        ret_string = {"Quantity": posts[0][0], "Revenue": posts[0][1]}

        return ret_string

    # city id, date range -> total sales quantity and revenue
    elif "city_id" in json_dict:
        print("city_id request received")
        query = sql_queries.city_rev.format(json_dict["city_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        ret_string = {"Quantity": posts[0][0], "Revenue": posts[0][1]}

        return ret_string

    # product_id, date range -> total volume
    elif "product_id" in json_dict:
        print("product_id request received")
        query = sql_queries.volume.format(json_dict["product_id"], json_dict["start_date"], json_dict["end_date"])
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        ret_string = {"TotalVolume": posts[0][0]}

        return ret_string

    # (2018 public holiday dates in Sweden -> total revenue)
    elif "holidays" in json_dict:
        print("holiday revenue request received")

        # Create holiday table and add to db
        holidays_json = get_public_holidays.get_helgdagar()
        print(holidays_json)

        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS public_holidays''')
        cur.execute('''CREATE TABLE IF NOT EXISTS public_holidays(holiday_name,date)''')

        # return holidays_json

        for entry in holidays_json:
            print(entry['datum'])
            cur.execute("INSERT INTO public_holidays(holiday_name, date) VALUES(?, ?)",
                        (entry['helgdag'], entry['datum']))

        # perform db query to get total revenue on public holidays
        query = sql_queries.holidays
        cur = conn.cursor()

        print("query calculated")
        print(query)

        cur.executescript(query)
        posts = cur.execute("SELECT * FROM resultTable").fetchall()
        ret_string = {"TotalVolume": posts[0][0]}

        return ret_string

    else:
        print("No matching request type")
        return "Record not found", 400


@app.get('/query/<request_json>')
def json_query(request_json):
    print(request_json)

    conn = get_db_connection()
    response = query_db(conn, request_json)
    conn.close()
    return jsonify(response)
