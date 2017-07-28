from time import sleep

# Change to the port that you use
rightPort = "/dev/tty.usbmodem1411"

# Start the webgui service without starting the browser
webgui = Runtime.create("WebGui","WebGui")
webgui.autoStartBrowser(False)
webgui.startService()
# Then start the browsers and show the WebkitSpeechRecognition service named i01.ear
webgui.startBrowser("http://localhost:8888/#/service/i01.ear")

# As an alternative you can use the line below to show all services in the browser. In that case you should comment out all lines above that starts with webgui. 
# webgui = Runtime.createAndStart("webgui","WebGui")

mouth = Runtime.createAndStart("i01.mouth", "Acapella")

#mouth.setGoogleURI()
##############
# starting parts
i01 = Runtime.createAndStart("i01", "InMoov")
i01.startEar()
i01.startMouth()
#Voice="cmu-bdl" #Male US voice.You need to add the necessary file.jar to myrobotlab.1.0.XXXX/library/jar
#i01.mouth.setVoice(Voice)
#https://github.com/MyRobotLab/pyrobotlab/blob/ff6e2cef4d0642e47ee15e353ef934ac6701e713/home/hairygael/voice-cmu-bdl-5.2.jar

i01.startRightHand(rightPort)

# verbal commands
ear = i01.ear

ear.addCommand("attach your right hand", "i01.rightHand", "attach")
ear.addCommand("disconnect your right hand", "i01.rightHand", "detach")
ear.addCommand("rest", i01.getName(), "rest")
ear.addCommand("open your hand", "python", "handopen")
ear.addCommand("close your hand", "python", "handclose")
ear.addCommand("capture gesture", ear.getName(), "captureGesture")
ear.addCommand("manual", ear.getName(), "lockOutAllGrammarExcept", "voice control")
ear.addCommand("voice control", ear.getName(), "clearLock")

# Confirmations and Negations are not supported yet in WebkitSpeechRecognition
# So commands will execute immediatley
ear.addComfirmations("yes","correct","yeah","ya")
ear.addNegations("no","wrong","nope","nah")

ear.startListening()

lastPressed = 0

triggeredPins = [0] * 200 # Globally store the pin values

def publishPin(pins):
	global lastPressed
	lastPressed = max(lastPressed - 1, 0)
	for pin in range(0, len(pins)):
		pinval = pins[pin].value
		triggeredPins[pin] = pinval # Store pin value globally
		if pinval > 600 and lastPressed <= 0:
			i01.mouth.speak("You touched my button")
			lastPressed = 2000
			handopen()
		print str(pins[pin].address), ". pin pressed with value ", str(pinval)

i01.rightHand.attach()
i01.rightHand.arduino.addListener("publishPinArray","python","publishPin")
i01.rightHand.arduino.enablePin(54, 1000)

def handopen():
  i01.moveHand("right",0,0,0,0,0)
  i01.mouth.speak("ok I'll open my hand")

def handclose():
	i01.mouth.speak("ok I'm closing my hand")
	servoSensors = [54, 55, 56, 57, 58] # Respective sensor pins for each finger
	positions = [0, 0, 0, 0, 0]
	for i in range(18):
		# Loop through every finger
		for j in range(len(positions)):
			pin = servoSensors[j] # Get the pin number for this finger
			pinval = triggeredPins[pin] # Get the value of the finger's sensor
			if pinval < 600:
				positions[j] = i * 10 # Update the servo position only if sensor is untriggered
			# Else the finger will stay as-is

		i01.moveHand("right", positions[0], positions[1], positions[2], positions[3], positions[4])
		sleep(0.1) # Let the servo move

	i01.moveHand("right",180,180,180,180,180)


