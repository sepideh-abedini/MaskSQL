import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = [
    {
        'model': "Perfect Masking",
        'RIS': 0.13
    },
    {
        'model': "TrustSQL (Full)",
        'RIS': 0.24
    },
    {
        'model': "TrustSQL (Partial)",
        'RIS': 0.27
    },
]

df = pd.DataFrame(data)

sns.barplot(df, x="model", y="RIS", legend=False, )
plt.ylim(0, 1)
plt.show()
