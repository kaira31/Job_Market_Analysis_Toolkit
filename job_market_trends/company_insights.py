import pandas as pd

def company_info(df1, company_id):
    """
    Returns company information for a given company ID from a DataFrame.

    Args:
    df (DataFrame): The DataFrame containing company data.
    company_id (int or str): The ID of the company to retrieve information for.

    Returns:
    DataFrame: A DataFrame containing the rows matching the given company ID.
    """
    comp_info = df1[df1['Job Id'] == company_id]
    return comp_info


def trending_skill(df1):
    """
    Finds the most demanded skill across companies in a DataFrame.

    Args:
    df (DataFrame): The DataFrame containing skills data in the 'skills' column.

    Returns:
    str: The most frequently occurring skill.

    Raises:
    ValueError: If the 'skills' column is missing or empty.
    """
    if 'skills' not in df1.columns or df1['skills'].empty:
        raise ValueError("The 'skills' column is missing or empty.")
    trending_skill = df1['skills'].value_counts().idxmax()
    return trending_skill

def company_type(df1, company_id):
    """
    Returns the type of company by company ID from a DataFrame.

    Args:
    df (DataFrame): The DataFrame containing company data.
    company_id (int or str): The ID of the company for which to retrieve the sector.

    Returns:
    str: The sector of the company corresponding to the given company ID.

    Raises:
    KeyError: If the 'Sector' column is missing from the DataFrame.
    ValueError: If no entries match the provided company ID.
    """
    if 'Sector' not in df1.columns:
        raise KeyError("The 'Sector' column is missing from the DataFrame.")
    filtered_df = df1[df1['Job Id'] == company_id]
    if filtered_df.empty:
        raise ValueError(f"No entries found for company ID {company_id}.")
    company_type = filtered_df['Sector'].iloc[0]
    return company_type

def location_type(df1, location):
    """
    Analyzes and returns the distribution of industries prevalent in a given location from a DataFrame.

    Args:
    df (DataFrame): The DataFrame containing company data with 'location' and 'Industry' columns.
    location (str): The location to analyze for industry distribution.

    Returns:
    Series: A Pandas Series showing the count of each industry in the given location.

    Raises:
    KeyError: If the 'location' or 'Industry' columns are missing from the DataFrame.
    ValueError: If no entries are found for the specified location.
    """
    if 'location' not in df1.columns or 'Industry' not in df1.columns:
        raise KeyError("Required columns 'location' or 'Industry' are missing from the DataFrame.")
    location_data = df1[df1['location'] == location]['Industry']
    if location_data.empty:
        raise ValueError(f"No entries found for location '{location}'.")
    location_types = location_data.value_counts()
    return location_types

def company_size_distribution(df1, industry=None, location=None):
    """
    Returns a distribution of company sizes, optionally filtered by industry or location.

    Args:
    df (DataFrame): DataFrame with columns 'Company Size', 'Industry', and 'location'.
    industry (str, optional): Filter companies by industry.
    location (str, optional): Filter companies by location.

    Returns:
    Series: A Pandas Series showing the count of companies by size.

    Raises:
    KeyError: If necessary columns are missing.
    """
    required_columns = {'Company Size', 'Industry', 'location'}
    if not required_columns.issubset(df1.columns):
        raise KeyError(f"DataFrame must include the columns: {required_columns}")

    query = ' & '.join([f"{col} == '{val}'" for col, val in (('Industry', industry), ('location', location)) if val])
    company_sizes = df1.query(query)['Company Size'] if query else df1['Company Size']
    if company_sizes.empty:
        raise ValueError("No matching entries found.")
    return company_sizes.value_counts()


def industry_specialization_by_location(df1):
    """
    Identifies predominant industries in each location.

    Args:
    df (DataFrame): DataFrame with columns 'location' and 'Industry'.

    Returns:
    DataFrame: A DataFrame with each location and the most prevalent industry.

    Raises:
    KeyError: If 'location' or 'Industry' columns are missing.
    """
    if 'location' not in df1.columns or 'Industry' not in df1.columns:
        raise KeyError("DataFrame must include 'location' and 'Industry' columns.")
    dominant_industries = df1.groupby('location')['Industry'].apply(lambda x: x.mode()[0]).reset_index(name='Dominant Industry')
    return dominant_industries

