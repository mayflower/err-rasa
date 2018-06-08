import logging
import "./../utils"

from rasa_core.actions import Action

class ActionOrderPizza(Action):
    def name(self):
        return 'action_order_pizza'
    def run(self, dispatcher, tracker, domain):
        size = tracker.get_slot('size') if tracker.get_slot('size') is None else 'No size set'
        toppings = tracker.get_slot('toppings') if tracker.get_slot('toppings') is None else 'No toppings set'
        dispatcher.utter_message('Lets order some pizza with size "'+size+'" and with toppings: "'+toppings)
        return []

class ActionPedant(Action):
    def name(self):
        return 'action_pedant'
    def run(self, dispatcher, tracker, domain):
        correction = tracker.get_slot('correction') if tracker.get_slot('correction') is not None else 'Got nothing'
        logging.info("Domain: {}".format(domain))
        dispatcher.utter_message('You are not concrete enough - '+correction)
        return []
class ActionIllnessFromTo(JiraAwareAction):
    @staticmethod
    def required_fields():
        return [
            EntityFormField("last"),
            EntityFormField("first", "today"),
            BooleanFormField("user")
        ]
    def name(self):
        return 'action_report_illness_from_to'
    def run(self, dispatcher, tracker, domain):
        first = tracker.get_slot('first')
        last = tracker.get_slot('last')
        user = tracker.get_slot('user')

        message = _createReportIllnessMessage(first, last)
        client = self._jira_client(self, user)

        dispatcher.utter_message('Get will soon. Will insert illness from "'+first+'" to "'+last+'"')
        return []

class ActionIllnessDuration(JiraAwareAction):
    @staticmethod
    def required_fields():
        return [
            EntityFormField("duration"),
            EntityFormField("first", "today"),
            BooleanFormField("user")
        ]
    def name(self):
        return 'action_report_illness_duration'
    def run(self, dispatcher, tracker, domain):
        duration = tracker.get_slot('duration')
        first = tracker.get_slot('first') if tracker.get_slot('first') is not None else 'today'
        
        dispatcher.utter_message('Get will soon. Will insert illness from "'+first+'" for "'+duration+'"')
        return []