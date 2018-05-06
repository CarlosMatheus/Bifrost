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
    def start_new_day(cls):
        data = cls.db.child("Today").get()
        cls.db.child("All Time").set(data.val())
        cls.db.child("Today").remove()

    @classmethod
    def read_from_db(cls):
        result = None
        all_senders = cls.db.child("Today").get()
        for user in all_senders.each():

