from apps.utils.db import insert, get_restaurant_id_from_name, select_one, select_all
from apps.models.room import Room
from apps.utils.token import set_room_token
import time

def save_room(room_d):
    if room_d is None:
        return "Unvalid input", 404

    query = "insert into room (ROOM_ID, LOCATION_ID, CHIEF_ID, RESTAURANT_ID, ROOM_EXIST, CREATED, ROOM_PW, ROOM_TITLE, ROOM_INWON) values (ROOM_ID_SEQ.nextval, '%d', '%d', '%d', 1, SYSDATE, '%s', '%s', '%d')"
    room_d.restaurant_id = get_restaurant_id_from_name(room_d.restaurant_name)
    insert(query % (room_d.location_id, room_d.host_id, room_d.restaurant_id, room_d.room_pw, room_d.room_title, int(room_d.room_inwon)))
    #이 부분 전체적인 수정필요.

    return ""

def getRoom(request_data):
    room = Room()
    room.room_pw = request_data['passwd']
    room.room_id = request_data['roomid']

    query = "select room_pw from room where room_id = '%d'"
    table = select_one(query % int(room.room_id))

    if table[0] != room.room_pw:
        room = None

    return room

def roomin(request_data, uid):
    room = getRoom(request_data)
    if room is None:
        return "Unvalid password!", 400

    response =  set_room_token(time.time(), room.room_id, room.room_pw, uid)

    return response

def intoTheRoom(room_id, user_id):
    query1 = "update room_list set user_present = 0 where user_id = '%d' and user_present = 1"
    insert(query1 % user_id)

    query2 = "insert into room_list values('%d', '%d', 1, 0)"
    insert(query2 % (room_id, user_id))

    return ""

def outOfTheRoom(room_id, user_id):
    query = "update room_list set user_present = 0 where room_id = '%d'and user_id = '%d'"
    query2 = "delete from user_orderlist where room_id = '%d' and user_id = '%d'"
    insert(query % (int(room_id), int(user_id)))
    insert(query2 % (room_id, user_id))
    return ""

def selectPayer(room_id, user_id):
    query = "update room set payer_id = '%d' where room_id = '%d'"
    insert(query% (int(user_id), room_id))
    return ""

def getUserNumber(room_id):
    query = "select count(user_id) from room_list where user_present = 1 and room_id = '%d' and user_ready = 1"
    get_table = select_one(query % room_id)
    return get_table[0]

def getPayerInfo(room_id):
    query = "select payer_id from room where room_id = '%d'"
    get_table = select_one(query % room_id)
    if get_table is None:
        return None
    else:
        return get_table[0]

def CompleteOrder(room_id):
    query = "select room_exist from room where room_id = '%d'"
    get_table = select_one(query % room_id)
    room_exist = get_table[0]

    if(room_exist == 0):
        return None

    query = "update room set room_exist = 0 where room_id = '%d'"
    insert(query % room_id)
    return ""

def calculateTotal(room_id):
    query = "select payer_id from room where room_id = '%d'"
    get_table = select_one(query % room_id)
    payer_id = get_table[0]

    query = "select user_id from room_list where room_id = '%d' and user_present = 1"
    get_table = select_all(query % room_id)
    user_list = list()
    query = "select sum(food_price) from user_orderlist where room_id = '%d' and user_id = '%d' group by user_id"
    for one_table in get_table:
        user_id = one_table[0]
        if payer_id == user_id:
            continue
        price = select_one(query % (room_id, user_id))
        user_price = price[0]
        user_dic = {'user_id': user_id, 'user_price': user_price}
        user_list.append(user_dic)

    list_length = len(user_list)
    i = 0
    query = "insert into total_price (giver, taker, price, room_id) values ('%d', '%d', '%d', '%d')"
    while i < list_length:
        insert(query % (user_list[i]['user_id'], payer_id, user_list[i]['user_price'], room_id))
        i+=1

    return ""
