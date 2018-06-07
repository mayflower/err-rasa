FROM python:3.6

RUN mkdir -p /mnt/bot && mkdir /mnt/bot/data && mkdir /mnt/bot/models
WORKDIR /mnt/bot

COPY config plugin actions.py config.py nlu_model.py dialogue_model.py create_models.sh requirements.txt /mnt/bot/
RUN pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -m spacy link en_core_web_sm en && ./mnt/bot/create_models.sh

CMD ["errbot", "config.py"]