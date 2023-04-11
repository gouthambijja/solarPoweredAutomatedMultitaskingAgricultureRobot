# Simple HTTP Server Example
# Control an LED and read a Button using a web browser

import time
import utime
import network
import socket
import _thread
from machine import Pin
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#lcd setup
I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1,sda = machine.Pin(14),scl = machine.Pin(15),freq = 400000)
lcd = I2cLcd(i2c,I2C_ADDR, I2C_NUM_ROWS,I2C_NUM_COLS)


#pin setup
led = Pin(2, Pin.OUT)
m1cw = Pin(3,Pin.OUT)
m1acw = Pin(4,Pin.OUT)
m2cw = Pin(5,Pin.OUT)
m2acw = Pin(6,Pin.OUT)
gcutter = Pin(7,Pin.OUT)
plougherDown = Pin(8,Pin.OUT)
plougherUp = Pin(16,Pin.OUT)
ssower = Pin(9,Pin.OUT)
trigger = Pin(10,Pin.OUT)
echo = Pin(11,Pin.OUT)
gcutter.value(0)
ipAdd=''

ssid = 'Goutham'
password = 'KakaRot@8897139849'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html lang="en">
<head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SPAMAR</title>
</head>
<body>
      %s  
</body>
<script>{window.onload = (event) => {let new_window =open(location, '_self');new_window.close();};}
</script>
</html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    ipAdd = status[0]
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(status[0])

    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

#global variables
automatic_flag = 0



def ultra():
   print("hello")
   if automatic_flag:
       trigger.low()
       utime.sleep_us(2)
       trigger.high()
       utime.sleep_us(5)
       trigger.low()
       print('ehlo')
       while echo.value() == 0:
           signaloff = utime.ticks_us()
       while echo.value() == 1:
           signalon = utime.ticks_us()
       print('eho')
       timepassed = signalon - signaloff
       distance = (timepassed * 0.0343) / 2
       print(distance)
       return distance
    
def move():
    print("helo")
    rotation=0
    direction_change = 0
    print(automatic_flag)
    while(automatic_flag):
        if(direction_change == 1):
            time.sleep(8.2)
        else:
            time.sleep(1)
        distance = ultra()
        print(distance)
        if(distance > 50):
            direction_change = 0
            print('forward')
            m1acw.value(0)
            m1cw.value(1)
            m2acw.value(0)
            m2cw.value(1)
        else:
            direction_change = 1
            if(rotation):
                print('left')
                m1acw.value(0)
                m1cw.value(0)
                m2cw.value(1)
                m2acw.value(0)
                rotation = 0
            else:
                print('right')
                m1acw.value(0)
                m1cw.value(1)
                m2cw.value(0)
                m2acw.value(0)
                rotation=1

# Listen for connections, serve client
while True:
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        grasscutter_on = request.find('grasscutter=on')
        grasscutter_off = request.find('grasscutter=off')
        plougher_on = request.find('plougher=on')
        plougher_off = request.find('plougher=off')
        seedsower_on = request.find('seedsower=on')
        seedsower_off = request.find('seedsower=off')
        forward = request.find('direction=forward')
        backward = request.find('direction=backward')
        right = request.find('direction=right')
        left = request.find('direction=left')
        stop = request.find('direction=stop')
        automatic = request.find('motioncontrol=on')
        automaticoff = request.find('motioncontrol=off')
        if automatic == 8:
            automatic_flag=1
            led.value(1)
        elif automaticoff == 8:
            automatic_flag=0
            led.value(0)
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        
        if led_on == 8:
            print("led on")
            led.value(1)
        elif led_off == 8:
            print("led off")
            led.value(0)
        elif grasscutter_on == 8:
            gcutter.value(0)
        elif grasscutter_off == 8:
            gcutter.value(1)
        elif plougher_on == 8:
            plougherDown.value(1)
            time.sleep(0.5)
            plougherDown.value(0)
        elif plougher_off == 8:
            plougherUp.value(1)
            time.sleep(0.5)
            plougherUp.value(0)
        elif seedsower_on == 8:
            ssower.value(1)
        elif seedsower_off == 8:
            ssower.value(0)
        elif forward == 8:
            print("forward");
            m1acw.value(0)
            m1cw.value(1)
            m2acw.value(0)
            m2cw.value(1)
        elif backward == 8:
            m1cw.value(0)
            m2cw.value(0)
            m1acw.value(1)
            m2acw.value(1)
        elif right == 8:
            m1acw.value(0)
            m1cw.value(1)
            m2cw.value(0)
            m2acw.value(0)
        elif left == 8:
            m1cw.value(0)
            m2acw.value(0)
            m1acw.value(0)
            m2cw.value(1)
        elif stop == 8:
            m1cw.value(0)
            m2acw.value(0)
            m1acw.value(0)
            m2cw.value(0)
        elif automatic_flag:
            _thread.start_new_thread(move,())
        elif automatic_flag == 0:
            print("heelo")
            m1cw.value(0)
            m2acw.value(0)
            m1acw.value(0)
            m2cw.value(0)
            
        
            
        # Create and send response
        stateis = ipAdd 
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')

