# This script uploads a file in chunks. If the upload fails at any point,
# rerunning the script will pick up from the last successful chunk.

# This script assumes you know your workspaceGuid, modelGuid, and file metadata.
# If you do not have this information, please run 'getWorkspaces.py',
# 'getModels.py', and 'getFiles.py' and retrieve this information from the
# resulting json files.

# This script assumes that you have already split your file into chunks.
# IMPORTANT: Script only works if file was split with 'split' terminal command.

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
# Insert the file prefix used when the file was split.
chunkFilePrefix = ''
# Set chunkCount value to number of chunks you will be uploading, or to -1 if
# you do not know the number of chunks you will be uploading. Replace the rest
# with your file metadata
fileData = {
  'id' : '',
  'name' : '',
  'chunkCount' : ,
  'delimiter' : '',
  'encoding' : '',
  'firstDataRow' : ,
  'format' : '',
  'headerRow' : ,
  'separator' : ''
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

postCountHeaders = {
    'Authorization': user,

    'Content-type': 'application/json'
}

postHeaders = {
    'Authorization': user,

    'Content-Type': 'application/json'
}

putHeaders = {
    'Authorization': user,

    'Content-Type': 'application/octet-stream'
}

startFrom = ''
if os.path.isfile('chunkStop.txt'):
    startFrom = open('chunkStop.txt', 'r').read()
else:
    postChunkCount = requests.post(url,
                                   headers=postCountHeaders,
                                   json=fileData)

# Generates the chunk file names based on chunk count
filenames = {}
chunkNumber = 0
for i in string.ascii_lowercase:
    for x in string.ascii_lowercase:
        chunkName = f'{chunkFilePrefix}{i}{x}'
        if os.path.exists(chunkName) and not startFrom:
            filenames[chunkNumber] = chunkName
        elif os.path.exists(chunkName) and startFrom:
            if startFrom >= chunkName:
                pass
            else:
                filenames[chunkNumber] = chunkName
        chunkNumber += 1

# Posts each chunk to the server, starting at the last successful chunk
for i in range((sorted(filenames.keys())[-1])+1):
    try:
        with open(filenames[i], 'r') as dataFile:
            data = dataFile.read()
        print(url + f'/chunks/{i}')
        print(filenames[i])
        putChunk = requests.put(url + f'/chunks/{i}',
                                headers=putHeaders,
                                data=data)
        if putChunk.ok:
            print('Chunk successfully uploaded.')
            with open('chunkStop.txt', 'w') as chunkStop:
                chunkStop.write(filenames[i])
        elif putChunk.status_code != 204:
            print('Status Code: ' + str(putChunk.status_code))
            print('There was an issue with your upload')
            print('If your connection was interrupted,' +
                  'please run the script again when your' +
                  'connection is restored.')
            sys.exit()
    except KeyError:
        pass

markComplete = requests.post(url + '/complete',
                             headers=postHeaders,
                             json=fileData)
if markComplete.ok:
    os.remove('chunkStop.txt')
