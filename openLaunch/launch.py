import json
import subprocess
import os
import requests
import sys
import argparse

parser = argparse.ArgumentParser(prog='launch.py',description='Launch RuneLite logged in with a previous Jagex Account session')

parser.add_argument('-c','--character')

character = parser.parse_args().character

f = open("sessionid.json", "r")

jx_session_id = json.load(f)['sessionId']

accountsJson = requests.get("https://auth.jagex.com/game-session/v1/accounts",headers={"Authorization": "Bearer "+jx_session_id}).text
accounts = json.loads(accountsJson)

acc = None

if character == None:
    i = 0
    for x in accounts:
        print(i,accounts[i]['displayName'])
        i = i+1

    acc = int(input("Select an account (0 to "+str(i-1)+"): "))
else:
    i = 0
    for x in accounts:
        if(accounts[i]['displayName'].lower() == character.lower()):
            acc = i
            break
        i = i+1

if acc == None:
    print('Character not found')
    exit()

jx_character_id = accounts[acc]['accountId']
jx_display_name = accounts[acc]['displayName']


envs = os.environ

envs["JX_ACCESS_TOKEN"]  = ""
envs["JX_CHARACTER_ID"]  = jx_character_id
envs["JX_DISPLAY_NAME"]  = jx_display_name
envs["JX_REFRESH_TOKEN"] = ""
envs["JX_SESSION_ID"]    = jx_session_id

subprocess.run(["java","-jar","RuneLite.jar"],env=envs)
