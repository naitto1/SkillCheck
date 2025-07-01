
import pandas as pd
import re

def clean_text(text):
    """Remove special characters and convert to lowercase."""
    if isinstance(text, str):
        return re.sub(r'[^A-Za-z0-9\s]+', '', text).lower()
    return text

def clean_data():
    """Cleans and prepares the job posting data."""
    # Load datasets
    try:
        job_postings = pd.read_csv('/home/yusse/Coding/SkillCheck/dataset/job_postings.csv')
        job_skills = pd.read_csv('/home/yusse/Coding/SkillCheck/dataset/job_skills.csv')
        job_summary = pd.read_csv('/home/yusse/Coding/SkillCheck/dataset/job_summary.csv')
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None

    # Clean text data
    for df in [job_postings, job_skills, job_summary]:
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(clean_text)

    # Merge dataframes
    merged_df = pd.merge(job_postings, job_skills, on='job_link', how='left')
    merged_df = pd.merge(merged_df, job_summary, on='job_link', how='left')

    # Filter for specific job titles
    job_titles = ['data scientist', 'machine learning engineer', 'data analyst']
    filtered_df = merged_df[merged_df['job_title'].str.contains('|'.join(job_titles), case=False, na=False)]

    # Save cleaned data
    filtered_df.to_csv('/home/yusse/Coding/SkillCheck/dataset/cleaned_job_postings.csv', index=False)
    print("Data cleaning complete. Cleaned data saved to 'cleaned_job_postings.csv'")
    return filtered_df

if __name__ == '__main__':
    clean_data()
