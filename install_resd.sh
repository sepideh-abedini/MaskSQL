set -euo pipefail

cd resdsql

for d in eval_results models tensorboard_log third_party predictions; do
    mkdir -p "$d"
done

python3.8 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
pip install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
python nltk_downloader.py

cd models
for model in "text2sql-t5-base" "text2sql_schema_item_classifier"
do
  wget "https://storage.googleapis.com/sepiid/resd/$model.zip"
  unzip $model.zip
done

