# errbot plugin to rasa nlu

# Requirements

- errbot or [install it](http://errbot.io/en/latest/user_guide/setup.html#installation)
- python > 3
- [virtualenv](https://virtualenv.pypa.io)


# Install

```bash
mkdir my-errbot
cd my-errbot
errbot --init

# clon the repo
git clone git@github.com:mayflower/err-rasa.git plugins/rase-plugin
cd plugins/rasa-plugin
# install required python packages
python install -r requirements.txt
cd -

# use the predefined configuration
cp plugins/rasa-plugin/config_slack.py ./config.py
```

Edit config:

- add your slack token
- set `BOT_EXTRA_PLUGIN_DIR` value to `./plugins/rasa-plugin`

# Training
to add more training data copy the content of `config/chatito` and to to [Chatito](https://rodrigopivi.github.io/Chatito/) and copy it into the left field of the edtor.
there you can adjust the left side, generate the json and copy that into the training_data.json


# Run

```bash
# run errbot

errbot # should use config.py

``` 
