from apps.utils.db import insert, select_one
from flask import jsonify
from apps.utils.token import set_token
import time


def get_user(user):
    query="select * from pr_user where user_email ='%s'"
    user=select_one(query % user.user_email)
    return user


def signin(user):
    dbuser=get_user(user)
    if dbuser is None:
        return "User not existed", 404

    if dbuser[4] != user.user_pw:
        return "Incorrect password", 400

    response=set_token(time.time(),dbuser)

    return response


def save_user(user):
    if user is None:
        return "Unvalid university name", 400

    if get_user(user)is not None:
        return "User already existed", 409

    query="insert into pr_user values (USER_ID_SEQ.nextval , '%d', '%s','%s','%s')"
    insert(query % (user.univ_id, user.user_name, user.user_email, user.user_pw))
    return ""

