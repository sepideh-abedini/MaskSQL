import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns


def format_model(row):
    if row['Variant']:
        return f"{row['Model']}\n({row['Variant']})"
    return f"{row['Model']}"


df = pd.read_json("charts/final/data.json")
df = df[df["Model"] != "GroundTruth Masking"]
df["Model"] = df.apply(format_model, axis=1)
df["ours"] = df["Model"].apply(lambda x: "TrustSQL" in x)
df = df.sort_values(by="EA")
df['Execution Accuracy'] = df['EA']

plt.rcParams.update({'font.size': 17})  # set global font size
plt.figure(dpi=300, figsize=(14, 6))
palette = {True: '#2ca02c', False: "#1f77b4"}
sns.barplot(df, x="Model", y="Tokens", hue="ours", palette=palette, legend=False, width=0.6)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x / 1000)}k'))
plt.yticks(fontsize=15)
# plt.xticks(fontsize=20)
plt.xlabel("")
plt.ylabel("Total Token Usage")
# plt.ylim(0, 15)
# plt.show()
plt.savefig("charts/final/token_usage.png", bbox_inches="tight")
plt.show()
