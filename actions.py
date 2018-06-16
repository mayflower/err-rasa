
from rasa_core.actions import Action
from rasa_core.events import AllSlotsReset, SlotSet
from jira import JIRA

import logging
import arrow
import json

from lib.jira_oauth import JiraOauth

import config
from multiprocessing.managers import dispatch
from rasa_core import tracker_store

class JiraNeedsAuthorization(Exception):
    pass

class JiraAwareAction(Action):
    def __init__(self):
        self.metadata = {}
    def evaluate_from_to_by_tracker(self, tracker):
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

    def _evaluate_user_id(self, dispatcher, tracker):
        """ we use the userr given thorugth slot with a higher
            priority. If thr is no one we ask the dispatcher to hand out a
        """
        person = dispatcher.output_channel.get_person_by_id(dispatcher.sender_id)
        user = tracker.get_slot('user')
        if user is None:
            # Todo Replace self assignment
            user = person.aclattr

        return user

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

class ActionWhoKnowsTopic(Action):
    def name(self):
        return 'action_who_knows_topic'
    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic') if tracker.get_slot('topic') else None
        if topic is None:
            dispatcher.utter_message('Ich habe kein Topic bekommen')
            return []

        topic = str(topic)
        bests = []
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'skills' not in skillData:
            return []

        for persistedTopic in skillData['skills']:
            if topic.lower() != persistedTopic.lower() or len(skillData['skills'][persistedTopic]) == 0: continue
            for user in skillData['skills'][persistedTopic]: bests.append(user)
        if len(bests) == 0:
            dispatcher.utter_message('Kein Kollege weiß etwas zun Thema {}'.format(topic))
        else:
            bestsString = ''
            for user in bests:
                bestsString += user['name']+' (Score: '+str(user['score'])+'), '
            if bestsString.endswith(", "): bestsString = bestsString[:-2]
            dispatcher.utter_message('Die folgenden Kollegen meinen Ahnung zu haben: '+bestsString)
        return [AllSlotsReset()]

class ActionIForgot(Action):
    def name(self):
        return 'action_forgotten'
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Action forgotten')
        return []

class ActionConfirmation(Action):
    def name(self):
        return 'action_confirmation'
    def run(self, dispatcher, tracker, domain):
        confirmed = tracker.get_slot('confirmation')
        if confirmed is True:
            dispatcher.utter_message('Cool, dann gehts weiter')
            return []
        else:
            dispatcher.utter_message('Schisser')
            return []
        return []

class ActionClaimToKnowTopic(JiraAwareAction):
    def name(self):
        return 'action_claim_to_know_topic'
    def run(self, dispatcher, tracker, domain):
        topic = tracker.get_slot('topic')
        user = self._evaluate_user_id(dispatcher, tracker)
        if topic is None:
            dispatcher.utter_message('No topic given')
            return []
        if user is None:
            dispatcher.utter_message('No user given')
            return []
        topic = str(topic)
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'skills' not in skillData:
            dispatcher.utter_message('Keine Skills sinds vorhanden')
            return []
        if topic not in skillData['skills']:
            skillData['skills'][topic] = []
            dispatcher.utter_message('Das Topic '+topic+' ist noch nicht bekannt, wird angelegt')
        persistedTopic = skillData['skills'][topic]

        foundUser = False
        for key in persistedTopic:
            if persistedTopic[key].name == user:
                persistedTopic[key].score = persistedTopic[key].score + 1
                dispatcher.utter_message('User '+user+'` Score um eins erhöht für Topic: '+topic)
                foundUser = True
                break
        if foundUser is True:
            skillData[topic].append({"name": user, "score": 1})
            dispatcher.utter_message('User '+user+'` wurde für das Topic vermerkt: '+topic)

        return [AllSlotsReset()]

    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))

class ActionTopicsInCategory(Action):
    def name(self):
        return 'action_topics_in_category'
    def run(self, dispatcher, tracker, domain):
        category = tracker.get_slot('category') if tracker.get_slot('category') else 'None'
        category = str(category)
        with open('./data/skills.json') as f:
            skillData = json.load(f)
        if 'categories' not in skillData:
            dispatcher.utter_message('Keine Skills sinds vorhanden')
            return []
        for persistedCategory in skillData['categories']:
            if persistedCategory.lower() != category.lower():
                continue
            topics = skillData['categories'][persistedCategory]
            if len(topics) == 0:
                dispatcher.utter_message('Kein Topic gefunden in Kategroie: '+category)
                return []
            topicsString = ''
            for topic in topics:
                topicsString += ', '+topic
            dispatcher.utter_message('Folgen Topics habe ich in Kategoie '+category+' gefunden: '+topicsString)
            return [AllSlotsReset()]

        categories = ''
        for category in skillData['categories']:
            categories += ', '+category
        dispatcher.utter_message('Keine Kategorie mit dem name '+category+' gefunden, wähle doch eine von '+categories)

class ActionPreReportIllness(JiraAwareAction):
    def name(self):
        return 'action_pre_report_illness'
    def run(self, dispatcher, tracker, domain):
        """
            Called in dialog, when from and to are select
            and we can create and send a jira ticket
        """

        first, last = self.evaluate_from_to_by_tracker(tracker)
        user = tracker.get_slot('user')


        if user is None:
            # Todo Replace self assignment
            user = dispatcher.sender_id
        person = dispatcher.output_channel.get_person_by_id(user)
        subject = "Krankmeldung [{}]".format(person.fullname)
        body = """
Wer ist krank: [{}]

Erster Krankheitstag: {}

Voraussichtlicher letzter Krankheitstag: {}
        """.format(person.fullname, first, last)
        response_message = """
Ich würde dir dieses Ticket anlegen:
Subject: {}
{}
        """.format(subject,body)
        dispatcher.utter_message(response_message)
        try:
            self._handle_jira_auth(user)
        except JiraNeedsAuthorization as e:
            dispatcher.utter_message("Authorisation Needed {}".format(e))
            return [SlotSet('auth_confirmation_required', True)]
        return [
            SlotSet('subject', subject),
            SlotSet('body', body),
            SlotSet('user', user),
            SlotSet('confirmation_required', True)
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

        user = self._evauate_user(tracker, dispatcher)
        try:
            jira = self._jira_client(user)
            issue = jira.create_issue(project=config.JIRA_PROJECT_HR,
                                summary=tracker.get_slot('subject'),
                                description=tracker.get_slot('body'),
                                issuetype={'name': 'Story'})
        except JiraNeedsAuthorization as e:
            dispatcher.utter_message(str(e))

            return [SlotSet('auth_confirmation_required', True)]
        dispatcher.utter_message('Ich habe dir Ticket {} angelegt. Gute Besserung'.format(issue))

        return [SlotSet('confirmation_required', False)]
