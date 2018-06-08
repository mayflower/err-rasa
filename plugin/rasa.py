import random
from errbot import BotPlugin
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent

import attlassian

class Rasa(BotPlugin):
    def activate(self):
        super().activate()
        self.agent = Agent.load('./models/dialogue', interpreter=RasaNLUInterpreter('./models/nlu/default/chat'))

    def callback_message(self, message):
        sendTo = getattr(message.frm, 'room', message.frm)
        text = message.body
        self.log.debug(text)
        reply = self.agent.handle_message(message.body)
        for e in reply:
            if e['text'] is not None:
                self.send(sendTo, e['text'])
