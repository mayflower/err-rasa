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

# Run

```bash
# run errbot

errbot # should use config.py

``` 
