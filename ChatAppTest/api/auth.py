from api.base import *;
import bcrypt;
import secrets;
import hashlib;
import base64;

class Auth:


	@staticmethod
	def login(username,pwd):
		'''
		Attempt login as given username and password, returns token if success
		
		@param username: given username
		@param pwd: the password
		@return: token if success

		'''

		# !!! WARNING : SEND A HASHED PASSWORD FROM THE SITE, HASH THE PASSWORD WITHIN THE BROWSER AND THEN SEND IT HERE

		cursor.execute(f"SELECT id,Username,password FROM chatusers WHERE Username = {username};");

		if (len(cursor) == 0):
			raise Exception("Invalid username");

		data = cursor.fetchone();

		if (data[2] == None):
			raise Exception("No password set");

		if (bcrypt.checkpw(base64.b64encode(hashlib.sha256(pwd).digest()),data[2])):
			cursor.execute(f"SELECT token FROM tokens WHERE (expires > GETDATE() && user=={data[0]});");
			if (len(cursor) == 0):
				# Create new token
				token = secrets.token_hex(128);
				id = snowflakegen.__next__();
				cursor.execute(f"INSERT INTO tokens VALUES({id},\"{token}\",DATEADD(m,1,GETDATE()),{data[1]});");
				db.commit();
				return token;
			else:
				token = cursor.fetchone();
				return token;

		raise Exception("Invalid password");

	@staticmethod
	def register(username,pwd,permissions):
		'''
		Register user from username,password and permissions flags. Returns token

		@param username: username
		@param pwd: the password
		@param permissions: the set of flags
		@return: user token

		'''
		id = snowflakegen.__next__();
		hash = bcrypt.hashpw(base64.b64encode(hashlib.sha256(pwd).digest()),bcrypt.gensalt());

		cursor.execute(f"INSERT INTO chatdb VALUES({id},\"{username}\",\"{hash}\",{permissions});");
		db.commit();

		return login(username,pwd);

	@staticmethod
	def authorize(token):
		'''
		Authorize token. Returns True if success

		@param token: token
		@return: True if success
		'''
		cursor.execute(f"SELECT token FROM tokens WHERE (expires > GETDATE() && token=={token});");
		if (len(cursor) == 0):
			return False;
		return True;