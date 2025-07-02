import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('/home/yusse/Coding/SkillCheck/dataset/cleaned_job_postings.csv')
        return df
    except FileNotFoundError:
        st.error("Error: cleaned_job_postings.csv not found at the specified path. Please ensure the file exists.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

# Function to get the most common items from a series of comma-separated strings
def get_most_common(series, top_n=20, col_name='Skill/Tool/Language'):
    series = series.dropna()
    all_items = [item.strip() for sublist in series.str.split(',') for item in sublist]
    return pd.DataFrame(Counter(all_items).most_common(top_n), columns=[col_name, 'Count'])

# Function to plot a bar chart
def plot_bar_chart(df, title, x, y):
    fig = px.bar(df, x=x, y=y, title=title, orientation='h')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(layout="wide")
    st.title("SKillCheck")

    df = load_data()

    if df is not None:
        with st.expander("Data Preview and Understanding"):
            st.write("Here's a preview of the dataset:")
            st.dataframe(df.head())
            st.write("Columns:", df.columns.tolist())
            st.write("Number of postings:", len(df))


        st.header("Overall Distribution:")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Top Coding Languages:")
            if 'Languages' in df.columns:
                common_languages = get_most_common(df['Languages'], 10, 'Language')
                plot_bar_chart(common_languages, "Most Common Coding Languages", 'Count', 'Language')
            else:
                st.warning("'Languages' column not found.")

        with col2:
            st.subheader("Top General Skills:")
            if 'Skills' in df.columns:
                common_skills = get_most_common(df['Skills'], 20, 'Skill')
                plot_bar_chart(common_skills, "Most Common Skills", 'Count', 'Skill')
            else:
                st.warning("'Skills' column not found.")

        with col3:
            st.subheader("Top Tools:")
            if 'Tools' in df.columns:
                common_tools = get_most_common(df['Tools'], 20, 'Tool')
                plot_bar_chart(common_tools, "Most Common Tools", 'Count', 'Tool')
            else:
                st.warning("'Tools' column not found.")


        # --- Role-Specific Analysis ---
        st.header("Role-Specific Analysis")
        if 'Job Title' in df.columns:
            roles = df['Job Title'].unique()
            selected_role = st.selectbox("Select a Job Role to analyze", roles)

            if selected_role:
                role_df = df[df['Job Title'] == selected_role]
                st.subheader(f"Analysis for: {selected_role}")

                col_role1, col_role2, col_role3 = st.columns(3)

                with col_role1:
                    st.subheader("Top Skills")
                    if 'Skills' in role_df.columns:
                        role_skills = get_most_common(role_df['Skills'], 5, col_name='Skill')
                        plot_bar_chart(role_skills, f"Top 5 Skills for {selected_role}", 'Count', 'Skill')
                    else:
                        st.warning("'Skills' column not found.")

                with col_role2:
                    st.subheader("Top Tools")
                    if 'Tools' in role_df.columns:
                        role_tools = get_most_common(role_df['Tools'], 5, col_name='Tools')
                        plot_bar_chart(role_tools, f"Top 5 Tools for {selected_role}", 'Count', 'Tools')
                    else:
                        st.warning("'Tools' column not found.")

                with col_role3:
                    st.subheader("Top Languages")
                    if 'Languages' in role_df.columns:
                        role_languages = get_most_common(role_df['Languages'], 3, col_name='Languages')
                        plot_bar_chart(role_languages, f"Top 3 Languages for {selected_role}", 'Count', 'Languages')
                    else:
                        st.warning("'Languages' column not found.")
        else:
            st.warning("'Job Title' column not found for role-specific analysis.")


if __name__ == '__main__':
    main()