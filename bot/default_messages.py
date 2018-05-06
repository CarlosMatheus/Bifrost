class DefaultMessages:
    @classmethod
    def contact_on_direct(cls):
        return 'Ola! Se quiser mandar uma mensagem motivadora para alguém é só me mandar um direct'

    @classmethod
    def send_daily(cls):
        return 'Olá! É uma ótima hora de enviar sua mensagem diária'

    @classmethod
    def default_thanks(cls):
        return 'Obrigado!  Você fará o dia de alguém melhor =)'

    @classmethod
    def custom_thanks(cls, nome):
        return 'Obrigado! Sua mensagem será enviada para ' + nome
