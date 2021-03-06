from api.base import *
from api.auth import Auth
from api.permissions import Permissions


class Announcement(ToDictable):
    def __init__(self, id, creator, byclass, content):
        self.id = id
        self.creator = creator
        self.byclass = byclass
        self.content = content

    def ToDict(self):
        return {"id": self.id, "creator": self.creator, "class": self.byclass, "content": self.content}


class Announcements:
    @staticmethod
    def make_announcement(user: str, destclass: str, text: str) -> int:
        """Creates an announcement for the specified class

        Args:
            user (int): The user creating the announcement
            destclass (str): The specified class
            text (str): The announcement contents

        Returns:
            int: The announcement id, if the announcement was successfully created
        """
        with DBConnection() as (cursor, conn):
            perms = Auth.get_permissions(user)
            if Permissions.has_permission(perms, Permissions.MANAGE_ANNOUNCE):
                id = snowflakegen.__next__()
                cursor.execute("INSERT INTO announcements VALUES(%s,%s,%s,%s);", (id, user, destclass, text))
                conn.commit()
                return id
            else:
                return False

    @staticmethod
    def revoke_announcement(user: str, announcementid: str) -> bool:
        """Delete an announcement specified by its id

        Args:
            user (int): The user id who revokes the announcement
            announcementid (int): The announcement id

        Returns:
            bool: True if success
        """
        with DBConnection() as (cursor, conn):
            perms = Auth.get_permissions(user)
            if Permissions.has_permission(perms, Permissions.MANAGE_ANNOUNCE):
                print(announcementid);
                cursor.execute("DELETE FROM announcements WHERE id = %s;", (announcementid,))
                conn.commit()
                return True
            else:
                return False

    @staticmethod
    def get_announcements_by_user(user: int) -> list[Announcement]:
        """Gets a list of announcements for the user

        Args:
            user (int): The user id

        Returns:
            list[Announcement]: The list of announcements
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT a.id,c.username,a.class,a.content FROM announcements as a,chatusers as b,chatusers as c WHERE b.class = a.class && b.id = %s && c.id=a.byuser;", (user,))
            res = cursor.fetchall()
            L = []
            for result in res:
                L.append(Announcement(str(result['id']), result['username'], result['class'], result['content']))

            conn.commit();
            return L

    @staticmethod
    def get_announcements_by_class(userclass: str) -> list[Announcement]:
        """Gets a list of announcements for the class

        Args:
            userclass (str): The class

        Returns:
            list[Announcement]: The list of announcements
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT DISTINCT a.id,b.username,a.class,a.content FROM announcements as a,chatusers as b WHERE a.class = %s && a.byuser = b.id;", (userclass,))
            L = []
            for result in cursor.fetchall():
                L.append(Announcement(str(result['id']), result['username'], result['class'], result['content']));

            conn.commit();
            return L
