import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to retrieve company information by company ID
def company_info(df1, company_id):
    """
    Returns information for a given company ID from the DataFrame.

    Args:
        df1 (DataFrame): The DataFrame containing company data.
        company_id (int or str): The ID of the company to retrieve information for.

    Returns:
        DataFrame: Rows corresponding to the given company ID.

    Raises:
        ValueError: If no matching company ID is found.
    """
    comp_info = df1[df1['Job Id'] == company_id]
    if comp_info.empty:
        raise ValueError(f"No matching company ID found: {company_id}.")
    return comp_info


# Function to find the most demanded skill across companies
def trending_skill(df1):
    """
    Finds the most demanded skill across companies in a DataFrame.

    Args:
        df1 (DataFrame): The DataFrame containing skills data.

    Returns:
        str: The most frequently occurring skill.

    Raises:
        ValueError: If the 'skills' column is missing or empty.
    """
    if 'skills' not in df1.columns or df1['skills'].empty:
        raise ValueError("The 'skills' column is missing or empty.")
    return df1['skills'].value_counts().idxmax()


# Function to get the type of company by company ID
def company_type(df1, company_id):
    """
    Returns the type of company (sector) for a given company ID.

    Args:
        df1 (DataFrame): The DataFrame containing company data.
        company_id (int or str): The ID of the company to retrieve the sector for.

    Returns:
        str: The sector of the company.

    Raises:
        KeyError: If the 'Sector' column is missing.
        ValueError: If no matching company ID is found.
    """
    if 'Sector' not in df1.columns:
        raise KeyError("The 'Sector' column is missing from the DataFrame.")
    filtered_df = df1[df1['Job Id'] == company_id]
    if filtered_df.empty:
        raise ValueError(f"No entries found for company ID: {company_id}.")
    return filtered_df['Sector'].iloc[0]


# Function to analyze industry types in a given location
def location_type(df1, location):
    """
    Analyzes the distribution of industries in a specified location.

    Args:
        df1 (DataFrame): The DataFrame containing company data.
        location (str): The location to analyze.

    Returns:
        Series: A Pandas Series with the count of each industry in the specified location.

    Raises:
        KeyError: If 'location' or 'Industry' columns are missing.
        ValueError: If no matching entries are found for the specified location.
    """
    if 'location' not in df1.columns or 'Industry' not in df1.columns:
        raise KeyError("Required columns 'location' or 'Industry' are missing.")
    location_data = df1[df1['location'] == location]['Industry']
    if location_data.empty:
        raise ValueError(f"No entries found for location: {location}.")
    return location_data.value_counts()


# Function to analyze company size distribution
def company_size_distribution(df1, industry=None, location=None):
    """
    Returns the distribution of company sizes, optionally filtered by industry or location.

    Args:
        df1 (DataFrame): DataFrame with company-related data.
        industry (str, optional): The industry to filter by.
        location (str, optional): The location to filter by.

    Returns:
        Series: A Pandas Series with the count of companies by size.

    Raises:
        KeyError: If the required columns are missing.
        ValueError: If no matching entries are found.
    """
    required_columns = {'Company Size', 'Industry', 'location'}
    if not required_columns.issubset(df1.columns):
        raise KeyError("The DataFrame must contain 'Company Size', 'Industry', and 'location'.")
    
    query = ' & '.join([f"{col} == '{val}'" for col, val in (('Industry', industry), ('location', location)) if val])
    company_sizes = df1.query(query)['Company Size'] if query else df1['Company Size']
    
    if company_sizes.empty:
        raise ValueError("No matching entries found.")
    
    return company_sizes.value_counts()


# Function to identify industry specialization by location
def industry_specialization_by_location(df1):
    """
    Identifies the most prevalent industry in each location from the DataFrame.

    Args:
        df1 (DataFrame): DataFrame with 'location' and 'Industry' columns.

    Returns:
        DataFrame: A DataFrame with the most prevalent industry for each location.

    Raises:
        KeyError: If 'location' or 'Industry' columns are missing.
    """
    if 'location' not in df1.columns or 'Industry' not in df1.columns:
        raise KeyError("Required columns 'location' or 'Industry' are missing.")
    
    dominant_industries = df1.groupby('location')['Industry'].apply(lambda x: x.mode()[0]).reset_index(name='Dominant Industry')
    
    return dominant_industries


# Function to filter records based on work type and company
def work_type(df1, work_type, company=None):
    """
    Filters records based on work type and optionally by company.

    Args:
        df1 (DataFrame): The DataFrame with 'Company' and 'Work Type'.
        work_type (str): The work type to filter by.
        company (str, optional): The company to further filter by.

    Returns:
        DataFrame: A DataFrame containing filtered records.

    Raises:
        ValueError: If the required arguments are not provided.
    """
    if df1 is None or work_type is None:
        raise ValueError("Please provide 'df1' and 'work_type'.")

    filtered_data = df1[df1['Work Type'] == work_type]

    if company is not None:
        filtered_data = filtered_data[filtered_data['Company'] == company]

    return filtered_data[['Company', 'Work Type', 'Role']]


# Function to analyze benefits data
def benefits(df1, benefits=None, company=None):
    """
    Analyzes benefits data from the DataFrame.

    Args:
        df1 (DataFrame): DataFrame containing benefits data.
        benefits (str, optional): Name of the benefits to filter by.
        company (str, optional): The company to further filter by.

    Returns:
        list or Series: Depending on the inputs, this function returns:
                        - A list of the top 5 repeated benefits.
                        - A Series with companies where the benefits contain the specified benefits.
                        - A list of the top 5 benefits for a given company.

    Raises:
        ValueError: If 'df1' is not provided.
    """
    if df1 is None:
        raise ValueError("Please provide a DataFrame.")

    if benefits is None and company is None:
        return df1['Benefits'].str.split(', ').explode().value_counts().head(5).index.tolist()
    
    elif benefits is not None:
        return df1[df1['Benefits'].str.contains(benefits)]['Company']
    
    elif company is not None:
        return df1[df1['Company'] == company]['Benefits'].str.split(', ').explode().value_counts().head(5).index.tolist()
    

import seaborn as sns
import matplotlib.pyplot as plt

def gender_ratio(df1, company=None):
    """
    Visualize the gender preferences ratio from the provided DataFrame.

    Args:
        df1 (DataFrame): The DataFrame containing gender preference data.
        company (str, optional): The company name to filter the data (default is None).

    Returns:
        None: Displays a bar chart showing the distribution of gender preferences.

    Raises:
        ValueError: If 'df1' is not provided.
    """
    if df1 is None:
        raise ValueError("Please provide a DataFrame.")

    sns.set_palette("pastel")  # Set color palette for the plot

    if company is None:
        # Plot the count of unique values in the 'Preference' column
        preferences_counts = df1['Preference'].value_counts()
        preferences_counts.plot(kind='bar')
        plt.title('Gender Preferences Ratio')
        plt.xlabel('Gender Preferences')
        plt.ylabel('Count')
        plt.show()
    else:
        # Filter by company and plot the count of unique values in the 'Preference' column
        filtered_data = df1[df1['Company'] == company]
        preferences_counts = filtered_data['Preference'].value_counts()
        preferences_counts.plot(kind='bar')
        plt.title(f'Gender Preferences Ratio for {company}')
        plt.xlabel('Gender Preferences')
        plt.ylabel('Count')
        plt.show()

