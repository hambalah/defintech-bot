# import requests

# url = "https://api.sandbox.finverse.net/auth/customer/token"
# # url = "https://api.sandbox.finverse.net/"

# payload = '{"client_id": "01GM0P2KSGQ8WM4JXD7GW7AQ41", "client_secret": "fv-c-1670765432-041f50d3f3aac096f3d2ace466e093eb83b5c72017446c345f4b87ea1172d45b", "grant_type": "01GM0P2KTYEMZGHK40QQSMMBBX"}'

# headers = {'X-Request-Id': '01GM0P2KTYEMZGHK40QQSMMBBX'}

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.json())
# # print(response.text)

import requests

url = "https://api.sandbox.finverse.net/payments/01GGYH1YFR4109SDXCYDGVSRRK"

payload={}
headers = {
  'X-Request-Id': '01GM0P2KTYEMZGHK40QQSMMBBX'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
