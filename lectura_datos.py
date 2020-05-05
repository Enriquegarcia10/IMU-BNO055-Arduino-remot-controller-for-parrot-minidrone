 #Lee los datos del puerto serie y los imprime


import serial
import time
import simplejson
 
 
 
 
arduino = serial.Serial('/dev/ttyUSB0', 115200)

while True:

       
    jsonResult=arduino.readline()

    try:

        jsonObject=simplejson.loads(jsonResult)
        x,y,z= jsonObject["x"], jsonObject["y"], jsonObject["z"]
        Z=float(z)*100/180
        Y=float(y)*100/90
        X=(((float(x)-0)*(180-(-180)))/(360-0))+(-180)
        print (X , " " , Y , " " , Z)
        mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=1)
        

        

    except Exception:
        pass


    

   


    