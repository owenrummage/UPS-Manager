import datetime
import json
from flask import Flask, render_template
from nut2 import PyNUTClient
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

json_data = """ 
[ 
    
    {"name": "network_ups", "charge": 82, "load": 455, "state": "OL-CHG" , "runtime": 1200}, 
    {"name": "prod_ups", "charge": 100, "load": 278, "state": "OL-CHD", "runtime": 3470 }

]
"""

apc_units = json.loads(json_data)


def getUnits():
    client = PyNUTClient(host=os.getenv("HOST"))
    return client.list_ups()


def getUPSValues(name):
    client = PyNUTClient(host=os.getenv("HOST"))

    try:
        if client.list_vars(name).get("output.voltage") is None:
            print("Device {name} does not support OUTPUT values".format(name=name))
            return {
                "name": name, 
                "runtime": int(client.list_vars(name).get("battery.runtime")),
                "load": False,
                "charge": int(client.list_vars(name).get("battery.charge")),
                "status": client.list_vars(name).get("ups.status")
            }
        else:                 
            return {
                "name": name, 
                "runtime": int(client.list_vars(name).get("battery.runtime")),
                "load": float(client.list_vars(name).get("output.voltage"))*float(client.list_vars(name).get("output.current")),
                "charge": int(client.list_vars(name).get("battery.charge")),
                "status": client.list_vars(name).get("ups.status")
            }
    except Exception as error:
        print(error)
        print("Feces has impacted the wind circulation device for " + name)



@app.route('/')
def hello():
    units = []
    metrics = {
        "totalUsage": 0,
        "runtime": 0,
        "charge": 0
    }

    for i in getUnits():
        values = getUPSValues(i)

        metrics["totalUsage"] = metrics["totalUsage"] + values.get("load")
        metrics["charge"] = metrics["charge"] + values.get("charge")

        units.append(values)

    metrics["charge"] = metrics["charge"] / len(units)
    units.sort(reverse=False, key=lambda unit: unit["runtime"])
    metrics["runtime"] = units[0]["runtime"]

    return render_template('index.html', units=units, metrics=metrics)


if __name__ == "__main__":
    if os.getenv("DEBUG") == "true":
        app.run(port=8000, debug=True)
    else:
        app.run(port=8000)