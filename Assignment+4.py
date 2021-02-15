
# coding: utf-8

# ---
#
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
#
# ---

# In[ ]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments -
#you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet,
#or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related.
#And of course, the discussion forums are open for interaction with your peers and the course staff.
#
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
#
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
#
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
#
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[ ]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[ ]:


def get_list_of_university_towns():
    handle = open('university_towns.txt')
    towns = handle.read()
    towns = towns.split('\n')
    lst = []
    for i in towns:
        if '[edit]' in i:
            i = i.strip('[edit]')
            key = i
        if '(' in i:
            i = i.split('(')
            value = i[0]
            pair = [key, value]
            lst.append(pair)
    df = pd.DataFrame(lst, columns=['State', 'RegionName']) #finally thanks God!
    df.State = df.replace(states.values(), states.keys())
    return df


# In[ ]:


def get_recession_start():
    df2 = pd.read_excel('gdplev.xls', skiprows=4)
    df2 = df2.drop([1, 2])
    df2.pop('Unnamed: 3')
    df2.pop('Unnamed: 7')
    df2.rename(columns={'Unnamed: 0': 'Years', 'Unnamed: 1':'GDP current Y', 'Unnamed: 2': 'GDP chained 2009 Y','Unnamed: 4': 'Quarters', 'Unnamed: 5': 'GDP current Q', 'Unnamed: 6':'GDP chained 2009 Q'}, inplace=True)
    df2 = df2.drop(0).reset_index()
    df2.pop('index')


    data_y = df2['GDP current Y']
    data_q = df2['GDP current Q']
    quarter = df2['Quarters']
    data_q = list(data_q)

    plt.plot(data_q, linestyle=':', marker='s')
    regr = df2.loc[246:249, ['Quarters', 'GDP current Q']]
    x = df2.loc[246:253, 'Quarters']
    y = df2.loc[246:253, 'GDP current Q']
    plt.plot(x, y)
    plt.show()

    return '2008q3'


# In[ ]:


def get_recession_end():
    df2 = pd.read_excel('gdplev.xls', skiprows=4)
    df2 = df2.drop([1, 2])
    df2.pop('Unnamed: 3')
    df2.pop('Unnamed: 7')
    df2.rename(columns={'Unnamed: 0': 'Years', 'Unnamed: 1':'GDP current Y', 'Unnamed: 2': 'GDP chained 2009 Y','Unnamed: 4': 'Quarters', 'Unnamed: 5': 'GDP current Q', 'Unnamed: 6':'GDP chained 2009 Q'}, inplace=True)
    df2 = df2.drop(0).reset_index()
    df2.pop('index')


    data_y = df2['GDP current Y']
    data_q = df2['GDP current Q']
    quarter = df2['Quarters']
    data_q = list(data_q)

    plt.plot(data_q, linestyle=':', marker='s')
    regr = df2.loc[246:249, ['Quarters', 'GDP current Q']]
    x = df2.loc[246:253, 'Quarters']
    y = df2.loc[246:253, 'GDP current Q']
    plt.plot(x, y)

    return '2009q4'


# In[ ]:


def get_recession_bottom():
    df2 = pd.read_excel('gdplev.xls', skiprows=4)
    df2 = df2.drop([1, 2])
    df2.pop('Unnamed: 3')
    df2.pop('Unnamed: 7')
    df2.rename(columns={'Unnamed: 0': 'Years', 'Unnamed: 1':'GDP current Y', 'Unnamed: 2': 'GDP chained 2009 Y','Unnamed: 4': 'Quarters', 'Unnamed: 5': 'GDP current Q', 'Unnamed: 6':'GDP chained 2009 Q'}, inplace=True)
    df2 = df2.drop(0).reset_index()
    df2.pop('index')


    data_y = df2['GDP current Y']
    data_q = df2['GDP current Q']
    quarter = df2['Quarters']
    data_q = list(data_q)

    plt.plot(data_q, linestyle=':', marker='s')
    regr = df2.loc[246:249, ['Quarters', 'GDP current Q']]
    x = df2.loc[246:253, 'Quarters']
    y = df2.loc[246:253, 'GDP current Q']
    plt.plot(x, y)

    return '2009q2'


