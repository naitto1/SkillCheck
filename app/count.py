import pandas as pd
from collections import Counter
import re 


csv_file_path = '../dataset/job_skills.csv'
skills_column_name = 'job_skills'
output_csv_path = '../dataset/skill_counts.csv'

skill_delimiters = [',', ';', '/', '|']

try:
    df = pd.read_csv(csv_file_path)
    print(f"Successfully loaded data from '{csv_file_path}'")
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns available: {df.columns.tolist()}")

except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    print("Please check the file path and make sure the file exists.")
    exit() 
except Exception as e:
    print(f"An error occurred while loading the CSV file: {e}")
    exit()


if skills_column_name not in df.columns:
    print(f"Error: Column '{skills_column_name}' not found in the CSV.")
    print(f"Available columns are: {df.columns.tolist()}")
    exit() 

all_skills = []


for skills_string in df[skills_column_name].astype(str).dropna():
    individual_skills = re.split('|'.join(map(re.escape, skill_delimiters)), skills_string)

    for skill in individual_skills:
        cleaned_skill = skill.strip().lower()

        if cleaned_skill:
            all_skills.append(cleaned_skill)

skill_counts = Counter(all_skills)

print(f"\nFound {len(skill_counts)} unique skills.")
print("Top 10 most common skills:")
for skill, count in skill_counts.most_common(10):
    print(f"- {skill}: {count}")

counts_df = pd.DataFrame.from_dict(skill_counts, orient='index', columns=['Count'])

counts_df = counts_df.sort_values(by='Count', ascending=False)

try:
    counts_df.to_csv(output_csv_path, index_label='Skill')
    print(f"\nSkill counts saved to '{output_csv_path}'")
except Exception as e:
    print(f"An error occurred while saving the skill counts CSV: {e}")

