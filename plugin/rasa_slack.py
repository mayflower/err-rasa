import logging
import json
from pylint.test.functional import no_self_use
from asn1crypto.core import InstanceOf
from errbot.backends.base import Card

class RasaSlack():
    """The rasa slack bot interface slightly differs from the errbot
    interface so this one will be an adapter"""
    def __init__ (self, bot):
        self.bot = bot
        self.log = logging
        self.person_by_id={}
        self.channels_by_id={}

    def set_person_by_id(self, user_id, person):
        self.person_by_id[user_id] = person

    def get_person_by_id(self, user_id):
        return self.person_by_id[user_id]

    def send_text_message(self, recipient_id, message):
        # type: (Text, Text) -> None
        """Send a message through this channel."""

        self.bot.send(identifier=self._evaluate_identifier_by_recipient_id(recipient_id),
                        text=message)

    def _evaluate_identifier_by_recipient_id(self, recipient_id, prefer_user = False):
        """To either send to user or to channel"""
        person = self.get_person_by_id(recipient_id)
        if type(person).__name__ == 'SlackRoomOccupant' and prefer_user is False:
            identifier_id = str(person.room)
        else:
            identifier_id = str(person)

        return self.bot.build_identifier(identifier_id)

    def _send_to_card_or_text (self, value, recipient_id):
        if hasattr(self.bot, 'send_card') and callable(getattr(self.bot, 'send_card')):
            method = getattr(self.bot, 'send_card')
            method(value)
        else:
            text = """
Title: {}
Summary: {}
Fields: {}
        """.format(value.title, value.saummary, json.dumps(value.fields))
            self.send_text_message(recipient_id, text)

    def send_image_url(self, recipient_id, image_url):
        # type: (Text, Text) -> None
        """Sends an image. Default will just post the url as a string."""
        self.bot._send_to_card_or_text({"image": image_url, "title": "Image"})
        return True

    def _convert_to_slack_buttons (self, buttons):
        return [{"text": b['title'],
                 "name": b['payload'],
                 "value": b['value'],
                 "style": b['style'],
                 "type": "button"} for b in buttons]

    def send_text_with_buttons(self, recipient_id, message, buttons):
        if len(buttons) > 5:
            logging.warn("Slack API currently allows only up to 5 buttons."
                        "If you add more, all will be ignored.")
            return self.send_text_message(recipient_id, message)
        card = Card(summary=message,
                    title="Nachricht vom {}".format(self.bot.bot_identifier),
                    to=self._evaluate_identifier_by_recipient_id(recipient_id),
                    fields=self._convert_to_slack_buttons(buttons)
                    )

        self._send_to_card_or_text(card, recipient_id)

    def send_custom_message(self, recipient_id, elements):
        # type: (Text, Iterable[Dict[Text, Any]]) -> None
        """Sends elements to the output.
        Default implementation will just post the elements as a string."""

        for element in elements:
            element_msg = "{title} : {subtitle}".format(
                    title=element['title'], subtitle=element['subtitle'])
            self.send_text_with_buttons(
                    recipient_id, element_msg, element['buttons'])

