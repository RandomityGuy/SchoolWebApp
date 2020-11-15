from flask import Flask, render_template,url_for,request,jsonify,make_response, abort,redirect;

import mysql.connector;
import jinja2;
import snowflake;
import api;


app = Flask(__name__);

def authenticate_user():
	token = request.args.get('token');
	userid = api.Auth.get_token_user_id(token);
	if (userid == None):
		return abort(403)
	return userid;

@app.route("/api/channels/", methods = ['GET'])
def get_channels():
	userid = authenticate_user();
	return jsonify(api.ChannelModel(api.Channel.get_channel_list(userid)).toDict());

@app.route("/api/channels/<channel>/messages",methods = ['GET'])
def get_chat_messages(channel):
	userid = authenticate_user();

	canAccessThisChannel = api.Channel.validate_access(channel,userid);
	if (not canAccessThisChannel):
		abort(403);

	msgcount = int(request.args.get('messages',50));
	fromtimestamp = int(request.args.get('after',0));
	if (msgcount > 100):
		msgcount = 100;
	chatmsgs = api.Channel.get_chat_messages(channel,msgcount,fromtimestamp);
	lastmsgid = -1;
	if (len(chatmsgs)!=0):
		lastmsgid = chatmsgs[-1].id;
	jdict = api.ChatModel(chatmsgs,lastmsgid,channel).toDict();
	return jsonify(jdict);

@app.route("/api/channels/<channel>/users",methods = ['GET'])
def get_user_list(channel):
	userid = authenticate_user();

	canAccessThisChannel = api.Channel.validate_access(channel,userid);
	if (not canAccessThisChannel):
		abort(403);

	users = api.Channel.get_user_list(channel);
	jlist = [];
	for user in users:
		jlist.append(user.toDict());
	return jsonify(jlist);

	
@app.route("/api/channels/<channel>/messages",methods = ['POST'])
def send_chat_message(channel):
	msg = request.json.get["messagebox"];
	userid = authenticate_user();

	canAccessThisChannel = api.Channel.validate_access(channel,userid);
	if (not canAccessThisChannel):
		abort(403);

	if (api.Channel.send_message(channel,userid,msg)):
		api.cursor.execute(f"SELECT Username FROM ChatUsers WHERE Id = {userid};");
		author = "";
		for (username) in api.cursor:
			author = username;
			break;
		return jsonify(id = id,authorname = author,authorid=userid,content = msg);
	else:
		abort(403);

	return abort(403);

@app.route("/channels/<channel>/chat",methods = ['GET'])
def chat(channel):
	loginperson = authenticate_user();
	#request.form["loginid"] if (request.cookies.get('loginid') is None) else request.cookies.get('loginid');
	canAccessThisChannel = api.Channel.validate_access(channel,loginperson);

	if (not canAccessThisChannel):
		abort(403);

	chatmsgs = api.Channel.get_chat_messages(channel,50,0);
	lastid = chatmsgs[-1].id if (len(chatmsgs)!=0) else 0;
	channelmodel = api.Channel.get_channel_list(loginperson);
	usermodel = api.Channel.get_user_list(channelmodel[0].id);

	return make_response(render_template("chat.html",Model = api.ChatModel(chatmsgs,lastid,channel),userid=loginperson,Channels = api.ChannelModel(channelmodel),Users = api.UserModel(usermodel)));

@app.route("/users/<user>/chat",methods = ['GET'])
def userDM(user):
	userid = int(request.cookies.get('loginid'));

@app.route("/api/authorize",methods = ['POST'])
def auth():
	username = request.json.get('username')
	pwd = request.json.get('pwd');

	try:
		token = api.Auth.login(username, pwd);
		resp = {"token": token};
		return jsonify(resp);
	except Exception:
		abort(403);

@app.route("/api/announcements/",methods = ['GET','POST'])
def announcements():
	if (request.method == 'GET'):
		userid = authenticate_user();
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
			user = api.Auth.get_token_user_id(token);
			if (user != None):
				api.Announcements.make_announcement(user,toclass,content);
				return "OK";
			else:
				return abort(403);
		return abort(403);



@app.route("/")
def login():
	return render_template("login.html");