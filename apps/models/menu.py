from apps.utils.db import select_one, select_all, get_univid_from_db, get_userid_from_db, do_Hashing

class Menu:
    def __init__(self):
        self.food_name = None
        self.food_price = None
