from apps.utils.db import select_all, insert, get_restaurant_id_from_roomid, select_one
from apps.models.menu import Menu

def showingMenu_from_rid(rid):
    query = "select food_name, food_price from pr_food where restaurant_id = '%d'"
    table_all = select_all(query % (rid))

    return table_all

def save_user_menu(uid, rid, request_data):
    restaurant_id = get_restaurant_id_from_roomid(rid)
    query = "insert into user_orderlist values ('%d', '%d', '%s', '%d', '%d');"
    query2 = "select food_id from pr_food where restaurant_id = '%d' and food_name = '%s'"
    query3 = "select food_price from pr_food where food_id = '%d'"
    query4 = "delete from user_orderlist where room_id = '%d' and user_id = '%d'"
    insert(query4 % (rid, uid))
    for i in range (1, request_data[0]+1):
        food_id = select_one(query2 % (restaurant_id, request_data[i]))
        food_price = select_one(query3 % int(food_id[0]))
        insert(query % (rid, uid,request_data[i], int(food_id[0]), int(food_price[0])))

    return ""