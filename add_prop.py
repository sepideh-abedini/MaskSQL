import json

from ut.json_utils import read_json, write_json

src = "out/latest/trust_partial_new_very_new/3_FilterAnonLinks.json"
dst = "out/latest/trust_partial_new_very_new_final/21_Attack.json"
prop = "filt_anon_links"

src_data = read_json(src)

dst_data = read_json(dst)

updated_data = []

for i, row in enumerate(dst_data):
    s_row = src_data[i]
    row[prop] = s_row[prop]
    updated_data.append(row)

write_json(dst, updated_data)
