import argparse
import json

parser = argparse.ArgumentParser(description="Copy JSON property from source to dest")
parser.add_argument("--src", required=True, help="Path to source JSON file")
parser.add_argument("--dst", required=True, help="Path to destination JSON file")
parser.add_argument("--out", required=True, help="Path to output file")
parser.add_argument("--prop", required=True, help="Property to copy from source to dest")
args = parser.parse_args()

with open(args.src) as src_file:
    src_data = json.load(src_file)

with open(args.dst) as dst_file:
    dst_data = json.load(dst_file)

updated_data = []

for i, row in enumerate(dst_data):
    s_row = src_data[i]
    row[args.prop] = s_row[args.prop]
    updated_data.append(row)

with open(args.out, 'w') as f:
    f.write(json.dumps(updated_data, indent=4))
