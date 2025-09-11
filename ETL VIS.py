import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("C:/Users/hp/OneDrive/Desktop/python py/data/processed/cleaned_data.csv")


# BMI Distribution
sns.histplot(df['BMI'], kde=True, color='skyblue')
plt.title('BMI Distribution')
plt.savefig('../visuals/bmi_distribution.png')
plt.show()

# Age vs BMI
sns.scatterplot(x='Age', y='BMI', hue='Gender', data=df)
plt.title('Age vs BMI')
plt.savefig('../visuals/age_bmi_scatter.png')
plt.show()
