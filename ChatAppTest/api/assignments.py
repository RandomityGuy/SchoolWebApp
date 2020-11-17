from datetime import date
from api.base import *
import datetime


class AssignmentInfo:
    def __init__(self, id: int, assignmentid: int, userid: int, status: int, attachment):
        self.id = id
        self.assignmentid = assignmentid
        self.userid = userid
        self.status = status
        self.attachment = attachment


class Assignment:
    NOT_SUBMITTED = 0
    UPLOADED = 1
    COMPLETE = 2
    INCOMPLETE = 3

    def __init__(self, id: int, studentclass: str, content: str, duedate: date, attachment=None):
        self.id = id
        self.studentclass = studentclass
        self.content = content
        self.duedate = duedate
        self.attachment = attachment

    @staticmethod
    def create_assignment(studentclass: str, content: str, duedate: datetime.date, attachment=None) -> int:
        """Creates an assignment for the given class of contents and due date with optional attachment

        Args:
            studentclass (str): The target class
            content (str): The content of the assigment, can be a short description as well
            duedate (datetime.date): The due date of the assigment
            attachment ([type], optional): The attachment. Defaults to None.

        Returns:
            int: The assigment id
        """
        id = snowflakegen.__next__()
        cursor.execute("INSERT INTO assignments VALUES(%s,%s,%s,%s,%s)", (id, studentclass, content, attachment, duedate.isoformat()))
        db.commit()
        return id

    @staticmethod
    def upload_assignment(userid: int, assignmentid: int, attachment):
        """Submit an assigment

        Args:
            userid (int): The user submitting the assigment
            assignmentid (int): The assigment id
            attachment ([type]): The attachment

        Returns:
            [type]: True if success
        """
        cursor.execute("SELECT id FROM assignments WHERE (submission > CURDATE() && id == %s);", (assignmentid,))
        if cursor.rowcount == 0:
            return False
            # You uploaded it too late
        cursor.execute("INSERT INTO assignmentinfo VALUES(%s,%s,%s,%s,%s);", (snowflakegen.__next__(), assignmentid, userid, 0, Assignment.UPLOADED, attachment))
        db.commit()
        return True

    @staticmethod
    def mark_complete(assignmentinfoid: int):
        """Mark a given assigment by the student as complete

        Args:
            assignmentinfoid (int): The assigment info id
        """
        cursor.execute("UPDATE assignmentinfo SET status=2 WHERE id = %s;", (assignmentinfoid,))
        db.commit()

    @staticmethod
    def mark_incomplete(assignmentinfoid: int):
        """Mark a given assigment by the student as incomplete

        Args:
            assignmentinfoid (int): The assigment info id
        """
        cursor.execute("UPDATE assignmentinfo SET status=3 WHERE id = %s;", (assignmentinfoid,))
        db.commit()

    @staticmethod
    def mark_status(assignmentinfoid: int, status: int):
        """Mark a given assigment by the student as given status

        Args:
            assignmentinfoid (int): The assigment info id
            status (int): The status code of the assigment
        """
        cursor.execute("UPDATE assignmentinfo SET status=%s WHERE id = %s;", (status, assignmentinfoid))
        db.commit()

    @staticmethod
    def get_assignment(assignmentid: int):
        """Gets an assignment by its id

        Args:
            assignmentid (int): The assigment id

        Returns:
            Assignment: The assigment if success
        """
        cursor.execute("SELECT * FROM assignments WHERE id = %s;", (assignmentid,))
        if cursor.rowcount == 0:
            return None
        res = cursor.fetchone()
        assignment = Assignment(res[0], res[1], res[2], res[4], res[3])
        return assignment

    @staticmethod
    def get_assignments_for_class(studentclass: str) -> list:
        """Gets an assignment by the class

        Args:
            studentclass (str): The class

        Returns:
            list: The list of assigments
        """
        cursor.execute("SELECT * FROM assignments WHERE class = %s;", (studentclass,))
        L = []
        for (id, studentclass, content, attachment, submission) in cursor:
            L.append(Assignment(id, studentclass, content, submission, attachment))
        return L

    @staticmethod
    def get_submitted_assignments(assignmentid: int) -> list[AssignmentInfo]:
        """Gets a list of submitted assigment data

        Args:
            assignmentid (int): The assigment id

        Returns:
            list[AssignmentInfo]: The submitted assigment data
        """
        cursor.execute("SELECT * FROM assignmentinfo WHERE assignmentid = %s;", (assignmentid,))
        L = []
        for (id, aid, userid, status, attachment) in cursor:
            L.append(AssignmentInfo(id, aid, userid, status, attachment))
        return L
