import with_admin as wa
import with_user as wu
import settings
import auth
import time


own_session = auth.own_auth()
group_session = auth.group_auth()

# ПОДОБИЕ БД
# users = {}
# admins = {settings.admin_id: ac.verified}


def get_user_name(message):
    values_for_users = {'user_ids': [message['user_id']]}
    user = own_session.method('users.get', values_for_users)
    return user[0]['first_name']


def write_msg(user_id, s):
    group_session.method('messages.send', {'user_id': user_id, 'message': s})


def main():
    values = {'out': 0, 'count': 100, 'time_offset': 10}
    group_session.method('messages.get', values)

    admin_logic = wa.AdminDialogLogic()
    user_logic = wu.UserDialogLogic()

    while True:
        # массив объектов "личное сообщение"
        response_messages = group_session.method('messages.get', values)
        if response_messages['items']:
            values['last_message_id'] = response_messages['items'][0]['id']

        for item in response_messages['items']:
            current_id = item['user_id']
            if current_id == settings.admin_id:  # if current_id in admins:
                admin_logic.answer(item)
            else:
                user_logic.answer(item)

        time.sleep(1)

if __name__ == '__main__':
    main()
