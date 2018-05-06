class DefaultMessages:
    @classmethod
    def contact_on_direct(cls):
        return 'Hey there! If you want to talk please send a direct message'

    @classmethod
    def send_daily(cls):
        return 'Hey there! It\'s a great time now to send your daily message'

    @classmethod
    def default_thanks(cls):
        return 'Obrigado!  Você fará o dia de alguém melhor =)'

    @classmethod
    def custom_thanks(cls, nome):
        return 'Obrigado! Sua mensagem será enviada para ' + nome
