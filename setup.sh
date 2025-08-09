set -e

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
python nltk_downloader.py
python nltk_downloader.py

for d in eval_results models tensorboard_log third_party predictions; do
    mkdir -p "$d"
done

cd third_party
git clone https://github.com/ElementAI/spider.git
git clone https://github.com/ElementAI/test-suite-sql-eval.git
mv ./test-suite-sql-eval ./test_suite
cd ..

unzip data.zip
unzip database.zip