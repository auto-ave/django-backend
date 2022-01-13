import boto3
import requests
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat
from urllib.request import urlopen
import json

KEY = "AKIAVFDW7UCVKEHHNJBO"
SECRET = "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"
BUCKET = "autoave-backend-staticfiles"

from io import BytesIO
def send_image_to_s3(url, name):
    print("sending image")
    bucket_name = BUCKET
    AWS_SECRET_ACCESS_KEY = SECRET
    AWS_ACCESS_KEY_ID = KEY

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    response = requests.get(url)
    img = BytesIO(response.content)

    file_name = f'population_data/{name}'
    r = s3.upload_fileobj(img, bucket_name, file_name)
    print(r)

    return 'https://cdn.autoave.in/' + file_name

with open('./common/data_population/vehicle_brands.json') as f:
    data = json.load(f)
    count = 0
    for item in data:
        url = item['image']
        url = url.strip().split('?')[0]
        name = url.strip().split('/')[-1]
        s3_path = send_image_to_s3(url, name)
        print('after: ', s3_path)
        item['image'] = s3_path
        count = count + 1
    print('count: ', count)
    print(data)
 