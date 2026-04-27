from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token = 'YOUR_ACCESS_TOKEN'

# create an instance of the API class
api_instance = swagger_client.ActivitiesApi()
name = name_example # String | The name of the activity.
sportType = sportType_example # String | Sport type of activity. For example - Run, MountainBikeRide, Ride, etc.
#startDateLocal = 2013-10-20T19:20:30+01:00 # Date | ISO 8601 formatted date time.
elapsedTime = 56 # Integer | In seconds.
type = type_example # String | Type of activity. For example - Run, Ride etc. (optional)
description = description_example # String | Description of the activity. (optional)
distance = 3.4 # Float | In meters. (optional)
trainer = 56 # Integer | Set to 1 to mark as a trainer activity. (optional)
commute = 56 # Integer | Set to 1 to mark as commute. (optional)

try: 
    # Create an Activity
    api_response = api_instance.createActivity(name, sportType, startDateLocal, elapsedTime, type=type, description=description, distance=distance, trainer=trainer, commute=commute)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->createActivity: %s\n" % e)