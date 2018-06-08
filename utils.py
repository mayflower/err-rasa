import logging
attlassian = __import__('./attlassian.py')
jira_oauth = __import__('./jira_oauth.py')
config = __import__('./../config.py')

from rasa_core.actions import Action

from jira_oauth import JiraOauth

from jira import JIRA, JIRAError

class JiraNeedsAuthorization(Exception):
    pass

class JiraAwareAction(Action):
    def _ transformToDateString(self, value):
        return value

    def _createReportIllnessMessage(self, user, first, last, duration = None):
        subject = "krankmeldung [%s]", user
        body = "\
        Wer ist krank: [%s] \
        \
        Erster Krankheitstag: %s \
        \
        Voraussichtlicher letzter Krankheitstag: %s \
        ", user, first, last
        project = config.JIRA_P

    def _handle_jira_auth(self, user):
        oauth = JiraOauth()
        link, state = oauth.request_token()
        self['oauth_request_{}'.format(user)] = state

        return link

    def _jira_req_auth(self, frm):
            link = self._handle_jira_auth(frm)
            text = 'To use the errbot JIRA integration please give permission at: {}'.format(link)
            self.sendd(self.build_identifier(frm), text)
            raise JiraNeedsAuthorization()

    def _jira_client(self, frm):
        request_key = 'oauth_request_{}'.format(frm)
        access_key = 'oauth_access_{}'.format(frm)
        self.log.warn("FROM: %s", frm)
        if self.get(request_key):
            oauth = JiraOauth()
            state = self[request_key]
            try:
                self[access_key] = oauth.accepted(state)
            except KeyError:
                self._jira_req_auth(frm)
            del self[request_key]
        if not self.get(access_key):
            self._jira_req_auth(frm)
        token, secret = self[access_key]
        oauth_config = {
          'access_token': token,
          'access_token_secret': secret,
          'consumer_key': config.JIRA_OAUTH_KEY,
          'key_cert': config.JIRA_OAUTH_PEM,
        }

        return JIRA(config.JIRA_BASE_URL, oauth=oauth_config)