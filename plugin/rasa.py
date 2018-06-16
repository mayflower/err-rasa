from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

import json
import config



from errbot import BotPlugin, botcmd
from plugin.rasa_slack import RasaSlack

class Rasa(BotPlugin):
    """Plugin to enable rasa converstions in an errbot"""
    OWN_COMMANDS = ['!learnonline']
    dialog_model_dir = './models/dialogue'
    chat_model_dir = './models/nlu/default/chat'
    domain_file = './config/chat_domain.yml'
    training_data_file= 'config/stories.md'
    agent = None
    backend_adapter = None
    def activate(self):
        """To enable our classes we need like the agent and its tracker"""
        super(Rasa, self).activate()
        self.dialog_model_dir = './models/dialogue'
        self.chat_model_dir = './models/nlu/default/chat'
        self.domain_file = './config/chat_domain.yml'
        self.training_data_file= 'config/stories.md'
        self.agent = Agent.load(self.dialog_model_dir,
                            interpreter=RasaNLUInterpreter(self.chat_model_dir))
        self.backend_adapter = RasaSlack(self._bot)

    def callback_message(self, message):
        """Override to hook into the messaging and calling rase """
        super(Rasa, self).callback_message(message)
        text = message.body
        if text == '!learnonline':
            self.log.debug("Do not send something as it is an own commmand: "+text)
            return
        
        token = config.BOT_IDENTITY['token']
        if token is None:
          raise Exception('No slack token')
        frm = getattr(message.frm, 'aclattr', message.frm.person)
        userid = getattr(message.frm, 'userid', frm)
        self.backend_adapter.set_person_by_id(userid, message.frm)
        self.log.debug("From: {}".format(frm))
        self.agent.handle_message(message.body,
                                    sender_id=userid,
                                    output_channel=self.backend_adapter)

    @botcmd()
    def learnonline(self, msg, args):
        """Command to trigger learn_online on rasa agent"""
        token = config.BOT_IDENTITY['token']
        if token is None:
            raise Exception('No slack token')
        train_agent= Agent(self.domain_file,
                  policies=[MemoizationPolicy(max_history=2), KerasPolicy()],
                  interpreter=RegexInterpreter())
        training_data = train_agent.load_data(self.training_data_file)
        train_agent.train_online(training_data,
                                 input_channel=self.backend_adapter,
                                 batch_size=50,
                                 epochs=200,
                                 max_training_samples=300)
