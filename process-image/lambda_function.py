import json, boto3, psycopg2
from datetime import datetime


def lambda_handler(event, context):
    img_src = event["Records"][0]["s3"]["object"]["key"]
    client = boto3.client('rekognition')
    response = client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': 'hackaway2020',
                    'Name': img_src
                }
            }
        )
    detected_objects = []
    
    for label in response["Labels"]:
        if len(label["Instances"]) > 0:
            item = {
                "label_name": label["Name"],
                "bounding_box": json.dumps(label["Instances"][0]["BoundingBox"]),
                "confidence": label["Confidence"]
            }
            
            detected_objects.append(item)

    psql_save(img_src, detected_objects)
    

    return {
        'statusCode': 200,
    }

def psql_save(img_src, detected_objects):
    try:
        conn = psycopg2.connect(host="hackawaydb.c8pcgo7bynyp.eu-west-2.rds.amazonaws.com", database="hackawaydb", user="postgres", password="seLYXH0File2HyParm4q")
        cur = conn.cursor()
        sql = "INSERT INTO event(created, img_src) VALUES(%s,%s) RETURNING id"
        cur.execute(sql, (datetime.now(), img_src,))
        
        event_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()