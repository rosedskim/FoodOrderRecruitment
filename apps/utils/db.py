import pyodbc
import hashlib

_db = None

def init_db():
    global _db
    if _db is None:
        _db = pyodbc.connect('DSN=tibero')

def get_cursor():
    return _db.cursor()

def commit():
    _db.commit()

def close():
    _db.close()

def select_one(sql):
    cursor = get_cursor()
    cursor.execute(sql)
    return cursor.fetchone()

def select_all(sql):
    cursor = get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def insert(sql):
    cursor = get_cursor ()
    cursor.execute(sql)
    commit()

def get_id_from_db(get_session):
    query = "select * from pr_session where session_key = '%s'"
    get_table = select_one(query % get_session)
    userTable_id = get_table[0]
    return userTable_id

def get_univid_from_db(univ_name):
    query = "select univ_id from pr_university where univ_name = '%s'"
    get_table = select_one(query % univ_name)

    if get_table is None:
        return False

    univ_id = get_table[0]
    return univ_id

def get_userid_from_db():
    query = "select max(user_id) from pr_user"
    get_table = select_one(query)

    return get_table[0]+1

def get_username_from_db(uid):
    query = "select user_name from pr_user where user_id = '%d'"
    get_table = select_one(query % uid)

    return get_table[0]

def get_restaurantname_from_db(rid):
    query = "select restaurant_name from pr_restaurant where restaurant_id = '%d'"
    get_table = select_one(query % rid)
    return get_table[0]

def do_Hashing(email, pw):
    filehash = hashlib.md5()
    h = '%s/%s' % (email, pw)
    filehash.update(h.encode('utf-8'))
    return filehash.hexdigest()

def get_locationid_from_univ(univ_id):
    query = "select location_id from pr_university where univ_id = '%d'"
    get_table = select_one(query % univ_id)
    return get_table[0]

def get_univ_from_user(user_id):
    query = "select univ_id from pr_user where user_id = '%d'"
    get_table = select_one(query % user_id)
    return get_table[0]

def get_restaurant_id_from_name(restaurant_name):
    query = "select restaurant_id from pr_restaurant where restaurant_name = '%s'"
    get_table = select_one(query % restaurant_name)
    return get_table[0]

def get_room_id_from_session(rsession):
    query = "select room_id from room_session where session_key = '%s'"
    get_table = select_one(query % rsession)
    return get_table[0]

def get_restaurant_id_from_roomid(room_id):
    query = "select restaurant_id from room where room_id = '%d'"
    get_table = select_one(query % room_id)
    return get_table[0]

def get_host_id_from_roomid(room_id):
    query = "select chief_id from room where room_id = '%d'"
    get_table = select_one(query % room_id)
    return get_table[0]