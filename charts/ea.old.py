import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = [
    {
        'model': "Qwen2.5",
        'EA': 0.32,
        'Tokens': 1383,
        'Latency': 1.4,
        'us': False
    },
    {
        'model': "DAIL (Qwen)",
        'EA': 0.44,
        'Tokens': 3492,
        'Latency': 12.2,
        'us': False
    },
    {
        'model': "MSc-SQL",
        'EA': 0.48,
        'Tokens': 8342,
        'Latency': 10.30,
        'us': False
    },
    {
        'model': "DIN (Qwen)",
        'EA': 0.50,
        'Tokens': 24812,
        'Latency': 12.2,
        'us': False
    },
    {
        'model': "TrustSQL",
        'EA': 0.55,
        'Tokens': 6114,
        'Latency': 9.60,
        'us': True
    },
    {
        'model': "DAIL (GPT-4.1)",
        'EA': 0.63,
        'Tokens': 3385,
        'Latency': 11.31,
        'us': False
    },
    {
        'model': "DIN (GPT-4.1)",
        'EA': 0.73,
        'Tokens': 23036,
        'Latency': 7.51,
        'us': False
    },
    {
        'model': "GPT-4.1",
        'EA': 0.81,
        'Tokens': 1351,
        'Latency': 1.53,
        'us': False
    },
]

df = pd.DataFrame(data)

plt.figure(figsize=(12, 6))
sns.barplot(df, x="model", y="EA", hue='us',palette={True: '#2ca02c', False:"#1f77b4"}, legend=False)
plt.ylim(0, 1)
plt.show()
