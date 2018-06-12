import config

from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.events import SlotSet
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.channels.slack import SlackInput, SlackBot

from errbot import BotPlugin, botcmd
from asn1crypto.core import Null
class Rasa(BotPlugin):
    OWN_COMMANDS = ['!learnonline']
    def activate(self):
        """To enable our classes we need like the agent and its tracker"""
        super(Rasa, self).activate()
        self.dialog_model_dir = './models/dialogue'
        self.chat_model_dir = './models/nlu/default/chat'
        self.domain_file = './config/chat_domain.yml'
        self.training_data_file= 'config/stories.md'
        self.agent = Agent.load(self.dialog_model_dir,
                            interpreter=RasaNLUInterpreter(self.chat_model_dir))

    def callback_message(self, message):
        """Override to hook into the messaging and calling rase """
        super(Rasa, self).callback_message(message)
        text = message.body
        if text in self.OWN_COMMANDS:
            self.log.debug("Do not send something as it is an own commmand: "+text)
            return ''
        self.log.debug(text)
        
        #frm = getattr(message.frm, 'real_jid', message.frm.person)
        room = getattr(message.frm, 'room', message.frm)
        self.log.debug("User: {}".format(message.frm))
        token = config.BOT_IDENTITY['token']
        if token is Null:
            raise Exception('No slack token')
        self.agent.handle_message(message.body,
                                    sender_id=config.BOT_RASA_SENDER_ID,
                                    output_channel=SlackBot(token, slack_channel=room))


        
    @botcmd()
    def learnonline(self, msg, args):
        token = config.BOT_IDENTITY['token']
        if token is Null:
            raise Exception('No slack token')
        interpreter = RegexInterpreter()
        room = getattr(msg.frm, 'room', msg.frm)
        train_agent= Agent(self.domain_file,
                  policies=[MemoizationPolicy(max_history=2), KerasPolicy()],
                  interpreter=interpreter)
        training_data = train_agent.load_data(self.training_data_file)
        train_agent.train_online(training_data,
                        input_channel=SlackInput(token, slack_channel=room),
                        batch_size=50,
                        epochs=200,
                        max_training_samples=300)
