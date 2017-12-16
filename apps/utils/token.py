import hashlib
from apps.utils.db import insert, select_one
from flask import current_app, request, make_response, render_template
from datetime import datetime

def set_token(time, user):
    corrent_time = str(time)
    filehash = hashlib.md5()
    h = '%s/%s/%s' % (user[3], user[4], corrent_time)
    filehash.update(h.encode('utf-8'))
    filename = filehash.hexdigest()

    response = current_app.make_response("/")
    response.set_cookie('pr_session', value=filename)

    query = "insert into pr_session values ('%d','%s', SYSDATE)"
    insert(query % (user[0], filename))

    return response

def check_token():
    if 'pr_session' in request.cookies:
        return True
    else:
        return False

def set_room_token(time, rid, rpw, uid):
    current_time = str(time)
    filehash = hashlib.md5()
    h = '%s/%s/%s/%s' % (rid, uid, rpw, current_time)
    filehash.update(h.encode('utf-8'))
    filename = filehash.hexdigest()

    response = current_app.make_response("/")
    response.set_cookie('room_session', value = filename)

    query = "insert into room_session values ('%s', '%d', '%d', SYSDATE)"
    insert(query % (filename, int(uid), int(rid)))

    return response

def check_room_token(room_id):
    if 'room_session' in request.cookies:
        session_key = request.cookies['room_session']
        query = "select room_id from room_session where session_key = '%s'"
        table = select_one(query % (session_key))
        if room_id == int(table[0]):
            return True
    return False