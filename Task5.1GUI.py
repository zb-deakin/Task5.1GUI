import atexit
import time
from tkinter import *

import RPi.GPIO as GPIO


# cleanup when program exits
@atexit.register
def cleanup():
    GPIO.cleanup()
    print("\n---> CLEANUP COMPLETE :)\n")


# board setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# gui setup
guiWindow = Tk()
guiWindow.title("LED controller")
Label(guiWindow, text="Select the LED you want to light up:", padx=25, pady=10).pack(anchor="w")

# set up state-management for radio buttons
nothingSelected = None
previouslySelectedLed = nothingSelected
# tkinter variable: track which radio button is selected
guiSelectedRadioButton = IntVar(guiWindow, nothingSelected)

# prepare GPIO pin data
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
    global guiSelectedRadioButton
    global previouslySelectedLed
    _selectedPin = guiSelectedRadioButton.get()

    # stop here if chosen pin is invalid
    if _selectedPin not in allValidPins:
        print(f'ERROR: Pin "{_selectedPin}" is not a valid selection')
        return

    # if an LED was lit up before, turn it off now
    if previouslySelectedLed != nothingSelected:
        GPIO.output(previouslySelectedLed, GPIO.LOW)

    # light up selected LED
    GPIO.output(_selectedPin, GPIO.HIGH)

    # update state-tracking
    previouslySelectedLed = _selectedPin


# set up LED GPIO pins and GUI radio buttons
for _ledPin in allValidPins:
    # setup GPIO for this pin
    GPIO.setup(_ledPin, GPIO.OUT)
    GPIO.output(_ledPin, GPIO.LOW)
    time.sleep(0.25)

    # create a GUI radio button for this LED
    Radiobutton(
        guiWindow,
        text=ledNames[_ledPin],
        value=int(_ledPin),
        variable=guiSelectedRadioButton,
        command=activateChosenLed,
        width=25,
        justify=LEFT,
    ).pack()

Label(guiWindow, text=" ").pack()

# open the GUI window
guiWindow.mainloop()
