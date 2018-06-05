echo "Download space dictionary"
python -m spacy download en_core_web_md
echo "link it"
python -m spacy link en_core_web_md en

python nlu_model.py


python dialogue_model.py
