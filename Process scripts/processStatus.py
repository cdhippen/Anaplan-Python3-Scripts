# This script writes the metadata for the selected process task to
# processTask.json based on the taskID you select when running the script.

# This script assumes you know your workspaceGuid, modelGuid, and process ID.
# If you do not have this information, please run 'getWorkspaces.py',
# 'getModels.py', and 'getProcesses.py' and retrieve this information from the
# resulting json files.

# If you are using certificate authentication, this script assumes you have
# converted your Anaplan certificate to PEM format, and that you know the
# Anaplan account email associated with that certificate.

# This script uses Python 3 and assumes that you have the following modules
# installed: requests, base64, json

import requests
import base64
import json

# Replace with your workspace Guid
wGuid = ''
# Replace with your model Guid
mGuid = ''
# Replace with your process ID
processID = ''
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
       f'processes/{processID}/tasks')

getHeaders = {
    'Authorization': user,

    'Accept': 'application/json'
}

dumpHeaders = {
    'Authorization': user,

    'Content-Type': 'text/csv'
}

# Gets all taskIDs associated with the import, and asks which the user wants to
# view the status of
getProcessTasks = requests.get(url,
                              headers=getHeaders)

with open('processTasks.json', 'wb') as f:
    f.write(getProcessTasks.text.encode('utf-8'))

with open('processTasks.json', 'r') as f:
    f2 = json.load(f)

count = 0
for i in f2:
    print(f'This task is at index {count}')
    print(i)
    print('\n')
    count += 1

x = f2[int(input('Enter the index for the task you would like to view: '))]
i = x['taskId']

# Puts the task metadata into 'processStatus.json'
processStatus = requests.get(url + f'/{i}',
                          headers=getHeaders)

with open('processStatus.json', 'wb') as f:
    f.write(processStatus.text.encode('utf-8'))

# Loads the status file, and reports status as well as writing any failure
# dump to a csv
with open('processStatus.json', 'r') as f:
    f2 = json.load(f)

if f2['taskState'] == 'IN_PROGRESS':
    print('In progress. See "processStatus.json"')
    print('Progress: ' + str(f2['progress']))
    print('Task Status: ' + f2['taskState'])
elif f2['result']['failureDumpAvailable']:
    print('Failure dump available. Writing to "processDump.csv"')
    getFailDump = requests.get(url + f'/{i}/dump',
                               headers=getHeaders)
    with open('processDump.csv', 'wb') as f:
        f.write(getFailDump.text.encode('utf-8'))
    print('Task Status: ' + f2['taskState'])
elif f2['result']['nestedResults'][0]['failureDumpAvailable']:
    print('Failure dump available. Writing to "processDump.csv"')
    objectID = f2['result']['nestedResults'][0]['objectId']
    getFailDump = requests.get(url + f'/{i}/dumps/{objectID}',
                               headers=dumpHeaders)
    with open('processDump.csv', 'wb') as f:
        f.write(getFailDump.text.encode('utf-8'))
    print('Task Status: ' + f2['taskState'])
else:
    print('No failures')
    print('Task Status: ' + f2['taskState'])
