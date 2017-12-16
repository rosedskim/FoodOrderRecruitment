from __future__ import division
import pandas as pd
from sklearn.cluster import KMeans
from flask import Flask, send_file, redirect
from flask import render_template, request, jsonify
from apps.models.user import User
from apps.models.room import Room
import json
from apps.controllers.login import signin, save_user
from apps.controllers.room import save_room, roomin, intoTheRoom, outOfTheRoom, selectPayer, getUserNumber, getPayerInfo, CompleteOrder, calculateTotal
from apps.controllers.menu import showingMenu_from_rid, save_user_menu
from apps.utils.db import init_db, get_id_from_db, select_one, select_all, insert, get_username_from_db, get_restaurantname_from_db, get_locationid_from_univ, get_univ_from_user, get_room_id_from_session, get_restaurant_id_from_roomid, get_host_id_from_roomid
from apps.utils.token import check_token, check_room_token


app = Flask(__name__, template_folder='../templates', static_folder = '../static')


@app.route("/")
def index():
    if check_token():
        return render_template("main.html"), 200
    return render_template("login.html"), 200

@app.route("/static/js/login.js")
def loginjs():
    return send_file('..\\static\\js\\login.js')

@app.route("/static/js/main.js")
def mainjs():
    return send_file('..\\static\\js\\main.js')

@app.route("/static/js/CreationRoom.js")
def creationroomjs():
    return send_file('..\\static\\js\\CreationRoom.js')

@app.route("/static/css/login.css")
def logincss():
    return send_file('..\\static\\css\\login.css')

@app.route("/static/css/main.css")
def maincss():
    return send_file('..\\static\\css\\main.css')

@app.route("/static/css/CreationRoom.css")
def creationroomcss():
    return send_file('..\\static\\css\\CreationRoom.css')

@app.route("/user", methods=["POST"])
def login():
    #print("login")
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    user=User.create_from_request(data)
    #user.getUserEmail()
    user.getHashing()

    response=signin(user)

    return response

@app.route("/user", methods=["PUT"])
def signup():
    #print("signup")
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    user=User.create_from_request(data)

    if(user is not None):
        user.getHashing()


    response=save_user(user)
    return response

@app.route('/createroom', methods=["PUT"])
def create_room():
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    room = Room.create_from_request(data)

    get_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(get_session)
    univ_id = get_univ_from_user(user_id)
    room.host_id = user_id
    room.location_id = get_locationid_from_univ(univ_id)

    response = save_room(room)

    return response

@app.route("/roomList", methods=["GET"])
def roomList():
    get_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(get_session)

    query = "select chief_id, room_title, restaurant_id, created, room_id from room as r1, (select e2.location_id as location_id from (select univ_id from pr_user where user_id = '%d') as e1, pr_university as e2 where e1.univ_id = e2.univ_id) as r2 where r1.room_exist = 1 and r1.location_id = r2.location_id order by created desc;"
    table_all = select_all(query % user_id)
    room_List = list()
    for table_one in table_all:
        username = get_username_from_db(table_one[0])
        rname = get_restaurantname_from_db(table_one[2])
        room_dic = { 'user_name':username,'room_title': table_one[1], 'restaurant_name':rname,'created':table_one[3], 'room_id':table_one[4]}
        room_List.append(room_dic)

    return jsonify(results = room_List)

@app.route('/room/<int:room_id>')
def show_room(room_id):
    if check_token():
        if check_room_token(room_id):
            query = "select chief_id from room where room_id = '%d'"
            host_id = select_one(query % room_id)

            query = "select user_name from pr_user where user_id = '%d'"
            host_name = select_one(query % host_id[0])

            query2 = "select restaurant_name, restaurant_location, restaurant_phone, r1.restaurant_id from pr_restaurant as r1, (select restaurant_id from room where room_id = '%d') as r2 where r1.restaurant_id = r2.restaurant_id;"
            restaurant_info = select_one(query2 % room_id)

            query3 = "select room_title from room where room_id = '%d'"
            room_title = select_one(query3 % room_id)

            query4 = "select created from room where room_id = '%d'"
            created = select_one(query4 % room_id)

            query5 = "select room_inwon from room where room_id = '%d'"
            room_inwon = select_one(query5 % room_id)

            menu_table = showingMenu_from_rid(restaurant_info[3])

            return render_template("room.html", host_name = host_name[0], rname = restaurant_info[0], rlocation = restaurant_info[1], rphone = restaurant_info[2], menu_table = menu_table, room_title = room_title[0], created = created[0], room_inwon = int(room_inwon[0])), 200

        return render_template("password.html", room_id = room_id), 200

