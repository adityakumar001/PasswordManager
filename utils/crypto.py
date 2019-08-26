import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

iterations = 100000

'''This function is called whenever the application is run for the first time or when the key file is deleted.'''


def create_salt():
    salt = os.urandom(16)
    with open("./key", mode="wb") as salt_file:
        salt_file.write(salt)
    return salt


'''This function is called get the salt from the key file '''


def get_salt():
    if os.path.isfile("./key"):
        with open("./key", mode='rb') as password_file:
            salt = password_file.read(16)
        if len(salt) is 0:
            salt = create_salt()
    else:
        salt = create_salt()
    return salt


'''This function is called to create the key using salt and password provided!!!'''


def create_key(password):
    salt = get_salt()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA3_512(), length=32, salt=salt, iterations=iterations,
                     backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)


def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)
