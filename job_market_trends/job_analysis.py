# Import the necessary modules and functions
import re  # For regular expressions


import re

# Function to extract salary ranges and convert to numerical values
def extract_salary(salary_str):
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
    # Apply salary extraction and drop NaN in max_salary
    df['min_salary'], df['max_salary'] = zip(*df['Salary Range'].apply(extract_salary)) 
    df = df.dropna(subset=['max_salary'])
    
    # Get the top 5 jobs with the highest maximum salary
    return df.nlargest(10, 'max_salary')[['Job Title', 'max_salary']]


def average_salary(df1=None, company=None):
    data = df1
    # Filter DataFrame if company is specified
    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    # Calculate average salary
    average_salary = filtered_data['Salary'].mean()

    return average_salary

def median_salary(df1=None, company=None):
    df = df1
    # Filter DataFrame if company is specified
    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    # Calculate average salary
    median_salary = filtered_data['Salary'].median()

    return median_salary

def mode_salary(df1=None, central_tendency=None, company=None):
    df = df1
    ct = central_tendency
    # Filter DataFrame if company is specified
    if company:
        filtered_data = df1[df1['Company'] == company]
    else:
        filtered_data = df1

    # Calculate central tendency of salary
    if ct == 'mean':
        result = filtered_data['Salary'].mean()
    elif ct == 'median':
        result = filtered_data['Salary'].median()
    elif ct == 'mode':
        result = filtered_data['Salary'].mode().iloc[0]  # Mode may return multiple values, so we select the first one

    return result