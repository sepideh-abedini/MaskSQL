import os.path

from fine.json_utils import read_json, write_json

data = read_json("out/bird/18_ExecAccCalc.json")

total = 0
count = 0
for row in data:
    if row['eval']['acc'] == 0:
        total += 1
        idx = row['idx']
        anon_path = f"out/fine/300_anon/{idx}.json"
        if os.path.exists(anon_path):
            anon = read_json(anon_path)
            write_json(f"out/fine/unwinds_final/{idx}.json", anon)
            count += 1
        else:
            anon = read_json(f"out/fine/unwinds_final/{idx}.json")
            write_json(f"out/fine/unwinds_check/{idx}.json", anon)
            print(idx)

print("-" * 100)
print(count)
print(total)
