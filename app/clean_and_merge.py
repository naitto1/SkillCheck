import pandas as pd
import re

# Load the datasets
try:
    postings_df = pd.read_csv("/home/yusse/Coding/SkillCheck/job_postings.csv")
    skills_df = pd.read_csv("/home/yusse/Coding/SkillCheck/job_skills.csv")
    summary_df = pd.read_csv("/home/yusse/Coding/SkillCheck/job_summary.csv")
except FileNotFoundError as e:
    print(f"Error loading data: {e}")
    exit()

# Merge the dataframes
merged_df = pd.merge(postings_df, skills_df, on="job_link", how="left")
merged_df = pd.merge(merged_df, summary_df, on="job_link", how="left")

# Function to classify job titles
def classify_role(title):
    title_lower = str(title).lower()
    if "data scientist" in title_lower:
        return "Data Scientist"
    elif "machine learning" in title_lower or "ml" in title_lower:
        return "Machine Learning Engineer"
    elif "data analyst" in title_lower:
        return "Data Analyst"
    else:
        return "Other"

# Apply the classification
merged_df["Job Title"] = merged_df["job_title"].apply(classify_role)

# Filter out 'Other' roles
merged_df = merged_df[merged_df["Job Title"] != "Other"]

# Extract skills, tools, and languages
def extract_skills(text):
    if not isinstance(text, str):
        return ""
    # Simple extraction based on common keywords, can be improved
    skills = re.findall(r'''(python|sql|r|java|c\+\+|scala|julia|sas|matlab|tensorflow|pytorch|keras|scikit-learn|pandas|numpy|scipy|matplotlib|seaborn|ggplot|shiny|tableau|power bi|excel|spark|hadoop|aws|azure|gcp|docker|kubernetes|git|linux|unix|bash|shell|api|rest|graphql|soap|xml|json|html|css|javascript|react|angular|vue|django|flask|fastapi)''', text.lower())
    return ",".join(sorted(list(set(skills))))

merged_df["Skills"] = merged_df["job_skills"].fillna('') + ' ' + merged_df["job_summary"].fillna('')
merged_df["Cleaned Skills"] = merged_df["Skills"].apply(extract_skills)


# Define tools and languages based on extracted skills
def assign_tools(skills):
    tools = [skill for skill in skills.split(',') if skill in ['tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'ggplot', 'shiny', 'tableau', 'power bi', 'excel', 'spark', 'hadoop', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git']]
    return ",".join(tools)

def assign_languages(skills):
    languages = [skill for skill in skills.split(',') if skill in ['python', 'sql', 'r', 'java', 'c++', 'scala', 'julia', 'sas', 'matlab', 'bash', 'shell', 'html', 'css', 'javascript']]
    return ",".join(languages)

merged_df["Tools"] = merged_df["Cleaned Skills"].apply(assign_tools)
merged_df["Languages"] = merged_df["Cleaned Skills"].apply(assign_languages)


# Select and rename columns to match the target format
output_df = merged_df[["Job Title", "Cleaned Skills", "Tools", "Languages"]].rename(columns={"Cleaned Skills": "Skills"})

# Append to the existing cleaned_job_postings.csv
try:
    output_df.to_csv("/home/yusse/Coding/SkillCheck/dataset/cleaned_job_postings.csv", mode='a', header=False, index=False)
    print("Data cleaned and appended successfully.")
except Exception as e:
    print(f"Error writing to file: {e}")

