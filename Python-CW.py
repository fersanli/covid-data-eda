#!/usr/bin/env python
# coding: utf-8

# # Analysis of the Effect of Vaccinations and Restrictions on Covid-19 Cases and Hospital Admissions by Age in London

# ## Project Proposal

# ### 1 . Introduction & Context

# The Covid-19 pandemic is a major global health threat. SARS-CoV-2 virus was first seen in China towards the end of 2019. In the UK, first case was recorded in the end of January 2020. The first Covid-19 jab was administered on 8th December 2020. In those earlier days of the pandemic, age was determined to be the one of the main factors. After two waves, several restrictions and millions of vaccinations, today there's an apparent threat of the third wave which is predominantly propelled by the Delta variant.
# 
# Covid-19 is changing the world, it certainly has changed mine. I am interested in the dynamics of the pandemic, i.e. who is more affected, are the restrictions working, how effective are the vaccinations, what do new variants cause, etc. What would be more interesting is to relate geographically more with the outcome, hence the analysis is restricted to London.
# 
# In conclusion, the aim of this coursework is to analyze the effect of the restrictions and the vaccination program on the age distribution of Covid-19 cases.

# ### 2. Data

# Data is downloaded from London Datastore$^{[1]}$ of Greater London Authority, providing the key data for London from Public Health England (PHE) alongside related data published by NHS and Office of National Statistics (ONS).
# 
# The static links of the files are used therefore there's no need to store the files or download the files to retrieve new data. Since the data is conveniently available, web scraping is not needed. The size of the files are managable so a database schema is not setup either.
# 
# The consideration for choosing data includes if the key variables are available to appropriately identify the outcome and covariates. Data is sufficiently granular, contain historical information to analyze the changes from the start of the pandemic. The chosen data meet these criterias.
# 
# The data contains age data for cases, hospitalizationsm vaccinations, testing and restrictions data that relate to the aim of the report. The data files are in csv format to be converted to dataframes for processing.
# 
# The data is publicly available and anonymised.

# ### 3. Intro

# In[1]:


import numpy as np
import pandas as pd

# visualization
import plotly.graph_objects as go
import plotly.tools as tls
import plotly.offline as py


# In[2]:


# import data files
cases_by_age = pd.read_csv("https://data.london.gov.uk/download/coronavirus--covid-19--cases/d15e692d-5e58-4b6e-80f2-78df6f8b148b/phe_cases_age_london.csv")
vaccines_by_age = pd.read_csv("https://data.london.gov.uk/download/coronavirus--covid-19--cases/ae4d5fc9-5448-49a6-810f-910f7cbc9fd2/phe_vaccines_age_london_boroughs.csv")
admissions_by_age = pd.read_csv("https://data.london.gov.uk/download/coronavirus--covid-19--cases/ad037e43-0f09-473a-8d62-b576de380af6/phe_healthcare_admissions_age.csv")
restrictions = pd.read_csv("https://data.london.gov.uk/download/covid-19-restrictions-timeseries/ae1b5b4c-3b5c-471f-b3e5-ba4fbc3eced9/restrictions_daily.csv")
testing = pd.read_csv("https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=uniquePeopleTestedBySpecimenDateRollingSum&format=csv")


# In[3]:


# functions for plotting graphs
def one_variable_graph(df_name, date_column_name, value_column_name, graph_title, xaxis_title, yaxis_title):
    
    df = df_name.groupby(date_column_name).sum()
    df = df[[value_column_name]]
    df = df.sort_values(date_column_name, ascending=True).sort_index()
    data = go.Bar(x=df.index, y=df[value_column_name],marker_color="Blue")

    layout = go.Layout(dict(title=graph_title,
                            xaxis=dict(title = xaxis_title,
                                         color="darkBlue",
                                         showgrid=True,
                                         zeroline=True,
                                         showline=True,),
                            yaxis=dict(title = yaxis_title,
                                         color="darkBlue",
                                         showgrid=True,
                                         zeroline=True,
                                         showline=True,)))

    py.iplot(dict(data=data, layout=layout))


