
from rasa_core.actions import Action
from rasa_core.events import SlotSet
from jira import JIRA

import logging
import arrow

from lib.jira_oauth import JiraOauth

import config
from rasa_core import domain
from numpy.ma.core import empty

class JiraNeedsAuthorization(Exception):
    pass

class JiraAwareAction(Action):
    def __init__(self):
        self.metadata = {}
    def _evaluateFromToByTracker(self, tracker):
        """By the help of ducking we got a a good answer of duratio, or from - to information"""
        time = tracker.get_slot('time')
        number = tracker.get_slot('number')
        first = None
        last = None
        if number is not None and isinstance(time, str):
            first = arrow.get(time).format(config.DATE_FORMAT)
            last = arrow.get(time).shift(days=+number).format(config.DATE_FORMAT)
        elif isinstance(time,dict):
            if time['to'] is not None:
                last = arrow.get(time['to']).format(config.DATE_FORMAT)
            if time['from'] is not None:
                first = arrow.get(time['from']).format(config.DATE_FORMAT)
        
        if first is None:
            first = arrow.utcnow().format(config.DATE_FORMAT)
        if last is None:
            logging.debug('Ducking does not work.')
            first = tracker.get_slot('last')
        return first, last

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
        try:
            link, state = oauth.get_request_token()
            self.metadata['oauth_request_{}'.format(user)] = state
            return link
        except Exception as e:
            logging.warn("Problem to connect to jira: {}".format(e))

    def _jira_req_auth(self, frm):
        link = self._handle_jira_auth(frm)
        if link is not None:
            text = 'To use the errbot JIRA integration please give permission at: {}'.format(link)
        else:
            text = 'To use the errbot JIRA integration please give permission, but we are not able to connect to jira at the moment'
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

class ActionPreReportIllness(JiraAwareAction):
    def name(self):
        return 'action_pre_report_illness'
    def run(self, dispatcher, tracker, domain):
        """

            Called in dialog, when from and to are select and we can create and send a jira ticket
        """

        first, last = self._evaluateFromToByTracker(tracker)
        user = tracker.get_slot('user')
        
        if user is None:
            # Todo Replace self assignment
            user = '@electricmaxxx'
        subject, body = self._createReportIllnessMessage(user, first, last)
        responseMessage = """
Ich würde dir dieses Ticket anlegen:
Subject: {}
{}
            """.format(subject, body)
        dispatcher.utter_message(responseMessage)
        try:
            self._handle_jira_auth(user)
        except JiraNeedsAuthorization as e:
            dispatcher.utter_message("Authorisation Needed {}".format(e))
        return [
            SlotSet('confirmation', False),
            SlotSet('subject', subject),
            SlotSet('body', body),
            SlotSet('user', user)
        ]

class ActionReportIllness(JiraAwareAction):
    def name(self):
        return 'action_report_illness'
    def run(self, dispatcher, tracker, domain):
        """
            Called in dialog, when from and to are select and we can create and send a jira ticket
        """
        confirmation = tracker.get_slot('confirmation')
        if confirmation == 'confirmation_declined':
            dispatcher.utter_message('Ich hoffe ich konnte trotzdem helfen.')
            return []
        elif confirmation != 'confirmation_accept':
            dispatcher.utter_message('Hier ist uns ein falscher Wert gekommen: '+confirmation)
            return []
        
        try:
            jira = self._jira_client(tracker.get_slot('user'))
            issue = jira.create_issue(project=config.JIRA_PROJECT_HR,
                                summary=tracker.get_slot('subject'),
                                description=tracker.get_slot('body'),
                                issuetype={'name': 'Story'})
        except JiraNeedsAuthorization as e:
            dispatcher.utter_message(str(e))
            return [SlotSet('auth_required', True)]
        dispatcher.utter_message('Ich habe dir Ticket {} angelegt. Gute Besserung'.format(issue))

        return []
