from errbot import BotPlugin

class ErrRasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)
        self.send(getattr(message.frm, 'room', message.frm))

