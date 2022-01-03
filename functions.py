import nxt.locator
import nxt.motor
import nxt.sensor.generic

import math
import time

from bluetooth.btcommon import BluetoothError

def connect(address):
    global brick
    global mB; global mC
    global s1; global s2; global s3; global s4
    global tempo
    global my_address
    try:
        #address = {2: '00:16:53:0A:9B:72', \
		#   3: '00:16:53:0A:9D:F2', \
		#   4: '00:16:53:0A:5C:72', 
		#   5: '00:16:53:08:D5:59', \
		#   6: '00:16:53:08:DE:51', \
		#   7: '00:16:53:0A:5A:B4', \
		#   8: '00:16:53:0A:9B:27', \
		#   9: '00:16:53:0A:9E:2C', \
		#  10: '00:16:53:17:92:8A', \
		#  11: '00:16:53:17:94:E0', \
		#  12: '00:16:53:1A:C6:BD'}
        brick = nxt.locator.find(host=address)
        my_address = address
        mB = nxt.motor.Motor(brick, nxt.motor.Port.B)
        mC = nxt.motor.Motor(brick, nxt.motor.Port.C)
        s1 = nxt.sensor.generic.Touch(brick, nxt.sensor.Port.S1)
        s2 = nxt.sensor.generic.Sound(brick, nxt.sensor.Port.S2)
        # s2.set_input_mode(0x08,0x80) # dB adjusted, percentage
        s3 = nxt.sensor.generic.Light(brick, nxt.sensor.Port.S3)
        s3.set_illuminated(True)
        # s3.set_input_mode(0x05,0x80) # Light active, percentage
        s4 = nxt.sensor.generic.Ultrasonic(brick, nxt.sensor.Port.S4)
        tempo = 0.5
        print("\x1b[32mRobot connectat.\x1b[0m")
    except BluetoothError as e:
        errno, errmsg = eval(e.args[0])
        if errno==16:
            print("\x1b[31mNo es pot connectar, hi ha un altre programa ocupant la connexió.\x1b[0m")
        elif errno==13:
            print("\x1b[31mNo es pot connectar, el dispositiu no està emparellat.\x1b[0m")
        elif errno == 112:
            print("\x1b[31mNo es troba el brick, assegurat que estiga encés.\x1b[0m")
        else:
            print("Error %d: %s" % (errno, errmsg))
    except KeyError:
        print("\x1b[31mNúmero de robot incorrecte.\x1b[0m")

def disconnect():
    try:
        brick.close()
        print("\x1b[32mRobot desconnectat.\x1b[0m")
    except NameError:
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")

def stop():
    try:
        mB.idle()
        mC.idle()
    except NameError:
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")

def forward(speed=50,speed_B=50,speed_C=50):
    move(speed_B=min(abs(speed),abs(speed_B)),speed_C=min(abs(speed),abs(speed_C)))
    
def backward(speed=50,speed_B=50,speed_C=50):
    move(speed_B=-min(abs(speed),abs(speed_B)),speed_C=-min(abs(speed),abs(speed_C)))
    
def right(speed=50):
    move(speed_B=abs(speed),speed_C=0)

def right_sharp(speed=50):
    move(speed_B=abs(speed),speed_C=-abs(speed))
       
def left(speed=50):
    move(speed_B=0,speed_C=abs(speed))

def left_sharp(speed=50):
    move(speed_B=-abs(speed),speed_C=abs(speed))

def move(speed_B=0,speed_C=0):
    max_speed = 100
    speed_B = int(speed_B)
    speed_C = int(speed_C)
    if speed_B > 100:
        speed_B = 100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    if speed_B < -100:
        speed_B = -100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    if speed_C > 100:
        speed_C = 100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    if speed_C < -100:
        speed_C = -100
        print("\x1b[33mLa velocitat màxima és 100.\x1b[0m")
    try:
        mB.run(int(speed_B*max_speed/100), True)
        mC.run(int(speed_C*max_speed/100), True)
    except NameError:
        print("\x1b[31mNo hi ha connexió amb el robot.\x1b[0m")

def touch():
    return s1.is_pressed()
    
def sound():
    return int(s2.get_loudness() * 100 / 1023)

def light():
    return min(100,int(s3.get_lightness() * 100 / 600))

from nxt.error import ProtocolError

def ultrasonic():
    global s4
    try:
        return s4.get_distance()
    except KeyboardInterrupt:
    	return 255
    except ProtocolError:
        disconnect()
        print("\x1b[33mError de connexió, reintentant...\x1b[0m")
        time.sleep(1)
        connect(my_address)
        return s4.get_distance()
        
def play_sound(s):
    brick.play_sound_file(False, bytes((s+'.rso').encode('ascii')))

def say(s):
    play_sound(s)

def play_tone(f,t):
    try:
        brick.play_tone_and_wait(f, int(t*1000*tempo))
        time.sleep(0.01)
    except:
        pass

from IPython.display import clear_output

def read_and_print(sensor):
    try:
        while True:
            clear_output(wait=True)
            print(sensor())
    except KeyboardInterrupt:
        pass
    
def test_sensors():
    try:
        while True:
            clear_output(wait=True)
            print("     Touch: %d\n     Light: %d\n     Sound: %d\nUltrasonic: %d" % (touch(),light(),sound(), ultrasonic()))
    except KeyboardInterrupt:
        pass
    
import matplotlib.pyplot as plt

def plot(l):
    plt.plot(l)
    
