import os.path

from fine.json_utils import read_json, write_json

data = read_json("out/bird/18_ExecAccCalc.json")

total = 0
count = 0

merge_data = []

for row in data:
    if row['eval']['acc'] == 0:
        total += 1
        idx = row['idx']
        orig_path = f"out/fine/300_anon/{idx}.json"
        check_path = f"out/fine/unwinds_check/{idx}.json"
        if os.path.exists(orig_path):
            anon = read_json(orig_path)
        else:
            anon = read_json(check_path)
        merge_data.append(anon)

write_json("out/new_fine/1_input.json", merge_data)

print("-" * 100)
print(count)
print(total)
