
import requests
import time
import hashlib


server_time = requests.get('https://eu.api.ovh.com/1.0/auth/time')
print(server_time)
server_time = int(server_time.text)
print(server_time)
time_delta = server_time - int(time.time())
print(time_delta)


application_key = ''
application_secret = ''
consumer_key = ''

now = str(int(time.time()) + time_delta)
url = 'https://eu.api.ovh.com/1.0/me'

signature = hashlib.sha1()
signature.update(
    "+".join([application_secret, consumer_key, 'GET', url, '', now]).encode(
        "utf-8"
    )
)

# Headers
headers = {
    'X-Ovh-Application': application_key,
   # 'X-Ovh-Application-Secret': application_secret,
    'X-Ovh-Consumer': consumer_key,
    'X-Ovh-Timestamp' : now,
    'X-Ovh-Signature' : "$1$" + signature.hexdigest()
}

response = requests.get(url, headers=headers)
print(response.content)

