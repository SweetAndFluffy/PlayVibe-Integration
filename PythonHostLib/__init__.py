'''
Documentation, License etc.

@package PythonHostLib
'''

import ConfigParser
import json
import atexit
import time
import threading
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
app = Flask(__name__)

@app.route("/")
def hello():
    return "Vibrator Control Program"

@app.route("/points/<int:value>/")
def setPoints(value):
    global lLock
    lLock.acquire()
    vibratorManager.set_points(value)
    lLock.release()
    return "1"

@app.route("/config/", methods=['GET']):
def getConfig():
    lLock.acquire()
    global config
    with open('playvibe_config.ini', 'w') as config_file:
        config.write(config_file)
        data = config_file.read()
        return data
    return "No config file found!"

def readConfigFromFile():
    lLock.acquire()
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
    
    # Process available vibrators
    for vibe in vibrators:
        vibrator = VibratorAdapter(vibe)
        vibratorManager.add_vibe(vibrator)
    lLock.release()

def setConfig(configContent):
    with open('playvibe_config.ini', 'w') as config_file:
        config.write(config_file)
    readConfigFromFile()

@app.route("/config/", methods=['POST']):
def setConfigOverHTTP():
    configData = request.form['json']
    setConfig(str(configData))

def start():
    lLock.acquire()
    # Parse the configuration
    readConfigFromFile()
        
    app.run(host='0.0.0.0')
    
currentTime = 0
    
def periodicUpdate():
    global vibratorManager
    
    global currentTime
    
    vibratorManager.update_vibes(currentTime, sequence_time)
    currentTime += update_intervall
    if currentTime >= sequence_time:
        currentTime = 0

    lLock.release()

def periodicUpdateThread():
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

    tThread.terminate()
    GPIOController.destroy()


if __name__ == "__main__":
    print("STARTING UP")
    GPIOController.init()
    atexit.register(end)
    tThread = Thread(target=periodicUpdateThread)
    tThread.start()
    start()
    
