import json
import os.path

import natsort
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from natsort import natsorted

from src.cat.catter import Catter

out_dir = os.path.join("out", "new")

catter = Catter()

df_rows = []
for model in ["gpt", "qwen"]:
    for masking in ["full", "partial"]:
        expr_dir = os.path.join(out_dir, f"{model}-{masking}")
        results_file = os.path.join(expr_dir, "18_ExecAccCalc.json")
        with open(results_file) as f:
            data = json.load(f)
            for row in data:
                sql = row['query']
                cat = catter.get_category(sql)
                sub = catter.get_sub_category(sql)
                df_rows.append({
                    "Execution Accuracy": row['eval']['acc'] * 100,
                    "SubCategory": sub.name.upper(),
                    "Category": cat.name.upper(),
                    "Model": model,
                    "Masking": masking
                })

df = pd.DataFrame(df_rows)
df['Model'] = df['Model'].replace({
    'gpt': 'GPT-4.1',
    'qwen': 'Qwen-2.5 + GPT-4.1'
})

df = df[df['Masking'] == "full"]
df['count'] = 1

order = natsorted(df['Category'].unique())
sub_order = natsorted(df['SubCategory'].unique())

cat_grouped = df.groupby("Category").agg({
    "count": "sum",
    "Execution Accuracy": "mean"
}).reset_index()

cat_grouped.to_csv("out/charts/cat.csv")

cat_grouped = df.groupby("SubCategory").agg({
    "count": "sum",
    "Execution Accuracy": "mean"
}).reset_index()

cat_grouped.to_csv("out/charts/sub.csv")

# plt.figure(figsize=(10, 6))
# sns.barplot(data=df, x='Category', y='Execution Accuracy', hue='Model', order=order, errorbar=None)
# sns.barplot(data=df, x='SubCategory', y='Execution Accuracy', hue='Model', order=sub_order, errorbar=None)

# plt.xlabel("SubCategory")
# plt.ylabel("Execution Accuracy")
# plt.legend(title="Model")
# plt.xticks(rotation=45)
# plt.savefig(os.path.join("out/charts", "exec_accuracy_by_sub.png"), dpi=300)
# plt.tight_layout()
# plt.show()
