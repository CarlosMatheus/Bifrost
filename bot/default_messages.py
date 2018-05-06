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

    @classmethod
    def mensagem_ajuda(cls):
        return 'Esse bot ajuda a espalhar mensagens no ambiente de trabalho, ' \
               'por meio dele são enviadas mensagens para seus colegas de trabalho.' \
               'Basta enviar uma mensagem para o bot. Se você quiser mandar para alguém específico,' \
               'basta incluir o prefixo @\n' \
               'Exemplo:\n' \
               '@Bot tudo bom?' \
               'Para ver os comando digite \comandos'

    @classmethod
    def mensagem_comandos(cls):
        return 'Comandos:\n' \
               '\\ajuda\n' \
               '\\comandos'

