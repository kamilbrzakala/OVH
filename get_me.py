import requests
import time
import hashlib
import ssl

context = ssl._create_unverified_context()

#requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

server_time = requests.get('https://eu.api.ovh.com/1.0/auth/time', verify=False)

server_time = int(server_time.text)
time_delta = server_time - int(time.time())
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

#ca_bundle_path = r'C:\Users\brzakalak\Downloads\certs.pem'

response = requests.get(url, headers=headers)
response.content


