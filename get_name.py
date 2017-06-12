import vk_bot as vkb


def get_user_name(user_id):
    values_for_users = {'user_ids': user_id}
    user = vkb.own_session.method('users.get', values_for_users)
    return user[0]['first_name']
