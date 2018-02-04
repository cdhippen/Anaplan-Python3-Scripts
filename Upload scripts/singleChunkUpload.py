# This script uploads a file in a single chunk.

# This script assumes you know your workspaceGuid, modelGuid, and file metadata.
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
import string
import os
import json

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert the Anaplan account email being used
username = ''
# Replace with your file metadata
fileData = {
  "id" : "",
  "name" : '',
  "chunkCount" : ,
  "delimiter" : "",
  "encoding" : "",
  "firstDataRow" : ,
  "format" : "",
  "headerRow" : ,
  "separator" : ""
}

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

url = (f'https://api.anaplan.com/1/3/workspaces/{wGuid}/models/{mGuid}/' +
       f'files/{fileData["id"]}')

getHeaders = {
    'Authorization': user,

    'Content-type': 'application/json',
}

putHeaders = {
    'Authorization': user,

    'Accept': 'application/octet-stream'
}

# Opens the data file (filData['name'] by default) and encodes it to utf-8
dataFile = open(fileData['name'], 'r').read()).encode('utf-8')

fileUpload = requests.put(url,
                          headers=putHeaders,
                          data=(dataFile)
if fileUpload.ok:
    print('File Upload Successful.')
else:
    print('There was an issue with your file upload: '
          + str(fileUpload.status_code))
