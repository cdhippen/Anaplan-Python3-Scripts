# This script returns all actions in the selected workspace and model to a json
# array saved in file 'actions.json'. Reference that file for future use.

# This script assumes you know your workspaceGuid and modelGuid.
# If you do not have this information, please run 'getWorkspaces.py' and
# 'getModels.py' and retrieve this information from the resulting json files.

# If you are using certificate authentication, this script assumes you have
# converted your Anaplan certificate to PEM format, and that you know the
# Anaplan account email associated with that certificate.

# This script uses Python 3 and assumes that you have the following modules
# installed: requests, base64

import requests
import base64

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert the Anaplan account email being used
username = ''

# If using cert auth, replace cert.pem with your pem converted certificate
# filename. Otherwise, remove this line.
cert = open('cert.pem').read()

# If using basic auth, insert your password. Otherwise, remove this line.
password = ''

# Uncomment your authentication method (cert or basic). Remove the other.
user = 'AnaplanCertificate ' + str(base64.b64encode((
       f'{username}:{cert}').encode('utf-8')).decode('utf-8'))

# user = 'Basic ' + str(base64.b64encode((f'{username}:{password}'
#                                         ).encode('utf-8')).decode('utf-8'))

getHeaders = {
    'Authorization': user
}

getActions = requests.get(f'https://api.anaplan.com/1/3/workspaces/{wGuid}/' +
                        f'models/{mGuid}/actions',
                        headers=getHeaders)

with open('actions.json', 'wb') as f:
    f.write(getActions.text.encode('utf-8'))
