from api.channel import Channel
from api.assignments import AssignmentInfo
from api.permissions import Permissions
from flask import Flask, render_template, url_for, request, jsonify, make_response, abort, redirect
from flask.wrappers import Response
from utils.QueryList import QueryList

import mysql.connector
import jinja2
from werkzeug.datastructures import Headers
import snowflake
import api
import magic
import datetime


app = Flask(__name__)


def authenticate_user() -> int:
    token = request.args.get("token")
    userid = api.Auth.get_token_user_id(token)
    if userid == None:
        return abort(403)
    return userid


@app.route("/api/channels", methods=["GET"])
def get_channels():
    userid = authenticate_user()
    return jsonify(api.ChannelModel(api.Channel.get_channel_list(userid)).toDict())


@app.route("/api/channels/<channel>/messages", methods=["GET"])
def get_chat_messages(channel):
    userid = authenticate_user()

    canAccessThisChannel = api.Channel.validate_access(channel, userid)
    if not canAccessThisChannel:
        abort(403)

    msgcount = int(request.args.get("messages", 50))
    fromtimestamp = int(request.args.get("after", 0))
    if msgcount > 100:
        msgcount = 100
    chatmsgs = api.Channel.get_chat_messages(channel, msgcount, fromtimestamp)
    lastmsgid = -1
    if len(chatmsgs) != 0:
        lastmsgid = chatmsgs[-1].id
    jdict = api.ChatModel(chatmsgs, lastmsgid, channel).toDict()
    return jsonify(jdict)


@app.route("/api/channels/<channel>", methods=["DELETE"])
def leave_channel(channel):
    userid = authenticate_user()
    if request.args.get("userid", None) == None:
        api.Channel.leave_channel(channel, userid)
        return "OK", 200
    else:
        perms = api.Auth.get_permissions(userid)
        if api.Permissions.has_permission(perms, api.Permissions.CAN_MODIFY_STUDENT):
            api.Channel.leave_channel(channel, request.args.get("userid"))
            return "OK", 200
        return abort(403)


@app.route("/api/channels/<channel>/users", methods=["GET"])
def get_user_list(channel):
    userid = authenticate_user()

    canAccessThisChannel = api.Channel.validate_access(channel, userid)
    if not canAccessThisChannel:
        abort(403)

    users = api.Channel.get_user_list(channel)
    jlist = []
    for user in users:
        jlist.append(user.toDict())
    return jsonify(jlist)


@app.route("/api/channels/<channel>/messages", methods=["POST"])
def send_chat_message(channel):
    msg = request.json.get["messagebox"]
    userid = authenticate_user()

    canAccessThisChannel = api.Channel.validate_access(channel, userid)
    if not canAccessThisChannel:
        abort(403)

    if api.Channel.send_message(channel, userid, msg):
        api.cursor.execute(f"SELECT Username FROM ChatUsers WHERE Id = {userid};")
        author = ""
        for username in api.cursor:
            author = username
            break
        return jsonify(id=id, authorname=author, authorid=userid, content=msg)
    else:
        abort(403)


@app.route("/channels/<channel>/chat", methods=["GET"])
def chat(channel):
    loginperson = authenticate_user()
    # request.form["loginid"] if (request.cookies.get('loginid') is None) else request.cookies.get('loginid');
    canAccessThisChannel = api.Channel.validate_access(channel, loginperson)

    if not canAccessThisChannel:
        abort(403)

    chatmsgs = api.Channel.get_chat_messages(channel, 50, 0)
    lastid = chatmsgs[-1].id if (len(chatmsgs) != 0) else 0
    channelmodel = api.Channel.get_channel_list(loginperson)
    usermodel = api.Channel.get_user_list(channelmodel[0].id)

    return make_response(render_template("chat.html", Model=api.ChatModel(chatmsgs, lastid, channel), userid=loginperson, Channels=api.ChannelModel(channelmodel), Users=api.UserModel(usermodel)))


@app.route("api/users/<user>/DM", methods=["GET"])
def userDM(user):
    userid = authenticate_user()
    thisuser = api.User.get_user(userid)
    otheruser = api.User.get_user(user)
    if otheruser == None:
        return abort(403)
    if thisuser.studentclass == otheruser.studentclass or Permissions.has_permission(thisuser.permissions, Permissions.DM_ANYONE):
        dm = api.Channel.get_channel(api.Channel.create_DM(userid, user))
        return jsonify(dm.toDict())
    else:
        return abort(403)


