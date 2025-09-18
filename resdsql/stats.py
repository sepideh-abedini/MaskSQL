# import json
# import os.path
#
# import natsort
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# import pandas as pd
# from natsort import natsorted
#
# from src.taxonomy.cat.catter import Catter
#
# out_dir = os.path.join("out", "new")
#
# catter = Catter()
#
# df_rows = []
# for model in ["gpt", "qwen"]:
#     for masking in ["full", "partial"]:
#         expr_dir = os.path.join(out_dir, f"{model}-{masking}")
#         results_file = os.path.join(expr_dir, "18_ExecAccCalc.json")
#         with open(results_file) as f:
#             data = json.load(f)
#             for row in data:
#                 sql = row['query']
#                 cat = catter.get_category(sql)
#                 sub = catter.get_sub_category(sql)
#                 df_rows.append({
#                     "ea": row['eval']['acc'],
#                     "Model": model,
#                     "Masking": masking
#                 })
#
# df = pd.DataFrame(df_rows)
# # df = df[df['Masking'] == "full"]
#
#
# g = df.groupby(['Model','Masking']).sum()
# print(g)
