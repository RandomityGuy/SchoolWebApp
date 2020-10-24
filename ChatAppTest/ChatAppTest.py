from flask import Flask, render_template,url_for,request,jsonify,make_response, abort,redirect;
from pypika import Query, Table, Field;

import mysql.connector;
import jinja2;
import snowflake;
import api;


app = Flask(__name__);

@app.route("/api/channels/")
def getChannels():

	userid = int(request.cookies.get('loginid'));
	return jsonify(ChannelModel(api.Channel.getChannelList(userid)).toDict());

@app.route("/api/channels/<channel>/messages",methods = ['GET'])
def getChatMessages(channel):
	msgcount = int(request.args.get('messages',50));
	fromtimestamp = int(request.args.get('after',0));
	if (msgcount > 100):
		msgcount = 100;
	chatmsgs = api.Channel.getChatMessages(channel,msgcount,fromtimestamp);
	lastmsgid = -1;
	if (len(chatmsgs)!=0):
		lastmsgid = chatmsgs[-1].id;
	jdict = api.ChatModel(chatmsgs,lastmsgid,channel).toDict();
	return jsonify(jdict);

@app.route("/api/channels/<channel>/users",methods = ['GET'])
def getUserList(channel):
	users = api.Channel.getUserList(channel);
	jlist = [];
	for user in users:
		jlist.append(user.toDict());
	return jsonify(jlist);

	
@app.route("/api/channels/<channel>/messages",methods = ['POST'])
def sendChatMessage(channel):
	msg = request.form["messagebox"];
	userid = request.cookies.get('loginid');

	canAccessThisChannel = api.Channel.validateAccess(channel,userid);
	if (not canAccessThisChannel):
		abort(403);

	if (api.Channel.sendMessage(channel,userid,msg)):
		cursor.execute(f"SELECT Username FROM ChatUsers WHERE Id = {userid};");
		author = "";
		for (username) in cursor:
			author = username;
			break;
		return jsonify(id = id,authorname = author,authorid=userid,content = msg);
	else:
		abort(403);

	return abort(403);

@app.route("/channels/<channel>/chat",methods = ['GET'])
def chat(channel):
	loginperson = request.cookies.get('loginid',None);
	if (loginperson == None):
		abort(403);
	#request.form["loginid"] if (request.cookies.get('loginid') is None) else request.cookies.get('loginid');
	canAccessThisChannel = api.Channel.validateAccess(channel,loginperson);

	if (not canAccessThisChannel):
		abort(403);

	chatmsgs = api.Channel.getChatMessages(channel,50,0);
	lastid = chatmsgs[-1].id if (len(chatmsgs)!=0) else 0;
	channelmodel = api.Channel.getChannelList(loginperson);
	usermodel = api.Channel.getUserList(channelmodel[0].id);

	return make_response(render_template("chat.html",Model = api.ChatModel(chatmsgs,lastid,channel),userid=loginperson,Channels = api.ChannelModel(channelmodel),Users = api.UserModel(usermodel)));

@app.route("/users/<user>/chat",methods = ['GET'])
def userDM(user):
	userid = int(request.cookies.get('loginid'));

@app.route("/api/authorize",methods = ['POST'])
def auth():
	loginperson = request.form["loginid"];
	channels = api.Channel.getChannelList(loginperson);

	if (len(channels) == 0):
		abort(403);

	redir = redirect(url_for("chat",channel=channels[0].id));
	redir.set_cookie('loginid',loginperson);
	return redir;

@app.route("/api/announcements/",methods = ['GET','POST'])
def announcements(user):
	if (request.method == 'GET'):
		userid = request.cookies.get('loginid');
		anns = api.Announcements.get_announcements_by_user(userid);
		L = [];
		for a in anns:
			L.append(a.ToDict());

		return jsonify(L);

	if (request.method == 'POST'):
		token = request.form.get('token');
		toclass = request.form.get('class');
		content = request.form.get('content');

		if (not api.Auth.authorize(token)):
			return abort(403);

		perms = api.Auth.get_token_permissions(token);
		if (api.Permissions.has_permission(perms,api.Permissions.MANAGE_ANNOUNCE)):
			user = api.Auth.get_token_user(token);
			if (user != None):
				api.Announcements.make_announcement(user,toclass,content);
				return "OK";
			else:
				return abort(403);
		return abort(403);



@app.route("/")
def login():
	return render_template("login.html");