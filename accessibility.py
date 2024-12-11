import os
import matplotlib.pyplot as plt

file_directory = 'file'

dataset_name = 'dataset'

w1 = 0.2
w2 = 0.8

file_types = [f.split('.')[-1] for f in os.listdir(file_directory) if os.path.isfile(os.path.join(file_directory, f))]
unique_file_types = set(file_types)

file_type_diversity = len(unique_file_types)
max_file_type_diversity = 10
FTD_score = file_type_diversity / max_file_type_diversity

easy_formats = {'csv', 'json'}
easy_format_presence = any(fmt in unique_file_types for fmt in easy_formats)
PTP_score = 1 if easy_format_presence else 0

score = w1 * FTD_score + w2 * PTP_score

print(f"File Type Diversity Score: {FTD_score:.2f}")
print(f"Presence of Easy-to-Process Formats Score: {PTP_score:.2f}")
print(f"Accessibility Score: {score:.2f}")

scores = [FTD_score, PTP_score]
labels = ['AFT', 'DU']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, scores, color=['thistle', 'thistle'])
plt.ylim(0, 1)
plt.xlabel(f"Total Score: {score:.2f}")
plt.ylabel(dataset_name)
plt.title('Accessibility')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, round(yval, 2), ha='center', va='bottom')

plt.show()
