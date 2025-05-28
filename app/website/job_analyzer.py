import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Job Skills Analyzer")

# --- App Title ---
st.title("📊 Job Skills Analyzer")
st.markdown("Visualizing skill requirements for a specific job role.")
st.markdown("---")

# --- Placeholder Data ---
# You would replace this with your actual data loading and processing logic.
# For example, you might scrape a job description, parse it, and then count occurrences.

# For a hypothetical "Data Scientist" role
job_title_placeholder = "Data Scientist"

# 1. Education Level Data (Percentages)
education_data = {
    'Level': ['Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'Associate\'s Degree', 'High School Diploma/GED'],
    'Percentage': [45, 35, 15, 3, 2] # Example distribution
}
education_df = pd.DataFrame(education_data)

# 2. Languages and General Skills Data (Frequency or Importance Score)
languages_skills_data = {
    'Skill': ['Python', 'SQL', 'R', 'Machine Learning', 'Statistics', 'Communication', 'Problem Solving', 'Data Visualization', 'Teamwork', 'Critical Thinking'],
    'Frequency': [90, 85, 60, 95, 80, 70, 88, 75, 65, 78] # Example frequencies/importance
}
languages_skills_df = pd.DataFrame(languages_skills_data).sort_values(by='Frequency', ascending=False)

# 3. Specific Tools & Technologies Data (Frequency or Importance Score)
tools_tech_data = {
    'Tool/Technology': ['AWS', 'Azure', 'GCP', 'Spark', 'Hadoop', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'PostgreSQL', 'Docker', 'Git', 'Jupyter Notebooks'],
    'Frequency': [70, 50, 40, 60, 45, 75, 65, 90, 95, 92, 55, 60, 80, 85] # Example frequencies/importance
}
tools_tech_df = pd.DataFrame(tools_tech_data).sort_values(by='Frequency', ascending=False)

# --- Main Application ---
st.header(f"Analysis for: {job_title_placeholder}")
st.markdown("Below are visualizations based on typical requirements for this role.")

# Create columns for better layout
col1, col2 = st.columns([1, 1.5]) # Adjust ratios as needed

with col1:
    # --- 1. Education Level Pie Chart ---
    st.subheader("🎓 Education Level Distribution")
    if not education_df.empty:
        fig_edu = px.pie(education_df,
                         names='Level',
                         values='Percentage',
                         title='Typical Education Requirements',
                         color_discrete_sequence=px.colors.sequential.RdBu)
        fig_edu.update_traces(textposition='inside', textinfo='percent+label')
        fig_edu.update_layout(legend_title_text='Education Levels')
        st.plotly_chart(fig_edu, use_container_width=True)
    else:
        st.warning("No education data available to display.")

with col2:
    # --- 2. Languages and General Skills Bar Chart ---
    st.subheader("💻 Languages & General Skills")
    if not languages_skills_df.empty:
        fig_lang_skills = px.bar(languages_skills_df.head(10), # Display top 10
                                 x='Frequency',
                                 y='Skill',
                                 orientation='h',
                                 title='Top Languages & General Skills',
                                 labels={'Frequency': 'Relevance/Frequency Score', 'Skill': 'Language/Skill'},
                                 color='Frequency',
                                 color_continuous_scale=px.colors.sequential.Viridis)
        fig_lang_skills.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_lang_skills, use_container_width=True)
    else:
        st.warning("No language/skill data available to display.")

st.markdown("---")

# --- 3. Specific Tools & Technologies Bar Chart ---
st.subheader("🛠️ Specific Tools & Technologies")
if not tools_tech_df.empty:
    fig_tools_tech = px.bar(tools_tech_df.head(15), # Display top 15
                            x='Tool/Technology',
                            y='Frequency',
                            title='Key Tools & Technologies Mentioned',
                            labels={'Frequency': 'Relevance/Frequency Score', 'Tool/Technology': 'Tool/Technology'},
                            color='Frequency',
                            color_continuous_scale=px.colors.sequential.Plasma)
    fig_tools_tech.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_tools_tech, use_container_width=True)
else:
    st.warning("No tools/technology data available to display.")


st.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "This app visualizes hypothetical skill and education requirements for a job role. "
    "Replace the placeholder data with actual data from job descriptions for real insights."
)
st.sidebar.header("How to Use")
st.sidebar.markdown("""
1.  **Save this code** as a Python file (e.g., `job_analyzer.py`).
2.  **Open your terminal or command prompt.**
3.  **Navigate to the directory** where you saved the file.
4.  **Run the app** using the command: `streamlit run job_analyzer.py`
""")

# --- Example of how you might get data (conceptual) ---
# def extract_skills_from_description(job_description_text):
#     # This would be a complex function using NLP or regex
#     # For example, looking for keywords
#     education_keywords = {"bachelor": 0, "master": 0, "phd": 0}
#     skill_keywords = {"python": 0, "java": 0, "aws": 0, "azure": 0, "sql":0, "communication":0}
#     # ... parse text and update counts ...
#     # return education_data, skills_data, tools_data
#     pass

# if st.checkbox("Analyze a new Job Description (Conceptual)"):
#     job_desc = st.text_area("Paste Job Description Here")
#     if st.button("Analyze"):
#         if job_desc:
#             # edu_data, skill_data, tool_data = extract_skills_from_description(job_desc)
#             # Then update your DataFrames and re-plot
#             st.success("Analysis complete! (Conceptual - no actual processing done here)")
#         else:
#             st.error("Please paste a job description.")
