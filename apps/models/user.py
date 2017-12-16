from apps.utils.db import select_one, select_all, get_univid_from_db, get_userid_from_db, do_Hashing


class User:
    def __init__(self):
        self.user_id = None
        self.univ_id = None
        self.user_name=None
        self.user_email = None
        self.user_pw= None

    @classmethod
    def create_from_request(cls, request_data):
        user = User()
        user.user_email = request_data['email']
        user.user_pw = request_data['passwd']
        if 'username' in request_data:
            user.user_name = request_data['username']
            user.univ_id = get_univid_from_db(request_data['univ'])
            if user.univ_id is False:
                return None

        return user

    def getHashing(self):
        self.user_pw = do_Hashing(self.user_email, self.user_pw)

