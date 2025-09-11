import json
from abc import ABC, abstractmethod
from dataclasses import dataclass


def read_json(path):
    with open(path) as f:
        return json.load(f)


def write_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=4))
