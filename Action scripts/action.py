# This script runs your selected action. Run 'actionStatus.py' to retrieve
# the task metadata for the import task.

# This script assumes you know your workspaceGuid, modelGuid, and action
# metadata.
# If you do not have this information, please run 'getWorkspaces.py',
# 'getModels.py', and 'getImports.py' and retrieve this information from the
# resulting json files.

# If you are using certificate authentication, this script assumes you have
# converted your Anaplan certificate to PEM format, and that you know the
# Anaplan account email associated with that certificate.

# This script uses Python 3 and assumes that you have the following modules
# installed: requests, base64, json

import requests
import base64
import sys
import json

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert the Anaplan account email being used
username = ''
# Replace with your action metadata
actionData = {
  "id" : "",
  "name" : ""
} 

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

url = (f'https://api.anaplan.com/1/3/workspaces/{wGuid}/models/{mGuid}/' +
       f'actions/{actionData["id"]}/tasks')

postHeaders = {
    'Authorization': user,

    'Content-type': 'application/json',
}

# Runs an action request, and returns metadata to 'postAction.json'
print(url)
action = requests.post(url,
                       data='{"localeName": "en_US"}',
                       headers=postHeaders)

print('Action status code: ' + str(action.status_code))
with open('postAction.json', 'wb') as f:
    f.write(action.text.encode('utf-8'))
