import logging
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
class ActionIllnessFromTo(Action):
    def name(self):
        return 'action_report_illness_from_to'
    def run(self, dispatcher, tracker, domain):
        first = tracker.get_slot('first') if tracker.get_slot('first') is not None else 'today'
        last = tracker.get_slot('last') if tracker.get_slot('last') is not None else 'Not set'

        dispatcher.utter_message('Get will soon. Will insert illness from "'+first+'" to "'+last+'"')
        return []

class ActionIllnessDuration(Action):
    def name(self):
        return 'action_report_illness_duration'
    def run(self, dispatcher, tracker, domain):
        duration = tracker.get_slot('duration')
        first = tracker.get_slot('first') if tracker.get_slot('first') is not None else 'today'
        dispatcher.utter_message('Get will soon. Will insert illness from "'+first+'" for "'+duration+'"')
        return []