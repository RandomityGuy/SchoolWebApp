class Permissions:
    STUDENT = 0
    MANAGE_ANNOUNCE = 1

    @staticmethod
    def has_permission(flags,permission):
        return (flags & permission) == permission;