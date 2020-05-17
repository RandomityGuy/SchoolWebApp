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

@app.route("/api/channels/<channel>/getChatMessages",methods = ['GET'])
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

	
@app.route("/api/channels/<channel>/sendChatMessage",methods = ['POST'])
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

	return make_response(render_template("chat.html",Model = api.ChatModel(chatmsgs,lastid,channel),userid=loginperson,Channels = api.ChannelModel(channelmodel)));

@app.route("/api/authorize",methods = ['POST'])
def auth():
	loginperson = request.form["loginid"];
	channels = api.Channel.getChannelList(loginperson);

	if (len(channels) == 0):
		abort(403);

	redir = redirect(url_for("chat",channel=channels[0].id));
	redir.set_cookie('loginid',loginperson);
	return redir;

@app.route("/")
def login():
	return render_template("login.html");