@app.route("api/users/<user>/avatar", methods=["GET", "POST"])
def userAvatar(user):
    if request.method == "GET":
        avatar = api.User.get_avatar(user)
        resp = Response(avatar)
        resp.headers["Content-Type"] = magic.from_buffer(avatar)
        return resp
    if request.method == "POST":
        token = authenticate_user()
        tokenuser = api.Auth.get_token_user_id(token)
        if tokenuser != user:
            perms = api.Auth.get_token_permissions(token)
            if api.Permissions.has_permission(perms, api.Permissions.CAN_MODIFY_AVATAR):
                api.User.set_avatar(user, request.data)
            else:
                abort(403)
        else:
            api.User.set_avatar(user, request.data)
        return "OK", 200
    abort(403)


@app.route("/api/authorize", methods=["POST"])
def auth():
    username = request.json.get("username")
    pwd = request.json.get("pwd")

    try:
        token = api.Auth.login(username, pwd)
        resp = {"token": token}
        return jsonify(resp)
    except Exception:
        abort(403)


@app.route("/api/announcements", methods=["GET", "POST"])
def announcements():
    if request.method == "GET":
        userid = authenticate_user()
        anns = api.Announcements.get_announcements_by_user(userid)
        L = []
        for a in anns:
            L.append(a.toDict())

        return jsonify(L)

    if request.method == "POST":
        token = request.form.get("token")
        toclass = request.form.get("class")
        content = request.form.get("content")

        if not api.Auth.authorize(token):
            return abort(403)

        perms = api.Auth.get_token_permissions(token)
        if api.Permissions.has_permission(perms, api.Permissions.MANAGE_ANNOUNCE):
            user = api.Auth.get_token_user_id(token)
            if user != None:
                api.Announcements.make_announcement(user, toclass, content)
                return "OK"
            else:
                return abort(403)
        return abort(403)


@app.route("/api/assignments/<studentclass>", methods=["GET", "POST"])
def assignments(studentclass):
    if request.method == "GET":
        userid = authenticate_user()
        user = api.User.get_user(userid)
        if user.studentclass == studentclass or api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
            assignments = api.Assignment.get_assignments_for_class(studentclass)
            js = {}
            L = []
            for assignment in assignments:
                L.append(assignment.toDict())
            js["assignments"] = L
            return jsonify(js)
        else:
            return abort(403)

    if request.method == "POST":
        userid = authenticate_user()
        perms = api.Auth.get_permissions(userid)
        if api.Permissions.has_permission(perms, api.Permissions.MANAGE_ASSIGNMENT):
            content = request.args.get("content")
            duedate = datetime.date.fromisoformat(request.args.get("due-date"))
            attachmentname = request.args.get("attachment-name", None)
            api.Assignment.create_assignment(studentclass, content, duedate, attachmentname, request.data)
            return "OK", 200
        else:
            return abort(403)


@app.route("/api/assignment/<assignmentid>", methods=["GET", "POST"])
def assignment(assignmentid):
    if request.method == "GET":
        userid = authenticate_user()
        user = api.User.get_user(userid)
        assignment = api.Assignment.get_assignment(assignmentid)
        if assignment == None:
            return abort(403)
        if user.studentclass == assignment.studentclass or api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
            return jsonify(assignment.toDict())
        else:
            return abort(403)

    if request.method == "POST":
        userid = authenticate_user()
        user = api.User.get_user(userid)
        assignment = api.Assignment.get_assignment(assignmentid)
        if assignment == None:
            return abort(403)
        if user.studentclass == assignment.studentclass or api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
            submitted = api.Assignment.upload_assignment(userid, assignment, request.args.get("attachment-name"), request.data)
            if submitted:
                return "OK", 200
            else:
                return abort(403)
        else:
            return abort(403)


@app.route("/api/assignment/<assignmentid>/attachment", methods=["GET"])
def assignmentattachment(assignmentid):
    userid = authenticate_user()
    user = api.User.get_user(userid)
    assignment = api.Assignment.get_assignment(assignmentid)
    if assignment == None:
        return abort(403)
    if user.studentclass == assignment.studentclass or api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
        if assignment.attachment == None:
            return abort(403)
        resp = Response[assignment.attachment]
        resp.headers["Content-Type"] = "application/octet-stream"
        return resp
    else:
        return abort(403)


@app.route("/api/assignment/<assignmentid>/submissions/<submissionid>/file", methods=["GET"])
def assignmentinfo(assignmentid, submissionid):
    userid = authenticate_user()
    user = api.User.get_user(userid)
    assignment = api.Assignment.get_assignment(assignmentid)
    if assignment == None:
        return abort(403)
    if api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
        submission = api.Assignment.get_submitted_assignment(submissionid)
        if submission == None:
            return abort(403)
        resp = Response(submission.attachment)
        resp.headers["Content-Type"] = "application/octet-stream"
        return resp
    else:
        return abort(403)


