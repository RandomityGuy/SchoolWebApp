class Permissions:
    STUDENT = 0
    MANAGE_ANNOUNCE = 1
    CAN_MODIFY_AVATAR = 2
    CAN_MODIFY_STUDENT = 4
    CAN_VIEW_ANY_CHANNEL = 8
    MANAGE_ASSIGNMENT = 16

    @staticmethod
    def has_permission(flags: int, permission: int) -> bool:
        """Check if the given flags has the permission

        Args:
            flags (int): The flags
            permission (int): The permission

        Returns:
            bool: True if the flags has permission
        """
        return (flags & permission) == permission
