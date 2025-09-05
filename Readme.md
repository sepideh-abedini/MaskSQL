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

Download [this zip file](https://drive.google.com/file/d/1Fd7IroWv1-m9sJFj4DsGM2F9wHPBUfzt/view?usp=drive_link)
and extract it to the `data` directory.
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

