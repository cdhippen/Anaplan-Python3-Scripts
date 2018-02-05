# This script downloads a file in chunks. It will write all chunks to a newly
# created local file with the same name as the file. It will also write all
# chunk metadata to a file 'downloadChunkData.json'.

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
import json

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert your fileID
fileID = ''
# Insert your fileName
fileName = ''
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

url = (f'https://api.anaplan.com/1/3/workspaces/{wGuid}/models/{mGuid}/' +
       f'files/{fileID}/chunks')

getHeaders = {
    'Authorization': user
}

downloadHeaders = {
    'Authorization': user,

    'Accept': 'application/octet-stream'
}

getChunkData = requests.get(url,
                            headers=getHeaders)
with open('downloadChunkData.json', 'wb') as f:
    f.write(getChunkData.text.encode('utf-8'))

with open('downloadChunkData.json', 'r') as f:
    f2 = json.load(f)

with open(f'{fileName}', 'wb') as f:
    for i in f2:
        chunkData = i
        chunkID = i['id']
        print(f'Getting chunk {chunkID}')
        getChunk = requests.get(url + f'/{chunkID}',
                                headers=downloadHeaders)
        f.write(getChunk.content)
        print('Status code: ' + str(getChunk.status_code))