def two_variable_stacked_graph(df_name, date_column_name, value_column_name, legend_column_name, graph_title, xaxis_title, yaxis_title):

    df = df_name.groupby([legend_column_name,date_column_name]).sum()
    df = df.sort_values(date_column_name, ascending=True).sort_index()
    df = df[[value_column_name]]

    data_fig=[]
    for i,j in enumerate(df_name.eval(legend_column_name).unique()):
        data_fig.append('go.Bar(name="'+j+'",x=df.index.get_level_values(date_column_name), y=df.filter(like = "'+j+'", axis=0).loc[:value_column_name][value_column_name])')
        i+=1
    data_fig=list(map(eval, data_fig))

    fig = go.Figure(data=data_fig)
    fig.update_layout(barmode='stack', title_text=graph_title, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
    fig.show()
    
    
def two_variable_grouped_graph(df_name, date_column_name, value_column_name, legend_column_name, graph_title, xaxis_title, yaxis_title):

    df = df_name.groupby([legend_column_name,date_column_name]).sum()
    df = df.sort_values(date_column_name, ascending=True).sort_index()
    df = df[[value_column_name]]

    data_fig=[]
    for i,j in enumerate(df_name.eval(legend_column_name).unique()):
        data_fig.append('go.Bar(name="'+j+'",x=df.index.get_level_values(date_column_name), y=df.filter(like = "'+j+'", axis=0).loc[:value_column_name][value_column_name])')
        i+=1
    data_fig=list(map(eval, data_fig))

    fig = go.Figure(data=data_fig)
    fig.update_layout(barmode='group', title_text=graph_title, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
    fig.show()
    
    
def multi_value_stacked_graph(df_name, date_column_name, graph_title, xaxis_title, yaxis_title):
    df = df_name.groupby([date_column_name]).sum()
    df = df.sort_values(date_column_name, ascending=True).sort_index()

    data_fig=[]
    for i,j in enumerate(df_name.columns):
        if j == date_column_name:
            continue
        else:
            data_fig.append('go.Bar(name="'+j+'",x=df.index, y=df["'+j+'"])')
            i+=1
    data_fig=list(map(eval, data_fig))

    fig = go.Figure(data=data_fig)
    fig.update_layout(barmode='stack', title_text=graph_title, xaxis_title=xaxis_title, yaxis_title=yaxis_title)
    fig.show()


# ### 4. A peek at the data

# In[4]:


print('The shape of cases by age:', cases_by_age.shape)
print('The shape of admissions by age:', admissions_by_age.shape)
print('The shape of vaccines by age:', vaccines_by_age.shape)
print('The shape of restrictions:', restrictions.shape)
print('The shape of testing:', testing.shape)


# In[5]:


cases_by_age.head()


# In[6]:


admissions_by_age.head()


# In[7]:


vaccines_by_age.head()


# In[8]:


restrictions.head()


# In[9]:


testing.head()


# The admissions data is weekly whereas the others are daily. Decision on how to proceed will be taken on the next section.

# In[10]:


# age bands
print(cases_by_age.age_band.unique())
print(admissions_by_age.age.unique())
print(vaccines_by_age.age_band.unique())


# * The granularity of the age bands of cases and vaccinations are quite adequate, whereas it would be preferable if the adult portion (18-64 years) of the admissions data wasn't that large. 
# * There is an "unassigned" value in the cases by age dataframe. This will be investigated below in the dataframe specific section.

# In[11]:


# area names
print(cases_by_age.area_name.unique())
print(admissions_by_age.area_name.unique())
print(vaccines_by_age.area_name.unique())
print(testing.areaName.unique())


# Though it might be interesting to analyze the data by borough, the unique values of "area_name" columns in three dataframes shows us that the data is not fully available. More importantly, borough breakdown is not needed to satisfy the aim of this report. Therefore, area_name and area_code columns will be removed.

# ##### Cases by age

# In[12]:


cases_by_age.isnull().sum()


# In[13]:


# unassigned cases
print('Number of cases that are not assigned to an age band:', cases_by_age[cases_by_age['age_band'] == 'unassigned']['cases'].sum())
print('Total number of cases:', cases_by_age['cases'].sum())
unassigned_ratio = cases_by_age[cases_by_age['age_band'] == 'unassigned']['cases'].sum() / cases_by_age['cases'].sum()
unassigned_percent = "{:.2%}".format(unassigned_ratio)
print('The percentage of unassigned cases to total cases:',  unassigned_percent)


# In[14]:


cases_by_age_unassigned = cases_by_age[cases_by_age['age_band'] == 'unassigned']
one_variable_graph(cases_by_age_unassigned, 'date', 'cases', 'Unassigned Cases', 'Date', 'Number of Cases')


# The number of unassigned cases seem to be very small and they are well distributed throughout the dates. It is apparent that if they were to be dropped, it would have a negligible impact on the results. Therefore, they will be.

# In[15]:


one_variable_graph(cases_by_age, 'date', 'cases', 'Daily Cases', 'Date', 'Number of Cases')


# Looking at the data, daily data is too granular, and as discussed above the admissions data is weekly whereas the others are daily. For our purpose, weekly data would be sufficient and easier to read. Therefore, all daily data will be converted into weekly data in the transformations sections.

# ##### Admissions by age

# In[16]:


admissions_by_age.isnull().sum()


# In[17]:


two_variable_stacked_graph(admissions_by_age, 'week_ending', 'weekly_admissions', 'age', 'Weekly Admissions', 'Week ending with', 'Number of Admissions')


# ##### Vaccines by age

# In[18]:


vaccines_by_age.isnull().sum()


# In[19]:


two_variable_stacked_graph(vaccines_by_age, 'date', 'cum_doses', 'age_band', 'Vaccination by Age', 'Date', 'Number of Vaccinations (1st and 2nd doses combined)')


# There are too many age groups, they''ll be combined into fewer buckets.

# In[20]:


two_variable_stacked_graph(vaccines_by_age, 'date', 'cum_doses', 'dose', 'Vaccination by Dose', 'Date', 'Number of Vaccinations')


# In[21]:


two_variable_grouped_graph(vaccines_by_age, 'age_band', 'new_doses', 'dose', 'Vaccination by Dose', 'Age Bands', 'Number of Vaccinations')


# It's obvious that the second dose uptake decreases by age band. The number of doses taken by different age bands might play a crucial role when analyzing the effectivity of the vaccination program. This table is constructed using 'new_doses' column but it can be done with 'cum_doses' column as well, so we can remove the 'new_doses' column.

# ##### Restrictions

# In[22]:


restrictions.isnull().sum()


# In[23]:


restrictions.columns


# "Eat out to help out" is not a restriction, in the opposite it was a campaign to encourage public to eat in restaurants or cafes so that hospitality sector could get a boost. Therefore, the figures will be converted to -1 to emphasize it's the opposite of restriction.

# In[24]:


multi_value_stacked_graph(restrictions, 'date', 'Restrictions', 'Date', 'Restrictions')


# ##### Testing

# In[25]:


testing.isnull().sum()


# In[26]:


one_variable_graph(testing, 'date', 'uniquePeopleTestedBySpecimenDateRollingSum', 'Daily Testing', 'Date', 'Number of Tests')


# ### 5. Data transformations

# The transformations to be applied, where applicable are:
# 
# 
# * For all dataframes:
#     * Step 1: Converting daily data to weekly.
#     * Step 2: Keeping the columns to be used and renaming the columns to make more sense and match across dataframes.
#     * Step 3: Combining age groups into fewer buckets.
# 
# 
# * For restrictions dataframe: Reversing the sign of the "eat out to help out" column.
# * For cases by age dataframe: Dropping the rows including "unassigned" as age_band.

# ##### Cases by age

# In[27]:


# Step 1: Convert daily data to weekly
# Note: rolling_sum column contains 7 days rolling cases information, therefore this column will be kept to show weekly cases.

# Set the index to be aligned to (not needed for other dataframes)
filters_index = admissions_by_age.set_index(['week_ending'])

# Align indices
to_be_filtered_index = cases_by_age.set_index(['date'])

# Calculate & apply mask
weekly_cases_by_age = to_be_filtered_index[to_be_filtered_index.index.isin(filters_index.index)].reset_index()

# Step 2: Keep the columns to be used and remove the rest, rename the columns
weekly_cases_by_age = weekly_cases_by_age[['date','age_band','rolling_sum','population']]
weekly_cases_by_age = weekly_cases_by_age.rename(columns = {'rolling_sum' : 'weekly_cases', 'age_band':'age_band_original'}, inplace = False)

# Case specific step: Drop the rows including "unassigned" as age_band.
weekly_cases_by_age = weekly_cases_by_age[weekly_cases_by_age.age_band_original != 'unassigned']

# Step 3: Combine age groups into fewer buckets
# The new buckets will be as follows: 0 - 24 years, 25 - 39 years, 40 - 54 years, 55 - 69 years, 70+ years.

# Create a list of our conditions
conditions = []
for i,j in enumerate(weekly_cases_by_age.age_band_original.unique()):
    conditions.append("(weekly_cases_by_age['age_band_original'] == '" + j +"')")
    i+=1
conditions=list(map(eval, conditions))

# Create a list of the values we want to assign for each condition
values = ['0 - 24 years','0 - 24 years','0 - 24 years','0 - 24 years','0 - 24 years','25 - 39 years','25 - 39 years','25 - 39 years','40 - 54 years','40 - 54 years','40 - 54 years','55 - 69 years','55 - 69 years','55 - 69 years',
         '70+ years','70+ years','70+ years','70+ years','70+ years']

# Create a new column and assign values to it using our lists as arguments
weekly_cases_by_age['age_band'] = np.select(conditions, values)

# Remove age_band_original column
weekly_cases_by_age = weekly_cases_by_age[['date','age_band','weekly_cases','population']]

# Remove duplicate rows
weekly_cases_by_age[['weekly_cases', 'population']] = weekly_cases_by_age.groupby(['date','age_band'], as_index=False)[['weekly_cases', 'population']].transform('sum')
weekly_cases_by_age = weekly_cases_by_age.drop_duplicates()

weekly_cases_by_age.head()


# In[28]:


one_variable_graph(weekly_cases_by_age, 'date', 'weekly_cases', 'Weekly Cases', 'Date', 'Number of Cases')


# ##### Vaccinations by age

# In[29]:


# Step 1: Convert daily data to weekly
# Note: Cumulative vaccination data will be used, therefore cum_doses column will be used.

# Align indices
to_be_filtered_index = vaccines_by_age.set_index(['date'])

# Calculate & apply mask
weekly_vaccines_by_age = to_be_filtered_index[to_be_filtered_index.index.isin(filters_index.index)].reset_index()

# Step 2: Keep the columns to be used and remove the rest, rename the columns
weekly_vaccines_by_age = weekly_vaccines_by_age[['date','dose','age_band','cum_doses','population']]

# Remove duplicate rows
weekly_vaccines_by_age[['cum_doses', 'population']] = weekly_vaccines_by_age.groupby(['date','dose','age_band'], as_index=False)[['cum_doses', 'population']].transform('sum')
weekly_vaccines_by_age = weekly_vaccines_by_age.drop_duplicates()

# Step 3: Combine age groups into fewer buckets
# Note: The new buckets will be as follows: 0 - 24 years, 25 - 39 years, 40 - 54 years, 55 - 69 years, 70+ years.

# Create a list of our conditions
conditions = []
for i,j in enumerate(weekly_vaccines_by_age.age_band.unique()):
    conditions.append("(weekly_vaccines_by_age['age_band'] == '" + j +"')")
    i+=1
conditions=list(map(eval, conditions))

# Create a list of the values we want to assign for each condition
values = ['0 - 24 years','25 - 39 years','25 - 39 years','25 - 39 years','40 - 54 years','40 - 54 years','40 - 54 years','55 - 69 years','55 - 69 years','55 - 69 years',
         '70+ years','70+ years','70+ years']

# Create a new column and assign values to it using our lists as arguments
weekly_vaccines_by_age['age_band_new'] = np.select(conditions, values)

# Remove age_band_original column and rename the new column
weekly_vaccines_by_age = weekly_vaccines_by_age[['date','dose','age_band_new','cum_doses','population']]
weekly_vaccines_by_age = weekly_vaccines_by_age.rename(columns = {'age_band_new' : 'age_band'}, inplace = False)

# Remove duplicate rows
weekly_vaccines_by_age[['cum_doses', 'population']] = weekly_vaccines_by_age.groupby(['date','dose','age_band'], as_index=False)[['cum_doses', 'population']].transform('sum')
weekly_vaccines_by_age = weekly_vaccines_by_age.drop_duplicates()


weekly_vaccines_by_age.head()


# In[30]:


one_variable_graph(weekly_vaccines_by_age, 'date', 'cum_doses', 'Cumulative Vaccination Figures', 'Date', 'Number of Vaccinations (1st and 2nd dose combined)')


# ##### Admissions by age

# In[31]:


# Step 1: Not needed, data is already weekly.
# Step 2: Keep the columns to be used and remove the rest, rename the columns
weekly_admissions_by_age = admissions_by_age[['week_ending','age','weekly_admissions']]
weekly_admissions_by_age = weekly_admissions_by_age.rename(columns = {'week_ending': 'date', 'age': 'age_band_original'}, inplace = False)

# Step 3: Combine age groups into fewer buckets
# Note: Unfortunately, the age groups of this dataset doesn't match the other datasets, and is not granular enough.
# Note: The new buckets will be as follows: 0 - 17 years, 18 - 64 years, 65+ years.

# Create a list of our conditions
conditions = []
for i,j in enumerate(weekly_admissions_by_age.age_band_original.unique()):
    conditions.append("(weekly_admissions_by_age['age_band_original'] == '" + j +"')")
    i +=1
conditions=list(map(eval, conditions))

# Create a list of the values we want to assign for each condition
values = ['0 - 17 years','18 - 64 years','0 - 17 years','65+ years','65+ years']

# Create a new column and assign values to it using our lists as arguments
weekly_admissions_by_age['age_band'] = np.select(conditions, values)

# Remove age_band_original column
weekly_admissions_by_age = weekly_admissions_by_age[['date','age_band','weekly_admissions']]

# Remove duplicate rows
weekly_admissions_by_age[['weekly_admissions']] = weekly_admissions_by_age.groupby(['date','age_band'], as_index=False)[['weekly_admissions']].transform('sum')

weekly_admissions_by_age = weekly_admissions_by_age.drop_duplicates()


# In[32]:


one_variable_graph(weekly_admissions_by_age, 'date', 'weekly_admissions', 'Weekly Hospital Admissions', 'Date', 'Number of Admissions')


# ##### Restrictions

# In[33]:


# Step 1: Convert daily data to weekly
# When converting to daily, some data may be lost due to some restrictions starting within the week, however this is negligible for our purpose.

# Align indices
to_be_filtered_index = restrictions.set_index(['date'])

# Calculate & apply mask
weekly_restrictions = to_be_filtered_index[to_be_filtered_index.index.isin(filters_index.index)].reset_index()

# Case specific step: Reverse the sign of the "eat out to help out" column
weekly_restrictions['eat_out_to_help_out'] = weekly_restrictions['eat_out_to_help_out'] * -1

# Step 2 and 3 are not applicable.

weekly_restrictions.head()


# In[34]:


multi_value_stacked_graph(weekly_restrictions, 'date', 'Restrictions', 'Date', 'Restrictions')


# ##### Testing

# In[35]:


# Step 1: Convert daily data to weekly
# Note: uniquePeopleTestedBySpecimenDateRollingSum field already includes rolling 7 day figures.

# Align indices
to_be_filtered_index = testing.set_index(['date'])

# Calculate & apply mask
weekly_testing = to_be_filtered_index[to_be_filtered_index.index.isin(filters_index.index)].reset_index()

# Step 2: Keep the columns to be used and remove the rest, rename the columns
weekly_testing = weekly_testing[['date','uniquePeopleTestedBySpecimenDateRollingSum']]
weekly_testing = weekly_testing.rename(columns = {'uniquePeopleTestedBySpecimenDateRollingSum': 'weekly_PCR_tests'}, inplace = False)

# Step 3 is not applicable.

weekly_testing.head()


# In[36]:


one_variable_graph(weekly_testing, 'date', 'weekly_PCR_tests', 'Weekly PCR Tests', 'Date', 'Number of PCR Tests')


# ### 6. Limitations

# * The age bands of admissions dataset is not optimal. 18 - 64 years section is very large. The data will be used as is, because despite the low granularity, the dataset will be sufficient for our purpose.

# ### 7. Conclusion and Future Work

# The data required to analyze the effect of the restrictions and the vaccination program on the age distribution of Covid-19 cases and hospitalizations in London are modified and prepared for analysis and they are fit for purpose.
# 
# The rate of cases (cases per a certain population i.e. 100K) and the rate of hospitalizations will be calculated and evaluated against vaccinations data to see the changes between age bands. This will be quite instrumental when analyzing if the link between cases and hospitalizations is broken due to vaccinations. Restrictions will be brought into the picture and their relation with age bands (i.e. school closure is aimed at the young population whereas WFH or pub closure are aimed at the adult population) will be investigated. The vaccine uptake per age band will be calculated and its correlation with the rate of cases and the rate of hospitalization will be investigated.
# 
# Therefore, following research questions will be attempted to be answered:
# * Did the vaccination program and the restrictions cause the change in the age group distribution of Covid-19 cases?
# * Is the lower age group dominance of the new cases caused by low vaccine uptake?
# 
# Additionally, utilising more advanced techniques, the data can be modelled to predict the future number of cases and to evaluate and recommend restriction options to flatten the curve.

# ### 8. References

# [1] London Datastore, https://data.london.gov.uk/

# In[ ]:




