# MaskSQL

# Table of Contents

- [Installation](#installation-and-setup-instruction)
- [Run MaskSQL](#run-masksql)
- [MaskSql Framework](Framework.md)
- [MaskSQL Pipeline Stages](Stages.md)

## Installation and Setup Instructions

### System Requirements

python 3.11, virtualenv

You can use pyenv to setup Python 3.11

```shell
pyenv local 3.11
```

### Install Requirements

```shell
python3.11 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Download Dataset

Download [this zip file](https://www.dropbox.com/scl/fi/0zu1hpsnvn0u9blutb76o/data.zip?rlkey=84tfxxtr7n9tzs34uh33vbvut&st=lkvv9esa&dl=0)
and extract it to the `data` directory:

```shell
wget -O data.zip "https://www.dropbox.com/scl/fi/0zu1hpsnvn0u9blutb76o/data.zip?rlkey=84tfxxtr7n9tzs34uh33vbvut&st=lkvv9esa&dl=0"
unzip data.zip
```

Your data directory should look like this:

```shell
data/
├── databases/
├── 1_input.json
.
.
.
```

### Set Environment Variables

```shell
cp .env.example .env
```

The only required variable to set is `OPENAI_API_KEY`.
By default, we are using [OpenRouter](https://openrouter.ai/), so you need to set the api key
for OpenRouter.

You may also change the `LIMIT` variable to modify the number of entries to be read from the dataset.
`START` specifies the start index for reading from the dataset.

For instance, set `LIMIT=10` to run the pipeline for a dataset of size 10.

`SLM_MODEL` and `LLM_MODEL` specify the ID of small/large language models to be used in the pipeline.
These IDs should be set based on the LM provider being used.
For instance, since we are using OpenRouter, model identifiers should be specified accordingly, e.g.,
`openai/gpt-4.1` for GPT-4.1.

### Run RESDSQL
To run MaskSQL, first we need to filter the schema items
using RESDSQL.
Follow these [instructions](./Resd.md) to run the RESDSQL
and generated the file needed for the MaskSQL pipeline.
Then, you need to run the MaskSQL with the `--resd` option.

### Run MaskSQL
To run the MaskSQL, first you need to activate the venv and set the environment variables:

```shell
source .venv/bin/activated
export $(cat .env | xargs)
export PYTHONPATH=.
```

Then you can simply run the `main.py`:

```shell
python main.py
```
Or, if you want to run with the RESDSQL run the following:
```shell
python main.py --resd
```
> Not that if you use `--resd` option you should first run the RESDSQL
> using the instruction described [here](./Resd.md)  

