set -e

pyenv local 3.8
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.0/en_core_web_sm-2.3.0.tar.gz
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
python nltk_downloader.py

for d in eval_results models tensorboard_log third_party predictions; do
    mkdir -p "$d"
done

cd third_party
git clone https://github.com/ElementAI/spider.git
git clone https://github.com/ElementAI/test-suite-sql-eval.git
mv ./test-suite-sql-eval ./test_suite
cd ..

unzip -o ../data/resdsql/text2sql-t5-base.zip -d models
unzip -o ../data/resdsql/text2sql_schema_item_classifier.zip -d models

pip install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
