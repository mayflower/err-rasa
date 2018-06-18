import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Slack'  # Errbot will start in slack mode (connected to slack backend) and will answer commands from your slack client.

BOT_DATA_DIR = './data'
BOT_EXTRA_PLUGIN_DIR = './plugin'

BOT_LOG_LEVEL = logging.DEBUG
BOT_LOG_FILE = False

BOT_ADMINS = ('@globin', )  # !! Don't leave that to 'CHANGE ME' if you connect your errbot to a chat system !!

BOT_IDENTITY = {
    'token': 'REDACTED'
}

BOT_PREFIX_OPTIONAL_ON_CHAT = True
