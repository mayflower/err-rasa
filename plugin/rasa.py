import random
import logging

from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder
from errbot import BotPlugin

class Rasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)        
        builder = ComponentBuilder(use_cache=True)
        model_directory = './models/nlu/default/chat'
        interpreter = Interpreter.load(model_directory, builder)
        res = interpreter.parse(message.body)
        self.log.info('rasa parse res: {}'.format(res))
        if res['intent']:
            if res['intent']['name']:
                name = res['intent']['name']
                self.log.debug('Name: '+name)    
                self.send(getattr(message.frm, 'room', message.frm), 'Name: '+name)
            else:
                self.log.debug('No name set')    
                self.send(getattr(message.frm, 'room', message.frm), 'No name set')    
            
            if res['intent']['confidence']:
                confidence = str(res['intent']['confidence'])
                self.log.debug('Name: '+confidence)    
                self.send(getattr(message.frm, 'room', message.frm), 'Confidence: '+confidence)
            else:
                self.log.debug('No name set')    
                self.send(getattr(message.frm, 'room', message.frm), 'No confidence set')  

        else:
            self.log.debug('No intent set')    
            self.send(getattr(message.frm, 'room', message.frm), 'No intent set')
