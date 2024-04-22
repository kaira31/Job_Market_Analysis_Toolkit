import re  # For regular expressions

# Function to extract salary ranges and convert to numerical values
def extract_salary(salary_str):
    """
    Extracts minimum and maximum salaries from a given salary range string.

    Args:
        salary_str (str): A string representing a salary range (e.g., "$59K-$99K").

    Returns:
        tuple: A tuple containing the minimum and maximum salaries in thousands.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(salary_str, str):
        raise TypeError("Input must be a string.")

    numbers = re.findall(r'\d+', salary_str)  # Extract all numbers in the salary range
    if len(numbers) >= 2:
        min_salary = float(numbers[0]) * 1000  # Convert 'K' to thousands
        max_salary = float(numbers[1]) * 1000
    elif len(numbers) == 1:
        min_salary = max_salary = float(numbers[0]) * 1000
    else:
        min_salary = max_salary = None  # Handle cases with no valid numbers
    return min_salary, max_salary


# Function to find high-paying jobs
def high_paying_job(df):
    """
    Identifies the top 10 high-paying jobs based on the maximum salary.

    Args:
        df (DataFrame): The DataFrame containing job data.

    Returns:
        DataFrame: A DataFrame with the top 10 high-paying jobs and their maximum salaries.

    Raises:
        KeyError: If 'Salary Range' is missing.
        ValueError: If no valid salary data is found.
    """
    if 'Salary Range' not in df.columns:
        raise KeyError("The 'Salary Range' column is missing.")
    
    df['min_salary'], df['max_salary'] = zip(*df['Salary Range'].apply(extract_salary)) 
    df = df.dropna(subset=['max_salary'])  # Drop NaN in max_salary
    
    return df.nlargest(10, 'max_salary')[['Job Title', 'max_salary']]


# Function to calculate average salary
def average_salary(df1, company=None):
    """
    Calculates the average salary, optionally filtered by company.

    Args:
        df1 (DataFrame): The DataFrame containing salary data.
        company (str, optional): The company to filter by (default is None).

    Returns:
        float: The average salary.

    Raises:
        KeyError: If 'Salary' column is missing.
    """
    if 'Salary' not in df1.columns:
        raise KeyError("The 'Salary' column is missing.")

    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    return filtered_data['Salary'].mean()


# Function to calculate median salary
def median_salary(df1, company=None):
    """
    Calculates the median salary, optionally filtered by company.

    Args:
        df1 (DataFrame): The DataFrame containing salary data.
        company (str, optional): The company to filter by (default is None).

    Returns:
        float: The median salary.

    Raises:
        KeyError: If 'Salary' column is missing.
    """
    if 'Salary' not in df1.columns:
        raise KeyError("The 'Salary' column is missing.")

    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    return filtered_data['Salary'].median()


# Function to calculate mode salary
def mode_salary(df1, central_tendency, company=None):
    """
    Calculates the mode, median, or mean salary, optionally filtered by company.

    Args:
        df1 (DataFrame): The DataFrame containing salary data.
        central_tendency (str): The central tendency to calculate ('mean', 'median', 'mode').
        company (str, optional): The company to filter by (default is None).

    Returns:
        float: The calculated central tendency value.

    Raises:
        ValueError: If the specified central tendency is not recognized.
        KeyError: If 'Salary' column is missing.
    """
    if 'Salary' not in df1.columns:
        raise KeyError("The 'Salary' column is missing.")

    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    if central_tendency == 'mean':
        result = filtered_data['Salary'].mean()
    elif central_tendency == 'median':
        result = filtered_data['Salary'].median()
    elif central_tendency == 'mode':
        result = filtered_data['Salary'].mode().iloc[0]  # Mode may return multiple values
    else:
        raise ValueError("Unrecognized central tendency: choose 'mean', 'median', or 'mode'.")

    return result
