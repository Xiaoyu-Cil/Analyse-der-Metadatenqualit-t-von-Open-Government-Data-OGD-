import pandas as pd
import json
import matplotlib.pyplot as plt

file_path = 'path/file.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

dataset_name = 'dataset'

features = data['features']
properties_list = [feature['properties'] for feature in features]
df = pd.DataFrame(properties_list)

def check_uniqueness(df):
    unique_id = df['ID'].nunique() == len(df)
    unique_id2 = df['ID2'].nunique() == len(df)
    return unique_id, unique_id2

def check_anomalies(df):
    anomalies = {}
    anomalies['PLZ'] = df['PLZ'].apply(lambda x: len(str(x)) == 5 and str(x).isdigit()).all()
    current_date = pd.to_datetime('now')
    anomalies['Stand'] = pd.to_datetime(df['Stand'], format='%Y%m%d%H%M%S', errors='coerce').apply(lambda x: x <= current_date).all()
    anomalies['letzte_aend'] = pd.to_datetime(df['letzte_aend'], format='%Y%m%d%H%M%S', errors='coerce').apply(lambda x: x <= current_date).all()
    anomalies['X'] = df['X'].apply(lambda x: isinstance(x, (int, float)) and 0 <= x <= 10000000).all()
    anomalies['Y'] = df['Y'].apply(lambda x: isinstance(x, (int, float)) and 0 <= x <= 10000000).all()
    return anomalies

def check_data_accuracy(df):
    accuracy = {}
    accuracy['Strasse'] = df['Strasse'].apply(lambda x: bool(pd.Series([x]).str.contains(r'\d+').any())).astype(int)
    accuracy['PLZ'] = df['PLZ'].notna().astype(int)
    accuracy['X'] = df['X'].notna().astype(int)
    accuracy['Y'] = df['Y'].notna().astype(int)
    return pd.DataFrame(accuracy)

def calculate_scores(df):
    unique_id, unique_strasse = check_uniqueness(df)
    uniqueness_score = sum([unique_id, unique_strasse]) / 2

    anomalies = check_anomalies(df)
    anomaly_score = sum(anomalies.values()) / len(anomalies)

    accuracy = check_data_accuracy(df)
    accuracy_score = accuracy['Strasse'].mean()

    return uniqueness_score, anomaly_score, accuracy_score

uniqueness_score, anomaly_score, accuracy_score = calculate_scores(df)

weights = [1/3, 1/3, 1/3]
score = weights[0] * uniqueness_score + weights[1] * anomaly_score + weights[2] * accuracy_score

print(f"Total Score: {score:.2f}")

scores = [uniqueness_score, anomaly_score, accuracy_score]
labels = ['UC', 'AC', 'DAC']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, scores, color=['palegoldenrod', 'palegoldenrod', 'palegoldenrod'])
plt.ylim(0, 1)
plt.xlabel(f"Total Score: {score:.2f}")
plt.ylabel(dataset_name)
plt.title('Accuracy')

for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.show()
