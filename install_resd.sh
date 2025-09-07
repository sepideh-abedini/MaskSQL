set -euo pipefail

cd resdsql

python3.8 -m venv .venv
source .venv/bin/activate
module load gcc cuda

pip install -r requirements.txt

#pip install spacy==2.2.2
#pip install nltk==3.9.1
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz
#pip install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
#pip install rapidfuzz==3.9.7
#pip install transformers==2.11.0
#pip install six==1.16.0
#pip install  scikit-learn==1.2.1
python nltk_downloader.py