import time
from pynput.keyboard import Key, Listener
import pyautogui as pya
import pyperclip 
from google_trans_new import google_translator  
from time import sleep
import sys
import logging
import re

SW_VERSION="0.1.1"
LOWER_TIMEOUT=0.05
UPPER_TIMEOUT=0.25
checkTime = 0
lst = []
translator = google_translator(url_suffix="vn")
detectmode = False

def transl(clipBoard):
    global translator
    global detectmode
    if detectmode==True:
        try:
            logging.error("Try detect")
            lang = translator.detect(clipBoard) 
            logging.error("Detect done")
            if lang == None or lang[0] == None:
                logging.error("Cannot detect language!")
                return "Cannot detect language!"
            if lang[0] == 'ko':
                translated = translator.translate(clipBoard, lang_src='ko', lang_tgt='en') 
                return translated  
            elif lang[0] == 'en':
                woSpecial=re.sub('[^a-zA-Z0-9 \n]', ' ', clipBoard)
                translated = translator.translate(woSpecial, lang_src='en', lang_tgt='vi')
                return translated 
            elif lang[0]== 'vi':
                return "except occur !"
        except:
            logging.error("except occur !")
            return "except occur !"
    elif detectmode ==False:
        translated = translator.translate(clipBoard, lang_src='ko', lang_tgt='en')
        return translated 

def on_press(key):
    if key == Key.esc:
        return False

def on_release(key):
    global checkTime
    global translator
    if key == Key.ctrl_l:
        if checkTime == 0 or round(time.time(),4) - checkTime > UPPER_TIMEOUT or round(time.time(),4) - checkTime < LOWER_TIMEOUT:
            checkTime = round(time.time(),4)
        elif round(time.time(),4) - checkTime < UPPER_TIMEOUT:
            logging.info('pyperclip copy')
            pyperclip.copy("") 
            pya.hotkey('ctrl', 'c')
            time.sleep(.05)  
            logging.info('pyperclip paste')
            clipBoard = pyperclip.paste()
            logging.info('pyperclip clipBoard')
            if not clipBoard.isspace():
                result = transl(clipBoard)
                print('{}'.format(repr(result) ))
            else: 
                return True
            logging.info("----------End session translate--------")
            print("---------------------------------------------------------")
            checkTime = 0

if __name__ == "__main__":
    #Make color 
    for i in range(21):
        sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()
    sleep(0.03)
    sys.stdout.write('\n')
    #Userguide
    print("Translater client started, v{}".format(SW_VERSION))
    print("Double press Left Ctrl to translate the selected text to Eng")
    print("---------------------------------------------------------")

    #Config logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='logs_file',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
 
    if len(sys.argv) > 1:
        if sys.argv[1] == 'detectmode':
            print(sys.argv[1])
            detectmode=True
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
