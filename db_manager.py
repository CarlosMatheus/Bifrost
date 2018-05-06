import pyrebase

class DbManager:

    firebase = None
    db = None

    @classmethod
    def init_db(cls) -> None:
        config = {
            "apiKey": "AIzaSyASmIDrS3ZTZt0Zk8L0h3T51mNVcMvaRFQ",
            "authDomain": "batatubas.firebaseapp.com",
            "databaseURL": "https://batatubas.firebaseio.com/",
            "storageBucket": "gs://batatubas.appspot.com/"
        }
        cls.firebase = pyrebase.initialize_app(config)
        cls.db = cls.firebase.database()

    @classmethod
    def add_to_today(cls, sender : str, receiver : str, msg : str) -> None:
        cls.db.child("Today").child(sender).push({"sender": sender, "text": msg})

    @classmethod
    def start_new_day(cls) -> None:
        data = cls.db.child("Today").get()
        cls.db.child("All Time").set(data.val())
        cls.db.child("Today").remove()

    @classmethod
    def read_from_db(cls) -> dict:
        dict_result = {}
        all_senders = cls.db.child("All Time").get()
        for sender in all_senders.each():
            user_data = sender.val()
            curr_user_data = []
            for key, value in user_data.items():
                curr_user_data.append(value)
            dict_result[sender.key()] = curr_user_data
        return dict_result
