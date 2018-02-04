# This script deletes the contents of the selected file. Note: This only
# removes private content. Default content and the import data source model
# object remain.

# This script assumes you know your workspaceGuid, modelGuid, and file ID
# If you do not have this information, please run 'getWorkspaces.py',
# 'getModels.py', and 'getFiles.py' and retrieve this information from the
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

# Replace with your workspace Guid
wGuid = ''
# Replace with your model Guid
mGuid = ''
# Replace with your file ID
fileID = ''
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

url = (f'https://api.anaplan.com/1/3/workspaces/{wGuid}/models/{mGuid}/' +
       f'files/{fileID}')

getHeaders = {
    'Authorization': user,

    'Content-type': 'application/json',
}

print(f'Deleting file')
delete = requests.delete(url,
                         headers=getHeaders)
print('File delete status code: ' + str(delete.status_code))
