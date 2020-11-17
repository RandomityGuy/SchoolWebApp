from api.base import *
import bcrypt
import secrets
import hashlib
import base64


class Auth:
    @staticmethod
    def login(username: str, pwd: str) -> str:
        """
        Attempt login as given username and password, returns token if success

        @param username: given username
        @param pwd: the password
        @return: token if success

        """

        # !!! WARNING : SEND A HASHED PASSWORD FROM THE SITE, HASH THE PASSWORD WITHIN THE BROWSER AND THEN SEND IT HERE

        cursor.execute("SELECT id,Username,password FROM chatusers WHERE Username = %s;", username)

        if cursor.rowcount == 0:
            raise Exception("Invalid username")

        data = cursor.fetchone()

        if data[2] == None:
            raise Exception("No password set")

        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(pwd).digest()), data[2]):
            cursor.execute("SELECT token FROM tokens WHERE (expires > CURDATE() && user=%s);", data[0])
            if cursor.rowcount == 0:
                # Create new token
                token = secrets.token_hex(128)
                id = snowflakegen.__next__()
                cursor.execute("INSERT INTO tokens VALUES(%s,%s,DATEADD(m,1,CURDATE()),%s);", (id, token, data[1]))
                db.commit()
                return token
            else:
                token = cursor.fetchone()
                return token

        raise Exception("Invalid password")

    @staticmethod
    def register(username: str, pwd: str, permissions: int) -> str:
        """
        Register user from username,password and permissions flags. Returns token

        @param username: username
        @param pwd: the password
        @param permissions: the set of flags
        @return: user token

        """
        id = snowflakegen.__next__()
        hash = bcrypt.hashpw(base64.b64encode(hashlib.sha256(pwd).digest()), bcrypt.gensalt())

        cursor.execute("INSERT INTO chatdb VALUES(%s,%s,%s,%s);", (id, username, hash, permissions))
        db.commit()

        return Auth.login(username, pwd)

    @staticmethod
    def authorize(token: str) -> bool:
        """
        Authorize token. Returns True if success

        @param token: token
        @return: True if success
        """
        cursor.execute("SELECT token FROM tokens WHERE (expires > CURDATE() && token=%s);", (token,))
        if cursor.rowcount == 0:
            return False
        return True

    @staticmethod
    def get_token_permissions(token: str) -> int:
        res = cursor.execute("SELECT permissions FROM tokens,chatusers WHERE (tokens.user = chatusers.id && token = %s);", (token,))
        if cursor.rowcount == 0:
            return None
        perms = res.fetchone()
        return perms

    @staticmethod
    def get_permissions(userid: int) -> int:
        res = cursor.execute("SELECT permissions FROM chatusers WHERE id = %s;", userid)
        if cursor.rowcount == 0:
            return None
        perms = res.fetchone()
        return perms

    @staticmethod
    def get_token_user_id(token: str) -> int:
        if Auth.authorize(token):
            query = "SELECT chatusers.id FROM tokens,chatusers WHERE tokens.user=chatusers.id;"
            cursor.execute(query)
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()[0]
        return None
