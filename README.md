# errbot plugin to rasa nlu

# Requirements

- errbot or [install it](http://errbot.io/en/latest/user_guide/setup.html#installation)
- python > 3
- [virtualenv](https://virtualenv.pypa.io)


## Usage for contribution

You will have to install [virtualenv](https://virtualenv.pypa.io) on to have a nice python environment to work in. Having that you can clone the repository where ever you whant to:

```bash
git clone git@github.com:mayflower/err-rasa.git plugins/rase-plugin
cd plugins/rasa-plugin
```

I would create a python environment there:

```bash
virtualenv --python `which python3` .errbot-ve
.errbot-ve/bin/pip install errbot
# install required python packages
.errbot-ve/bin/pip install -r requirements.txt
```
The folder lives inside the .gitignore and doing so we have a nice errbot installed inside our environment.

Now you have to prepare your working folder:

```bash
# create an empty folder for later data
mkdir data/
# create a demo config files with most needed parameters
cp config_slack.py config.py
# set `BOT_EXTRA_PLUGIN_DIR` value to `./plugin` - inside your working errbot instance you have to adopt this one
```

To have the german language available through `spacy` we have to download it:

```bash
# install and link german language pack for spacy (the analyzer)
python -m spacy download de
```

### Training data

We prepared a tool with name `chatitot` to create training data from a markdown file. So to use those data you have to run
a `npm install` and then run

```bash
# creates config/training_data.json from config/chatito
npm run chatito

# builds nlu model from config/training_data.json
npm run build:nlu-model

# builds dialoque model form config/stories.md and config/training_data.json
npm run build:dialog-model

# run trainer to get a better conversation
npm run train:dialog
```

Now grab your Slack-API-Key from [Slack apps overview](https://api.slack.com/apps) (There you have to create an app for you for Errbot if not done yet). If you click then into one app, the api token key is listed between the app properties.  
Then pass the key to the configuration as the last task and you can start your bot (``BOT_IDENTITY`` in ``config.py``).


```bash
# run errbot
.errbot-ve/bin/errbot
```

Using the `-T` or `--text` command will open a text based version inside your console. This command will open a connection to your slack.
