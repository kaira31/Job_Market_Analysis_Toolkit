import pandas as pd
import json
from collections import Counter

# Function to identify popular skills
def popular_skills(df):
    """
    Identifies the top 5 most frequently mentioned skills in a DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the 'skills' column.

    Returns:
        Series: A Pandas Series with the top 5 most common skills.

    Raises:
        KeyError: If the 'skills' column is missing.
    """
    if 'skills' not in df.columns:
        raise KeyError("The 'skills' column is missing.")

    return df['skills'].apply(lambda x: x if isinstance(x, str) else '').value_counts().head(5)


# Function to identify popular jobs
def popular_job(df):
    """
    Identifies the top 5 most common job titles in a DataFrame.

    Args:
        df (DataFrame): The DataFrame containing the 'Job Title' column.

    Returns:
        Series: A Pandas Series with the top 5 most common job titles.

    Raises:
        KeyError: If the 'Job Title' column is missing.
    """
    if 'Job Title' not in df.columns:
        raise KeyError("The 'Job Title' column is missing.")

    return df['Job Title'].value_counts().head(5)


# Function to count job postings based on company and state
def Job_Postings(df1, company=None, state=None):
    """
    Counts the number of job postings in the DataFrame, optionally filtered by company and state.

    Args:
        df1 (DataFrame): The DataFrame containing job postings.
        company (str, optional): The company to filter by (default is None).
        state (str, optional): The state to filter by (default is None).

    Returns:
        int: The count of job postings based on the specified filters.

    Raises:
        KeyError: If necessary columns are missing.
    """
    if 'Company' not in df1.columns or 'State' not in df1.columns:
        raise KeyError("Required columns 'Company' or 'State' are missing.")

    if company and state:
        filtered_data = df1[(df1['Company'] == company) & (df1['State'] == state)]
    elif company:
        filtered_data = df1[df1['Company'] == company]
    elif state:
        filtered_data = df1[df1['State'] == state]
    else:
        filtered_data = df1

    return len(filtered_data)


# Function to identify trending industries
def trending_industries(df):
    """
    Identifies the top 5 most common industries in the DataFrame.

    Args:
        df (DataFrame): The DataFrame containing 'Company Profile' data.

    Returns:
        Series: A Pandas Series with the top 5 most common industries.

    Raises:
        KeyError: If the 'Company Profile' column is missing.
        ValueError: If parsing JSON data fails.
    """
    if 'Company Profile' not in df.columns:
        raise KeyError("The 'Company Profile' column is missing.")

    def safe_load(json_str):
        try:
            return json.loads(json_str)  # Safely load JSON-like data
        except (json.JSONDecodeError, SyntaxError):
            return None  # Return None if parsing fails

    industry_series = df['Company Profile'].apply(lambda x: safe_load(x) if isinstance(x, str) else None)
    industry_series = industry_series.apply(lambda x: x['Industry'] if x else None)

    return industry_series.value_counts().head(5)  # Top 5 common industries


# Function to identify skills in demand
def skills_indemand(df1, company=None):
    """
    Identifies the top 5 most common words in the 'skills' column, excluding common stop words.
    Optionally filters by company.

    Args:
        df1 (DataFrame): The DataFrame containing skills data.
        company (str, optional): The company to filter by (default is None).

    Returns:
        list: A list of the top 5 most common words in the 'skills' column.

    Raises:
        KeyError: If the 'skills' column is missing.
    """
    if 'skills' not in df1.columns:
        raise KeyError("The 'skills' column is missing.")

    stop_words = {'and', 'example', 'etc'}  # Define common words to exclude

    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    all_skills = ' '.join(filtered_data['skills']).split()  # Split all skills into words
    filtered_skills = [word.lower() for word in all_skills if word.lower() not in stop_words]

    word_counts = Counter(filtered_skills)  # Count occurrences of each word
    most_common_words = word_counts.most_common(5)  # Top 5 most common words

    return [word for word, count in most_common_words]
