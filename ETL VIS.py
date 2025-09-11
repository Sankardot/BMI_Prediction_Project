import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# Setup folder
# -----------------------------
visuals_folder = 'C:/Users/hp/OneDrive/Desktop/python py/visuals'
os.makedirs(visuals_folder, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
csv_path = 'C:/Users/hp/OneDrive/Desktop/python py/transformed_data.csv'
df = pd.read_csv(csv_path)

# Calculate BMI
df['BMI'] = (df['Weight'] / (df['Height'] ** 2)).round(2)

# -----------------------------
# 1. BMI Distribution with KDE + Rug
# -----------------------------
plt.figure(figsize=(8,6))
sns.histplot(df['BMI'], kde=True, color='skyblue', edgecolor='black', stat='density')
sns.rugplot(df['BMI'], color='red')
plt.title('Advanced BMI Distribution')
plt.xlabel('BMI')
plt.ylabel('Density')
plt.savefig(os.path.join(visuals_folder, 'advanced_bmi_distribution.png'))
plt.show()

# -----------------------------
# 2. Weight vs BMI Bubble Plot (Height as size)
# -----------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(
    x='Weight', y='BMI', size='Height', hue='Name', data=df,
    sizes=(50, 300), alpha=0.7, palette='tab20'
)
plt.title('Weight vs BMI (Bubble Plot by Height)')
plt.xlabel('Weight')
plt.ylabel('BMI')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig(os.path.join(visuals_folder, 'weight_bmi_bubble.png'))
plt.show()

# -----------------------------
# 3. Height vs BMI with Regression Line
# -----------------------------
plt.figure(figsize=(8,6))
sns.regplot(x='Height', y='BMI', data=df, scatter_kws={'s':80, 'color':'orange'}, line_kws={'color':'blue'})
plt.title('Height vs BMI (Regression)')
plt.xlabel('Height')
plt.ylabel('BMI')
plt.savefig(os.path.join(visuals_folder, 'height_bmi_regression.png'))
plt.show()

# -----------------------------
# 4. Pairplot (Height, Weight, BMI)
# -----------------------------
sns.pairplot(df[['Height', 'Weight', 'BMI']], kind='scatter', diag_kind='kde', height=2.5)
plt.suptitle('Pairplot of Height, Weight, BMI', y=1.02)
plt.savefig(os.path.join(visuals_folder, 'pairplot.png'))
plt.show()

