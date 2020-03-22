import json
import os
import psycopg2

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_SCHEMA = os.environ["DB_SCHEMA"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]


def make_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            f"dbname={DB_NAME} user={DB_USER} host={DB_HOST} password={DB_PASS}  options='-c search_path={DB_SCHEMA}'"
        )
    except:
        print("I'm unable to connect to the database")
    return conn


def postLocation(event, context):
    payload = json.loads(event["body"])
    device_id = payload["deviceId"]
    sample_date = payload["sampleDate"]
    conn = make_conn()
    cursor = conn.cursor()
    # upsert on device table
    sql_statement = f"INSERT INTO contact_tracer.device (device_id, first_sample, latest_sample) VALUES ('{device_id}', '{sample_date}', '{sample_date}) ON CONFLICT (deviceId) DO UPDATE SET latest_sample = '{sample_date}' WHERE deviceId='{device_id}'"
    print(sql_statement)
    cursor.execute(sql_statement)
    # insert into device_location_table
    point_str = f"'POINT({payload['longitude']} {payload['latitude']})'"
    sql_statement = f"INSERT INTO contact_tracer.device_location (device_id,sample_date,location) VALUES ('{device_id}', '{sample_date}', postgis.ST_PointFromText({point_str}))"
    cursor.execute(sql_statement)
    conn.commit()
    response = {"statusCode": 200}
    return response


def postInfected(event, context):
    body = {
        "message": "POST /infected endpoint logic! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def getDevicesNearInfected(event, context):
    body = {
        "message": "GET /devices-near-infected endpoint logic! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
