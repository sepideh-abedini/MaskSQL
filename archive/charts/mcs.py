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
df["Leakage Score"] = 1 - df["MCS"]
df["Re-Identification Score"] = df['RIS']


sns.barplot(df, x="Model", y="Leakage Score", legend=False)
plt.ylim(0, 1)
plt.show()
