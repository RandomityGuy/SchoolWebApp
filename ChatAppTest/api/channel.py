from api.permissions import Permissions
from api.dmrequests import DMRequest
from api.auth import Auth
from api.base import *
from __future__ import annotations


class ChatModel(ToDictable):
    def __init__(self, messages, lastmessageid, channelid):
        self.messages = messages
        self.lastmessageid = lastmessageid
        self.channelid = channelid

    def toDict(self):
        d = {}
        L = []
        for m in self.messages:
            L.append(m.toDict())
        d["messages"] = L
        d["lastmessageid"] = self.lastmessageid
        d["channelid"] = self.channelid
        return d


class ChatMessageGroup(ToDictable):
    def __init__(self, id, author, messages):
        self.id = id
        self.author = author
        self.messages = messages

    def toDict(self):
        d = {"id": self.id, "author": self.author.toDict()}
        L = []
        for m in self.messages:
            L.append(m.toDict())
        d["messages"] = L
        return d


class ChatMessage(ToDictable):
    def __init__(self, id, content, attachment):
        self.id = id
        self.content = content
        self.attachment = attachment

    def toDict(self):
        return {"id": self.id, "content": self.content, "attachment": self.attachment}


class ChatAuthor(ToDictable):
    def __init__(self, id, name, avatarurl):
        self.id = id
        self.name = name
        self.avatarurl = avatarurl

    def toDict(self):
        return {"id": self.id, "name": self.name, "avatarurl": self.avatarurl}


