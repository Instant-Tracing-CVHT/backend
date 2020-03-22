import json
import os
import psycopg2
import requests
import i18n
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]

EXPO_PUSH_ENDPOINT = "https://exp.host/--/api/v2/push/send"

i18n.set('locale', 'en')
i18n.load_path.append('./config/translations')


def notifyDevice(deviceId, title, body):
    print(f"notifying {deviceId} with {title}|{body}")
    response = requests.post(EXPO_PUSH_ENDPOINT, json={'to': deviceId, 'title': title, 'body': body})
    print(response.content)


def make_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            f"dbname={DB_NAME} user={DB_USER} host={DB_HOST} password={DB_PASS}"
        )
    except:
        print("I'm unable to connect to the database")
    return conn


def postLocation(event, context):
    # body = {
    #     "message": "POST /location endpoint logic. Your function executed successfully!",
    #     "input": event,
    # }

    # response = {"statusCode": 200, "body": json.dumps(body)}
    conn = make_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT datname from pg_database;")
    raw = cursor.fetchall()
    response = {"statusCode": 200, "body": json.dumps(raw)}
    return response


def postInfected(event, context):
    # get db connection
    print(f"processing infected {event}")
    conn = make_conn()
    cursor = conn.cursor()
    # set the user to infected
    cursor.execute(
        f"update contact_tracer.device set infected = true, infected_date = '{event['infectionDate']}' where device_id = '{event['deviceId']}'; ")
    # get all devices that need to be notified
    cursor.execute(f"""
    select distinct dl3.device_id as notifyDeviceId
    from 
    contact_tracer.device_location dl 
    join lateral 
    (
        select * from contact_tracer.device_location where device_id != dl.device_id and ST_DistanceSphere(location,dl.location) < 500
        and abs(dl.sample_date - sample_date) <= interval '1 hour'
        ) dl3 on true 
        where dl.device_id  = '{event['deviceId']}'
        and dl.sample_date > now() - interval '14 days';
    """)

    deviceIdsToNotify = cursor.fetchall()
    print(f"the following devices need to be notified : {deviceIdsToNotify}")
    # send notification for each
    for deviceId in deviceIdsToNotify:
        notifyDevice(deviceId[0], i18n.t("wording.infected-notification-title"), i18n.t("wording.infected-notification-body"))

    cursor.execute(
        f"update contact_tracer.device set notification_sent = true where device_id = '{event['deviceId']}'; ")
    # get all devices that need to be notified

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
