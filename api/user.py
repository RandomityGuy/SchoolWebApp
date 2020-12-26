from __future__ import annotations
from os import curdir
from api.base import *


class User(ToDictable):
    def __init__(self, id, username, permissions, studentclass, avatarurl):
        self.id = id
        self.username = username
        self.permissions = permissions
        self.studentclass = studentclass
        self.avatarurl = avatarurl

    def toDict(self):
        D = {}
        D["id"] = str(self.id)
        D["username"] = self.username
        D["class"] = self.studentclass
        D["avatar-url"] = self.avatarurl
        D["permissions"] = self.permissions
        return D

    @staticmethod
    def get_avatar(userid: int):
        """Gets the avatar of the user by its id

        Args:
            userid (int): The user id

        Returns:
            str: The avatar data
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT avatar FROM chatusers WHERE Id=%s;", (userid,))
            if cursor.rowcount == 0:
                return None
            else:
                data = cursor.fetchone()['avatar']
                return data

    @staticmethod
    def set_avatar(userid: int, avatardata):
        """Sets the avatar for the user to the avatar data

        Args:
            userid (int): The user id
            avatardata ([type]): The avatar binary data
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("UPDATE chatusers SET avatar = %s WHERE Id = %s;", (avatardata, userid))
            conn.commit()

    @staticmethod
    def get_user(userid: int) -> User:
        """Gets a user by its id

        Args:
            userid (int): The user id

        Returns:
            User: The user if found, else None
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM chatusers WHERE id = %s", (userid,))
            if cursor.rowcount == 0:
                return None
            else:
                res = cursor.fetchone()
                user = User(res['Id'], res['Username'], res['permissions'], res['class'], f"api/users/{userid}/avatar")
                return user

    @staticmethod
    def modify_user(userid: int, username: str = None, permissions: int = None, studentclass: str = None):
        """Modifies a user's properties

        Args:
            userid (int): The user id whose properties have to be changed
            username (str, optional): The new username. Defaults to None.
            permissions (int, optional): The new permissions. Defaults to None.
        """
        with DBConnection() as (cursor, conn):
            if username != None:
                cursor.execute("UPDATE chatusers SET username=%s WHERE id=%s;", (username, userid))
            if permissions != None:
                cursor.execute("UPDATE chatusers SET permissions=%s WHERE id=%s;", (permissions, userid))
            if studentclass != None:
                cursor.execute("UPDATE chatusers SET class=%s WHERE id=%s;", (studentclass, userid))
            conn.commit()

    @staticmethod
    def delete_user(userid: int):
        """Deletes a user by its id

        Args:
            userid (int): The user id
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("DELETE FROM chatusers WHERE id=%s;", (userid,))
            conn.commit()

    @staticmethod
    def get_details(userid: int) -> str:
        """Gets the JSON user details for a user

        Args:
            userid (int): the user id

        Returns:
            str: the JSON details
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT data FROM userdetails WHERE userid=%s;",(userid,));
            if cursor.rowcount == 0:
                return "{}";
            data = cursor.fetchone()['data'];
            return data;

    @staticmethod
    def set_details(userid: int, details: str):
        """Sets the JSON user details for a user

        Args:
            userid (int): The user id
            details (str): the JSON user details
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT 1 FROM userdetails WHERE userid=%s;",(userid,));
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO userdetails VALUES(%s,%s,%s);",(snowflakegen.__next__(),userid,details));
            else:
                cursor.execute("UPDATE userdetails SET details=%s WHERE userid=%s;",(details,userid));
            conn.commit();
