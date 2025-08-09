import json

import spacy


def main():
    with open("dout/input.json") as f:
        data = json.load(f)
    with open("resdsql_test.orig.json") as resdfile:
        resd = json.load(resdfile)

    rows = []
    for i, entry in enumerate(data):
        entry['tc_original'] = resd[i]['tc_original']
        rows.append(entry)

    with open("dout/input.json", "w") as f:
        f.write(json.dumps(rows, indent=4))


if __name__ == '__main__':
    main()
