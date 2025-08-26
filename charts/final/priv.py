import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_json("charts/data.json")

df = df[df["Model"].isin(["TrustSQL", "GroundTruth Masking"])]


def format_model(row):
    if row['Variant']:
        return f"{row['Model']}({row['Variant']})"
    return f"{row['Model']}"


df["Model"] = df.apply(format_model, axis=1)
df = df.sort_values(by="MCS")
df["Masking Recall"] = df["MCS"]
df["Re-identification"] = 1 - df['RIS']

melt_cols = ["Masking Recall", "Re-identification"]
plt.figure(dpi=300)
plt.rcParams.update({'font.size': 17})  # set global font size
plt.figure(figsize=(8, 8))
df_melt = df.melt(id_vars=["Model"], value_vars=melt_cols, var_name="Privacy Metric", value_name="Score")
sns.barplot(df_melt, x="Model", y="Score", hue="Privacy Metric", width=0.6)
# sns.barplot(df, x="Model", y="Leakage Score", legend=False)
plt.ylim(0, 1)
plt.xticks(fontsize=15)
plt.xlabel("")
# plt.ylabel("Score", fontsize=20)
plt.savefig("charts/final/priv.png", bbox_inches="tight")
plt.show()
