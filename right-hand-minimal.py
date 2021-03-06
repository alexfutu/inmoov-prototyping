# Change to the port that you use (eg COM7)
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
ear = i01.ear

# Set voice commands (attach them to functions)
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

# Counter to allow for button pushing cooldown
lastPressed = 0

# Method to be called when pin values are refreshed
def publishPin(pins):
	global lastPressed
	lastPressed = max(lastPressed - 1, 0) # Gradually decrement cooldown (to zero)
	
	# Loop through every pin
	for pin in range(0, len(pins)):
		pinval = pins[pin].value

		# Pinval is the value of the pin (debug threshold through MRL)
		# Also make sure that cooldown is finished
		if pinval > 600 and lastPressed <= 0:
			i01.mouth.speak("You touched my button")
			lastPressed = 2000 # Start cooldown
			print str(pins[pin].address), ". pin pressed with value ", str(pinval)

i01.rightHand.attach()
# Trigger the publishPin method at the right time
i01.rightHand.arduino.addListener("publishPinArray","python","publishPin")
i01.rightHand.arduino.enablePin(54, 1000) # Pin 54 is A0 on Mega

def handopen():
  i01.moveHand("right",0,0,0,0,0)
  i01.mouth.speak("ok I'll open my hand")

def handclose():
  i01.moveHand("right",180,180,180,180,180)
  i01.mouth.speak("ok I'm closing my hand")