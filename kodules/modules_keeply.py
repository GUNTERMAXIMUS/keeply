from ctypes import Structure, windll, c_uint, sizeof, byref
from pyautogui import screenshot as pyscreenshot
from tempfile import TemporaryDirectory
from cryptography.fernet import Fernet
from datetime import datetime
from getpass import getuser
from platform import system
from shutil import rmtree
from time import sleep
from tqdm import tqdm

from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

import os
import webbrowser
import smtplib
import ssl

# GLOBAL VARIABLES
# screenshot
input_key = '', False
method_key = False


def installation():
    # Installations
    initialize_import = False
    print(f'\nSetting configuration to {system()}.\n')
    sleep(1)
    try:
        os.system('pip install -r requirements.txt' if os.name ==
                  'nt' else 'sudo pip3 install -r requirements.txt')

        if os.name == 'posix':
            os.system('sudo apt-get install scrot')

        initialize_import = True
        os.system('cls' if os.name == 'nt' else 'clear')
    except OSError as install_error:
        print('OSInstall error', install_error)
    finally:
        return initialize_import


class LASTINPUTINFO(Structure):
    _fields_ = [('cbSize', c_uint), ('dwTime', c_uint), ]


class Timing:
    def __init__(self):
        pass

    def date_funct(self):
        return datetime.now().strftime('%x %X %p')

    def get_sec(self):
        time_str = datetime.now().strftime('%X')
        print(time_str)
        day_str = datetime.now().strftime('%w')

        if len(time_str.split(':')) < 3:
            time_str = time_str + ':00'

        h, m, __ = time_str.split(':')
        day_sec, d = 86000, int(day_str)
        if d == 0:
            dx = day_sec * 7
        else:
            dx = day_sec * d
        return dx - (day_sec - (int(h) * 3600 + int(m) * 60))


class Temporary_Directory:
    def __init__(self):
        pass

    def open_temp_dir(self):
        user_os = getuser()
        if system() == 'Linux':
            path = f'/home/{user_os}/Escritorio/codes/'
        elif system() == 'Windows':
            path = f'C:/Users/{user_os}/Videos/Captures/'
        if not os.path.exists(path):
            os.mkdir(path)
        return TemporaryDirectory(dir=path, prefix='temp')

    def close_temp_dir(self, temp_dir):
        rmtree(temp_dir)
        print(f'{temp_dir} closed\n')


class Cryptography:
    def __init__(self):
        pass

    def cipher_key(self):
        KEY = Fernet.generate_key()
        return KEY

    def enrcypt_message(self, KEY, message):
        cipher = Fernet(KEY)
        encrypted_text = cipher.encrypt(bytes(message, encoding='utf-8',))
        return encrypted_text

    def decrypted_message(self, KEY, encrypted_text):
        cipher = Fernet(KEY)
        decrypted_text = (cipher.decrypt(encrypted_text)).decode()
        return decrypted_text


class Screenshots:
    def __init__(self, key_str, method=False):
        self.key_str = key_str
        self.method = method

    def capture(self, user, password, smtp_mail, port, args_temporary_file):
        global input_key, method_key
        if self.method == 'key':
            if method_key == False:
                input_key = self.key_str
                print(f'Predefine key: {input_key}')
                method_key = True
            else:
                if self.key_str == input_key:
                    fdate = Timing().date_funct()
                    fdate = fdate.replace('/', '-').replace(':', '.')
                    temp_dir = Temporary_Directory().open_temp_dir()  # OPEN Temporary Directory
                    print('\nTemporary directory created...')
                    print('Creating screenshot...')
                    filename = f'{temp_dir.name}/{fdate}.png'
                    myScreenshot = pyscreenshot()
                    myScreenshot.save(filename)
                    print(
                        f'Screenshot saved on:\nFile: {filename}\nTemporary directory: {temp_dir.name}\n')
                    with open(filename, 'rb') as fp:
                        img_data = fp.read()
                    EMAIL(message=img_data, user=user).send_mail(password=password, smtp_mail=smtp_mail, port=port,
                                                                 args_temporary_file=args_temporary_file, screenshot=True)
                    Temporary_Directory().close_temp_dir(temp_dir=temp_dir.name)
        elif self.method == 'keyword':
            pass
        elif self.method == 'click':
            pass


class EMAIL:
    '''send messages'''

    def __init__(self, message, user):
        self.message = message
        self.user = user

    def from_to_date_subject(self):
        self.message['From'] = self.user
        self.message['To'] = self.user
        self.message['Date'] = formatdate(localtime=True)
        self.message['Subject'] = f'{formatdate(localtime=True)} || KEEPLY ||'
        return self.message

    def mail_info(self, screenshot, args_temporary_file):
        if screenshot == True:
            filename = (Timing().date_funct()).replace(
                '/', '-').replace(':', '.')
            msg = EmailMessage()
            EMAIL(message=msg, user=self.user).from_to_date_subject()
            msg.add_attachment(self.message, maintype='image',
                               subtype='png', filename=(f'{filename}.png'))
        elif args_temporary_file == True:
            msg = MIMEMultipart()
            EMAIL(message=msg, user=self.user).from_to_date_subject()
            fdate = Timing().date_funct().replace('/', '-').replace(':', '.')

            # eventually change to default temp dir (?)
            with TemporaryDirectory(dir=f'C:/Users/{getuser()}/Videos/Captures/', prefix='temp_') as td:
                with open(f'{td}/{fdate}.txt', 'w+') as attach_txt:
                    attach_txt.write(self.message)
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
            EMAIL(message=msg, user=self.user).from_to_date_subject()
            msg.set_content(self.message)
        return msg

    def send_mail(self, password, smtp_mail, port, args_temporary_file, screenshot=False):
        msg = EMAIL(message=self.message, user=self.user).mail_info(
            screenshot=screenshot, args_temporary_file=args_temporary_file)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host=smtp_mail, port=port, context=context) as server:
            try:
                '''conect to the server'''
                server.login(user=self.user, password=password)
                server.sendmail(from_addr='Keeply',
                                to_addrs=self.user, msg=msg.as_string())
                print('\nSent email\n')
            except:
                print(
                    '\nGoogle is not allowing you to log in via smtplib because it has flagged this sort of login as "less secure".')
                print(
                    'While youre logged in to your google account, allow the access for less secure apps.')
                print(
                    '\nYour browser will be open to the google "lesssecureapps" link in 10 seconds.')
                for __ in tqdm(range(10)):
                    sleep(1)
                webbrowser.open(
                    'https://www.google.com/settings/security/lesssecureapps')
