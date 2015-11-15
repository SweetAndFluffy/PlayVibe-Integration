'''
Documentation, License etc.

@package PythonHostLib
'''

import ConfigParser
import json
import atexit
import time
import threading
import signal
import sys
import os
from threading import Thread

from VibratorManager import VibratorManager
from VibratorAdapter import VibratorAdapter
import GPIOController

config = ConfigParser.ConfigParser()
vibratorManager = VibratorManager()

update_intervall = 1
sequence_time = 120
bEnd = False
tThread = None

lLock = threading.Lock()

from flask import Flask
from flask import send_from_directory
app = Flask(__name__, static_url_path='/')
app._static_folder = os.path.dirname(os.path.realpath(__file__))

app.debug = False


@app.route("/points/<int:value>/")
def setPoints(value):
    global lLock
    lLock.acquire()
    vibratorManager.set_points(value)
    lLock.release()
    return "1"

@app.route("/points/")
def getPoints():
    global lLock
    lLock.acquire()
    points = vibratorManager.get_points()
    lLock.release()
    return str(points)

@app.route("/config/", methods=['GET'])
def getConfig():
    lLock.acquire()
    global config
    data = config.get("Vibrators", "data")
    return data

@app.route("/")
def getRoot():
    return app.send_static_file('frontend/index.html');

@app.route("/<path:path>")
def getFile(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory('frontend', path)

def readConfigFromFile():
    global config 
    config.read("playvibe_config.ini")
 
    if not config.has_section("Vibrators"):
        print("No vibrators were found in configuration!")
        print("A default vibrator will be created on pin 18.")
        
        config.add_section("Vibrators")
        config.set("Vibrators", "data", json.dumps([
            {'name': 'Default Vibrator', 'pin': 18, 'pwm': True, 'modes': [{'mode': 'ContinuousVibrations', 'min': 0, 'max': 100}]},
        ], indent=4, sort_keys=True))
        
    vibrators = config.get("Vibrators", "data")
    vibrators = json.loads(vibrators)
    
    global vibratorManager

    vibratorManager.clear()
    
    # Process available vibrators
    for vibe in vibrators:
        vibrator = VibratorAdapter(vibe)
        vibratorManager.add_vibe(vibrator)

def setConfig(configContent):
    global config
    config.set("Vibrators", "data", value=configContent)
    with open('playvibe_config.ini', 'w') as config_file:
        config.write(config_file)
    readConfigFromFile()

@app.route("/config/", methods=['POST'])
def setConfigOverHTTP():
    configData = request.form['json']
    setConfig(str(configData))

def start():
    print("Starting main logic.")
    lLock.acquire()
    # Parse the configuration
    print("Read config.")
    readConfigFromFile()

    lLock.release()
        
    try:
        print("Start the flask server")
        app.run(host='0.0.0.0')
    finally:
        end()
    
currentTime = 0
    
def periodicUpdate():
    global vibratorManager
    
    global currentTime
    
    lLock.acquire()

    vibratorManager.update_vibes(currentTime, sequence_time)
    currentTime += update_intervall
    if currentTime >= sequence_time:
        currentTime = 0

    lLock.release()

def periodicUpdateThread():
    print("Update worker has started!")
    while bEnd == False:
        periodicUpdate()
        time.sleep(update_intervall)

    print("Update worker has ended!")

def end():
    global config
    global bEnd
    global tThread
    bEnd = True
    print("Ending the program, write the configuration to a file")
    with open('playvibe_config.ini', 'w') as config_file:
        config.write(config_file)

    GPIOController.destroy()

if __name__ == "__main__":
    GPIOController.init()
    tThread = Thread(target=periodicUpdateThread)
    tThread.start()
    start()
    
