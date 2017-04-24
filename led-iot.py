#import Libraries
import RPi.GPIO as GPIO
import time
import pyrebase

#Firebase Configuration
config = {
  "apiKey": "apiKey",
  "authDomain": "demoiot-6579b.firebaseapp.com",
  "databaseURL": "https://demoiot-6579b.firebaseio.com",
  "storageBucket": "demoiot-6579b.appspot.com"
}

firebase = pyrebase.initialize_app(config)

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.IN, GPIO.PUD_DOWN)

#Firebase Database Intialization
db = firebase.database()

#While loop to run until user kills program
while(True):
    inputValue = GPIO.input(23)
    if (inputValue == True):
       print("button pressed")
       led = db.child("led").get()
       
       for user in led.each():
           if(user.val() == "OFF"):
              data = {'state':'ON'}
              db.child("led").update(data)               
           else: 
              data = {'state':'OFF'}
              db.child("led").update(data)
   	
    #Get value of LED 
    led = db.child("led").get()
    #Sort through children of LED(we only have one)
    for user in led.each():
        #Check value of child(which is 'state')
        if(user.val() == "OFF"):
            #If value is off, turn LED off
            GPIO.output(18, False)
        else:
            #If value is not off(implies it's on), turn LED on
            GPIO.output(18, True)

        #0.1 Second Delay
        time.sleep(0.1)   

	
