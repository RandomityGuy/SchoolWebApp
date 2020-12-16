from api.permissions import Permissions
from api.user import User
from api.base import *


class StudentClass:
    def get_everyone_for_class(classname: str) -> list[User]:
        """Gets a list of members for a given class

        Args:
            classname (str): The class name

        Returns:
            list[User]: The list of students
        """
        cursor.execute("SELECT id, username, permissions FROM chatusers WHERE class=%s;", (classname,))
        L = []
        for (id, username, perms) in cursor:
            L.append(User(id, username, perms, classname, f"/users/{id}/avatar"))
        return L

    def get_students_for_class(classname: str) -> list[User]:
        """Gets a list of students for a given class

        Args:
            classname (str): The class name

        Returns:
            list[User]: The list of students
        """
        cursor.execute("SELECT id, username, permissions FROM chatusers WHERE (class=%s && ((permissions & %s) != %s));", (classname, Permissions.CLASS_T, Permissions.CLASS_T))
        L = []
        for (id, username, perms) in cursor:
            L.append(User(id, username, perms, classname, f"/users/{id}/avatar"))
        return L

    def get_class_teachers(classname: str) -> list[User]:
        """Gets a list of class teachers for a given class

        Args:
            classname (str): The class name

        Returns:
            list[User]: The list of class teachers
        """
        cursor.execute("SELECT id, username, permissions FROM chatusers WHERE (class=%s && ((permissions & %s) == %s));", (classname, Permissions.CLASS_T, Permissions.CLASS_T))
        L = []
        for (id, username, perms) in cursor:
            L.append(User(id, username, perms, classname, f"/users/{id}/avatar"))
        return L

    def get_staff() -> list[User]:
        """Gets a list of staff members of the school

        Returns:
            list[User]: The list of staff members
        """
        cursor.execute("SELECT id, username, permissions FROM chatusers WHERE (class=%s && ((permissions & %s) == %s));", ("Staff", Permissions.SUPERUSER, Permissions.SUPERUSER))
        L = []
        for (id, username, perms) in cursor:
            L.append(User(id, username, perms, "Staff", f"/users/{id}/avatar"))
        return L

    def get_classes() -> list[str]:
        """Gets a list of classes

        Returns:
            list[str]: The list of classes
        """
        cursor.execute("SELECT DISTINCT class FROM chatusers")
        L = []
        for (res,) in cursor:
            L.append(res)
        return L
