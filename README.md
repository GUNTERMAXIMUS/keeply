# keeply
[![Unstable](https://poser.pugx.org/ali-irawan/xtra/v/unstable.svg)](https://poser.pugx.org/ali-irawan/xtra/v/unstable.svg)
[![Issues](https://img.shields.io/github/issues-raw/tterb/PlayMusic.svg?maxAge=25000)](https://github.com/Y4rd13/keeply/issues)  

> Keeloger for linux and windows with optional crypted messages (unique key and/or steganography) and screenshots to your transfer method and decrypted function to read i

## Features
* Transfer method: e-mail
* E-mail delivery supports SSL-TLS/STARTTLS.
* Captures mouse cursor
* Screenshots
* Keyword
* ... details here!

## Developing
* Invisible in task manager
* Capture WebCam
* Capture microphone
* Send logs: via ftp
* Send logs: Automatically flushes logs to a USB stick or to External HardDisk.
* Takes screenshot with predefined keywords
* Takes screenshot with predefined number of clicks
* Auto Uninstall at a specific date
* File monitoring - records paths and names of files or directories that are created, deleted or renamed.
* Steganography

## Installation & Development setup
To install all development dependencies
Windows: & Linux:
```python
pip3 install -r requirements.txt
```
or you can just run
```python
python3 keeply.py -i
```

## Usage example

```python
python keeply.py -h
```
```
optional arguments:
  -h, --help            show this help message and exit
  -i, --installation    Install core packages
  -tr , --transfer      Transfer method: fpt, email, usb, hdd
  -temp , --temporary_file
                        Creates a temporary directory with logs.txt [True, default: False] (recommended to encrypt the data --encrypt)
  -u , --user           Username (mail)
  -p , --password       Username passowrd
  --port                SMTP port (default=465)
  --smtp                SMTP mail (default=smtp.gmail.com)
  --encrypt             Encrypt message with key: True (default: False)
  -l , --lines          Max lines to send (default=5)
  -t , --timer          Set a timer to transfer in minutes (min: 1; default=10)
  -ss , --screenshot    Enable Screenshot: click, key, keyword
  --start               Initialize keeylogger
  -K , --key            Key to decrypth
  -F , --filename       Directory ../filename.txt with encrypted text
  --decrypth            Decrypth the message

Made by Y4rd13.
```

## Release History

* 0.0.0
    * CHANGE: ''

## Meta

[GITHUB](https://github.com/Y4rd13/)
