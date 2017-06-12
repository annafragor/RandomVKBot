import pymysql


class DBWorker:
    def __init__(self, with_who):
        self.connection = pymysql.connect(host='localhost', user='root', passwd='annesqlacc', db='workdb')
        self.cursor = self.connection.cursor()
        self.db_name = with_who

    def _get_id_name(self):
        if self.db_name == 'User':
            return 'user_id'
        else:
            return 'admin_id'

    def get(self, what, condition_to_select=''):
        sql = 'SELECT `' + what + '` FROM `' + self.db_name + '`' + condition_to_select
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def exist(self, required_id):
        self.cursor.execute('SELECT * FROM ' + self.db_name + ' WHERE `user_id` = ' + str(required_id))
        if self.cursor.fetchall():
            return True
        else:
            return False

    def add(self, values):
        if len(values) != 3:
            print('Can\'t add your string to the table ', self.db_name)
            return

        if self.db_name == 'User':
            sql = 'INSERT INTO User (user_id, participant_status, chat_status) VALUES (%s, %s, %s)'
        else:
            sql = 'INSERT INTO Administrator (admin_id, admin_status, confirm_user) VALUES (%s, %s, %s)'
        self.cursor.execute(sql, values)
        self.cursor.connection.commit()

    def update(self, what, new_value, required_id):
        id_name = self._get_id_name()
        sql = 'UPDATE ' + self.db_name + ' SET ' + what + ' = %s WHERE ' + id_name + ' = %s'
        self.cursor.execute(sql, (new_value, required_id))
        self.cursor.connection.commit()

    def delete_string(self, required_id):
        sql = 'DELETE FROM ' + self.db_name + ' WHERE ' + self._get_id_name() + ' = %s'
        self.cursor.execute(sql, (required_id,))
        self.cursor.connection.commit()
