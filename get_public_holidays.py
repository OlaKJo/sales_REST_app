# rest_app/app.py

import requests
import json
from os.path import exists

data_path = "data/helgdagar.json"


def get_helgdagar(path=data_path):
    if not exists(data_path):
        print("helgdagar api called")
        # api-endpoint
        # Really bad practice to have the client secret exposed in the code like this, not for production use!
        URL = "https://api.arbetsdag.se/v2/dagar.json?fran=2018-01-01&till=2018-12-31&key=v2yAkOeNIgvoqdriERZH3xtUBn91fpD08TubLX6z"

        # sending get request and saving the response as response object
        r = requests.get(url=URL)

        with open(path, 'w') as outfile:
            json.dump(r.json(), outfile)

        return r.json()
    else:
        print("helgdagar already exist")
        with open(path, 'r') as file:
            ret_json = json.load(file)

        return ret_json


def main():
        json_obj = get_helgdagar(data_path)
        print(json_obj['helgdagar'])


if __name__ == "__main__":
    main()
