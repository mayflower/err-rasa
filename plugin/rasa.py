import logging
import rasa_core

from errbot import BotPlugin
from rasa_nlu.model import Metadata, Interpreter
from rasa_core.agent import Agent
from rasa_nlu.components import ComponentBuilder
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)
class Rasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)
        self.send(getattr(message.frm, 'room', message.frm), message.body)
        from rasa_nlu.model import Metadata, Interpreter
        
        builder = ComponentBuilder(use_cache=True)
        model_directory = './models/nlu/default/chat';
        interpreter = Interpreter.load(model_directory, builder)
        result = interpreter.parse(message.body)

        self.log.debug(result)
        