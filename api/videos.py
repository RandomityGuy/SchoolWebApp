from typing import List
from api.base import *


class Video(ToDictable):
    def __init__(self, id, name, studentclass, link, path):
        self.id = id
        self.name = name
        self.studentclass = studentclass
        self.link = link
        self.path = path

    def toDict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["class"] = self.studentclass
        d["link"] = self.link
        d["path"] = self.path


class Videos:
    @staticmethod
    def store_video(name: str, link: str, studentclass: str, path: str) -> None:
        """Stores the video details to the database to the specified path

        Args:
            name (str): The name of the video
            link (str): The link to the video
            studentclass (str): The class that can view the video
            path (str): The path where the video is to be stored
        """
        with DBConnection() as (cursor, conn):
            id = snowflakegen.__next__()
            cursor.execute("INSERT INTO videos VALUES(%s,%s,%s,%s,%s);", (id, studentclass, name, link, path))
            conn.commit()

    @staticmethod
    def get_all_videos_for_class(studentclass: str) -> list[Video]:
        """Gets all the videos viewable by a class

        Args:
            studentclass (str): The class

        Returns:
            list[Video]: The list of videos
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM videos WHERE class=%s;", (studentclass,))
            ret = []
            for (id, studentclass, name, link, path) in cursor:
                ret.append(Video(id, name, studentclass, link, path))

            return ret

    @staticmethod
    def get_videos_in_folder(studentclass: str, folder: str) -> list[Video]:
        """Gets all the videos viewable by a class in a specified folder

        Args:
            studentclass (str): The student class
            folder (str): The folder path

        Returns:
            list[Video]: The list of videos
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("SELECT * FROM videos WHERE class=%s && path LIKE %s", (studentclass, folder))
            ret = []
            for (id, studentclass, name, link, path) in cursor:
                ret.append(Video(id, name, studentclass, link, path))

            return ret

    @staticmethod
    def get_folders(studentclass: str, folder: str) -> list[str]:
        """Gets a list of folders located in the path

        Args:
            studentclass (str): The student class
            folder (str): The folder path

        Returns:
            list[str]: The list of folder paths
        """
        with DBConnection() as (cursor, conn):
            regex = f"^{folder}\/[A-z0-9]*\/{{0,1}}"
            cursor.execute("SELECT DISTINCT TRIM(TRAILING '/' FROM REGEXP_SUBSTR(path,%s)) FROM videos WHERE path REGEXP %s;", (regex, regex))
            ret = []
            for (folder,) in cursor:
                ret.append(folder)
            return ret

    @staticmethod
    def delete_video(videoid: int):
        """Deletes a video by its id

        Args:
            videoid (int): The video id
        """
        with DBConnection() as (cursor, conn):
            cursor.execute("DELETE FROM videos WHERE id=%s", (videoid,))
            conn.commit()

    @staticmethod
    def modify_video(id: int, name: str, link: str, studentclass: str, path: str):
        """Modifies a video by its id

        Args:
            id (int): The video id
            name (str): The new name
            link (str): The new link
            studentclass (str): The new description
            path (str): The new path
        """
        with DBConnection() as (cursor, conn):
            Videos.delete_video(id)
            # We'll just delete instead and add the new one cause its less lines of code
            cursor.execute("INSERT INTO videos VALUES(%s,%s,%s,%s,%s);", (id, studentclass, name, link, path))
            conn.commit()
