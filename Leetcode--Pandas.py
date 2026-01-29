"""28th January 2026"""
#1 175. Combine Two Tables
import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(left = person, right = address, how = 'left', on = 'personId')
    result = result[['firstName','lastName','city','state']]
    return result


#2 176. Second Highest Salary
import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    employee.drop_duplicates(subset='salary',inplace = True)
    employee.sort_values(by='salary', ascending = False, inplace = True)
    employee = employee[['salary']]
    if len(employee) < 2:
        return pd.DataFrame({'SecondHighestSalary' : [None]})
    else:
        return pd.DataFrame({'SecondHighestSalary' : employee.iloc[1]})


#3 177. Nth Highest Salary 
import pandas as pd

def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    employee.drop_duplicates(subset='salary', inplace = True)
    employee.sort_values(by='salary', ascending = False, inplace = True)
    employee = employee[['salary']]
    if len(employee)<N or N<=0:
        return pd.DataFrame({f'getNthHighestSalary({N})':[None]})
    else:
        return pd.DataFrame({f'getNthHighestSalary({N})' : employee.iloc[N-1]})


#4 178. Rank Scores
import pandas as pd

def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    scores['rank'] = scores['score'].rank(method = 'dense', ascending = False)
    scores.sort_values(by= 'rank', ascending = True, inplace = True)
    scores = scores[['score','rank']]
    return scores


#5 180. Consecutive Numbers
import pandas as pd

def consecutive_numbers(logs: pd.DataFrame) -> pd.DataFrame:
        logs['is_consecutive'] = (logs['num'] == logs['num'].shift(1)) & (logs['num'] == logs['num'].shift(2))
        logs = logs[logs['is_consecutive'] == True][['num']]
        return pd.DataFrame({'ConsecutiveNums':logs['num'].unique()})


import pandas as pd

def consecutive_numbers(logs: pd.DataFrame) -> pd.DataFrame:
        logs['var'] = logs['num'].rolling(window=3).var()
        logs = logs[logs['var']==0][['num']]
        return pd.DataFrame({'ConsecutiveNums':logs['num'].unique()})


#6 181. Employees Earning More Than Their Managers
import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(left = employee, right=employee, left_on='managerId', right_on = 'id', how = 'inner', suffixes = ('_emp','_mng'))
    df.rename(columns = {'name_emp' : 'Employee'}, inplace = True)
    df = df[df['salary_emp']>df['salary_mng']][['Employee']]
    return df


#7 182. Duplicate Emails
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    person = person[person.duplicated(subset='email', keep='first')==True]
    return pd.DataFrame({'Email':person['email'].unique()})


import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    df = person.groupby('email').aggregate(count = ('email','size')).reset_index()
    df = df[df['count']>1]
    return pd.DataFrame({'Email':df.iloc[:,0]})


#8 183. Customers Who Never Order
import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    customers = customers[~customers['id'].isin(orders['customerId'])][['name']]
    customers.rename(columns = {'name':'Customers'}, inplace = True)
    return customers


#9 184. Department Highest Salary
import pandas as pd

def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(left=employee, right=department, how = 'left', left_on='departmentId', right_on='id', suffixes = ('_employee','_department'))
    df.rename(columns={'name_employee':'Employee', 'name_department':'Department', 'salary':'Salary'}, inplace=True)
    df['max_salary'] = df.groupby('Department')['Salary'].transform('max')
    df = df[df['Salary'] == df['max_salary']][['Department','Employee','Salary']]
    return df


#10 185. Department Top Three Salaries
import pandas as pd

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(left=employee, right=department, left_on='departmentId', right_on='id', how='left', suffixes=('_employee','_department'))
    df['rank'] = df.groupby('name_department')['salary'].rank(method='dense', ascending=False)
    df.rename(columns = {'name_employee':'Employee','name_department':'Department','salary':'Salary'}, inplace = True)
    df = df[df['rank']<=3] [['Department','Employee','Salary']]
    return df 


# 29th January 2026
#11 197. Rising Temperature
import pandas as pd

def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    weather.sort_values(by='recordDate', ascending = True, inplace = True)
    weather['temp_diff'] = weather['temperature'].diff()
    weather['recordDate_diff'] = weather['recordDate'].diff().dt.days
    weather = weather[(weather['temp_diff']>0) & (weather['recordDate_diff']==1)][['id']]
    return weather


#12 262. Trips and Users
import pandas as pd

def trips_and_users(trips: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    unbanned_users = users[users['banned'] == 'No']['users_id']
    trips = trips[trips['client_id'].isin(unbanned_users)&(trips['driver_id'].isin(unbanned_users))]
    trips = trips[trips['request_at'].between('2013-10-01','2013-10-03')]
    trips.rename(columns = {'request_at':'Day'}, inplace = True)
    
    final = trips.groupby('Day').aggregate(total_trips = ('status','count'),
    cancelled_trips = ('status', lambda x : (x!='completed').sum())).reset_index()
    final['Cancellation Rate'] = (final['cancelled_trips']/final['total_trips']).round(2)
    return final[['Day','Cancellation Rate']]
