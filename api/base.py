from pymysql.connections import Connection
import pymysql.cursors;
import pymysql;
import snowflake
import json

user = None
host = None
pwd = None

with open("config.json") as f:
    config = json.loads(f.read())
    user = config["user"]
    host = config["host"]
    pwd = config["password"]

db: Connection = None;
global_cursor: pymysql.cursors.Cursor = None;
snowflakegen = snowflake.generator(1, 1)

def connect():
    global db;
    db = pymysql.connect(host=host, user=user, password=pwd, database="chatdb", cursorclass=pymysql.cursors.DictCursor)
    return db;


def reset_cursor():
    global db, global_cursor;
    global_cursor.close();
    db.close();
    db = pymysql.connect(host=host, user=user, password=pwd, database="chatdb", cursorclass=pymysql.cursors.DictCursor)
    global_cursor = db.cursor()
class ToDictable:
    def toDict(self):
        return {}
