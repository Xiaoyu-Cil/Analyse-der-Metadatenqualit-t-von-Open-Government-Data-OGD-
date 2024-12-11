import pandas as pd
import datetime
import json
import matplotlib.pyplot as plt

file_path = 'path/file.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

dataset_name = 'dataset'

features = data['features']
properties = [feature['properties'] for feature in features]

df = pd.DataFrame(properties)
df['Stand'] = pd.to_datetime(df['Stand'], format='%Y%m%d%H%M%S', errors='coerce')

current_date = datetime.datetime.today()

six_months_ago = current_date - pd.DateOffset(months=6)
latest_data = df[df['Stand'] >= six_months_ago]
PLD = len(latest_data) / len(df)

print(f"PLD (Proportion of Latest Data): {PLD:.2f}")

df = df.sort_values(by='Stand')
df['time_diff'] = df['Stand'].diff().dt.days
avg_update_interval = df['time_diff'].mean()

if pd.isna(avg_update_interval):
    DUF = 0
else:
    DUF = min(7 / avg_update_interval, 1)

print(f"DUF (Data Update Frequency): {DUF:.2f}")

w1 = 0.5
w2 = 0.5
score = w1 * PLD + w2 * DUF
print(f"Timeliness: {score:.2f}")

labels = ['PLD', 'DUF']
scores = [PLD, DUF]

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, scores, color=['lightcoral', 'lightcoral'])
plt.ylim(0, 1)
plt.xlabel(f"Total Score: {score:.2f}")
plt.ylabel(dataset_name)
plt.title('Timeliness')

for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.show()
