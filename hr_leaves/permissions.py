from rolepermissions.permissions import register_object_checker
from .roles import SuperAdmin, Administrateur, Receveur, Simple_user, Manager

@register_object_checker()
def access_list_taxe(role, user):
    if role == SuperAdmin or role == Administrateur or role == Receveur or role == Simple_user or role == Manager :
        return True
    else:
        return False

def edit_taxe(role, user):
    if role == SuperAdmin or role == Administrateur or role == Receveur:
        return True
    else:
        return False