import requests

url = "https://api.sandbox.finverse.net/auth/customer/token"

payload = "{\n    client_id\": \"01GM0P2KSGQ8WM4JXD7GW7AQ41\",\n    \"client_secret\": \"fv-c-1670765432-041f50d3f3aac096f3d2ace466e093eb83b5c72017446c345f4b87ea1172d45b\",\n    \"grant_type\": \"client_credentials\"\n}"
headers = {
  'X-Request-Id': 'any_customer_app_id-1670764043'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)