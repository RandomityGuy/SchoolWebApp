import mysql.connector
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

db = mysql.connector.connect(host=host, user=user, password=pwd, database="chatdb")
cursor = db.cursor(buffered=True)
snowflakegen = snowflake.generator(1, 1)


class ToDictable:
    def toDict(self):
        return {}
