import pandas as pd
import matplotlib.pyplot as plt
import json

file_path = 'C:/Users/root/Desktop/TU Chemnitz/metadata/implementation/Stadtverwaltung.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

y = 'Stadtverwaltung'

features = data['features']
properties = [feature['properties'] for feature in features]

df = pd.DataFrame(properties)

# Ratio of Completely Missing Columns
cols = df.shape[1]
complete_missing_columns = df.isna().all().sum()
CMC = 1 - complete_missing_columns / cols
# Average Missing Data Rate
MDR = 1 - df.isna().mean(axis=1).mean()

w1 = 0.5
w2 = 0.5
score = w1 * (1 - CMC) + w2 * (1 - MDR)

print(f"Ratio of Completely Missing Columns: {CMC}")
print(f"Average Missing Data Rate: {MDR}")
print(f"Completeness Score: {score}")

fig, ax = plt.subplots(figsize=(10, 6))
categories = ['CMC', 'MDR']
values = [CMC, MDR]
bars = ax.bar(categories, values, color=['lightskyblue', 'lightskyblue'])

ax.set_ylim(0, 1)

ax.set_title('Completeness')
ax.set_xlabel(f"Total Score: {score:.2f}")
ax.set_ylabel(y)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

plt.show()
