from __future__ import annotations
from api.channel import Channel
from datetime import date
from api.base import *


class DMRequest(ToDictable):
    MAX_EXPIRE_DAYS = 7

    def __init__(self, id, to_user, by_user, content, expires):
        self.id = id
        self.to_user = to_user
        self.by_user = by_user
        self.content = content
        self.expires = expires

    def toDict(self):
        D = {}
        D["id"] = self.id
        D["to-user"] = self.to_user
        D["by-user"] = self.by_user
        D["content"] = self.content
        D["expires"] = self.expires
        return D

    @staticmethod
    def dm_exists(to_user: int, by_user: int) -> bool:
        """Check if a DM request between two users exists and/or it isnt expired

        Args:
            to_user (int): The user to which the request is to
            by_user (int): The user requesting

        Returns:
            bool: True if DM exists and it isnt expired.
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM dmrequests WHERE to = %s && by = %s && expires > CURDATE();", (to_user, by_user))
            if cursor.rowcount == 0:
                return False
            return True

    @staticmethod
    def request_dm(to_user: int, by_user: int, content: str) -> int:
        """Request a DM to be done to a user by a user.

        Args:
            to_user (int): The user towards which the DM is targeted at
            by_user (int): The user requesting the DM
            content (str): The request

        Returns:
            int: The DM request id
        """
        with DBConnection() as (cursor, conn):
            id = snowflakegen.__next__()
            cursor.execute("INSERT INTO dmrequests VALUES(%s,%s,%s,%s,DATE_ADD(CURDATE(), INTERVAL %s DAY));", (id, to_user, by_user, content, DMRequest.MAX_EXPIRE_DAYS))
            conn.commit()
            return id

    @staticmethod
    def get_sent_dm_requests(for_user: int) -> list[DMRequest]:
        """Gets a list of DM requests for a given user

        Args:
            for_user (int): The given user

        Returns:
            list[DMRequest]: The list of DM requests
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM dmrequests WHERE (by = %s && expires > CURDATE());", (for_user,))
            L = []
            for (id, to, by, content, expires) in cursor:
                L.append(DMRequest(id, to, by, content, date.fromisoformat(expires)))
            return L

    @staticmethod
    def get_dm_requests(for_user: int) -> list[DMRequest]:
        """Gets a list of DM requests for a given user

        Args:
            for_user (int): The given user

        Returns:
            list[DMRequest]: The list of DM requests
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM dmrequests WHERE (to = %s && expires > CURDATE());", (for_user,))
            L = []
            for (id, to, by, content, expires) in cursor:
                L.append(DMRequest(id, to, by, content, date.fromisoformat(expires)))
            return L

    @staticmethod
    def get_dm_request(id: int) -> DMRequest:
        """Gets a specific DM request from its id

        Args:
            id (int): The id of the DM request

        Returns:
            DMRequest: The DM request
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM dmrequests WHERE (id = %s && expires > CURDATE());", (id,))
            if cursor.rowcount == 0:
                return None
            res = cursor.fetchone()
            return DMRequest(res[0], res[1], res[2], res[3], date.fromisoformat(res[4]))

    @staticmethod
    def accept_dm(id: int) -> int:
        """Accepts a DM request and returns the DM channel created

        Args:
            id (int): The DM request id

        Returns:
            int: The DM channel id
        """
        with DBConnection() as (cursor, conn):
            req = DMRequest.get_dm_request(id)
            if req == None:
                return None
            return Channel.create_DM(req.by_user, req.to_user)

    @staticmethod
    def reject_dm(id: int):
        """Rejects a DM request

        Args:
            id (int): The DM request id
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("DELETE FROM dmrequests WHERE id = %s;", (id,))
            conn.commit()
