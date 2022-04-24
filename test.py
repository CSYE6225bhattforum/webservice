car = {'Item': 
        {'messageSent': 'Yes',
         'ttl': '22-04-17T23:20:42',
          'username': 'pankti.ra@gmail.com',
           'token': 'ad2964cc-7aff-4669-bfa1-7fdde1bee214',
            'messageType': 'Email'},
        'ResponseMetadata':
             {'RequestId': 'DCPU6GL85VR6L2PQGL1QLSA83FVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 17 Apr 2022 23:16:12 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '188', 'connection': 'keep-alive', 'x-amzn-requestid': 'DCPU6GL85VR6L2PQGL1QLSA83FVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3687994149'}, 'RetryAttempts': 0}}

x = car.get("Item", {})
y = x.get("token")
print(y)

import datetime
import time
date_obj = datetime.datetime.now() + datetime.timedelta(minutes=5)
unixtime2 = time.mktime(date_obj.timetuple())
print(type(unixtime2))
print("Timestamp of now: ", str(unixtime2)[0:10])