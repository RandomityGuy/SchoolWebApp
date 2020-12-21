from api.base import *
import bcrypt
import secrets
import hashlib
import base64


class Auth:
    @staticmethod
    def login(username: str, pwd: str) -> str:
        """Attempt to login as a given username with the password

        Args:
            username (str): The given username
            pwd (str): The password

        Raises:
            Exception: Invalid username
            Exception: No password
            Exception: Invalid password

        Returns:
            str: The token if success
        """

        # !!! WARNING : SEND A HASHED PASSWORD FROM THE SITE, HASH THE PASSWORD WITHIN THE BROWSER AND THEN SEND IT HERE

        cursor.execute("SELECT id,Username,password FROM chatusers WHERE Username = %s;", (username,))

        if cursor.rowcount == 0:
            raise Exception("Invalid username")

        data = cursor.fetchone()

        if data[2] == None:
            raise Exception("No password set")

        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(pwd.encode('utf-8')).digest()), data[2].encode('utf-8')):
            cursor.execute("SELECT token FROM tokens WHERE (expires > CURDATE() && user=%s);", (data[0],))
            if cursor.rowcount == 0:
                # Create new token
                token = secrets.token_hex(128)
                id = snowflakegen.__next__()
                cursor.execute("INSERT INTO tokens VALUES(%s,%s,DATE_ADD(CURDATE(), INTERVAL 1 MONTH),%s);", (id, token, data[0]))
                db.commit()
                return token
            else:
                token = cursor.fetchone()
                return token

        raise Exception("Invalid password")

    @staticmethod
    def register(username: str, pwd: str, permissions: int) -> str:
        """Register a user from given username, password and the permission flags

        Args:
            username (str): The given username
            pwd (str): The password
            permissions (int): The permission flags

        Returns:
            str: The token if sucess
        """
        id = snowflakegen.__next__()
        hash = bcrypt.hashpw(base64.b64encode(hashlib.sha256(pwd.encode('utf-8')).digest()), bcrypt.gensalt())

        cursor.execute("INSERT INTO chatusers VALUES(%s,%s,%s,%s,NULL,NULL);", (id, username, hash, permissions))
        db.commit()

        return Auth.login(username, pwd)

    @staticmethod
    def authorize(token: str) -> bool:
        """Authenticate a token

        Args:
            token (str): The token

        Returns:
            bool: True if success
        """
        cursor.execute("SELECT token FROM tokens WHERE (expires > CURDATE() && token=%s);", (token,))
        if cursor.rowcount == 0:
            return False
        return True

    @staticmethod
    def get_token_permissions(token: str) -> int:
        """Gets the permissions the token has

        Args:
            token (str): The token

        Returns:
            int: The permissions, None if token is expired/doesnt exist
        """
        res = cursor.execute("SELECT permissions FROM tokens,chatusers WHERE (tokens.user = chatusers.id && token = %s);", (token,))
        if cursor.rowcount == 0:
            return None
        perms = res.fetchone()
        return perms

    @staticmethod
    def get_permissions(userid: int) -> int:
        """Gets the permissions for a user

        Args:
            userid (int): The user id

        Returns:
            int: The permissions
        """
        res = cursor.execute("SELECT permissions FROM chatusers WHERE id = %s;", userid)
        if cursor.rowcount == 0:
            return None
        perms = res.fetchone()
        return perms

    @staticmethod
    def get_token_user_id(token: str) -> int:
        """Gets the user id from the token

        Args:
            token (str): The token

        Returns:
            int: The user id, None if token is expired/doesnt exist
        """
        if Auth.authorize(token):
            query = "SELECT chatusers.id FROM tokens,chatusers WHERE tokens.user=chatusers.id;"
            cursor.execute(query)
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()[0]
        return None