@app.route("/api/assignment/<assignmentid>/submissions", methods=["GET"])
def assignmentinfo(assignmentid):
    userid = authenticate_user()
    user = api.User.get_user(userid)
    assignment = api.Assignment.get_assignment(assignmentid)
    if assignment == None:
        return abort(403)
    if api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
        submissions = api.Assignment.get_submitted_assignments(assignmentid)
        resp = {"submissions": [submission.toDict() for submission in submissions]}
        return jsonify(resp)
    else:
        return abort(403)


@app.route("/api/assignment/<assignmentid>/submissions/<submissionid>", methods=["PUT"])
def assignmentinfomark(assignmentid, submissionid):
    userid = authenticate_user()
    user = api.User.get_user(userid)
    assignment = api.Assignment.get_assignment(assignmentid)
    if assignment == None:
        return abort(403)
    if api.Permissions.has_permission(user.permissions, api.Permissions.MANAGE_ASSIGNMENT):
        api.Assignment.mark_status(submissionid, request.args.get("status"))
        return "OK", 200
    else:
        return abort(403)


@app.route("/api/classes", methods=["GET"])
def getclasses(classname):
    userid = authenticate_user()
    return jsonify(api.Class.get_classes())


@app.route("/api/class/<classname>", methods=["GET"])
def getclassmembers(classname):
    userid = authenticate_user()
    return jsonify(QueryList(api.Class.get_everyone_for_class(classname)).Select(lambda x: x.toDict()).ToList())


@app.route("/api/class/<classname>/students", methods=["GET"])
def getclassstudents(classname):
    userid = authenticate_user()
    return jsonify(QueryList(api.Class.get_students_for_class(classname)).Select(lambda x: x.toDict()).ToList())


@app.route("/api/class/<classname>/teachers", methods=["GET"])
def getclassteachers(classname):
    userid = authenticate_user()
    return jsonify(QueryList(api.Class.get_class_teachers(classname)).Select(lambda x: x.toDict()).ToList())


@app.route("/api/staff", methods=["GET"])
def getstaff(classname):
    userid = authenticate_user()
    return jsonify(QueryList(api.Class.get_staff()).Select(lambda x: x.toDict()).ToList())


@app.route("/api/request/<requestid>", methods=["GET"])
def get_dm_request(requestid):
    userid = authenticate_user()
    req = api.DMRequest.get_dm_request(requestid)
    if req == None:
        return abort(403)
    if req.to_user == userid:
        return jsonify(req.toDict())
    return abort(403)


@app.route("/api/requests", methods=["GET", "POST"])
def get_dm_requests():
    userid = authenticate_user()
    if request.method == "GET":
        reqs = QueryList(api.DMRequest.get_dm_requests(userid)).Select(lambda x: x.toDict()).ToList()
        return jsonify(reqs)
    if request.method == "POST":
        touser = request.args.get("target")
        perms = api.Auth.get_permissions(touser)
        if api.Permissions.has_permission(perms, api.Permissions.SUPERUSER):
            api.DMRequest.request_dm(touser, userid, request.json["content"])
            return "OK", 200
        else:
            return abort(403)
    abort(403)


@app.route("/api/requests/sent", methods=["GET"])
def get_dm_requests():
    userid = authenticate_user()
    if request.method == "GET":
        reqs = QueryList(api.DMRequest.get_sent_dm_requests(userid)).Select(lambda x: x.toDict()).ToList()
        return jsonify(reqs)
    abort(403)


@app.route("/api/request/<requestid>/accept", methods=["GET"])
def accept_dm(requestid):
    userid = authenticate_user()
    req = api.DMRequest.get_dm_request(requestid)
    if req == None:
        return abort(403)

    if req.to_user == userid:
        dm = api.DMRequest.accept_dm(requestid)
        ch = api.Channel.get_channel(dm)
        return jsonify(ch.toDict())

    return abort(403)


@app.route("/api/requests/<requestid>/reject", methods=["GET"])
def accept_dm(requestid):
    userid = authenticate_user()
    req = api.DMRequest.get_dm_request(requestid)
    if req == None:
        return abort(403)

    if req.to_user == userid:
        dm = api.DMRequest.reject_dm(requestid)
        return "OK", 200

    return abort(403)


@app.route("/")
def login():
    return render_template("login.html")
