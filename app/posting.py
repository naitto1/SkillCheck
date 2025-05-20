
import pandas as pd
from collections import Counter
import re 

csv_file_path = '../dataset/job_postings.csv'
skills_column_name = 'job_title'
output_csv_path = '../dataset/skill_counts.csv'

df = pd.read_csv({csv_file_path})

name_and_location = []

for skills_string in df[skills_column_name].astype(str).dropna():
    job_name = re.split('|'.join(map(re.escape, skill_delimiters)), skills_string)


try:
    counts_df.to_csv(output_csv_path, index_label='Location')
    print(f"\nSkill counts saved to '{output_csv_path}'")
except Exception as e:
    print(f"An error occurred while saving the skill counts CSV: {e}")