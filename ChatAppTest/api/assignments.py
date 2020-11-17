from api.base import *
import datetime;

class Assignment:

    @staticmethod
    def create_assignment(class: str, content: str, duedate: datetime.date, attachment = None):
        id = snowflakegen.__next__();
        cursor.execute("INSERT INTO assignments VALUES(%s,%s,%s,%s,%s)",(id,class,content,attachment,duedate.isoformat()));
        db.commit();
        return id;

    @staticmethod
    def upload_assignment(userid: int, assignmentid: int, attachment):
        cursor.execute('SELECT id FROM assignments WHERE (submission > CURDATE() && id == %s);',(assignmentid,));