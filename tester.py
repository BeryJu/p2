import logging
import sys
import pprint

import boto3

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)

session = boto3.session.Session()

s3_client = session.client(
    service_name='s3',
    aws_access_key_id='test',
    aws_secret_access_key='e13b33d4ffdf4663a03d5b0e9951271c',
    endpoint_url='http://localhost:8000/s3/',
)

pprint.pprint(s3_client.list_buckets())

# import requests
# from awsauth import S3Auth

# ACCESS_KEY = 'ACCESSKEYXXXXXXXXXXXX'
# SECRET_KEY = 'AWSSECRETKEYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# url = 'http://localhost:8000'
# s = 'Lola is sweet'
# # Creating a file
# r = requests.put(url, data=s, auth=S3Auth(ACCESS_KEY, SECRET_KEY))

# # Downloading a file
# r = requests.get(url, auth=S3Auth(ACCESS_KEY, SECRET_KEY))
# if r.text == 'Lola is sweet':
#     print("It works")
