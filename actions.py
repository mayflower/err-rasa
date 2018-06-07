import logging
from rasa_core.actions import Action

class ActionOrderPizza(Action):
    def name(self):
        return 'action_order_pizza'
    def run(self, dispatcher, tracker, domain):
        logging.debug("Domain: {}".format(domain));
        dispatcher.utter_message('Lets order some pizza')
        return []

class ActionPedant(Action):
    def name(self):
        return 'action_pedant'
    def run(self, dispatcher, tracker, domain):
        logging.info("Domain: {}".format(domain));
        dispatcher.utter_message('You are not concrete enough')
        return []
class ActionIllness(Action):
    def name(self):
        return 'action_report_illness'
    def run(self, dispatcher, tracker, domain):
        logging.info("Domain: {}".format(domain));
        dispatcher.utter_message('Get will soon')
        return []