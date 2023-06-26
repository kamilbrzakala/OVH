import json
import csv
import ovh

# First step
application_key = 'xxx'
application_secret = 'xxx'
consumer_key = 'xxx'


# First function
def get_dedicatedCloud(applicationkey, applicationsecret, consumerkey):
    client = ovh.Client(
        endpoint='ovh-eu',
        application_key=applicationkey,
        application_secret=applicationsecret,
        consumer_key=consumerkey
    )

    result = client.get("/dedicatedCloud")
    return json.dumps(result, indent=4)

# Second function
def get_dedicatedCloud_ServiceName_Users(applicationkey, applicationsecret, consumerkey, serviceName):
    client = ovh.Client(
        endpoint='ovh-eu',
        application_key=applicationkey,
        application_secret=applicationsecret,
        consumer_key=consumerkey
    )

    result = client.get("/dedicatedCloud/" + serviceName + "/user")
    return json.dumps(result, indent=4)

# Third function
def get_dedicatedCloud_ServiceName_User(applicationkey, applicationsecret, consumerkey, serviceName, userId):
    client = ovh.Client(
        endpoint='ovh-eu',
        application_key=applicationkey,
        application_secret=applicationsecret,
        consumer_key=consumerkey
    )
    
    result = client.get("/dedicatedCloud/" + serviceName + "/user/" + userId)
    return json.dumps(result, indent=4)

# Fourth function
def get_identities(applicationkey, applicationsecret, consumerkey):
    # Retrieve OVH CloudManager users
    # https://api.ovh.com/console-preview/?section=%2Fme&branch=v1#get-/me/identity/user
    
    client = ovh.Client(
        endpoint='ovh-eu',
        application_key=applicationkey,
        application_secret=applicationsecret,
        consumer_key=consumerkey
    )
    
    result = client.get("/me/identity/user")
    return result

# Fifth function
def get_identity(applicationkey, applicationsecret, consumerkey, userId):
    # Get object's properties
    # https://api.ovh.com/console-preview/?section=%2Fme&branch=v1#get-/me/identity/user/-user-
    
    client = ovh.Client(
        endpoint='ovh-eu',
        application_key=applicationkey,
        application_secret=applicationsecret,
        consumer_key=consumerkey
    )
    
    result = client.get("/me/identity/user/" + userId)
    return json.dumps(result, indent=4)

# First step
# Get API Vcenter Users
# Get first function's result

result_first = get_dedicatedCloud(application_key, application_secret, consumer_key)
ids = json.loads(result_first)

# Second step
users_data = []
column_order = [
    "name",
    "receiveAlerts",
    "canManageNetwork",
    "phoneNumber",
    "state",
    "login",
    "fullAdminRo",
    "canManageRights",
    "canManageIpFailOvers",
    "type",
    "activationState",
    "userId",
    "activeDirectoryType",
    "nsxRight",
    "lastName",
    "activeDirectoryId",
    "isTokenValidator",
    "identityProviderId",
    "email",
    "encryptionRight",
    "firstName",
    "isEnableManageable"
]
# loop through first function's result

for item in ids:
    print("looping through Cloud: "+ item)
    serviceName = item
    
    # Get Second function's result
    result_second = get_dedicatedCloud_ServiceName_Users(application_key, application_secret, consumer_key, serviceName)
    user_ids = json.loads(result_second)
    
    # loop through second function's result
    for userId in user_ids:
        print("looping through userId: "+ str(userId))
        
        # Get third function's result
        result_third = get_dedicatedCloud_ServiceName_User(application_key, application_secret, consumer_key, serviceName, str(userId))
        
        user_data = json.loads(result_third)
        ordered_user_data = {key: user_data[key] for key in column_order}
        users_data.append(ordered_user_data)
        

# Fourth step
fieldnames = [
    "login",
    "identityProviderId",
    "userId",
    "activeDirectoryType",
    "fullAdminRo",
    "isTokenValidator",
    "isEnableManageable",
    "name",
    "phoneNumber",
    "canManageIpFailOvers",
    "state",
    "activeDirectoryId",
    "email",
    "nsxRight",
    "encryptionRight",
    "type",
    "lastName",
    "receiveAlerts",
    "canManageNetwork",
    "activationState",
    "firstName",
    "canManageRights"
]

# save result from third function to excel
print("Saving API VCenter Users to excel")
with open("API_VCenter_Users.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for user_data in users_data:
        writer.writerow(user_data)


# Fifth step

# Pull OVH CloudManager Users

identities_data = []
# Define the column order for CSV
column_order_ids = [
    "status",
    "lastUpdate",
    "login",
    "creation",
    "description",
    "email",
    "group",
    "passwordLastUpdate"
]

# Retrieve identities using fourth function
identities_json = get_identities(application_key, application_secret, consumer_key)

for identity in identities_json:
    print("Looping through OVH CloudManager User: " + identity)

    # Get fifth function's result
    result_fifth = get_identity(application_key, application_secret, consumer_key, identity)
    identity_data = json.loads(result_fifth)
    
    
    ordered_id_data = {key: identity_data[key] for key in column_order_ids}
    identities_data.append(ordered_id_data)
    
print("Saving OVH CloudManager Users to excel")
with open("OVH_CloudManager_Users.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=column_order_ids)
    writer.writeheader()
    for identity_data in identities_data:
        writer.writerow(identity_data)
