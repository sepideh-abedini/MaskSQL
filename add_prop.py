import json

from ut.json_utils import read_json, write_json

src = "out/latest/trust_full/20_Attack.json"
dst = "out/latest/ablation/8_slm_repair/16_AddConcreteSql.json"
prop = "attack"

src_data = read_json(src)

dst_data = read_json(dst)

updated_data = []

for i, row in enumerate(dst_data):
    s_row = src_data[i]
    row[prop] = s_row[prop]
    updated_data.append(row)

write_json(dst, updated_data)
