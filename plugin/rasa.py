import config

from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.agent import Agent
from rasa_core.events import SlotSet
from rasa_core.trackers import DialogueStateTracker
from errbot import BotPlugin
from rasa_core.slots import TextSlot
from rasa_core.domain import TemplateDomain
class Rasa(BotPlugin):
    def activate(self):
        """To enable our classes we need like the agent and its tracker"""
        super(Rasa, self).activate()
        self.agent = Agent.load('./models/dialogue',
                            interpreter=RasaNLUInterpreter('./models/nlu/default/chat'))

    def callback_message(self, message):
        """Override to hook into the messaging and calling rase """
        super(Rasa, self).callback_message(message)
        sendTo = getattr(message.frm, 'room', message.frm)
        text = message.body
        self.log.debug(text)
        frm = getattr(message.frm, 'real_jid', message.frm.person)
        reply = self.agent.handle_message(message.body, sender_id=config.BOT_RASA_SENDER_ID)
        self.log.debug("Reply: {}".format(reply))
        self.agent.tracker_store.create_tracker(sender_id=config.BOT_RASA_SENDER_ID).update(SlotSet('user', frm))
        responseText = ''
        for e in reply:
            if e['text'] is not None:
                responseText += e['text']+"\n"
        self.send_card(body=responseText,
                        title="Message From: {}".format(config.BOT_RASA_SENDER_ID),
                        in_reply_to=message)
