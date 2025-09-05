import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"

data = {
    'Model': [r'\textbf{Ground-Truth Masking}', r'\textbf{MaskSQL ($\Psi_{F}$)}', r'\textbf{MaskSQL ($\Psi_{C}$)}'],
    r'\textbf{Masking Recall}': [1.00, 0.6136, 0.3428],
    r'\textbf{Re-identification Score}': [0.8681, 0.7547, 0.7142]
}
df = pd.DataFrame(data)

category_order = [r'\textbf{Ground-Truth Masking}', r'\textbf{MaskSQL ($\Psi_{F}$)}',
                  r'\textbf{MaskSQL ($\Psi_{C}$)}']
df['Model'] = pd.Categorical(df['Model'], categories=category_order, ordered=True)

df_melt = df.melt(id_vars=["Model"], value_vars=[r"\textbf{Masking Recall}", r"\textbf{Re-identification Score}"],
                  var_name="Metric", value_name="Score")

fig, ax = plt.subplots(figsize=(12, 7), dpi=200)

sns.barplot(data=df_melt, y="Model", x="Score", hue="Metric", ax=ax, width=0.7, dodge=True, gap=0.08)

for container in ax.containers:
    labels = [rf'\textbf{{{v * 100: .2f}}}' for v in container.datavalues]
    ax.bar_label(container, labels=labels, padding=5, fontsize=18, color='black', fontweight="bold")

ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.set_xlim(0, 1.15)
ax.set_xlabel(r"\textbf{Privacy Score (\%)}", fontsize=22, fontweight="bold")
ax.set_ylabel("")

ax.tick_params(axis='y', labelsize=22, labelcolor='black')
ax.tick_params(axis='x', labelsize=20, labelcolor='black')

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight("bold")
    label.set_color("black")
    print(label)
    # label.set_text(label.get_text().replace(r'\textbf{', '').replace('}', ''))
    label.set_text("BAD")


# Manually set x- and y-tick labels, bold, black, no LaTeX commands
ax.set_xticklabels([r"\textbf{0\%}", r"\textbf{20\%}",r"\textbf{40\%}",r"\textbf{60\%}",r"\textbf{80\%}",r"\textbf{100\%}"], fontsize=20, fontweight="bold", color="black")

ax.grid(False)
ax.grid(axis='x', linestyle='--', color='grey', alpha=0.6, zorder=2000)
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

legend = ax.legend(title="", fontsize=22, loc="upper center",
                   bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)
for text in legend.get_texts():
    text.set_fontweight("bold")

plt.savefig("charts/final/priv.png", bbox_inches="tight")
plt.show()