@app.route('/showTotal', methods=["GET"])
def show_total():
    pr_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(pr_session)

    query = "select taker, price from total_price where giver = '%d'"    #내가 줘야되는 돈
    query2 = "select user_name from pr_user where user_id = '%d'"
    query3 = "select giver, price from total_price where taker = '%d'"   #내가 받아야되는 돈
    table_all = select_all(query % user_id)
    get_table = select_one(query2 % user_id)
    myname = get_table[0]

    pay_list = list()
    for table_one in table_all:
        name = select_one(query2 % table_one[0])
        taker_name = name[0]
        pay_dic = {'giver': myname, 'taker':taker_name, 'price': table_one[1]}
        pay_list.append(pay_dic)

    payed_list = list()
    table_all = select_all(query3 % user_id)
    for table_one in table_all:
        name = select_one(query2 % table_one[0])
        giver_name = name[0]
        pay_dic = {'giver': giver_name, 'taker': myname, 'price': table_one[1]}
        payed_list.append(pay_dic)
    return jsonify(results = pay_list, results2 = payed_list)

@app.route("/recommend", methods=["GET"])
def user_recommend():
    get_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(get_session)

    query = "select chief_id, room_title, restaurant_id, created, room_id from room as r1, (select e2.location_id as location_id from (select univ_id from pr_user where user_id = '%d') as e1, pr_university as e2 where e1.univ_id = e2.univ_id) as r2 where r1.location_id = r2.location_id order by created desc;"
    table_all = select_all(query % user_id)
    room_List = list()
    for table_one in table_all:
        username = get_username_from_db(table_one[0])
        rname = get_restaurantname_from_db(table_one[2])
        room_dic = { 'user_name':username,'room_title': table_one[1], 'restaurant_name':rname,'created':table_one[3], 'room_id':table_one[4]}
        room_List.append(room_dic)

    myindex = 0
    query = "select user_id from pr_user"
    userAll = select_all(query)

    userList = list()
    for index in userAll:
        userList.append(index[0])

    sets = [set() for _ in range(0, len(userList))]

    for index in range(0, len(userList)):
        if (userList[index] == user_id):
            myindex = index
        query = "select food_id from user_orderlist where user_id = '%d'"
        temp = select_all(query % userList[index])
        orderList = list()
        for i in temp:
            orderList.append(i[0])

        for i in range(0, len(orderList)):
            sets[index].add(orderList[i])

    datas = []

    for i in range(0, len(userList)):
        temp = []
        for j in range(0, len(userList)):
            if (i != j):
                a = sets[i]
                b = sets[j]
                temp.append(len(a & b) / len(a | b))
            else:
                temp.append(0)

        datas.append(temp)
    #print(datas)
    df_x = pd.DataFrame(datas)
    nCluster = len(userList) ** 0.5

    kmeans = KMeans(n_clusters=round(nCluster), random_state=0).fit(df_x)
    print(kmeans.labels_)
    recommands = set()
    mine = sets[myindex]
    print(myindex)
    for index in range(0,len(kmeans.labels_)):
        if (kmeans.labels_[myindex] == kmeans.labels_[index]):
            recommands = recommands.union(sets[index] - mine)

    recommend_list = list(recommands)
    print(recommend_list)
    list_len = len(recommend_list)
    recommend_info = list()
    i = 100
    print(len(recommend_list))
    while i < 120:
        if(recommend_list[i] >= 10000):
            print(recommend_list[i])
            query = "select restaurant_id from pr_food where food_id = '%d'"
            get_table = select_one(query % recommend_list[i])
            query2 = "select restaurant_name from pr_restaurant where restaurant_id = '%d'"
            rname = select_one(query2 % get_table[0])
            restaurant_name = rname[0]
            query3 = "select food_name from pr_food where food_id = '%d'"
            fname = select_one(query3 % recommend_list[i])
            food_name = fname[0]
            query4 = "select food_price from pr_food where food_id = '%d'"
            fprice = select_one(query4 % recommend_list[i])
            food_price = fprice[0]
            rdic = {'restaurant_name': restaurant_name, 'food_name': food_name, 'food_price': food_price}
            recommend_info.append(rdic)
        i+=1

    return jsonify(results = recommend_info)

@app.route('/roomlogin', methods=["POST"])
def room_login():
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    get_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(get_session)
    response = roomin(data, user_id)

    room_id = int(data['roomid'])
    intoTheRoom(room_id, user_id)

    return response

@app.route('/roomOut', methods=["GET"])
def room_out():
    pr_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(pr_session)
    room_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(room_session)
    response = outOfTheRoom(room_id, user_id)

    return response

@app.route('/select')
def select_menu():
    get_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(get_session)
    pr_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(pr_session)

    host_id = get_host_id_from_roomid(room_id)

    query = "select restaurant_id from room where room_id = '%d'"
    restaurant_id = select_one(query % (room_id))

    query = "select food_name, food_price from pr_food where restaurant_id = '%d'"
    food_table = select_all(query % int(restaurant_id[0]))
    food_List = list()
    for table_one in food_table:
        food_dic = {'food_name': table_one[0], 'food_price': table_one[1]}
        food_List.append(food_dic)

    uinfo = list()

    if host_id == user_id:
        info = 0
        uinfo.append(info)
    else:
        query = "select user_name from pr_user where user_id = '%d'"
        get_table = select_one(query % user_id)
        info = get_table[0]
        uinfo.append(info)

    return jsonify(results = food_List, results2 = uinfo)

