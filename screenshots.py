from tkinter import *
import pyautogui
import os
from pynput import keyboard
import time
import pyscreeze

# Open aditional window to screenshot
win = Tk()
win.title("Screenshot")
win.minsize(300,300)

# Function to take screenshot and save in the right folder
def takeScreenshot():
    screenshot = pyautogui.screenshot(region=(770,170, 580, 550))
    name = screenshotName()
    screenshot.save(fr"./screenshots_todo/{name}")

# Function that return the name for the screenshot to be saved
def screenshotName():
    files = os.listdir("./screenshots_todo")
    name = "screenshot1.png"
    while True:
        if name not in files:
            break
        name = "screenshot{}.png".format(int(name.split(".")[0].split("t")[1])+1)
    return name

btn = Button(win, text="Printa", command=takeScreenshot, bg="blue", fg="white")
btn.place(relx= 0.5, rely= 0.5, anchor= CENTER)

# Bind that work anywhere to screenshot rounds

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.Key.f6}
]
 
# The currently active modifiers
current = set()
 
def execute():
    takeScreenshot()
 
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()
 
def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)
 
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    win.mainloop() # TKINTER inicio
    listener.join()