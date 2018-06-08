import random
from errbot import BotPlugin
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent

from jira import JIRA, JIRAError

import config from '../config'
from jira_oauth import JiraOauth

class Rasa(BotPlugin):
    COULD_NOT_PARSE_MSGS = [
        "Sorry, I don't know it",
        "Next time I will know, but not now",
        "Sorry, can't get what do you mean",
        "Try something else"
    ]
    GREET_MSGS = ["Hola!", "Privet!", "Xin chao!"]
    INTENT_GREET = "greet"
    INTENT_ORDER_PIZZA = 'order_pizza'
    INTENT_PEDANT = 'pedant'
    ENTITY_SIZE = 'size'
    ENTITY_TOPPINGS = "toppings"
    ENTITY_CORRECTION = "correction"

    def activate(self):
        super().activate()
        model_dir = './models/nlu/default/chat'

        self.agent = Agent.load('./models/dialogue', interpreter=RasaNLUInterpreter('./models/nlu/default/chat'))
        #builder = ComponentBuilder(use_cache=True)
        #self.interpreter = Interpreter.load(model_dir, builder)
        # store unparsed messages, so later we can train bot
        self.unparsed_messages = []

    def callback_message(self, message):
        sendTo = getattr(message.frm, 'room', message.frm)
        # if self.interpreter is None:
        #     self.log.debug('No interpreter found')
        #     return
        text = message.body
        self.log.debug(text)
        # self.send(sendTo, 'Understand: '+text)
        #reply = self.find_reply(text)
        reply = self.agent.handle_message(message.body)
        for e in reply:
            if e['text'] is not None:
                self.send(sendTo, e['text'])
                return e['text']        
        return 'No answer'

    def find_reply(self, message):
        res = self.interpreter.parse(message)
        self.log.debug('rasa parse res: {}'.format(res))
        reply = ''
        if not 'intent' in res or res['intent'] is None:
            # later we can do something with unparsed messages, probably train bot
            self.unparsed_messages.append(message)
            return random.choice(self.COULD_NOT_PARSE_MSGS)
        intent = res['intent']
        if not 'name' in intent or intent['name'] is None:
            # later we can do something with unparsed messages, probably train bot
            self.unparsed_messages.append(message)
            return random.choice(self.COULD_NOT_PARSE_MSGS)
        name = intent['name']
    
        if name == self.INTENT_PEDANT:
            if len(res["entities"]) > 0:
                for e in res["entities"]:
                    entity = res["entities"][e]
                    if entity['text'] == self.ENTITY_CORRECTION:
                        return e["value"]
                    else:
                        self.unparsed_messages.append(message)
                        return "I will get you some day"

        if name == self.INTENT_GREET:
            return random.choice(self.GREET_MSGS)
        
        if name == self.INTENT_ORDER_PIZZA:
            if len(res["entities"]) > 0:
                for e in res["entities"]:
                    if e["entity"] == self.ENTITY_TOPPINGS:
                        return 'Toppings: '+self.get_short_answer(e["value"])
                    elif e["entity"] == self.ENTITY_SIZE:
                        return 'Size: '+self.get_short_answer(e["value"])
                    else:
                        return 'Unknown entity: '+e["entity"]
            else:
                self.unparsed_messages.append(message)      
                return 'No entities found'
    
        # later we can do something with unparsed messages, probably train bot
        self.unparsed_messages.append(message)
        return random.choice(self.COULD_NOT_PARSE_MSGS)

        def get_short_answer(query):
            return query

        # saves unparsed messages into a file
        def snapshot_unparsed_messages(self, filename):
            with open(filename, "a") as f:
                for msg in self.unparsed_messages:
                    f.write("{}\n".format(msg))