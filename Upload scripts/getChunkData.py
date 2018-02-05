# This script returns the metadata for each chunk in a file to a json array
# saved in file 'chunkData.json'.

# This script assumes you know the workspaceGuid, modelGuid, and fileID for the
# file you want to check. If you do not know this information, please run
# 'getWorkspaces.py', 'getModels.py', and 'getFiles.py' respectively.

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
# Insert your file ID
fileID = ''
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

getChunkData = requests.get('https://api.anaplan.com/1/3/workspaces/' +
                            f'{wGuid}/models/{mGuid}/files/{fileID}' +
                            '/chunks',
                            headers=getHeaders)

with open('chunkData.json', 'wb') as f:
    f.write(getChunkData.text.encode('utf-8'))
