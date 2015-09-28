'''
Documentation, License etc.

@package PythonHostLib
'''

import configparser
import json
import atexit
import time
import sched

from . import VibratorManager
from . import VibratorAdapter

config = configparser.ConfigParser()
vibratorManager = VibratorManager.VibratorManager()

update_intervall = 1
sequence_time = 120

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Vibrator Control Program"

@app.route("/points/<int:value>/")
def setPoints(value):
    vibratorManager.set_points(value)
    return "1"

def start():
    # Parse the configuration
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
        vibratorManager.add_vibe(vibe)
        
    app.debug = True
    app.run(host='0.0.0.0')
    
currentTime = 0
s = sched.scheduler(time.time, time.sleep)
    
def periodicUpdate(sc):
    global vibratorManager
    
    global currentTime
    
    sc.enter(update_intervall, 1, periodicUpdate, (sc,))
    
    vibratorManager.update_vibes(currentTime, sequence_time)
    currentTime += update_intervall
    
    print("Hello!")
    
    if currentTime >= sequence_time:
        currentTime = 0

def end():
    global config
    print("Ending the program, write the configuration to a file")
    with open('playvibe_config.ini', 'w') as config_file:
        config.write(config_file)

if __name__ == "__main__":
    print("STARTING UP")
    s.enter(update_intervall, 1, periodicUpdate, (s,))
    s.run(blocking=False)
    start()
    atexit.register(end)
    
