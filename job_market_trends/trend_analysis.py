# Function to identify popular skills
def popular_skills(df):
    # Extract skills and count their occurrences
    return df['skills'].apply(lambda x: x if isinstance(x, str) else '').value_counts().head(5)

# Function to identify popular jobs
def popular_job(df):
    return df['Job Title'].value_counts().head(5)  # Top 5 most common job titles


def Job_Postings(df1=None, company=None, state=None):
    df1=df1
    company=company
    state=state
# Filter DataFrame based on company and state if provided
    if company is not None and state is not None:
        filtered_data = df1[(df1['Company'] == company) & (df1['State'] == state)]
    elif company is not None:
        filtered_data = df1[df1['Company'] == company]
    elif state is not None:
        filtered_data = df1[df1['State'] == state]
    else:
        filtered_data = df1

    # Count the number of job postings
    count = len(filtered_data)

    return count

import json  # For JSON parsing
import pandas as pd

def trending_industries(df):
    def safe_load(json_str):
        # Safely load JSON-like string
        try:
            return json.loads(json_str)  # Use JSON parsing
        except (json.JSONDecodeError, SyntaxError):
            return None  # Return None if parsing fails
    
    # Apply the safe_load function to 'Company Profile'
    industry_series = df['Company Profile'].apply(lambda x: safe_load(x) if isinstance(x, str) else None)
    
    # Extract the 'Industry' key, handling errors gracefully
    industry_series = industry_series.apply(lambda x: x['Industry'] if x else None)
    
    # Return the top 5 most common industries
    return industry_series.value_counts().head(5)  # Top 5 common industries



from collections import Counter

def skills_indemand(df1, company=None):
    """
    Return the 5 most repeated words in the 'skills' column of the DataFrame, excluding common words.
    If company is specified, filter records based on the company name.

    Args:
    - data: DataFrame containing job postings data
    - company: (Optional) Company name to filter job postings

    Returns:
    - List of the 5 most repeated words in the 'skills' column (excluding common words)
    """
    # Define common words to exclude
    stop_words = {'and', 'example', 'etc'}  # Add more common words as needed

    # Filter DataFrame based on company if provided
    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    # Concatenate all skills into a single string and split into words
    all_skills = ' '.join(filtered_data['skills']).split()

    # Remove stop words
    filtered_skills = [word for word in all_skills if word.lower() not in stop_words]

    # Count the occurrences of each word
    word_counts = Counter(filtered_skills)

    # Get the 5 most common words
    most_common_words = word_counts.most_common(5)

    # Extract only the words from the tuples
    most_common_words = [word for word, count in most_common_words]

    return most_common_words
