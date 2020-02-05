import boto3
from botocore.exceptions import ClientError
import logging
import config
import os

def upload_image(image_filename):
    print("Uploading image...")
    s3_client = boto3.client('s3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY)
    try:
        response = s3_client.upload_file(image_filename, "hackaway2020", image_filename, ExtraArgs={'ContentType': 'image/png'})
    except ClientError as e:
        logging.error(e)
        print("---_______---")
        return False
    print("Remove file:", image_filename)
    os.remove(image_filename)
    return True

def main():
    response = upload_image("linus.jpg")
    if response:
        print("yeet")

if __name__ == '__main__':
    main()
