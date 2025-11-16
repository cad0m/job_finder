from curl_cffi import requests

response = requests.get('https://httpbin.org/get', headers={'User-Agent': 'Mozilla/5.0'})

print(response.json())