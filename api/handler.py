import json
import psycopg2

DB_HOST = "db_host"
DB_PORT = "db_port"
DB_NAME = "db_name"
DB_USER = "db_user"
DB_PASS = "db_pass"


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
    response = json.dumps(raw)
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
