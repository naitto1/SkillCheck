import pandas as pd
from collections import Counter
import re # Import the regular expression module for cleaning

# --- Configuration ---
# Replace 'your_job_data.csv' with the actual path to your CSV file
csv_file_path = '../dataset/job_skills.csv'
# Replace 'Skills' with the actual name of the column containing job skills
skills_column_name = 'job_skills'
# Replace 'skill_counts.csv' with the desired name for the output file
output_csv_path = '../dataset/skill_counts.csv'

# Define common delimiters you might find in the skills column
# Add or remove delimiters as needed based on your data
skill_delimiters = [',', ';', '/', '|']

# --- Data Loading ---
try:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    print(f"Successfully loaded data from '{csv_file_path}'")
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns available: {df.columns.tolist()}")

except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
    print("Please check the file path and make sure the file exists.")
    exit() # Exit the script if the file is not found
except Exception as e:
    print(f"An error occurred while loading the CSV file: {e}")
    exit()

# --- Data Processing ---
# Check if the specified skills column exists in the DataFrame
if skills_column_name not in df.columns:
    print(f"Error: Column '{skills_column_name}' not found in the CSV.")
    print(f"Available columns are: {df.columns.tolist()}")
    exit() # Exit if the column is not found

# Initialize a list to hold all individual skills
all_skills = []

# Iterate through each row in the DataFrame's skills column
# Use .astype(str) to handle potential non-string data like NaNs
for skills_string in df[skills_column_name].astype(str).dropna():
    # Split the string by multiple delimiters using regex
    # re.split will handle cases like "Skill1, Skill2; Skill3"
    # The regex pattern joins delimiters with '|' (OR)
    individual_skills = re.split('|'.join(map(re.escape, skill_delimiters)), skills_string)

    # Process each extracted skill
    for skill in individual_skills:
        # Clean up whitespace, convert to lowercase, and remove non-alphanumeric chars
        cleaned_skill = skill.strip().lower()
        # Optional: Further cleaning if needed, e.g., removing specific symbols
        # cleaned_skill = re.sub(r'[^a-z0-9+#.\- ]', '', cleaned_skill) # Example: keeps alphanumeric, +, #, ., -, space

        # Only add non-empty strings to our list
        if cleaned_skill:
            all_skills.append(cleaned_skill)

# --- Counting Skills ---
# Use Counter to count the occurrences of each unique skill
skill_counts = Counter(all_skills)

# --- Results ---
print(f"\nFound {len(skill_counts)} unique skills.")
print("Top 10 most common skills:")
for skill, count in skill_counts.most_common(10):
    print(f"- {skill}: {count}")

# --- Saving Results ---
# Convert the Counter object to a pandas DataFrame for easy saving
counts_df = pd.DataFrame.from_dict(skill_counts, orient='index', columns=['Count'])

# Sort the skills by count in descending order
counts_df = counts_df.sort_values(by='Count', ascending=False)

try:
    # Save the skill counts to a new CSV file
    counts_df.to_csv(output_csv_path, index_label='Skill')
    print(f"\nSkill counts saved to '{output_csv_path}'")
except Exception as e:
    print(f"An error occurred while saving the skill counts CSV: {e}")

