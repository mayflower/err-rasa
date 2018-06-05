from errbot import BotPlugin
import rasa_core
from rasa_core.agent import Agent
agent = Agent.load('./models/dialogue')

class Rasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)
        response = agent.handle_message(message.body)
        self.log.debug(response)
        self.send(getattr(message.frm, 'room', message.frm), response[0]["text"])
