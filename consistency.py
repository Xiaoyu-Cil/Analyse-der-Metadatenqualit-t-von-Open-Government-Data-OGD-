import pandas as pd
import matplotlib.pyplot as plt
import json

file_path = 'path/file.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

dataset_name = 'dataset'

features = data['features']
properties_list = [feature['properties'] for feature in features]
df = pd.DataFrame(properties_list)

def check_column_type_consistency(df):
    consistency_scores = {}
    for column in df.columns:
        consistency_scores[column] = df[column].apply(type).nunique() == 1
    return consistency_scores

def check_date_format_consistency(df, date_columns):
    consistency_scores = {}
    for column in date_columns:
        try:
            pd.to_datetime(df[column], format='%Y%m%d%H%M%S', errors='raise')
            consistency_scores[column] = True
        except ValueError:
            consistency_scores[column] = False
    return consistency_scores

def check_duplicates(df):
    duplicate_rows = df.duplicated().sum()
    
    transposed_df = df.T
    duplicate_columns = transposed_df.duplicated().sum()
    
    return duplicate_rows, duplicate_columns

def calculate_scores(df, date_columns):
    type_consistency = check_column_type_consistency(df)
    date_consistency = check_date_format_consistency(df, date_columns)
    duplicate_rows, duplicate_columns = check_duplicates(df)

    total_columns = len(df.columns)
    total_rows = len(df)
    
    type_consistency_score = sum(type_consistency.values()) / total_columns
    date_consistency_score = sum(date_consistency.values()) / len(date_columns)
    duplicate_score = 1 - ((duplicate_rows + duplicate_columns) / (total_rows + total_columns))
    
    return type_consistency_score, date_consistency_score, duplicate_score

date_columns = ['Stand', 'letzte_aend']

type_consistency_score, date_consistency_score, duplicate_score = calculate_scores(df, date_columns)

weights = [1/3, 1/3, 1/3]
score = weights[0] * type_consistency_score + weights[1] * date_consistency_score + weights[2] * duplicate_score

print(f"type consistency: {type_consistency_score}")
print(f"data format consistency: {date_consistency_score}")
print(f"no duplicates: {duplicate_score}")
print(f"Total Score: {score:.2f}")

scores = [type_consistency_score, date_consistency_score, duplicate_score]
labels = ['DC', 'DFC', 'DRC']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, scores, color=['lightgreen', 'lightgreen', 'lightgreen'])
plt.ylim(0, 1)
plt.xlabel(f"Total Score: {score:.2f}")
plt.ylabel('Scores')
plt.title('Consistency')

for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height:.2f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom')

plt.show()
