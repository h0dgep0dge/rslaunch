import requests
import auth_secrets

url = "https://account.jagex.com/oauth2/token"

post_data = {
    "grant_type":"authorization_code",
    "client_id":"com_jagex_auth_desktop_launcher",
    "code":auth_secrets.jagex_code,
    "code_verifier":auth_secrets.code_verifier,
    "redirect_uri":"https://secure.runescape.com/m=weblogin/launcher-redirect"
}

post_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

x = requests.post(url,data=post_data,headers=post_headers)

print(x.text)
