# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 21:31:11 2021

@author: Aman Rajput
"""

import pandas as pd
import datetime
now=datetime.datetime.now()
year=now.year
print(year)
df=pd.read_csv('glassdoor_jobs.csv')

# parsing  Salary
df['Hourly']=df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['Employer Provided']=df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df=df[df['Salary Estimate']!='-1']
salary=df['Salary Estimate'].apply(lambda x:x.split('(')[0])
kd=salary.apply(lambda x:x.replace('$','').replace('K',''))

minus_hr=kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))
df['Min Salary']=minus_hr.apply(lambda x: int(x.split('-')[0]))
df['Max Salary']=minus_hr.apply(lambda x: int(x.split('-')[1]))

# hourly wage to annual

df['Min Salary']=df.apply(lambda x:x['Min Salary']*2 if x.Hourly==1 else x['Min Salary'], axis=1)
df['Max Salary']=df.apply(lambda x:x['Max Salary']*2 if x.Hourly==1 else x['Max Salary'], axis=1)

df['Avg Salary']=(df['Min Salary']+df['Max Salary'])/2

#company name text only
df['Company_Name']=df.apply(lambda x: x['Company Name'] if x['Rating'  ]<0 else x['Company Name'][:-3],axis=1)
df['Company_Name']=df['Company_Name'].apply(lambda x:x.replace('<','').replace('>',""))

#company age
df['Company Age']=df.Founded.apply(lambda x: x if x<1 else year-x)

#state field
df['job_state']=df.Location.apply(lambda x:x.split(',')[1])
df['job_state']=df['job_state'].apply(lambda x:x.strip() if x.strip().lower() !='los angeles' else "CA")
#Job is in heaquarter
df['same_state']=df.apply(lambda x:1 if x.Location== x.Headquarters else 0,axis=1)

#parsing of job description (python,spark etc)
df.columns
#python
df['python_yn']=df['Job Description'].apply(lambda x:1 if 'python' in x.lower() else 0)
df['python_yn'].value_counts()
#spark
df['spark_yn']=df['Job Description'].apply(lambda x:1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()
#R studio
df['R_yn']=df['Job Description'].apply(lambda x:1 if 'r-studio' in x.lower() or 'r studio' in x.lower() else 0)
df.R_yn.value_counts()
#aws
df['AWS']=df['Job Description'].apply(lambda x:1 if 'aws' in x.lower() else 0)
df.AWS.value_counts()
#excel
df['Excel']=df['Job Description'].apply(lambda x:1 if 'aws' in x.lower() else 0)
df.Excel.value_counts()

#tableau
df['Tableau']=df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df.Tableau.value_counts()

#Drop first column
df.columns
df=df.drop(['Unnamed: 0'],axis=1)


#define function to simplify the Job Title

def title_simplified(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'na'
    
#define function for senior and junior level 
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr.' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'junior'
    else:
        return 'na'
    
df['job_simp']=df['Job Title'].apply(title_simplified)
df['job_simp'].value_counts()

df['seniority']=df['Job Title'].apply(seniority)
df['seniority'].value_counts()


# Job description length
df['desc_len']=df['Job Description'].apply(lambda x: len(x))

#Competitor Count

df['num_com']=df['Competitors'].apply(lambda x:len(x.split(','))if x!='-1' else 0)


df.columns

df.to_csv('salary_clean.csv',index=False)