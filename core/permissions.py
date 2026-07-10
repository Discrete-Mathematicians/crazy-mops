def can_manage_object(user, owner):
    return user.is_authenticated and (user == owner or user.is_staff)
