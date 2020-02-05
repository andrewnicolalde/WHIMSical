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
            if item["label_name"] != "Person":
                detected_objects.append(item)

    print("Detected Items: " + json.dumps(detected_objects))
    missing_items = compare_recent(detected_objects)
    print("Missing Items: " + json.dumps(missing_items))
    
    psql_save(img_src, detected_objects, missing_items)
    

    return {
        'statusCode': 200,
    }

def psql_save(img_src, detected_objects, missing_items):
    try:
        conn = psycopg2.connect(host="hackawaydb.c8pcgo7bynyp.eu-west-2.rds.amazonaws.com", database="hackawaydb", user="postgres", password="seLYXH0File2HyParm4q")
        cur = conn.cursor()
        sql_event = "INSERT INTO wims_event(created, img_src) VALUES(%s,%s) RETURNING id"
        cur.execute(sql_event, (datetime.now(), img_src,))
        
        event_id = cur.fetchone()[0]
        
        sql_item = "INSERT INTO wims_item(event_id, label, confidence, box) VALUES (%s, %s, %s, %s)"
        
        
        for object in detected_objects:
            cur.execute(sql_item, (event_id, object["label_name"], object["confidence"], object["bounding_box"]))
            
        sql_missing = "INSERT INTO wims_missing_items(label, event_id) VALUES (%s, %s)"
        
        for item in missing_items:
            cur.execute(sql_missing, (item, event_id))
        
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def compare_recent(detected_objects):
    try:
        conn = psycopg2.connect(host="hackawaydb.c8pcgo7bynyp.eu-west-2.rds.amazonaws.com", database="hackawaydb", user="postgres", password="seLYXH0File2HyParm4q")
        cur = conn.cursor()
        
        latest_items_sql = "SELECT label FROM wims_item WHERE wims_item.event_id = (SELECT  wims_event.id FROM wims_event ORDER BY created DESC LIMIT 1);"
        
        cur.execute(latest_items_sql)
        items = cur.fetchall()
        
        conn.commit()
        cur.close()
        conn.close()
        item_labels = [item[0] for item in items]
        detected_object_labels = [item['label_name'] for item in detected_objects]
        
        missing_items = [label for label in item_labels if label not in detected_object_labels]
        
        return missing_items
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def remove_on_no_change(img_src):
    print(img_src)
    s3 = boto3.resource("s3")
    object = s3.Object("hackaway2020", img_src)
    object.delete()