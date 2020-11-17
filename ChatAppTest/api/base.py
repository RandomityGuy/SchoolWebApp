import mysql.connector
import snowflake

db = mysql.connector.connect(user="root", password="qwertyuiop", database="chatdb")
cursor = db.cursor(buffered=True)
# type: db.cursor
snowflakegen = snowflake.generator(1, 1)


class ToDictable:
    def toDict(self):
        return {}
