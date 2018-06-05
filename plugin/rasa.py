from errbot import BotPlugin

class Rasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)
        self.send(getattr(message.frm, 'room', message.frm), message.body)
