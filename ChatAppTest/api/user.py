from api.base import *;

class User:

    @staticmethod
    def get_avatar(userid):
        ''' Gets the avatar of the user by their user id

            @param userid: the user id of the user
            @returns: the avatar binary data if success else None
        '''
        cursor.execute("SELECT avatar FROM chatusers WHERE Id=%s;",(userid,));
        if (cursor.rowcount == 0):
            return None;
        else:
            data = cursor.fetchone()[0];
            return data;

    @staticmethod
    def set_avatar(userid,avatardata):
        ''' Sets the avatar of the user by their user id

            @param userid: the user id of the user
            @param avatardata: the binary data of the avatar
        '''
        cursor.execute("UPDATE chatusers SET avatar = %s WHERE Id = %s;",(avatardata,userid));
        db.commit();