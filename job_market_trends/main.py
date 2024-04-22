import pandas as pd
from job_analysis import high_paying_job

from trend_analysis import popular_skills, trending_industries, popular_job, Job_Postings, trending_industries, skills_indemand
from job_analysis import extract_salary, average_salary, median_salary, mode_salary

from company_insights import company_info, trending_skill, company_type, location_type, company_size_distribution, industry_specialization_by_location
from company_insights import gender_ratio, work_type, benefits


# Load the data
df = pd.read_csv("df/job_data.csv")  

df1 = pd.read_csv("df1/Final_data.csv")

# Apply salary extraction
df['min_salary'], df['max_salary'] = zip(*df['Salary Range'].apply(extract_salary))

# Remove duplicates and NaN values
df = df.dropna(subset=['max_salary'])  # Remove NaN in max_salary
df = df.drop_duplicates(subset=['Job Title', 'Salary Range'])  # Remove duplicates

# Call functions to perform analysis
print("\n--- Popular Jobs ---")
print(popular_job(df))  # Top 5 popular jobs

print("\n--- High-Paying Jobs ---")
print(high_paying_job(df))  # Top 10 high-paying jobs

print("\n--- Popular Skills ---")
print(popular_skills(df))  # Top 5 popular skills

print("\n--- Trending Industries ---")
print(trending_industries(df))  # Top 5 trending industries

print("\n--- Job Postings---")
print(Job_Postings(df1,None,'Ohio')) 

print("\n--- Skills in demand ---")
print(skills_indemand(df1)) 

print("\n--- Average Salary ---")
print(average_salary(df1,'Otis Worldwide')) 

print("\n--- Median Salary ---")
print(median_salary(df1,'Otis Worldwide')) 

print("\n--- Mode Salary ---")
print(mode_salary(df1,'median','Fidelity Investments, Inc.')) 

print("\n--- Company Info ---")
print(company_info(df,406587759130697))

print("\n--- Trending Skills ---")
print(trending_skill(df1))

print("\n--- Company Type ---")
print(company_type(df1, 406587759130697))

print("\n--- Loaction Type ---")
print(location_type(df1, "Douglas"))

print("\n--- Company Size Distribution ---")
print(company_size_distribution(df1))

print("\n--- Industry Specialization by Location ---")
print(industry_specialization_by_location(df1))

print("\n--- Work Type ---")
print(work_type(df1,'Intern'))

print("\n--- Benefits ---")
print(benefits(df1,None,'Otis Worldwide'))

print("\n--- Gender Ratio ---")
print(gender_ratio(df1,"Casey's General Stores"))