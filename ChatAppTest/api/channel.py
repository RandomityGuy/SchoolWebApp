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
	def __init__(self,id,name):
		self.id = id;
		self.name = name;

	def toDict(self):
		return {"id":self.id,"name":self.name};

	@staticmethod
	def validateAccess(channel,userid):
		print(cursor);
		print(db);
		query = f"select id from channelmembers where channelId = {channel} && userid = {userid};";
		cursor.execute(query);

		for (id) in cursor:
			return True;

		return False;

	@staticmethod
	def createChannel(channelname,members):
		channelid = snowflakegen.__next__();
		query = f"INSERT INTO channels VALUES({channelid},\"{channelname}\");";
		cursor.execute(query);
		for member in members:
			cursor.execute(f"INSERT INTO channelmembers VALUES({snowflakegen.__next__()},{channeld},{member});");
		db.commit();

	@staticmethod
	def getChannelList(userid):
		query = f"select channelId,name from channelmembers,channels where (channelmembers.channelid = channels.id && userid = {userid});";
		cursor.execute(query);
		retlist = [];
		for (id,name) in cursor:
			retlist.append(Channel(id,name));
		return retlist;

	@staticmethod
	def getUserList(channelid):
		query = f"select chatusers.id,username from channelmembers,chatusers where (channelid = {channelid} && userid = chatusers.id);";
		cursor.execute(query);
		retlist = [];
		for (id,name) in cursor:
			retlist.append(ChatAuthor(id,name,""));
		return retlist;

	@staticmethod
	def sendMessage(channel,userid,msg):
		id = snowflakegen.__next__();
		canAccessThisChannel = api.Channel.validateAccess(channel,userid);
		if (not canAccessThisChannel):
			return False;
		query = f"INSERT INTO ChatMessages VALUES({id},{userid},\"{msg}\",{channel});";
		#cursor = db.cursor(buffered = True);
		cursor.execute(query);
		db.commit();
		return True;

	@staticmethod
	def getChatMessages(channel,lim = 100,after = 0):
		if (lim > 100):
			lim = 100;
		query = f"SELECT ChatMessages.Id,ChatUsers.Id,Username,Content FROM ChatMessages,ChatUsers WHERE (ChatMessages.User = ChatUsers.Id && ChatMessages.Id > {after} && ChatMessages.Channel = {channel} ) ORDER BY ChatMessages.Id ASC LIMIT {lim};";
		cursor.execute(query);
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