@app.route('/roomMember', methods = ["GET"])
def room_member():
    room_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(room_session)

    menu_list = list()

    query1 = "select user_id from room_list where room_id = '%d' and user_present = 1"
    user_table = select_all(query1 % (room_id))

    restaurant_id = get_restaurant_id_from_roomid(room_id)
    query2 = "select food_name, food_price from user_orderlist where user_id = '%d' and room_id = '%d' order by user_id" #음식 정보 가져오기
    query3 = "select user_name from pr_user where user_id = '%d'"   #유저이름 가져오기
    query4 = "select user_ready from room_list where room_id = '%d' and user_id = '%d' and user_present = 1"    #유저 레디 정보 가져오기
    ftable_dic = dict()

    for utable_one in user_table:
        total_price = 0
        food_list = list()
        food_table = select_all(query2 % (int(utable_one[0]), room_id))
        for ftable_one in food_table:
            ftable_dic = {'food_name': ftable_one[0], 'food_price': ftable_one[1]}
            total_price += int(ftable_one[1])
            food_list.append(ftable_dic)

        user_name = select_one(query3 % utable_one[0])
        ready = select_one(query4 % (room_id, utable_one[0]))
        utable_dic = {'user_name': user_name[0], 'user_choice': food_list, 'user_pay': total_price, 'user_ready': ready[0]}
        menu_list.append(utable_dic)

    uinfo = list()
    for table_one in user_table:
        query = "select user_name from pr_user where user_id = '%d'"
        uname = select_one(query % table_one[0])
        p_dic = {'user_name': uname[0], 'user_id': table_one[0]}
        uinfo.append(p_dic)

    return jsonify(results = menu_list, results2 = uinfo)

@app.route('/finalOrder', methods = ["PUT"])
def final_decision():
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    room_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(room_session)
    ready_number=getUserNumber(room_id)
    total_num = int(data)

    if ready_number == total_num:
        payerID = getPayerInfo(room_id)
        if payerID is None:
            return "결제자 선택이 완료되지 않았습니다", 400

        response = CompleteOrder(room_id)
        if response is None:
            return "이미 최종 선택된 방입니다", 400

        response = calculateTotal(room_id)
        return response

    return "전원 준비되지 않았습니다", 400



@app.route('/orderReady', methods = ["POST"])
def order_ready():
    pr_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(pr_session)
#유저 id와 방 id를 가지고 RoomList에서 user_ready를 1로 바꿔주면 땡
    room_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(room_session)

    query = "select user_ready from room_list where user_present = 1 and room_id = '%d' and user_id = '%d'"
    ready = select_one(query % (room_id, user_id))

    if ready[0]:
        query2 = "update room_list set user_ready = 0 where room_id = '%d' and user_id = '%d' and user_present = 1"
        insert(query2 % (room_id, user_id))
    else:
        query2 = "update room_list set user_ready = 1 where room_id = '%d' and user_id = '%d' and user_present = 1"
        insert(query2 % (room_id, user_id))

    return jsonify(results = ready[0])


@app.route('/order', methods=["PUT"])
def order_menu():
    try:
        data=json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    pr_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(pr_session)
    room_session = request.cookies.get('room_session')
    room_id = get_room_id_from_session(room_session)

    save_user_menu(user_id, room_id, data)

    return ""

@app.route('/getPayer', methods=["PUT"])
def get_payer():
    try:
        data = json.loads(request.data)
    except ValueError:
        return "Input must be json format", 400

    if data != None:
        room_session = request.cookies.get('room_session')
        room_id = get_room_id_from_session(room_session)
        response = selectPayer(room_id, data['user_id'])
        return response

    return -1


@app.route('/creation')
def new_room():
    if check_token():
        return render_template("CreationRoom.html"), 200

@app.route('/restaurant<int:rid>', methods={"GET"})
def restaurant(rid):
    get_session = request.cookies.get('pr_session')
    user_id = get_id_from_db(get_session)

    query = "select restaurant_name, restaurant_phone, restaurant_location, restaurant_id from pr_restaurant as r1, (select e2.location_id as location_id from (select univ_id from pr_user where user_id = '%d') as e1, pr_university as e2 where e1.univ_id = e2.univ_id) as r2 where r1.location_id = r2.location_id and r1.restaurant_kind = '%d';"
    query2 = "select food_name, food_price from pr_food where restaurant_id = '%d'"

    table_all = select_all(query % (user_id, rid))
    restaurant_List = list()
    menu_dic = dict()

    for table_one in table_all:
        menu_list = list()
        menu_table = select_all(query2 % int(table_one[3]))
        for mtable_one in menu_table:
            menu_dic = {'food_name': mtable_one[0], 'food_price': mtable_one[1]}
            menu_list.append(menu_dic)


        r_dic = {'phoneNumber': table_one[1], 'location': table_one[2], 'title': table_one[0], 'menulist': menu_list}
        restaurant_List.append(r_dic)

    return jsonify(results = restaurant_List)


if __name__ == '__main__':
    app.debug = True
    init_db()
    app.run('163.180.118.174', port = 5000)
