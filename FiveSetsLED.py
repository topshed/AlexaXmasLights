from flask import Flask, jsonify, abort
from flask import request
import threading
import colorsys
import time
from gpiozero import PWMLED
from random import randint
from gpiozero.tools import random_values,sin_values, scaled, cos_values,inverted

cols1 = PWMLED(14) # string of coloured LEDs
tree = PWMLED(8) # green tree-shaped LEDs
warm=PWMLED(25) # warm white LEDs
balls=PWMLED(23) # big bright white balls
snow=PWMLED(4) # snowflakes
cols2=PWMLED(7) # string of coloured LEDs

all_lights=[cols1,tree,warm,balls,snow,cols2]

def lightson():
    for l in range(len(all_lights)):
        all_lights[l].on()
    time.sleep(1)
    for l in range(len(all_lights)):
        all_lights[l].off()

def lightsoff():
    for l in range(len(all_lights)):
        all_lights[l].off()

def winkingling(iterations):
        for l in range(len(all_lights)):
            all_lights[l].on()
        i=0
        while i < iterations:
            turn_off = randint(0,5)
            turn_on = randint(0,5)
            while all_lights[turn_off].is_lit == False and all_lights[turn_on].is_lit == True:
                turn_off = randint(0,5)
                turn_on = randint(0,5)
            all_lights[turn_off].off()
            all_lights[turn_on].on()
            time.sleep(0.5)
            i+=1

def candle(t):
    for i  in range(6):
        all_lights[i].source = random_values()
    time.sleep(t)
    for i  in range(6):
        all_lights[i].source = None

def pulsator(n):
    for i  in range(6):
        all_lights[i].pulse(fade_in_time=2, fade_out_time=2,n=n,background=True)
    time.sleep(12)

def trig():
    warm.source_delay = 0.01
    snow.source_delay = warm.source_delay
    tree.source_delay = snow.source_delay
    warm.source = scaled(sin_values(100), 0, 1, -1, 1)
    snow.source = inverted(warm.values)
    tree.source = scaled(cos_values(100), 0,1,-1,1)
    cols2.source = inverted(tree.source)
    time.sleep(10)
    snow.source = None
    warm.source = None
    tree.source = None
    cols2.source = None

def rainbow():
    print('starting')
    global running
    running = True
    while running:
        trig()
        if running: # check we haven't been stopped
            winkingling(10)
        if running:
            candle(5)
        if running:
            pulsator(10)
    lightsoff()

app = Flask(__name__)


@app.route('/todo/api/v1.0/lightson', methods=['POST'])
def turnon():
    t = threading.Thread(target=rainbow)
    t.start()


    return jsonify({'action': 'on'}), 201

@app.route('/todo/api/v1.0/lightsoff', methods=['POST'])
def turnoff():
    global running
    running = False

    return jsonify({'action': 'off'}), 201

# TODO : add code to select different lighting sequence
@app.route('/todo/api/v1.0/lightsseq', methods=['POST'])
def dim():
    if requset.json == '1':
        pass
    elif request.json == '2':
        pass
    else:
        pass

    return jsonify({'action': 'off'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
