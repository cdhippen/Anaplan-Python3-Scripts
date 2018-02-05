# This script writes the metadata for the selected import task to
# importTask.json based on the taskID you select when running the script.

# This script assumes you know your workspaceGuid, modelGuid, and import ID.
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
import json

# Insert your workspace Guid
wGuid = ''
# Insert your model Guid
mGuid = ''
# Insert your import ID
importID = ''
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
       f'imports/{importID}/tasks')

getHeaders = {
    'Authorization': user
}

# Gets all taskIDs associated with the import, and asks which the user wants to
# view the status of
getImportTasks = requests.get(url,
                              headers=getHeaders)

with open('importTasks.json', 'wb') as f:
    f.write(getImportTasks.text.encode('utf-8'))

with open('importTasks.json', 'r') as f:
    f2 = json.load(f)

count = 0
for i in f2:
    print(f'This task is at index {count}')
    print(i)
    print('\n')
    count += 1

x = f2[int(input('Enter the index for the task you would like to view: '))]
i = x['taskId']

# Puts the task metadata into 'importStatus.json'
importStatus = requests.get(url + f'/{i}',
                          headers=getHeaders)

with open('importStatus.json', 'wb') as f:
    f.write(importStatus.text.encode('utf-8'))


# Loads the status file, and reports status as well as writing any failure
# dump to a csv
with open('importStatus.json', 'r') as f:
    f2 = json.load(f)
    
if f2['taskState'] != "COMPLETE":
    print('In progress. See "importStatus.json"')
    print('Progress: ' + str(f2['progress']))
    print('Task Status: ' + f2['taskState'])
elif f2['result']['failureDumpAvailable']:
    print('Failure dump available. Writing to "importDump.csv"')
    getFailDump = requests.get(url + f'/{i}/dump',
                               headers=getHeaders)
    print(getFailDump.status_code)
    with open('importDump.csv', 'wb') as f:
        f.write(getFailDump.text.encode('utf-8'))
    print('Task Status: ' + f2['taskState'])
else:
    print('No failures')
    print('Task Status: ' + f2['taskState'])
