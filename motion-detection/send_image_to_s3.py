import boto3
from botocore.exceptions import ClientError
import logging
import config

def upload_image(image_filename):
    s3_client = boto3.client('s3',
    aws_access_key_id = config.ACCESS_KEY,
    aws_secret_access_key = config.SECRET_KEY)
    try:
        response = s3_client.upload_file(image_filename, "hackaway2020", image_filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def main():
    response = upload_image("linus.jpg")
    if response:
        print("yeet")

if __name__ == '__main__':
    main()