class Channel(ToDictable):
    DM_CHANNEL = 1
    REQ_CHANNEL = 2

    def __init__(self, id, name, flags):
        self.id = id
        self.name = name
        self.flags = flags

    def toDict(self):
        return {"id": self.id, "name": self.name, "flags": self.flags}

    @staticmethod
    def validate_access(channel: int, userid: int) -> bool:
        """Validate access for the given user for the channel

        Args:
            channel (int): The channel id
            userid (int): The given user id

        Returns:
            bool: True if the user can access the channel
        """

        if Permissions.has_permission(Auth.get_permissions(userid), Permissions.CAN_VIEW_ANY_CHANNEL):
            return True

        if Channel.is_expired(channel):
            return False

        cursor.execute("select id from channelmembers where channelId = %s && userid = %s;", (channel, userid))

        for id in cursor:
            return True

        return False

    @staticmethod
    def create_channel(channelname: str, members: list[int], flags: int) -> int:
        """Create a channel with given channel name and specified channel members and flags

        Args:
            channelname (str): The channel name
            members (list[int]): The list of members in the channel
            flags (int): The flags of the channel

        Returns:
            int: The created channel id
        """

        channelid = snowflakegen.__next__()
        cursor.execute("INSERT INTO channels VALUES(%s,%s,%s);", (channelid, channelname, flags))
        for member in members:
            cursor.execute("INSERT INTO channelmembers VALUES(%s,%s,%s);", (snowflakegen.__next__(), channelid, member))
        db.commit()
        return channelid

    @staticmethod
    def channel_exists(channelid: int) -> bool:
        """Check if a channel exists

        Args:
            channelid (int): The channel id

        Returns:
            bool: True if it exists
        """
        cursor.execute("SELECT id from channels WHERE id = %s;", (channelid,))
        if len(cursor) != 0:
            return True
        return False

    @staticmethod
    def DM_exists(userone: int, usertwo: int) -> int | None:
        """Checks if a DM between the two users exists

        Args:
            userone (int): The first user
            usertwo (int): The second user

        Returns:
            int | None: The DM channel id if it exists, else None
        """
        query = "SELECT A.channelId, COUNT(*) FROM (SELECT channelmembers.id, channelId, userId FROM channelmembers, channels WHERE (channels.flags & %s) = %s && channels.id = channelmembers.channelId) AS A WHERE A.userid IN (%s,%s) GROUP BY A.channelId HAVING COUNT(*) = 2;"
        cursor.execute(query, (Channel.DM_CHANNEL, Channel.DM_CHANNEL, userone, usertwo))
        if cursor.rowcount == 0:
            return None
        return cursor.fetchone()[0]

    @staticmethod
    def create_DM(userone: int, usertwo: int, is_req: bool = False) -> int:
        """Creates a DM channel between two users

        Args:
            userone (int): The first user
            usertwo (int): The second user
            is_req (bool, optional): Is this DM created from a DM request?. Defaults to False.

        Returns:
            int: The DM channel id
        """
        dm = Channel.DM_exists(userone, usertwo)
        if dm != None:
            return dm
        else:
            return Channel.create_channel(f"DM_{userone}_{usertwo}", [userone, usertwo], Channel.DM_CHANNEL | (Channel.REQ_CHANNEL if is_req else 0))

    @staticmethod
    def join_channel_if_exists(channelid: int, userid: int):
        """For the given user, join the given channel

        Args:
            channelid (int): The channel id
            userid (int): The user id
        """

        if Channel.channel_exists(channelid):
            cursor.execute("INSERT INTO channelmembers VALUES(%s,%s,%s);", (snowflakegen.__next__(), channelid, userid))
            db.commit()

    @staticmethod
    def leave_channel(channelid: int, userid: int):
        """For the given user, leave the given channel

        Args:
            channelid (int): The channel id
            userid (int): The user id
        """
        if Channel.channel_exists(channelid):
            cursor.execute("DELETE FROM channelmembers WHERE (channelId=%s && userid=%s);", (channelid, userid))
            db.commit()

    @staticmethod
    def get_channel_list(userid: int) -> list[Channel]:
        """Gets the channel list for the given user

        Args:
            userid (int): The given user id

        Returns:
            list[Channel]: The channel list
        """
        if Permissions.has_permission(Auth.get_permissions(userid), Permissions.CAN_VIEW_ANY_CHANNEL):
            cursor.execute("SELECT channelId,name,flags FROM channelmembers,channels WHERE userid = %s;", (userid,))
        else:
            cursor.execute("select channelId,name,flags from channelmembers,channels where (channelmembers.channelid = channels.id && userid = %s);", (userid,))
        retlist = []
        for (id, name, flags) in cursor:
            retlist.append(Channel(id, name, flags))
        return retlist

    @staticmethod
    def get_channel(channelid: int) -> Channel:
        """Gets a channel from its id

        Args:
            channelid (int): The given channel id

        Returns:
            Channel: The channel
        """
        cursor.execute("select channelId,name,flags from channelmembers,channels where id = %s;", (channelid,))
        if cursor.rowcount == None:
            return None
        retlist = []
        for (id, name, flags) in cursor:
            retlist.append(Channel(id, name, flags))
        return retlist[0]

    @staticmethod
    def is_expired(channelid: int) -> bool:
        """Checks if a given channel is expired because of expired DM request

        Args:
            channelid (int): The channel id

        Raises:
            Exception: The requested channel has invalid member count or flags

        Returns:
            bool: True if its expired
        """
        ch = Channel.get_channel(channelid)
        if ch == None:
            return True
        if Permissions.has_permission(ch, Channel.REQ_CHANNEL):
            members = Channel.get_user_list(channelid)
            if len(members) != 2:
                raise Exception("DM requested channel cannot have member count other than 2")
            return (not DMRequest.dm_exists(members[0].id, members[1].id)) and (not DMRequest.dm_exists(members[1].id, members[0].id))
        else:
            return False

    @staticmethod
    def get_user_list(channelid: int) -> list[ChatAuthor]:
        """Gets a list of users in the channel

        Args:
            channelid (int): The channel id

        Returns:
            list[ChatAuthor]: The list of users
        """
        cursor.execute("SELECT chatusers.id, username FROM channelmembers,chatusers WHERE (channelmembers.channelId = %s && channelmembers.userid = chatusers.id);", (channelid,))
        retlist = []
        for (id, name) in cursor:
            retlist.append(ChatAuthor(id, name, f"/users/{id}/avatar"))
        return retlist

    @staticmethod
    def send_message(channel: int, userid: int, msg: str, attachment=None, attachment_name: str = None) -> bool:
        """Sends a message to a given channel from the user

        Args:
            channel (int): The channel id
            userid (int): The user sending the message
            msg (str): The message
            attachment: (optional) The attachment data
            attachment_name (str): (optional) The attachment filename

        Returns:
            bool: True if success
        """
        id = snowflakegen.__next__()
        canAccessThisChannel = Channel.validate_access(channel, userid)
        if not canAccessThisChannel:
            return False

        attachment_id = None
        if attachment != None:
            attachment_id = snowflakegen.__next__()
            cursor.execute("INSERT INTO attachments VALUES(%s,%s,%s);", (attachment_id, attachment, attachment_name))

        cursor.execute("INSERT INTO ChatMessages VALUES(%s,%s,%s,%s,%s);", (id, userid, msg, channel, attachment_id))
        db.commit()
        return True

    @staticmethod
    def get_chat_messages(channel: int, lim=100, after=0) -> list[ChatMessageGroup]:
        """Gets a list of chat messages in a channel, can be limited and be searched by id

        Args:
            channel (int): The channel id
            lim (int, optional): The maximum number of messages to return. Defaults to 100.
            after (int, optional): The snowflake id after which the messages have to be retrieved from. Defaults to 0.

        Returns:
            list[ChatMessageGroup]: The list of messages
        """

        if lim > 100:
            lim = 100
        cursor.execute(
            "SELECT ChatMessages.Id,ChatUsers.Id,Username,Content,attachment FROM ChatMessages,ChatUsers WHERE (ChatMessages.User = ChatUsers.Id && ChatMessages.Id > %s && ChatMessages.Channel = %s ) ORDER BY ChatMessages.Id ASC LIMIT %s;",
            (after, channel, lim),
        )
        retlist = []
        for (id, userid, username, content, attachment) in cursor:
            retlist.append(ChatMessageGroup(id, ChatAuthor(userid, username, f"/users/{userid}/avatar"), [ChatMessage(id, content, attachment)]))

        return retlist

    @staticmethod
    def get_attachment(attachmentid: int) -> Attachment:
        """Gets the attachment for the attachment id

        Args:
            attachmentid (int): The attachment id

        Returns:
            Attachment: The attachment if found
        """
        cursor.execute("SELECT id, file, filename FROM attachments WHERE id = %s;", (attachmentid,))
        if cursor.rowcount == 0:
            return None
        res = cursor.fetchone()
        a = Attachment(res[0], res[1], res[2])
        return a


class UserModel(ToDictable):
    def __init__(self, users):
        self.users = users

    def toDict(self):
        d = {}
        L = []
        for m in self.channels:
            L.append(m.toDict())
        d["users"] = L
        return d


class ChannelModel(ToDictable):
    def __init__(self, channels):
        self.channels = channels

    def toDict(self):
        d = {}
        L = []
        for m in self.channels:
            L.append(m.toDict())
        d["channels"] = L
        return d


class Attachment(ToDictable):
    def __init__(self, id, attachment, name):
        self.attachment = attachment
        self.name = name
        self.id = id

    def toDict(self):
        d = {}
        d["name"] = self.name
        d["link"] = f"/chat/attachments/{id}"
        return d
