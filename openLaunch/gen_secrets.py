import sys
import pkce
import requests
import json

code_verifier = pkce.generate_code_verifier(length=45)
code_challenge = pkce.get_code_challenge(code_verifier)

auth_state = "ABCDEFGH" # Not used in this application, but is required by the auth server

print("Go to this url, log in, and bring me back your 'code'\n",file=sys.stderr)
print("https://account.jagex.com/oauth2/auth?auth_method=&login_type=&flow=launcher&response_type=code&client_id=com_jagex_auth_desktop_launcher&redirect_uri=https%3A%2F%2Fsecure.runescape.com%2Fm%3Dweblogin%2Flauncher-redirect&code_challenge="+code_challenge+"&code_challenge_method=S256&prompt=login&scope=openid+offline+gamesso.token.create+user.profile.read&state="+auth_state+"\n\n",file=sys.stderr)
print("Code: ",file=sys.stderr,end="")
code_input = input()

url = "https://account.jagex.com/oauth2/token"

post_data = {
    "grant_type":"authorization_code",
    "client_id":"com_jagex_auth_desktop_launcher",
    "code":code_input,
    "code_verifier":code_verifier,
    "redirect_uri":"https://secure.runescape.com/m=weblogin/launcher-redirect"
}

x = requests.post(url,data=post_data)

print(x.text)
