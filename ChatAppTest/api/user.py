from api.base import *
from __future__ import annotations


class User:
    def __init__(self, id, username, permissions, studentclass, avatarurl):
        self.id = id
        self.username = username
        self.permissions = permissions
        self.studentclass = studentclass
        self.avatarurl = avatarurl

    @staticmethod
    def get_avatar(userid: int):
        """Gets the avatar of the user by its id

        Args:
            userid (int): The user id

        Returns:
            str: The avatar data
        """
        cursor.execute("SELECT avatar FROM chatusers WHERE Id=%s;", (userid,))
        if cursor.rowcount == 0:
            return None
        else:
            data = cursor.fetchone()[0]
            return data

    @staticmethod
    def set_avatar(userid: int, avatardata):
        """Sets the avatar for the user to the avatar data

        Args:
            userid (int): The user id
            avatardata ([type]): The avatar binary data
        """
        cursor.execute("UPDATE chatusers SET avatar = %s WHERE Id = %s;", (avatardata, userid))
        db.commit()

    @staticmethod
    def get_user(userid: int) -> User:
        """Gets a user by its id

        Args:
            userid (int): The user id

        Returns:
            User: The user if found, else None
        """
        cursor.execute("SELECT * FROM chatusers WHERE id = %s", (userid,))
        if cursor.rowcount == 0:
            return None
        else:
            res = cursor.fetchone()
            user = User(res[0], res[1], res[3], res[4], f"/users/{userid}/avatar")
            return user
