from mysql.connector import connect, Error
from datetime import datetime
import bcrypt
import logging
import os
import json

logging.basicConfig(filename=os.path.join(os.getcwd(),'logs.log'), 
                    format='{asctime} {levelname} {funcName}->{lineno}: {msg}', 
                    style='{', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Connect:
    def __init__(self, host, user, password,db):
        self.conn = connect(
            host = host,
            user = user,
            password = password,
            database = db
        )


def connect_to_DB():
    with open(".conf.json") as f: # Открываем конфигурационный файл
        data = json.load(f)
    try:
        connect = Connect(data['mysql']['host'], data['mysql']['user'], data['mysql']['passwrd'].replace('D', 'd'), data['mysql']['db']) # Создаём экземпляр подключения
    except Error as e:
        logger.exception(f'Ошибка подключения БД, SQL: {e}') # Запись ошибок MySQL
        return None
    except Exception as ex:
        logger.exception(f'Ошибка подключения БД, SQL: {ex}') # Запись всех остальных ошибок
        return None
    return connect # Возвращаем экземпляр подключения к БД

def login(name, password):
    try:
        session = connect_to_DB()
        if session:
            with session.conn.cursor() as cursor:
                # cursor.execute(f"SELECT surname, password, level \
                #                FROM users \
                #                WHERE surname = '{name}' AND is_active = true")
                # data = cursor.fetchone()
                data = cursor.callproc('user_login', [name, 0, 0])
                if data[1] and bcrypt.checkpw(password.encode('utf8'), 
                                           data[1].encode('utf8')):
                # if data:
                    return name, data[2]
                else:
                    return False
    except Error as e:
        print('Error: ', e)
        logger.exception(f'Ошибка входа пользователя, SQL: {e}')
    finally:
        if session:
            session.conn.close()

def insert(data):
    
    # query = f"INSERT INTO material (plan, name, type, material, \
    #                                 size, {data[5]}, comments) \
    #         VALUES ('{data[0]}', '{data[1]}', '{data[2]}', \
    #                 '{data[3]}', '{data[4]}', {data[6]}, \
    #                 '{data[9]}')"
    # query2 = f"SELECT id FROM material \
    #             WHERE plan = '{data[0]}' \
    #             AND name = '{data[1]}' \
    #             AND type = '{data[2]}' \
    #             AND material = '{data[3]}' \
    #             AND size = '{data[4]}'"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
        #     time = datetime.now().replace(microsecond=0)
            # if data[5] == 'count':
                # cursor.callproc('insert_with_count', [data[0], data[1], data[2],
                #                                       data[3], data[4], data[6],
                #                                       data[7], data[8], data[9], time])
            # elif data[5] == 'length':
            #     cursor.callproc('insert_with_length', [data[0], data[1], data[2],
            #                                           data[3], data[4], data[6],
            #                                           data[7], data[8], data[9], time])
            # cursor.execute(query)
            # cursor.execute(query2)
            # id_item = cursor.fetchone()[0]
            # time = datetime.now().replace(microsecond=0)
            # query3 = f"INSERT INTO history (item_id, {data[5]}, \
            #                                 datetime, invoice, worker) \
            #         VALUES ('{id_item}', '{data[6]}', \
            #                 '{time}', '{data[7]}', '{data[8]}')"
            # cursor.execute(query3)
            cursor.callproc('insert_material', args=data)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка добавления новой позиции, SQL: {e}')
        return False
    finally:
        session.conn.close()

def update(data, predicat):
    time = datetime.now().replace(microsecond=0)
    option = data[1]
    value = data[2]
    if predicat == '-':
        value = data[2]*(-1)
    args = [data[0], value, time, data[3],
            data[4], data[5], data[6],
            data[7], data[8], predicat]
    # if predicat == '-':
    #     query = f"INSERT INTO history (item_id, {data[1]}, datetime, history.order, \
    #                                 requirement, master, plan_order, worker, receive) \
    #             VALUES ({data[0]}, {data[2]*(-1)}, '{time}', \
    #                     '{data[3]}', '{data[4]}', '{data[5]}', \
    #                     '{data[6]}', '{data[7]}', '{data[8]}')"
    #     query2 = f"UPDATE material SET {data[1]} = {data[1]} - {data[2]} \
    #             WHERE id = {data[0]}"
    # elif predicat == '+':
    #     query = f"INSERT INTO history (item_id, {data[1]}, datetime, invoice, worker) \
    #             VALUES ({data[0]}, {data[2]}, '{time}', '{data[3]}', '{data[4]}')"
    #     query2 = f"UPDATE material SET {data[1]} = {data[1]} + {data[2]} \
    #             WHERE id = {data[0]}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            if option == 'count':
                cursor.callproc('update_count', args=args)
            elif option == 'length':
                cursor.callproc('update_length', args=args)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка выдачи/получения материала, SQL: {e}')
        return False
    finally:
        session.conn.close()

def update_search_fields(flag):
    if flag == 'material':
        query = "SELECT type FROM material \
                WHERE is_active = true \
                GROUP BY type"
        query2 = "SELECT name FROM material \
                WHERE is_active = true \
                GROUP BY name"
        query3 = "SELECT material FROM material \
                WHERE is_active = true \
                GROUP BY material"
    elif flag == 'history':
        query = "SELECT type FROM material \
                INNER JOIN history ON material.id = history.item_id \
                GROUP BY type"
        query2 = "SELECT name FROM material \
                INNER JOIN history ON material.id = history.item_id \
                GROUP BY name"
        query3 = "SELECT history.order \
                FROM history GROUP BY history.order"
        query4 = "SELECT invoice FROM history \
                GROUP BY invoice"
        query5 = "SELECT requirement FROM history \
                GROUP BY requirement"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query2)
            names = [item[0] for item in cursor.fetchall()]
            cursor.execute(query)
            types = [item[0] for item in cursor.fetchall()]
            cursor.execute(query3)
            mat_or_ord = [item[0] for item in cursor.fetchall()]
            if flag == 'material':
                return names, types, mat_or_ord
            cursor.execute(query4)
            invoices = [item[0] for item in cursor.fetchall()]
            cursor.execute(query5)
            requirements = [item[0] for item in cursor.fetchall()]
            return names, types, mat_or_ord, invoices, requirements
    except Error as e:
        print('Error: ', e)
        logger.exception(f'Ошибка получения полей поиска, SQL: {e}')
    finally:
        session.conn.close()

