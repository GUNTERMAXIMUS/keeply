# keeply
> Keeloger for linux and windows with optional crypted messages (unique key and/or steganography) and screenshots to your transfer method and decrypted function to read i

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
