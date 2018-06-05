import logging
import rasa_core

from errbot import BotPlugin
from rasa_core.agent import Agent
from rasa_core.domain import Domain
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)
class Rasa(BotPlugin):
    def callback_message(self, message):
        self.log.debug(message.body)

        domain = __file__+'/../config/chat_domain.yml'
        interpreterPath = __file__+'/../models/nlu/default/chat'
        agent = Agent(domain, interpreter=interpreterPath)
        self.log.debug('Agent created')
        result = agent.handle_message(message.body)
        self.log.debug('done')
        self.log.debug(result)
        self.send(getattr(message.frm, 'room', message.frm), result)