def delete(id):
    query = f"DELETE FROM material WHERE id = {id}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка удаления материала из справочника, SQL: {e}')
        return False
    finally:
        session.conn.close()

def edit(data):
    # query = f"UPDATE material SET plan = '{data[1]}', name = '{data[2]}', type = '{data[3]}', \
    #         material = '{data[4]}', size = '{data[5]}', comments = '{data[6]}' \
    #         WHERE id = {data[0]}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('edit_material', args=data)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка редактирования материала, SQL: {e}')
        return False
    finally:
        session.conn.close()

def get_users(flag=None):
    if flag == 'all':
        query = "SELECT surname, level, id_user, is_active FROM users"
    else:
        query = "SELECT surname FROM users WHERE is_active = true"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
    except Error as e:
        print('Error: ', e)
        logger.exception(f'Ошибка получения списка пользователей, SQL: {e}')
    finally:
        session.conn.close()

def get_last_invoice():
    query = "SELECT invoice FROM history ORDER BY id DESC"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            data = [item[0] for item in cursor.fetchall() if item[0] != '']
            if data:
                return data[0]
            else:
                return None
    except Error as e:
        print('Error: ', e)
        logger.exception(f'Ошибка получения списка пользователей, SQL: {e}')
    finally:
        session.conn.close()

def add_user(data):
    hash_password = bcrypt.hashpw(data[1].encode('utf8'), bcrypt.gensalt())
    args = data[0], hash_password.decode(), data[2]
    # query = f'INSERT INTO users (surname, password, level) VALUES ("{data[0]}", "{hash_password.decode()}", {data[2]})'
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('user_add', args=args)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка добавления пользователя, SQL: {e}')
        return False
    finally:
        session.conn.close()

def delete_user(id):
    # query = f"UPDATE users SET is_active = false WHERE id_user = {id}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('user_delete', [id])
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка удаления пользователя, SQL: {e}')
        return False
    finally:
        session.conn.close()

def recover_user(id):
    # query = f"UPDATE users SET is_active = true WHERE id_user = {id}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('user_recovery', [id])
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка восттановления пользователя, SQL: {e}')
        return False
    finally:
        session.conn.close()

def change_password(data):
    hash_password = bcrypt.hashpw(data[1].encode('utf8'), bcrypt.gensalt())
    args = data[0], hash_password.decode()
    # query = f'UPDATE users SET password = "{hash_password.decode()}" WHERE id_user = {data[0]}'
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('password_change', args=args)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка смены пароля, SQL: {e}')
        return False
    finally:
        session.conn.close()

def change_lvl(data):
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('level_change', args=data)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка смены уровня, SQL: {e}')
        return False
    finally:
        session.conn.close()

def get_invoice_obj(obj):
    query = f"SELECT m.name, m.type,  m.size, m.material, h.count, \
                    h.length, h.invoice, h.order, h.master, h.worker \
            FROM history h INNER JOIN material m ON m.id = h.item_id \
            WHERE h.invoice = '{obj.invoice}'"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
    except Exception as e:
        print('Error: ', e)
        logger.exception(f'Ошибка получения списка на печать, SQL: {e}')
    finally:
        session.conn.close()

def edit_record(data):
    query = f"UPDATE material SET {data[1]} = {data[2]} WHERE id = {data[0]}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка выдачи/получения материала, SQL: {e}')
        return False
    finally:
        session.conn.close()

def add_to_base(id, flag):
    query = ''
    if flag == 'count':
        query = f"UPDATE material SET count = 0, length = NULL, is_active = 1 WHERE id = {id}"
    elif flag == 'length':
        query = f"UPDATE material SET length = 0, count = NULL, is_active = 1 WHERE id = {id}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.execute(query)
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка добавления материала в базу, SQL: {e}')
        return False
    finally:
        session.conn.close()

def remove_from_base(id):
    # query = f"UPDATE material SET is_active = false WHERE id = {id}"
    try:
        session = connect_to_DB()
        with session.conn.cursor() as cursor:
            cursor.callproc('delete_material', [id])
            session.conn.commit()
            return True
    except Error as e:
        print(e)
        session.conn.rollback()
        logger.exception(f'Ошибка удаления материала из базы, SQL: {e}')
        return False
    finally:
        session.conn.close()