from api.base import *;
from api.auth import Auth;
from api.permissions import Permissions;

class Announcement(ToDictable):
    def __init__(self,id,creator,byclass,content):
        self.id = id;
        self.creator = creator;
        self.byclass = byclass;
        self.content = content;

    def ToDict(self):
        return {"id":self.id, "creator":self.creator, "class": self.byclass, "content": self.content};

class Announcements:

    @staticmethod 
    def make_announcement(user,destclass,text):
        perms = Auth.get_permissions(user);
        if (Permissions.has_permission(perms,Permissions.MANAGE_ANNOUNCE)):
            id = snowflakegen.__next__();
            query = f"INSERT INTO announcements VALUES({id},{user},\"{destclass}\",\"{text}\");";
            cursor.execute(query);
            db.commit();
            return id;
        else:
            return False;

    @staticmethod
    def revoke_announcement(user,announcementid):
        perms = Auth.get_permissions(user);
        if (Permissions.has_permission(perms,Permissions.MANAGE_ANNOUNCE)):
            id = snowflakegen.__next__();
            query = f"DELETE FROM announcements WHERE id = {announcementid};";
            cursor.execute(query);
            db.commit();
            return True;
        else:
            return False;

    @staticmethod
    def get_announcements_by_user(user):
        query = f"SELECT a.id,a.byuser,a.class,a.content FROM announcements as a,chatusers WHERE chatusers.class = a.class && chatusers.id = {user};";

        res = cursor.execute(query);

        L = [];
        for (id,byuser,clas,content) in res:
            L.append(Announcement(id,byuser,clas,content));

        return L;

    @staticmethod
    def get_announcements_by_class(userclass):
        query = f"SELECT a.id,a.byuser,a.class,a.content FROM announcements as a,chatusers WHERE a.class = {userclass};";

        res = cursor.execute(query);

        L = [];
        for (id,byuser,clas,content) in res:
            L.append(Announcement(id,byuser,clas,content));

        return L;