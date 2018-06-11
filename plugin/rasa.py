import config

from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.events import SlotSet
from rasa_core.interpreter import RegexInterpreter
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.channels.slack import SlackInput

from errbot import BotPlugin, botcmd
class Rasa(BotPlugin):
    OWN_COMMANDS = ['learnonline']
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
        frm = getattr(message.frm, 'real_jid', message.frm.person)
        self.agent.tracker_store.create_tracker(sender_id=config.BOT_RASA_SENDER_ID).update(SlotSet('user', frm))
        reply = self.agent.handle_message(message.body, sender_id=config.BOT_RASA_SENDER_ID)
        self.log.debug("Reply: {}".format(reply))
        responseText = ''
        for e in reply:
            if e['text'] is not None:
                responseText += e['text']+"\n"
        self.send_card(body=responseText,
                        title="Message From: {}".format(config.BOT_RASA_SENDER_ID),
                        in_reply_to=message)

        
    @botcmd()
    def learnonline(self, msg, args):
        token = None
        for key in config.BOT_IDENTITY:
            if key == 'token':
                token = key
        interpreter = RegexInterpreter()
        self.input_channel= SlackInput(slack_token=token)
        self.train_agent= Agent(self.domain_file,
                  policies=[MemoizationPolicy(max_history=2), KerasPolicy()],
                  interpreter=interpreter)
        training_data = self.train_agent.load_data(self.training_data_file)
        self.train_agent.train_online(training_data,
                        input_channel=self.input_channel,
                        batch_size=50,
                        epochs=200,
                        max_training_samples=300)
        return "Ich übergebe an Rasa Agent"