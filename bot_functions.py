"""
Bot that helps a truck driver to sum the total revenues.
"""

# IMPORTS
import time
from datetime import datetime

import telepot
from telepot.loop import MessageLoop

from unicodes import Unicodes


class Bot():
    """
    Bot and chatbot functionalities.
    """
    def __init__(self):
        self.chatbot = telepot.Bot(
                '1448792413:AAEo0ajop3uyozGB42UGZBOoS42105GIUAU')
        self.ucd = Unicodes()

        self.administrator_chat_id = 764061009
        self.chat_id_list = [764061009, 1469694219]
        
        self.total = 0
        self.last_cache = None

    # FUNCTIONS
    def keep_chat_awake(self):
        """Send a message(.) every 10 minutes to keep the chatbot awake."""
        att_time = datetime.strftime(datetime.now(), '%H:%M')
        msg = self.chatbot.sendMessage(self.administrator_chat_id,
                                       f'{self.ucd.unicode_engrenagem}' +
                                       f' Conectado {att_time}.')
        time.sleep(600)
        self.chatbot.deleteMessage(telepot.message_identifier(msg))

    def send_message_all(self, msg):
        """Send a message to every user in the self.chat_id_list."""
        for chat_id in self.chat_id_list:
            self.chatbot.sendMessage(chat_id, msg)

    def active_reading(self):
        """Stay checking for new messages."""
        MessageLoop(self.chatbot, self.message_handle).run_as_thread()

    def message_handle(self, msg):
        """Receive the new messages from the active_reading function
        and execute some action."""
        #  banco = self.ucd.unicode_banco
        nota = self.ucd.unicode_nota_de_dineiro
        #  trofeu = self.ucd.unicode_trofeu
        #  raio = self.ucd.unicode_raio
        #  update = self.ucd.unicode_engrenagem
        certo = self.ucd.unicode_certo_verde
        caminhao = self.ucd.unicode_caminhao
        chat_id = msg['chat']['id']
        if chat_id in self.chat_id_list:
            command = msg['text']
            if '/total' in command:
                self.chatbot.sendMessage(chat_id, f'{nota} R${self.total}')
            elif '/nova' in command:
                try:
                    new_value = command.split(' ')[1]
                    new_value = float(str(new_value).replace(',', '.'))
                    self.new_entry(new_value)
                    self.chatbot.sendMessage(chat_id, f'{caminhao} Novo valor ' +
                                                      f'R${new_value} cadastrado!\n' +
                                                      f'\nTotal:\n{nota} {self.total}')
                except IndexError or ValueError:
                    self.chatbot.sendMessage(chat_id, 'Comando invalido! A forma correta é: \n"/nova 1234,56".')
            elif '/limpar' in command:
                self.last_cache = self.total
                self.clear()
                self.chatbot.sendMessage(chat_id, f'{certo} Historico apagado!')
            else:
                self.chatbot.sendMessage(chat_id, 'Comando invalido! (/comandos).')
        else:
            self.chatbot.sendMessage(chat_id, '!!! ACESSO NEGADO !!!')

    def new_entry(self, value):
        """ sum a new entry."""
        self.total += value
    
    def clear(self):
        """clear sum cache."""
        self.total = 0

bot = Bot()

bot.active_reading()
while True:
    bot.keep_chat_awake()
