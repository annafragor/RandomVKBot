import admin_conditions as ac
import settings
import user_conditions as uc
import vk_bot as vkb
import get_name as gn
import vk_api
from DBWorker import DBWorker


class UserDialogLogic:
    def __init__(self):
        self.id = 0
        self.text = ''
        self.username = ''
        self.user_worker = DBWorker('User')
        self.attachments = []

    @staticmethod
    def _write_msg(user_id, msg, attachment=()):
        vkb.group_session.method('messages.send', {'user_id': user_id, 'message': msg, 'attachment': attachment})

    def answer(self, item):
        self.id = item['user_id']
        self.text = item['body']
        self.username = gn.get_user_name(item['user_id'])

        is_in_users = self.user_worker.exist(self.id)  # существует ли пользователь в базе

        if self.text == '/start':
            # if self.id not in vkb.users:
            if not is_in_users:
                # если пользователь еще не начинал регистрацию
                # добавить пользователя в базу как неподтвержденного
                self.user_worker.add([self.id, uc.unverified_user, uc.just_started_chatting])

            # elif self.id is in vkb.users and vkb.users[self.id] > uc.unverified_user:
            else:
                if self.user_worker.get('participant_status', 'WHERE `user_id`= ' + str(self.id)) > uc.unverified_user:
                    # если пользователь уже прошел регистрацию
                    self._write_msg(self.id,
                                    'Здравствуйте, ' + self.username + '. Вы уже являетесь участником мероприятия.')
                else:
                    # if vkb.users[self.id] == uc.unverified_user:
                    if self.user_worker.get('participant_status',
                                            'WHERE `user_id`= ' + str(self.id)) == uc.unverified_user:
                        self._write_msg(self.id, 'напишите \'подтверждение\' для участия')

        elif self.text == 'подтверждение':
            # if self.id in vkb.users and vkb.users[self.id] > uc.unverified_user:
            if is_in_users and self.user_worker.get('participant_status',
                                                    'WHERE `user_id`= ' + str(self.id)) > uc.unverified_user:
                self._write_msg(self.id, self.username + ', Вы уже являетесь участником мероприятия.')

            # elif self.id not in vkb.users:
            elif not is_in_users:
                self._write_msg(self.id, 'напишите \'/start\' для начала регистрации')

            else:  # if users[self.id] == uc.unverified_user
                self._write_msg(self.id, 'Вы будете добавлены в ряды участников ' +
                                'после подтверждения вашей заявки администратором')
                self._write_msg(settings.admin_id, self.text + ' от пользователя ' + self.username)
                ac.verify_user = self.id

        elif self.text == 'кек':
            upload = vk_api.VkUpload(vkb.group_session)
            response = upload.photo_messages('/home/anne/programming/VKBot/kek.jpg')

            owner_id = str(response[0]['owner_id'])
            media_id = str(response[0]['id'])
            attachment = 'photo' + owner_id + '_' + media_id
            self._write_msg(self.id, 'ЧТО. ТЫ. СКАЗАЛ?', attachment)

        else:
            self._write_msg(self.id, 'Не понимаю тебя.')
