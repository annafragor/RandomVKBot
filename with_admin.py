from get_name import get_user_name
from DBWorker import DBWorker
import admin_conditions as ac
import user_conditions as uc
import vk_bot as vkb
import vk_api
import urllib.request
import shutil
import requests


class AdminDialogLogic:
    def __init__(self):
        self.id = 0
        self.text = ''
        self.username = ''
        self.attachments = []

        self.admin_worker = DBWorker('Administrator')
        self.user_worker = DBWorker('User')

    @staticmethod
    def _write_msg(user_id, msg, attachment=()):
        vkb.group_session.method('messages.send', {'user_id': user_id, 'message': msg, 'attachment': attachment})

    def confirm_user(self):
        res = self.admin_worker.get('confirm_user', condition_to_select=('WHERE `admin_id` = ' + str(self.id)))
        return res[0]

    def answer(self, item):
        self.id = item['user_id']
        self.text = item['body']
        self.username = get_user_name(item['user_id'])

        if 'attachments' in item:
            self.attachments = item['attachments']

        if self.text == '/start' or self.text == 'подтверждение':
            self._write_msg(self.id, 'Здравствуйте, ' + self.username + '. Вы уже являетесь администратором.')

        elif self.text == 'ок':
            if self.confirm_user() > 0:  # если админ этим сообщением должен одобрить чью-либо заявку
                participant_name = get_user_name(ac.verify_user)
                self._write_msg(self.id, 'Участник ' + participant_name + ' одобрен.')
                self._write_msg(ac.verify_user, 'Администратор рассмотрел вашу заявку. Теперь вы - участник!')
                vkb.users[ac.verify_user] = uc.verified_user
                ac.verify_user = 0

            else:
                self._write_msg(self.id, 'Новых заявок на участие нет.')

        elif self.text == 'кек':
            upload = vk_api.VkUpload(vkb.group_session)
            response = upload.photo_messages('/home/anne/programming/VKBot/kek.jpg')

            owner_id = str(response[0]['owner_id'])
            media_id = str(response[0]['id'])
            attachment = 'photo' + owner_id + '_' + media_id
            self._write_msg(self.id, 'ЧТО. ТЫ. СКАЗАЛ?', attachment)

        else:
            self._write_msg(self.id, 'Не понимаю тебя.')

        if self.attachments:
            k = 0
            url = ''
            for attachment in self.attachments:
                if attachment['photo']['photo_807']:
                    url = attachment['photo']['photo_807']
                elif attachment['photo']['photo_604']:
                    url = attachment['photo']['photo_604']
                elif attachment['photo']['photo_130']:
                    url = attachment['photo']['photo_130']

                file_name = '/home/anne/programming/VKBot/' + str(self.id) + '_' + str(k) + '.jpg'
                req = requests.get(url)
                file = open(file_name, 'wb')
                for chunk in req.iter_content(100000):
                    file.write(chunk)
                file.close()