# In[ ]:


def convert_housing_data_to_quarters():
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    drp = df.iloc[:, 6:51]
    data = df.drop(drp, axis=1)

    data['2000q1'] = data[['2000-01', '2000-02', '2000-03']].mean(axis=1)
    data['2000q2'] = data[['2000-04', '2000-05', '2000-06']].mean(axis=1)
    data['2000q3'] = data[['2000-07', '2000-08', '2000-09']].mean(axis=1)
    data['2000q4'] = data[['2000-10', '2000-11', '2000-12']].mean(axis=1)

    data['2001q1'] = data[['2001-01', '2001-02', '2001-03']].mean(axis=1)
    data['2001q2'] = data[['2001-04', '2001-05', '2001-06']].mean(axis=1)
    data['2001q3'] = data[['2001-07', '2001-08', '2001-09']].mean(axis=1)
    data['2001q4'] = data[['2001-10', '2001-11', '2001-12']].mean(axis=1)

    data['2002q1'] = data[['2002-01', '2002-02', '2002-03']].mean(axis=1)
    data['2002q2'] = data[['2002-04', '2002-05', '2002-06']].mean(axis=1)
    data['2002q3'] = data[['2002-07', '2002-08', '2002-09']].mean(axis=1)
    data['2002q4'] = data[['2002-10', '2002-11', '2002-12']].mean(axis=1)

    data['2003q1'] = data[['2003-01', '2003-02', '2003-03']].mean(axis=1)
    data['2003q2'] = data[['2003-04', '2003-05', '2003-06']].mean(axis=1)
    data['2003q3'] = data[['2003-07', '2003-08', '2003-09']].mean(axis=1)
    data['2003q4'] = data[['2003-10', '2003-11', '2003-12']].mean(axis=1)

    data['2004q1'] = data[['2004-01', '2004-02', '2004-03']].mean(axis=1)
    data['2004q2'] = data[['2004-04', '2004-05', '2004-06']].mean(axis=1)
    data['2004q3'] = data[['2004-07', '2004-08', '2004-09']].mean(axis=1)
    data['2004q4'] = data[['2004-10', '2004-11', '2004-12']].mean(axis=1)

    data['2005q1'] = data[['2005-01', '2005-02', '2005-03']].mean(axis=1)
    data['2005q2'] = data[['2005-04', '2005-05', '2005-06']].mean(axis=1)
    data['2005q3'] = data[['2005-07', '2005-08', '2005-09']].mean(axis=1)
    data['2005q4'] = data[['2000-10', '2005-11', '2005-12']].mean(axis=1)

    data['2006q1'] = data[['2006-01', '2006-02', '2006-03']].mean(axis=1)
    data['2006q2'] = data[['2006-04', '2006-05', '2006-06']].mean(axis=1)
    data['2006q3'] = data[['2006-07', '2006-08', '2006-09']].mean(axis=1)
    data['2006q4'] = data[['2006-10', '2006-11', '2006-12']].mean(axis=1)

    data['2007q1'] = data[['2007-01', '2007-02', '2007-03']].mean(axis=1)
    data['2007q2'] = data[['2007-04', '2007-05', '2007-06']].mean(axis=1)
    data['2007q3'] = data[['2007-07', '2007-08', '2007-09']].mean(axis=1)
    data['2007q4'] = data[['2007-10', '2007-11', '2007-12']].mean(axis=1)

    data['2008q1'] = data[['2008-01', '2008-02', '2008-03']].mean(axis=1)
    data['2008q2'] = data[['2008-04', '2008-05', '2008-06']].mean(axis=1)
    data['2008q3'] = data[['2008-07', '2008-08', '2008-09']].mean(axis=1)
    data['2008q4'] = data[['2008-10', '2008-11', '2008-12']].mean(axis=1)

    data['2009q1'] = data[['2009-01', '2009-02', '2009-03']].mean(axis=1)
    data['2009q2'] = data[['2009-04', '2009-05', '2009-06']].mean(axis=1)
    data['2009q3'] = data[['2009-07', '2009-08', '2009-09']].mean(axis=1)
    data['2009q4'] = data[['2009-10', '2009-11', '2009-12']].mean(axis=1)

    data['2010q1'] = data[['2010-01', '2010-02', '2010-03']].mean(axis=1)
    data['2010q2'] = data[['2010-04', '2010-05', '2010-06']].mean(axis=1)
    data['2010q3'] = data[['2010-07', '2010-08', '2010-09']].mean(axis=1)
    data['2010q4'] = data[['2010-10', '2010-11', '2010-12']].mean(axis=1)

    data['2011q1'] = data[['2011-01', '2011-02', '2011-03']].mean(axis=1)
    data['2011q2'] = data[['2011-04', '2011-05', '2011-06']].mean(axis=1)
    data['2011q3'] = data[['2011-07', '2011-08', '2011-09']].mean(axis=1)
    data['2011q4'] = data[['2011-10', '2011-11', '2011-12']].mean(axis=1)

    data['2012q1'] = data[['2012-01', '2012-02', '2012-03']].mean(axis=1)
    data['2012q2'] = data[['2012-04', '2012-05', '2012-06']].mean(axis=1)
    data['2012q3'] = data[['2012-07', '2012-08', '2012-09']].mean(axis=1)
    data['2012q4'] = data[['2012-10', '2012-11', '2012-12']].mean(axis=1)

    data['2013q1'] = data[['2013-01', '2013-02', '2013-03']].mean(axis=1)
    data['2013q2'] = data[['2013-04', '2013-05', '2013-06']].mean(axis=1)
    data['2013q3'] = data[['2013-07', '2013-08', '2013-09']].mean(axis=1)
    data['2013q4'] = data[['2013-10', '2013-11', '2013-12']].mean(axis=1)

    data['2014q1'] = data[['2014-01', '2014-02', '2014-03']].mean(axis=1)
    data['2014q2'] = data[['2014-04', '2014-05', '2014-06']].mean(axis=1)
    data['2014q3'] = data[['2014-07', '2014-08', '2014-09']].mean(axis=1)
    data['2014q4'] = data[['2014-10', '2014-11', '2014-12']].mean(axis=1)

    data['2015q1'] = data[['2015-01', '2015-02', '2015-03']].mean(axis=1)
    data['2015q2'] = data[['2015-04', '2015-05', '2015-06']].mean(axis=1)
    data['2015q3'] = data[['2015-07', '2015-08', '2015-09']].mean(axis=1)
    data['2015q4'] = data[['2015-10', '2015-11', '2015-12']].mean(axis=1)

    data['2016q1'] = data[['2016-01', '2016-02', '2016-03']].mean(axis=1)
    data['2016q2'] = data[['2016-04', '2016-05', '2016-06']].mean(axis=1)
    data['2016q3'] = data[['2016-07', '2016-08']].mean(axis=1)


    drop2 = data.iloc[:, 6:206]
    data = data.drop(drop2, axis=1)
    data = data.set_index(['RegionName', 'State'])
    data.pop('RegionID')
    data.pop('Metro')
    data.pop('SizeRank')
    data.pop('CountyName')
    return data


# In[ ]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    towns = get_list_of_university_towns()
    startdate = get_recession_start()
    bottomdate = get_recession_bottom()
    houses = convert_housing_data_to_quarters()

    houses = houses.reset_index()
    houses['recession_diff'] = houses[startdate] - houses[bottomdate]
    print(houses['recession_diff'])

    '''towns_houses = pd.merge(houses, towns, how='inner', on=['State', 'RegionName'])
    towns_houses['ctown'] = True
    houses = pd.merge(houses, towns_houses, how='outer', on = ['State', 'RegionName',
                                                              bottomdate, startdate,
                                                              'recession_diff'])
    houses['ctown'] = houses['ctown'].fillna(False)
    unitowns = houses[houses['ctown'] == True]
    not_unitowns = houses[houses['ctown'] == False]

    t, p = ttest_ind(unitowns['recession_diff'].dropna(), not_unitowns['recession_diff'].dropna())
    different = True if p < 0.01 else False
    betters = "university town" if unitowns['recession_diff'].mean() < not_unitowns['recession_diff'].mean() else "non-university town"

    return different,p,betters'''
