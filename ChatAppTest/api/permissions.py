class Permissions:
    STUDENT = 0
    MANAGE_ANNOUNCE = 1
    CAN_MODIFY_AVATAR = 2

    @staticmethod
    def has_permission(flags: int, permission: int) -> bool:
        return (flags & permission) == permission
