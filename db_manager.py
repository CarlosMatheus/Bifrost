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
        cls.db.remove()


    @classmethod
    def add_to_user_list(cls, name : str, sector: str) -> None:
        data = {"name" : name, "sector" : sector}
        cls.db.child("Users").push(data)

    @classmethod
    def add_to_today(cls, sender : str, receiver : str, msg : str) -> None:
        cls.db.child("Today").child(sender).push({"sender": sender, "receiver" : receiver, "text": msg})


    @classmethod
    def rm_from_today(cls, sender : str, receiver : str):
        all_senders = cls.db.child("Today").get()

        if all_senders.each() is not None:
            for curr_sender in all_senders.each():
                if curr_sender.key() == sender:
                    user_data = curr_sender.val()
                    for key, value in user_data.items():
                        if user_data[key]["receiver"] == receiver or user_data[key]["receiver"] == "-1":
                            data = cls.db.child("Today").child(curr_sender.key()).child(key).get()
                            cls.db.child("Today").child(curr_sender.key()).child(key).remove()
                            if user_data[key]["receiver"] != "-1":
                                cls.db.child("All Time").child(sender).push(data.val())


    @classmethod
    def start_new_day(cls) -> None:
        data = cls.db.child("Today").get()
        cls.db.child("All Time").set(data.val())
        cls.db.child("Today").remove()

    @classmethod
    def read_from_ul(cls) -> list:
        result = []

        all_senders = cls.db.child("Users").get()
        if all_senders.each() != None:
            for sender in all_senders.each():
                result.append(sender.val())

        return result

    @classmethod
    def read_from_db(cls) -> dict:
        dict_result = {}

        all_senders = cls.db.child("Today").get()
        if all_senders.each() != None:
            for sender in all_senders.each():
                user_data = sender.val()
                curr_user_data = []
                for key, value in user_data.items():
                    curr_user_data.append(value)
                dict_result[sender.key()] = curr_user_data

        return dict_result


    @classmethod
    def check_for_msg(cls, receiver : str) -> list:
        possible_senders = []

        all_senders = cls.db.child("Today").get()
        if all_senders.each() is not None:
            for sender in all_senders.each():
                user_data = sender.val()
                for key, value in user_data.items():
                    if user_data[key]["receiver"] == receiver or user_data[key]["receiver"] == "-1":
                        possible_senders.append(sender.key())

        return possible_senders


    @classmethod
    def send_msg(cls, receiver : str, sender=None) -> str:
        if sender == None:
            possible_senders = cls.check_for_msg(receiver)
            sender = possible_senders[0]

        text = -1
        all_senders = cls.db.child("Today").get()
        if all_senders.each() is not None:
            for curr_sender in all_senders.each():
                if curr_sender.key() == sender:
                    user_data = curr_sender.val()
                    for key, value in user_data.items():
                        if user_data[key]["receiver"] == receiver or user_data[key]["receiver"] == "-1":
                            text = user_data[key]["text"]
                            data = cls.db.child("Today").child(curr_sender.key()).child(key).get()
                            cls.db.child("Today").child(curr_sender.key()).child(key).remove()
                            if user_data[key]["receiver"] != "-1":
                                cls.db.child("All Time").child(sender).push(data.val())
                            break

        return text

