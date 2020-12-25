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

cursor: pymysql.cursors.Cursor = None;
conn: Connection = None;

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


def api_func(func):
    def inner(*args, **kwargs):
        conn = connect();
        retval = None;
        with conn.cursor() as cursor:
            g = func.__globals__

            conn_sentinel = object()
            cursor_sentinel = object()
            old_conn = g.get('conn', conn_sentinel)
            old_cursor = g.get('cursor', conn_sentinel)
            g['conn'] = conn;
            g['cursor'] = cursor;
            try:
                retval = func(*args, **kwargs);
            finally:
                if old_conn is conn_sentinel:
                    del g['conn']
                else:
                    g['conn'] = old_conn

                if old_cursor is cursor_sentinel:
                    del g['cursor']
                else:
                    g['cursor'] = old_cursor

        if conn.open:
            conn.close();
        return retval;
    return inner;

