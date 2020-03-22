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


def getDevicesExposed(deviceId,cursor) :
    cursor.execute(f"""
        select distinct dl3.device_id as notifyDeviceId
        from 
        contact_tracer.device_location dl 
        join lateral 
        (
            select * from contact_tracer.device_location where device_id != dl.device_id and postgis.ST_DistanceSphere(location,dl.location) < 10
            and abs(dl.sample_date - sample_date) <= interval '1 hour'
            ) dl3 on true 
            where dl.device_id  = '{deviceId}'
            and dl.sample_date > now() - interval '14 days';
        """)
    return [row[0] for row in cursor.fetchall()]


def postInfected(event, context):
    # get db connection
    print(f"processing infected {event}")
    conn = make_conn()
    cursor = conn.cursor()
    infectionDate = event['body']['infectionDate']
    infectedDeviceId = event['body']['deviceId']
    # set the user to infected
    cursor.execute(
        f"update contact_tracer.device set infected = true, infected_date = '{infectionDate}' where device_id = '{infectedDeviceId}'; ")
    # get all devices that need to be notified
    deviceIdsToNotify = getDevicesExposed(event['deviceId'],cursor)
    print(f"the following devices need to be notified : {deviceIdsToNotify}")
    # send notification for each
    for deviceId in deviceIdsToNotify:
        notifyDevice(deviceId, i18n.t("wording.infected-notification-title"), i18n.t("wording.infected-notification-body"))

    cursor.execute(
        f"update contact_tracer.device set notification_sent = true where device_id = '{infectedDeviceId}'; ")
    # get all devices that need to be notified

    body = {
        "message": "POST /infected endpoint logic! Your function executed successfully!",
        "input": event,
    }
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def getDeviceRisk(event, context):
    conn = make_conn()
    cursor = conn.cursor()
    deviceId = event['body']['deviceId']
    body = {
        "deviceId": deviceId,
        "score": getLatestDeviceScore(deviceId, cursor)
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response


def calculateScore(deviceId, cursor):
    exposedDevices = getDevicesExposed(deviceId, cursor)
    if not exposedDevices:
        return 1
    if len(exposedDevices) == 1:
        return 2
    if len(exposedDevices) > 1:
        return 3


def getLatestDeviceScore(deviceId, cursor):
    cursor.execute(f"select score from contact_tracer.device_risk where device_id = '{deviceId}';")
    row = cursor.fetchone()
    return row[0] if row else None


def calculatRiskScores(event, context):
    # get all devices
    conn = make_conn()
    cursor = conn.cursor()
    cursor.execute("select device_id from contact_tracer.device order by latest_sample desc;")
    devicesResponse = cursor.fetchall()
    # iterate over them, calculate the device score, if available get the previous score
    for row in devicesResponse :
        deviceId = row[0]
        score = calculateScore(deviceId, cursor)
        prevScore = getLatestDeviceScore(deviceId, cursor)
        if prevScore:
            # if the score changed send a notification
            if score != prevScore :
                notifyDevice(deviceId, i18n.t("wording.score-changed-title"), i18n.t("wording.score-changed-body"))
        # upsert the updated score
        cursor.execute(
            f"insert into contact_tracer.device_risk(device_id ,score ,last_calculated ) values('{deviceId}',{score},now()) on conflict(device_id) do update set score =EXCLUDED.score, last_calculated = EXCLUDED.last_calculated;")

    return "done"
