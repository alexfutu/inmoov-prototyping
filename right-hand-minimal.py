# Start the webgui service without starting the browser
webgui = Runtime.create("WebGui","WebGui")
webgui.autoStartBrowser(False)
webgui.startService()
# Then start the browsers and show the WebkitSpeechRecognition service named i01.ear
webgui.startBrowser("http://localhost:8888/#/service/i01.ear")

# As an alternative you can use the line below to show all services in the browser. In that case you should comment out all lines above that starts with webgui. 
# webgui = Runtime.createAndStart("webgui","WebGui")

# Change to the port that you use
rightPort = "/dev/tty.usbmodem1411"

#to tweak the default voice
Voice="dfki-prudence" # Default female for MarySpeech 
#Voice="cmu-bdl" #Male US voice.You need to add the necessary file.jar to myrobotlab.1.0.XXXX/library/jar
#https://github.com/MyRobotLab/pyrobotlab/blob/ff6e2cef4d0642e47ee15e353ef934ac6701e713/home/hairygael/voice-cmu-bdl-5.2.jar
voiceType = Voice
mouth = Runtime.createAndStart("i01.mouth", "MarySpeech")
#mouth.setVoice(voiceType)
#mouth.setGoogleURI()
##############
# starting parts
i01 = Runtime.createAndStart("i01", "InMoov")
i01.startEar()
i01.startMouth()


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

def publishPin(pins):
	global lastPressed
	lastPressed = max(lastPressed - 1, 0)
	for pin in range(0, len(pins)):
		pinval = pins[pin].value
		if pinval > 600 and lastPressed <= 0:
			i01.mouth.speak("You touched my button")
			lastPressed = 3000
			print str(pins[pin].address), ". pin pressed with value ", str(pinval)

i01.rightHand.attach()
i01.rightHand.arduino.addListener("publishPinArray","python","publishPin")
i01.rightHand.arduino.enablePin(54, 1000)


def handopen():
  i01.moveHand("right",0,0,0,0,0)
  i01.mouth.speak("ok I open my hand")

def handclose():
  i01.moveHand("right",180,180,180,180,180)
  i01.mouth.speak("a nice and wide open hand that is")