import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

plt.rcParams["text.usetex"] = True
# plt.rcParams["mathtext.fontset"] = "stix"     # options: 'cm', 'stix', 'dejavusans', 'dejavuserif'
plt.rcParams["font.family"] = "serif"  # or 'sans-serif', 'monospace'

# 1. Recreate the data from the chart image
# The scores are represented as floats (e.g., 100% = 1.0) for plotting.
data = {
    # 'Model': ['Ground-Truth Masking', 'TrustSQL (Full Policy)', 'TrustSQL (Category-Based Policy)'],
    # 'Model': ['Ground-Truth Masking', 'TrustSQL ($\psi_{F}$)', 'TrustSQL (Category-Based Policy)'],
    'Model': [r'\textbf{Ground-Truth Masking}', r'\textbf{MaskSQL ($\Psi_{F}$)}', r'\textbf{MaskSQL ($\Psi_{C}$)}'],
    r'\textbf{Masking Recall}': [1.00, 0.6136, 0.3428],
    # r'\textbf{Masking Recall}': [1.00, 0.6136, 0.6903],
    # r'\textbf{Masking Recall}': [1.00, 0.6136, 0.4194],
    r'\textbf{Re-identification Score}': [0.8681, 0.7547, 0.7142]
}
df = pd.DataFrame(data)

# 2. Set a specific order for the y-axis categories to match the image.
# We reverse the list because matplotlib plots from the bottom up.
# category_order = ['Ground-Truth Masking', 'TrustSQL (Full Policy)', 'TrustSQL (Category-Based Policy)']
category_order = [r'\textbf{Ground-Truth Masking}', r'\textbf{MaskSQL ($\Psi_{F}$)}',
                  r'\textbf{MaskSQL ($\Psi_{C}$)}']
df['Model'] = pd.Categorical(df['Model'], categories=category_order, ordered=True)

# 3. "Melt" the DataFrame to a long format suitable for seaborn's `hue`.
# This creates separate rows for each metric, allowing for grouped bars.
df_melt = df.melt(id_vars=["Model"], value_vars=[r"\textbf{Masking Recall}", r"\textbf{Re-identification Score}"],
                  var_name="Metric", value_name="Score")

# 4. Set up the plot
# Using an object-oriented approach (fig, ax) gives more control.
fig, ax = plt.subplots(figsize=(12, 7), dpi=200)

# 5. Create the bar plot
# Define custom colors to match the image.
# colors = ["#3F65C5", "#C57B34"] # A specific blue and orange
sns.barplot(data=df_melt, y="Model", x="Score", hue="Metric", ax=ax, width=0.7, dodge=True, gap=0.08)

# 6. Add data labels to the end of each bar
for container in ax.containers:
    # Format labels as integers (e.g., 0.87 -> 87)
    labels = [f'{v * 100: .2f}' for v in container.datavalues]
    ax.bar_label(container, labels=labels, padding=5, fontsize=18, color='dimgray')

# 7. Customize axes and grid
# Format the x-axis to show percentages
ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
ax.set_xlim(0, 1.15)  # Extend x-axis limit to make space for labels
ax.set_xlabel(r"\textbf{Privacy Score (\%)}", fontsize=22)
# ax.set_xlabel("Privacy Score (")
ax.set_ylabel("")  # Remove the y-axis label

# Set font sizes for the tick labels
ax.tick_params(axis='y', labelsize=22)
ax.tick_params(axis='x', labelsize=20)

# Style the grid to match the image (vertical, dashed lines)
ax.grid(False)  # Turn off the default grid
ax.grid(axis='x', linestyle='--', color='grey', alpha=0.6, zorder=2000)  # Add a custom x-axis grid
ax.set_axisbelow(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 8. Customize the legend
# Place it above the chart, remove the title and border.
ax.legend(title="", fontsize=22, loc="upper center",
          bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False)

# 9. Display and save the plot
plt.savefig("charts/final/priv.png", bbox_inches="tight")
plt.show()
