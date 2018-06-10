
from rasa_core.actions import Action
from rasa_core.events import SlotSet
from jira import JIRA

import logging
import arrow

from lib.date_converter import DateConverter
from lib.jira_oauth import JiraOauth

import config
from rasa_core import domain

class JiraNeedsAuthorization(Exception):
    pass

class JiraAwareAction(Action):
    def __init__(self):
        self.metadata = {}
        self.date_converter = DateConverter()

    def _evaluateUserBy(self, tracker):
        """Having the slack handle only can never be enoght. Swe we try to evaluate the real name"""
        user = tracker.get_slot('user')
        if user is None:
            # todo a way to get it from tracker after setting it in bot plugin
            user = '@elctricmaxxx'
        # Todo: find a way to get the clear names of the user from slack
        return user

    def _createReportIllnessMessage(self, user, first, last):
        subject = "krankmeldung [{}]".format(user)
        body = """
            Wer ist krank: [{}]
            
            Erster Krankheitstag: {}
            
            Voraussichtlicher letzter Krankheitstag: {}
            """.format(user, first, last)
        return subject, body

    def _handle_jira_auth(self, user):
        """Handles jira auth"""
        oauth = JiraOauth()
        link, state = oauth.get_request_token()
        self.metadata['oauth_request_{}'.format(user)] = state

        return link

    def _jira_req_auth(self, frm):
        link = self._handle_jira_auth(frm)
        text = 'To use the errbot JIRA integration please give permission at: {}'.format(link)
        raise JiraNeedsAuthorization(text)

    def _jira_client(self, frm):
        """  Creates the jira client or forces the user to authenticate"""
        request_key = 'oauth_request_{}'.format(frm)
        access_key = 'oauth_access_{}'.format(frm)
        logging.warn("FROM: %s", frm)
        logging.debug("Config %s", config.JIRA_OAUTH_URL)
        if self.metadata.get(request_key):
            oauth = JiraOauth()
            state = self.metadata[request_key]
            try:
                self.metadata[access_key] = oauth.accepted(state)
            except KeyError:
                self._jira_req_auth(frm)
            del self.metadata[request_key]
        if not self.metadata.get(access_key):
            self._jira_req_auth(frm)
        token, secret = self.metadata[access_key]
        oauth_config = {
            'access_token': token,
            'access_token_secret': secret,
            'consumer_key': config.JIRA_OAUTH_KEY,
            'key_cert': config.JIRA_OAUTH_PEM,
        }

        return JIRA(config.JIRA_BASE_URL, oauth=oauth_config)

class ActionOrderPizza(Action):
    def name(self):
        return 'action_order_pizza'
    def run(self, dispatcher, tracker, domain):
        size = tracker.get_slot('size')
        size = size if size is not None else 'No size set'
        toppings = tracker.get_slot('toppings')
        toppings = toppings if toppings is not None else 'No toppings set'
        dispatcher.utter_message("Lets order some pizza with size '%s' and with toppings: '%s'", size, toppings)
        return []
class ActionPedant(Action):
    def name(self):
        return 'action_pedant'
    def run(self, dispatcher, tracker, domain):
        correction = tracker.get_slot('correction')
        dispatcher.utter_message('Das reicht so nith - {}'.format(correction))
        return []

class ActionPreReportIllnessFromTo(JiraAwareAction):
    def name(self):
        return 'action_pre_report_illness_from_to'
    def run(self, dispatcher, tracker, domain):
        """
            Called in dialog, when from and to are select and we can create and send a jira ticket
        """
        first, last = self.date_converter.fromFirstAndDuration(
            tracker.get_slot('first'),
            tracker.get_slot('last'),
            tracker.get_slot('duration')
        )
        user = tracker.get_slot('user')

        if user is None:
            # Todo Replace self assignment
            user = '@electricmaxxx'
        handle_authorization = ''
        try:
            self._handle_jira_auth(user)
        except JiraNeedsAuthorization as e:
            handle_authorization = str(e)
        subject, body = self._createReportIllnessMessage(user, first, last)
        message  = """
                Ich würde dir dieses Ticket anlegen:
                Subject: {}
                {}

                {}
            """.format(subject, body, "Und: \n"+ handle_authorization if handle_authorization is not None else "")
        dispatcher.utter_message(message)
        return [
            SlotSet('to_confirm', True),
            SlotSet('confirmed', None),
            SlotSet('subject', subject),
            SlotSet('body', body),
            SlotSet('user', user)
            ]

class ActionIllnessFromTo(JiraAwareAction):
    def name(self):
        return 'action_report_illness_from_to'
    def run(self, dispatcher, tracker, domain):
        """
            Called in dialog, when from and to are select and we can create and send a jira ticket
        """

        if tracker.get_slot('confirmed') is not True:
            dispatcher.utter_message('Eigentlich hätt ich alles inkl. der Bestätigung')
            return [SlotSet('to_confirm', True), SlotSet('confirmed', None)]
        try:
            jira = self._jira_client(tracker.get_slot('user'))
            jira.create_issue(project=config.JIRA_PROJECT_HR,
                                summary=tracker.get_slot('subject'),
                                description=tracker.get_slot('body'),
                                issuetype={'name': 'Story'})
        except JiraNeedsAuthorization as e:
            dispatcher.utter_message(str(e))

        return [SlotSet('to_confirm', None), SlotSet('confirmed', None)]
            

class ActionIllnessDuration(JiraAwareAction):
    def name(self):
        return 'action_report_illness_duration'
    def run(self, dispatcher, tracker, domain):
        duration = tracker.get_slot('duration')
        first = tracker.get_slot('first') if tracker.get_slot('first') is not None else 'today'
        
        dispatcher.utter_message('Get will soon. Will insert illness from "'+first+'" for "'+duration+'"')
        return []
