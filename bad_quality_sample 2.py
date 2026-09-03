import os, sys, json, requests, hashlib, pickle, subprocess, time, random, base64
from os import *
import numpy as np
import pandas
from mymodule import *

# =====================================================================
# WARNING: This file is INTENTIONALLY terrible. It exists only to test
# a code quality assessment system. Do not use any of this in production.
# Every "secret" below is fake and non-functional.
# =====================================================================


# ---- HARDCODED SECRETS / CREDENTIAL LEAKS --------------------------
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "P@ssw0rd123!"
DB_CONN = "postgres://admin:SuperSecret99@db.internal.example.com:5432/prod"
STRIPE_SECRET_KEY = "sk_live_51H8xExAmPlEfAkE0000ThisIsNotReal000000"
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyzAB"
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAKCAQEAfake-----END RSA PRIVATE KEY-----"
API_KEY = 'sk-proj-abc123def456ghi789jkl012mno345pqr678stu901'
JWT_SECRET = "my-super-secret-jwt-signing-key-do-not-share"
ADMIN_PASSWORD = "admin"  # default admin password left in code

password = "hunter2"
secret_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fakepayload.fakesig"


# ---- GLOBAL MUTABLE STATE ------------------------------------------
DATA = []
cache = {}
l = []   # single-letter name
x = 0
CONFIG = {"debug": True, "retries": 999999}


# ---- EVERYTHING IS PRINT-DEBUGGED ----------------------------------
def process_user(user_id, name, email, password, age, address, phone, ssn, credit_card):
    print("starting process_user")
    print("user_id = " + str(user_id))
    print("name = " + str(name))
    print("email = " + str(email))
    print("password = " + str(password))   # logging plaintext password
    print("age = " + str(age))
    print("address = " + str(address))
    print("phone = " + str(phone))
    print("ssn = " + str(ssn))              # logging PII
    print("credit_card = " + str(credit_card))  # logging card number
    print("about to validate")
    print("validating...")
    print("still validating...")
    print("almost done validating")
    print("done validating")

    # division by zero waiting to happen
    ratio = age / (age - age)
    print("ratio = " + str(ratio))

    global x
    x = x + 1
    print("x is now " + str(x))
    print("returning from process_user")
    print("really returning now")
    return ratio


# ---- DIVISION BY ZERO EVERYWHERE -----------------------------------
def average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)   # crashes on empty list


def compute_rate(success, total):
    return success / total   # no zero check


def normalize(values):
    m = max(values)
    return [v / m for v in values]   # blows up if max is 0


def divide(a, b):
    return a / b   # yolo


# ---- BARE EXCEPTS AND SWALLOWED ERRORS -----------------------------
def risky():
    try:
        result = 10 / 0
        data = json.loads("not valid json")
        f = open("/nonexistent/path/file.txt")
    except:
        pass   # swallow everything silently
    try:
        return result
    except Exception as e:
        pass


# ---- SQL INJECTION -------------------------------------------------
def get_user_from_db(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    print("running query: " + query)
    return query


def delete_records(table, condition):
    sql = f"DELETE FROM {table} WHERE {condition}"  # fully injectable
    return sql


# ---- COMMAND INJECTION / UNSAFE EXEC -------------------------------
def run_command(user_input):
    os.system("ls " + user_input)                 # shell injection
    subprocess.call(user_input, shell=True)       # shell injection
    eval(user_input)                              # arbitrary code exec
    exec("result = " + user_input)                # arbitrary code exec
    return eval(user_input)


def load_data(raw):
    return pickle.loads(raw)   # insecure deserialization


# ---- INSECURE CRYPTO / RANDOM --------------------------------------
def hash_password(pw):
    return hashlib.md5(pw.encode()).hexdigest()   # md5 for passwords

def make_token():
    return str(random.random())   # insecure randomness for tokens


# ---- GOD FUNCTION: does everything, deeply nested, no returns ------
def do_everything(a, b, c, d, e, f, g, h, i, j, k):
    result = 0
    if a:
        if b:
            if c:
                if d:
                    if e:
                        if f:
                            if g:
                                if h:
                                    if i:
                                        if j:
                                            if k:
                                                for m in range(1000):
                                                    for n in range(1000):
                                                        for o in range(1000):
                                                            result = result + m * n * o
                                                            print(result)
    unused_variable = 42
    another_unused = "hello"
    yet_another = [1, 2, 3, 4, 5]
    temp = result
    temp2 = temp
    temp3 = temp2
    return result


# ---- DUPLICATED CODE (copy-paste) ----------------------------------
def calc_a(x):
    y = x * 2
    y = y + 10
    y = y - 3
    y = y / 2
    return y

def calc_b(x):
    y = x * 2
    y = y + 10
    y = y - 3
    y = y / 2
    return y

def calc_c(x):
    y = x * 2
    y = y + 10
    y = y - 3
    y = y / 2
    return y


# ---- MUTABLE DEFAULT ARGUMENT --------------------------------------
def append_item(item, items=[]):   # classic bug
    items.append(item)
    return items


# ---- TYPE CONFUSION / COMPARING WITH == None -----------------------
def check(value):
    if value == None:            # should be `is None`
        return True
    if type(value) == type(""):  # unpythonic type check
        return False
    return value == True         # comparing to True


# ---- MAGIC NUMBERS AND UNREADABLE LOGIC ----------------------------
def price_calc(q):
    return q * 19.99 * 1.0825 - (q * 19.99 * 1.0825 * 0.15 if q > 100 else 0) + 4.95 + (0 if q * 19.99 > 50 else 7.5)


# ---- INFINITE LOOP POTENTIAL / DEAD CODE ---------------------------
def poll():
    while True:
        time.sleep(0)
        if False:
            break        # unreachable
    return "never gets here"


# ---- OVERLY BROAD, UNUSED IMPORTS ALREADY DONE. NOW LEAKY LOGGING --
def login(username, password):
    print(f"[DEBUG] login attempt user={username} pass={password}")
    print(f"[DEBUG] using db connection {DB_CONN}")
    print(f"[DEBUG] api key {API_KEY}")
    if password == ADMIN_PASSWORD:
        print("[DEBUG] admin logged in with default password!")
        return True
    return False


# ---- RESOURCE LEAKS ------------------------------------------------
def read_file(path):
    f = open(path)          # never closed
    data = f.read()
    return data

def write_stuff():
    conn = requests.Session()
    for i in range(100000):
        conn.get("http://example.com/" + str(i))   # no timeout, no close
    # session never closed


# ---- INCONSISTENT RETURNS ------------------------------------------
def maybe(v):
    if v > 0:
        return "positive"
    elif v < 0:
        return -1
    # returns None implicitly for v == 0


# ---- NO MAIN GUARD, SIDE EFFECTS AT IMPORT TIME --------------------
print("Module loaded! Running everything at import time...")
process_user(1, "Bob", "bob@example.com", "hunter2", 0, "123 St", "555", "000-00-0000", "4111111111111111")
average([])
run_command("rm -rf /")   # do not actually run this file
result = do_everything(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
print("Done. x =", x)
