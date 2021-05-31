import time
from pynput.keyboard import Key, Listener
import pyautogui as pya
import pyperclip 
from googletrans import Translator
from time import sleep
import sys


SW_VERSION="0.1.0"
LOWER_TIMEOUT=0.1
UPPER_TIMEOUT=0.4
checkTime = 0
lst = []
translator = Translator(service_urls=['translate.googleapis.com'])
for i in range(21):
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.03)
sys.stdout.write('\n')


print("Translater client started, v{}".format(SW_VERSION))
print("Double press Left Ctrl to translate the selected text to Eng")
print("---------------------------------------------------------")

def transl(clipBoard):
    translated = translator.translate(clipBoard, src='korean', dest='english')
    return translated.text

def on_press(key):
    global checkTime
    global translator
    if key == Key.ctrl_l:
        if checkTime == 0 or round(time.time(),2) - checkTime > UPPER_TIMEOUT or round(time.time(),2) - checkTime < LOWER_TIMEOUT:
            checkTime = round(time.time(),2)
        elif round(time.time(),2) - checkTime < UPPER_TIMEOUT:
            pyperclip.copy("") 
            pya.hotkey('ctrl', 'c')
            time.sleep(.1)  
            clipBoard = pyperclip.paste()
            print('{}'.format(transl(clipBoard) )) 
            print("---------------------------------------------------------")
            checkTime = 0
        elif round(time.time(),2) - checkTime > UPPER_TIMEOUT:
            checkTime = 0


def on_release(key):
    if key == Key.esc:
        return False
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
