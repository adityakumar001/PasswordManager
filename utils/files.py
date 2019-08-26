from utils import crypto
import os
import json


def key_exists():
    return os.path.isfile("./key")


def save_data(data, key):
    encrypted = crypto.encrypt_data(data.encode(), key)
    with open("./passwords", mode="wb") as passwords_file:
        passwords_file.write(encrypted)


def get_values(key):
    with open("./passwords", mode='rb') as file:
        data = file.read()
    json_string = str(crypto.decrypt_data(data, key), 'utf-8')
    values = json.loads(json_string)
    return values


def store_values(password, user_values):
    key = crypto.create_key(password)
    values = get_values(key)
    password_list = values["passwords"]
    for password in password_list:
        if password == user_values:
            return -1
    password_list.append(user_values)
    json_string = json.dumps(values)
    save_data(json_string, key)
    return 1


'''This function is called whenever the application is run for the first time or when the key file is deleted.'''


def create_password_file(password):
    key = crypto.create_key(password)
    with open("./passwords", mode='wb') as passwords_file:
        json_str = json.dumps({"passwords": []})
        passwords_file.write(crypto.encrypt_data(json_str.encode(), key))
