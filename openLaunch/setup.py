# this is strictly a proof of concept, i avoided best practices like james bond dodging laser beams
# not only should you not use this program with any account you care about, you should only use it with accounts that you think it would be hilarious to get banned

import sys
import pkce
import requests
import json
import random
import string

code_verifier = pkce.generate_code_verifier(length=45)
code_challenge = pkce.get_code_challenge(code_verifier)

state = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(8))
# the state isn't used in this application, but may as well do it right

print("Go to this url, log in, and bring me back your 'code'\n")
print("https://account.jagex.com/oauth2/auth?auth_method=&login_type=&flow=launcher&response_type=code&client_id=com_jagex_auth_desktop_launcher&redirect_uri=https%3A%2F%2Fsecure.runescape.com%2Fm%3Dweblogin%2Flauncher-redirect&code_challenge="+code_challenge+"&code_challenge_method=S256&prompt=login&scope=openid+offline+gamesso.token.create+user.profile.read&state="+state+"\n\n")
code_input = input("Code: ")


post_data = {
    "grant_type":"authorization_code",
    "client_id":"com_jagex_auth_desktop_launcher",
    "code":code_input,
    "code_verifier":code_verifier,
    "redirect_uri":"https://secure.runescape.com/m=weblogin/launcher-redirect"
}

x = requests.post("https://account.jagex.com/oauth2/token",data=post_data).text

jwt = json.loads(x)['id_token']
nonce = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(48))

print("Go to this url, let it do its thing, and bring me back your 'id_token'\n")
print("https://account.jagex.com/oauth2/auth?id_token_hint="+jwt+"&nonce="+nonce+"&prompt=consent&redirect_uri=http%3A%2F%2Flocalhost&response_type=id_token+code&state="+state+"&client_id=1fddee4e-b100-4f4e-b2b0-097f9088f9d2&scope=openid+offline\n\n")
id_token = input("id_token: ")


post_data = {
    "idToken":id_token
}

sessionIdJson = requests.post("https://auth.jagex.com/game-session/v1/sessions",json=post_data).text

f = open("sessionid.json", "w")
f.write(sessionIdJson)
f.close()
