import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

df = pd.read_json("charts/final/data.json")

df = df[df["Model"].isin(["TrustSQL", "Ground-Truth Masking"])]


def format_model(row):
    if row['Variant']:
        return f"{row['Model']} ({row['Variant']})"
    return f"{row['Model']}"


# palette = ["#5C8AFF", "#C57B34"]  # orange, blue
# palette = ["#8AAEE0", "#E8A962"]

df["Model"] = df.apply(format_model, axis=1)
df = df.sort_values(by="MCS")
df["Masking Recall"] = df["MCS"]
df["Re-identification"] = 1 - df['RIS']

melt_cols = ["Masking Recall", "Re-identification"]
plt.figure(dpi=300)
plt.rcParams.update({'font.size': 26})
plt.figure(figsize=(8, 8))
df_melt = df.melt(id_vars=["Model"], value_vars=melt_cols, var_name="Privacy Metric", value_name="Score")
sns.barplot(df_melt, palette=palette, y="Model", x="Score", hue="Privacy Metric", width=0.6)
plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
# sns.barplot(df, x="Model", y="Leakage Score", legend=False)
plt.legend(fontsize=22, loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)
# plt.ylim(0, 1)
# plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
plt.ylabel("")
plt.yticks(rotation=0, ha='right', va='center')
# plt.ylabel("Score", fontsize=20)
plt.savefig("charts/final/priv.png", bbox_inches="tight")
plt.show()
