import pandas as pd

df = pd.read_csv("errors.csv")

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("errors.csv")

# Ensure the column name matches exactly
category_col = "Error Category"

# Split rows containing multiple categories separated by '+'
all_categories = []
for categories in df[category_col].dropna():
    split_values = [cat.strip() for cat in categories.split('+')]
    all_categories.extend(split_values)

# Count occurrences of each category
category_counts = pd.Series(all_categories).value_counts()

# Plot a pie chart
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Error Category Distribution")
plt.tight_layout()
plt.savefig("out/charts/error_pie.png")
plt.show()
