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
    def make_announcement(user: int, destclass: str, text: str) -> int:
        perms = Auth.get_permissions(user)
        if Permissions.has_permission(perms, Permissions.MANAGE_ANNOUNCE):
            id = snowflakegen.__next__()
            cursor.execute("INSERT INTO announcements VALUES(%s,%s,%s,%s);", (id, user, destclass, text))
            db.commit()
            return id
        else:
            return False

    @staticmethod
    def revoke_announcement(user: int, announcementid: int) -> bool:
        perms = Auth.get_permissions(user)
        if Permissions.has_permission(perms, Permissions.MANAGE_ANNOUNCE):
            id = snowflakegen.__next__()
            cursor.execute("DELETE FROM announcements WHERE id = %s;", (announcementid,))
            db.commit()
            return True
        else:
            return False

    @staticmethod
    def get_announcements_by_user(user: int) -> list[Announcement]:

        cursor.execute("SELECT a.id,a.byuser,a.class,a.content FROM announcements as a,chatusers WHERE chatusers.class = a.class && chatusers.id = %s;", (user,))
        res = cursor.fetchall()
        L = []
        for (id, byuser, clas, content) in res:
            L.append(Announcement(id, byuser, clas, content))

        return L

    @staticmethod
    def get_announcements_by_class(userclass: str) -> list[Announcement]:

        res = cursor.execute("SELECT a.id,a.byuser,a.class,a.content FROM announcements as a,chatusers WHERE a.class = %s;", (userclass,))

        L = []
        for (id, byuser, clas, content) in res:
            L.append(Announcement(id, byuser, clas, content))

        return L
