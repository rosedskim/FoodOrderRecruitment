from apps.utils.db import select_one, select_all, get_univid_from_db, get_userid_from_db, do_Hashing

class Room:
    def __init__(self):
        self.restaurant_id = None
        self.restaurant_name = None
        self.room_pw = None
        self.room_title = None
        self.room_inwon = None
        self.host_id = None
        self.location_id = None
        self.room_id = None


    @classmethod
    def create_from_request(cls, request_data):
        room_d = Room()
        room_d.room_title = request_data['title']
        room_d.room_pw = request_data['password']
        room_d.restaurant_name = request_data['rname']
        room_d.room_inwon = request_data['number']
        
        #if room.room_title is None or room.room_pw is None or room.restaurant_name is None or room.room_inwon is None:
        #    return None

        return room_d
