from api.base import *


class User:
    @staticmethod
    def get_avatar(userid: int):
        """Gets the avatar of the user by its id

        Args:
            userid (int): The user id

        Returns:
            str: The avatar data
        """
        cursor.execute("SELECT avatar FROM chatusers WHERE Id=%s;", (userid,))
        if cursor.rowcount == 0:
            return None
        else:
            data = cursor.fetchone()[0]
            return data

    @staticmethod
    def set_avatar(userid: int, avatardata):
        """Sets the avatar for the user to the avatar data

        Args:
            userid (int): The user id
            avatardata ([type]): The avatar binary data
        """
        cursor.execute("UPDATE chatusers SET avatar = %s WHERE Id = %s;", (avatardata, userid))
        db.commit()
