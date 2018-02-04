# This script returns all models you have access to to a json array saved in
# file 'models.json'. Reference that file for future use.

# If you know your workspaceGuid, you can replace wsGuid with your Workspace
# Guid to only return info about models in that workspace. Otherwise, leave
# wsGuid equal to '' and you will get all models that you have access to.

# If you are using certificate authentication, this script assumes you have
# converted your Anaplan certificate to PEM format, and that you know the
# Anaplan account email associated with that certificate.

# This script uses Python 3 and assumes that you have the following modules
# installed: requests, base64

import requests
import base64

# Replace with your workspace Guid or leave blank if you don't know it
wGuid = ''

# Replace with the Anaplan account email being used
username = ''

# If using cert auth, replace cert.pem with your pem converted certificate
# filename. Otherwise, remove this line.
cert = open('cert.pem').read()

# If using basic auth, replace with your password. Otherwise, remove this line.
password = ''

# Uncomment your authentication method (cert or basic). Remove the other.
user = 'AnaplanCertificate ' + str(base64.b64encode((
       f'{username}:{cert}').encode('utf-8')).decode('utf-8'))

# user = 'Basic ' + str(base64.b64encode((f'{username}:{password}'
#                                         ).encode('utf-8')).decode('utf-8'))

getHeaders = {
    'Authorization': user,

    'Content-type': 'application/json',
}

if wGuid:
    getModels = requests.get('https://api.anaplan.com/1/3/workspaces/' +
                             f'{wGuid}/models',
                             headers=getHeaders)
else:
    getModels = requests.get(f'https://api.anaplan.com/1/3/models',
                             headers=getHeaders)

with open('models.json', 'wb') as f:
    f.write(getModels.text.encode('utf-8'))
