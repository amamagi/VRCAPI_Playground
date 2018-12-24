# coding: utf-8
import requests
import getpass
import json
from requests.auth import HTTPBasicAuth
import time
from datetime import datetime

# ---Need to fill in---
# VRC Config
USER     = "USERNAME"
PASSWORD = "PASSWORD"

# IFTTT Config
event = "IFTTT_EVENT"
key   = "IFTTT_KEY"
# ----------------------

# Init VRC API
API_BASE = "https://api.vrchat.cloud/api/1"

url = "{}/config".format(API_BASE)
response = requests.get(url)
apiKey = json.loads(response.text)["clientApiKey"]

url = "{}/auth/user".format(API_BASE)
response = requests.get(url, 
                        params={"apiKey": apiKey},
                        auth=HTTPBasicAuth(USER, PASSWORD))
token = response.cookies["auth"]

# Let's Just H!
JUST_WORLD_ID = "wrld_e0e29017-9061-432f-b3d7-b2005dc323fc"
url = "{}/worlds/{}".format(API_BASE, JUST_WORLD_ID)
response = requests.get(url, params={"apiKey": apiKey, "authToken": token})
previousPrivateOccupants = response.json()["privateOccupants"]

# Init IFTTT
ifttt_url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(event, key)
params = {"value1" : ""}

# TImer
base_time = time.time()
next_time = 0
interval = 60

# execute every minute until 2018/12/25 12:00
while int(datetime.now().strftime("%Y%m%d%H")) < 2018122512: 
    print("{} [GET]VRC".format(datetime.now()))
    try:
        response = requests.get(url, params={"apiKey": apiKey, "authToken": token})
        print("privateOccupants:{}".format(response.json()["privateOccupants"]))
        print(response)
    except Exception as e:
        print(e)
        
    currentPrivateOccupants = response.json()["privateOccupants"]
    diff = currentPrivateOccupants - previousPrivateOccupants
    
    if(diff < 0):
        previousPrivateOccupants = currentPrivateOccupants
    
    elif(diff > 1):
        previousPrivateOccupants = currentPrivateOccupants
        params["value1"] = currentPrivateOccupants
        
        
        print("[POST]IFTTT".format(datetime.now()))
        try:
            response = requests.post(ifttt_url, params=params)
            print(response)
        except Exception as e:
            print(e)
    
    next_time = ((base_time - time.time()) % interval) or interval
    time.sleep(next_time)

