import atexit
import time
from tkinter import *

import RPi.GPIO as GPIO


# cleanup when program exits
@atexit.register
def cleanup():
    GPIO.cleanup()
    print("\n---> CLEANUP COMPLETE :)\n")


# set up the board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup the gui
window = Tk()
window.title("LED controller")
Label(window, text="Select the LED you want to light:").pack(anchor="w")

# track state of the GUI
dummyPin = 0
previouslySelectedLed = dummyPin
uiLedSelection = IntVar(window, dummyPin)

# prepare GPIO pins for use
redPin = 17
greenPin = 27
bluePin = 22

ledNames = {
    redPin: "Red",
    greenPin: "Green",
    bluePin: "Blue",
}

allValidPins = list(ledNames.keys())


# light up the selected LED on the breadboard
def activateChosenLed():
    # get shared variables
    global uiLedSelection
    global previouslySelectedLed
    _selectedPin = uiLedSelection.get()

    # stop here if chosen pin is invalid
    if _selectedPin not in allValidPins:
        print(f'ERROR: Pin "{_selectedPin}" is not a valid selection')
        return

    # if led was lit up before, turn it off now
    if previouslySelectedLed != dummyPin:
        GPIO.output(previouslySelectedLed, GPIO.LOW)

    # light up selected led
    GPIO.output(_selectedPin, GPIO.HIGH)

    # update tracker
    previouslySelectedLed = _selectedPin


# setup GPIO and generate radio butons for pins
for _ledPin in allValidPins:
    # create a radio button for this pin
    Radiobutton(
        window,
        text=ledNames[_ledPin],
        variable=uiLedSelection,
        value=int(_ledPin),
        command=activateChosenLed,
    ).pack(anchor="w")

    # setup GPIO for this pin
    GPIO.setup(_ledPin, GPIO.OUT)
    GPIO.output(_ledPin, GPIO.LOW)
    time.sleep(0.25)

# open the window
window.mainloop()
