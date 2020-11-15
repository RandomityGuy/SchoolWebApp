from api.base import *;

class ChatModel(ToDictable):
	def __init__(self,messages,lastmessageid,channelid):
		self.messages = messages;
		self.lastmessageid = lastmessageid;
		self.channelid = channelid;

	def toDict(self):
		d = {};
		L = [];
		for m in self.messages:
			L.append(m.toDict());
		d["messages"] = L;
		d["lastmessageid"] = self.lastmessageid;
		d["channelid"] = self.channelid;
		return d;

class ChatMessageGroup(ToDictable):
	def __init__(self,id,author,messages):
		self.id = id;
		self.author = author;
		self.messages = messages;

	def toDict(self):
		d = {"id" : self.id, "author" : self.author.toDict()}
		L = [];
		for m in self.messages:
			L.append(m.toDict());
		d["messages"] = L;
		return d;

class ChatMessage(ToDictable):
	
	def __init__(self,id,content):
		self.id = id;
		self.content = content;

	def toDict(self):
		return {"id" : self.id, "content" : self.content};

class ChatAuthor(ToDictable):
	def __init__(self,id,name,avatarurl):
		self.id = id;
		self.name = name;
		self.avatarurl = avatarurl;

	def toDict(self):
		return {"id" : self.id, "name": self.name, "avatarurl" : self.avatarurl };

class Channel(ToDictable):
	def __init__(self,id,name,flags):
		self.id = id;
		self.name = name;
		self.flags = flags;

	def toDict(self):
		return {"id":self.id,"name":self.name,"flags":self.flags};

	@staticmethod
	def validate_access(channel,userid):
		'''
		TODO: implement permissions flags
		Validate access for a user for given channel

		@param channel: the channel id
		@param userid: the user id
		@returns: True if success
		'''
		cursor.execute("select id from channelmembers where channelId = %s && userid = %s;",(channel,userid));

		for (id) in cursor:
			return True;

		return False;

	@staticmethod
	def create_channel(channelname,members,flags):
		'''
		Create a channel from given name and specified memmbers and flags

		@param channelname: the channel name
		@param members: list of user ids to put in the channel
		@param flags: the flags for a channel
		'''

		channelid = snowflakegen.__next__();
		cursor.execute("INSERT INTO channels VALUES(%s,%s,%s);",(channelid,channelname,flags));
		for member in members:
			cursor.execute("INSERT INTO channelmembers VALUES(%s,%s,%s);",(snowflakegen.__next__(),channelid,member));
		db.commit();

	@staticmethod
	def channel_exists(channelid):
		'''
		Check if a given channel exists

		@param channelid: the channel id to test
		@returns: True if channel exists
		'''
		cursor.execute("SELECT id from channels WHERE id = %s;",channelid);
		if (len(cursor) != 0):
			return True;
		return False;

	@staticmethod
	def DM_exists(userone,usertwo):
		# TODO: Figure this out
		query = f"select * from channels JOIN (select * from channelmembers group by channelId having count(*) = 2) as X where channels.id = X.channelId;";

	@staticmethod
	def join_channel_if_exists(channelid,userid):
		'''
		Insert user into a channel if the channel exists

		@param channelid: the channel id
		@param userid: the user id
		'''

		if (Channel.channel_exists(channelid)):
			cursor.execute("INSERT INTO channelmembers VALUES(%s,%s,%s);",(snowflakegen.__next__(),channelid,userid));
			db.commit();

	@staticmethod
	def leave_channel(channelid,userid):
		'''
		Remove user from specified channel

		@param channelid: the channelid
		@param userid: the user id
		'''
		if (Channel.channel_exists(channelid)):
			cursor.execute("DELETE FROM channelmembers WHERE (channelId=%s && userid=%s);",(channelid,userid));
			db.commit();

	@staticmethod
	def get_channel_list(userid):
		'''
		TODO: ADD PERMISSIONS OVERRIDES
		Gets the channel list for a specified user

		@param userid: the user id
		@returns: list of Channel objects
		'''
		cursor.execute("select channelId,name,flags from channelmembers,channels where (channelmembers.channelid = channels.id && userid = %s);",userid);
		retlist = [];
		for (id,name,flags) in cursor:
			retlist.append(Channel(id,name,flags));
		return retlist;

	@staticmethod
	def get_user_list(channelid):
		'''
		Get list of users in a channel

		@param channelid: the channel id
		@returns: list of ChatAuthor objects
		'''
		cursor.execute("SELECT chatusers.id, username FROM channelmembers,chatusers WHERE (channelmembers.channelId = %s && channelmembers.userid = chatusers.id);",(channelid,));
		retlist = [];
		for (id,name) in cursor:
			retlist.append(ChatAuthor(id,name,""));
		return retlist;

	@staticmethod
	def send_message(channel,userid,msg):
		'''
		Sends a message to channel as user

		@param channel: the channel id
		@param userid: the user id
		@param msg: the message
		@returns: if the message was successfully sent
		'''
		id = snowflakegen.__next__();
		canAccessThisChannel = Channel.validate_access(channel,userid);
		if (not canAccessThisChannel):
			return False;
		cursor.execute("INSERT INTO ChatMessages VALUES(%s,%s,%s,%s);",id,userid,msg,channel);
		db.commit();
		return True;

	@staticmethod
	def get_chat_messages(channel,lim = 100,after = 0):
		'''
		Gets list of chat messages in given channel

		@param channel: the channel id
		@param lim: (optional) maximum messages to retrieve
		@param after: (optional) the timestamp after which the messages have to be retrieved
		@returns: list of ChatMessageGroup objects
		'''

		if (lim > 100):
			lim = 100;
		cursor.execute("SELECT ChatMessages.Id,ChatUsers.Id,Username,Content FROM ChatMessages,ChatUsers WHERE (ChatMessages.User = ChatUsers.Id && ChatMessages.Id > %s && ChatMessages.Channel = %s ) ORDER BY ChatMessages.Id ASC LIMIT %s;",(after,channel,lim));
		retlist = [];
		for (id,userid,username,content) in cursor:
			retlist.append(ChatMessageGroup(id,ChatAuthor(userid,username,""),[ChatMessage(id,content)]));


		return retlist;

class UserModel(ToDictable):
	def __init__(self,users):
		self.users = users;

	def toDict(self):
		d = {};
		L = [];
		for m in self.channels:
			L.append(m.toDict());
		d["users"] = L;
		return d;

class ChannelModel(ToDictable):
	def __init__(self,channels):
		self.channels = channels;

	def toDict(self):
		d = {};
		L = [];
		for m in self.channels:
			L.append(m.toDict());
		d["channels"] = L;
		return d;