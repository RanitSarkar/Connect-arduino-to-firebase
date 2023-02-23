from typing import Any
import serial
import time as t
import firebase_admin
from firebase_admin import credentials,db
import json


def _authenticate():
    cred = credentials.Certificate("local/cred.json") #add your credential file from firebase
    firebase_admin.initialize_app(cred, {'databaseURL': 'your_site_link'})


def read_data():
    with open("data/data.json", "r") as f:
        data = json.load(f)
    return data


_authenticate()
db = db.reference("/Users")


def save():
    data = read_data()
    db.set(data)

SerialObj = serial.Serial('COM8') #add your the COM from device manager
SerialObj.baudrate = 9600
SerialObj.flushInput()

flowRate_list = []
tml_list = []
totalMilliLitres = 0


while True:
    flowRate = int(SerialObj.readline())
    flowMilliLitres = (flowRate / 60) * 1000
    totalMilliLitres += flowMilliLitres
    totalMilliLitres = int(totalMilliLitres)
    dic = {
        "flow_rate": flowRate,
        "ml": totalMilliLitres
    }

    with open("data/data.json", "w") as f:
        json.dump(dic, f)

    save()






