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
    def activate(self):
        logging.basicConfig(level='INFO')
        dialog_training_data_file = '/home/maximilian/Barcamp/2018/errbot/slack-plugin/config/stories.md'
        path_to_model = '/home/maximilian/Barcamp/2018/errbot/slack-plugin//models/dialogue'
        # domain = Domain()
        featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=5)
        self.agent = Agent('/home/maximilian/Barcamp/2018/errbot/slack-plugin//config/chat_domain.yml',
                    policies=[MemoizationPolicy(max_history=5),
                                KerasPolicy(featurizer)])

    def callback_message(self, message):
        self.log.debug(message.body)
        result = self.agent.handle_message(message.body)
        self.log(result)

        self.send(getattr(message.frm, 'room', message.frm), result)
        self.send(getattr(message.frm, 'room', message.frm), message.body)
