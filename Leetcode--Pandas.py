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


"""29th January 2026"""
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


"""30th January 2026"""
#13 1757. Recyclable and Low Fat Products
import pandas as pd

def find_products(products: pd.DataFrame) -> pd.DataFrame:
    products = products[(products['low_fats'] == 'Y') & (products['recyclable']=='Y')][['product_id']]
    return products


#14 584. Find Customer Referee
import pandas as pd

def find_customer_referee(customer: pd.DataFrame) -> pd.DataFrame:
    customer = customer[(customer['referee_id'] !=2) | (customer['referee_id'].isna()==True)][['name']]
    return customer


#15 595. Big Countries
import pandas as pd

def big_countries(world: pd.DataFrame) -> pd.DataFrame:
    world = world[(world['population']>=25000000) | (world['area']>=3000000)][['name','population','area']]
    return world


#16 1148. Article Views I
import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:
    views = views[views['author_id']==views['viewer_id']][['author_id']]
    views.rename(columns = {'author_id':'id'}, inplace = True)
    views.drop_duplicates(subset='id', inplace = True)
    views.sort_values(by='id',inplace = True)
    return views


#17 1683. Invalid Tweets
import pandas as pd

def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    tweets = tweets[tweets['content'].str.len() > 15][['tweet_id']]
    return tweets


#18 1378. Replace Employee ID With The Unique Identifier
import pandas as pd

def replace_employee_id(employees: pd.DataFrame, employee_uni: pd.DataFrame) -> pd.DataFrame:
    df = employees.merge(employee_uni, how='left', on='id')
    return df[['unique_id','name']]


#19 1068. Product Sales Analysis I
import pandas as pd

def sales_analysis(sales: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    df = sales.merge(product, how='left', on='product_id')
    df = df[['product_name','year','price']]
    return df


#20 1581. Customer Who Visited but Did Not Make Any Transactions
import pandas as pd

def find_customers(visits: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    df = visits.merge(transactions, how = 'left', on='visit_id')
    df = df[df['transaction_id'].isna()==True]
    result = df.groupby('customer_id').aggregate(count_no_trans = ('customer_id','size')).reset_index()
    result.sort_values(by='count_no_trans', ascending = False, inplace = True)
    return result


#21 197. Rising Temperature
import pandas as pd

def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    weather.sort_values(by='recordDate', ascending=True, inplace = True)
    weather['date_diff'] = weather['recordDate'].diff().dt.days
    weather['temp_diff'] = weather['temperature'].diff()
    weather = weather[(weather['date_diff']==1)&(weather['temp_diff']>0)][['id']]
    return weather


#22 1661. Average Time of Process per Machine
import pandas as pd

def get_average_time(activity: pd.DataFrame) -> pd.DataFrame:
    start_activity = activity[activity['activity_type']=='start']
    end_activity = activity[activity['activity_type'] =='end']
    df = start_activity.merge(end_activity, how='inner', on=['machine_id','process_id'], suffixes = ('_s','_e'))
    df['diff'] = df['timestamp_e']-df['timestamp_s']
    result = df.groupby('machine_id').aggregate(processing_time=('diff','mean')).reset_index().round(3)
    return result


#23 577. Employee Bonus
import pandas as pd

def employee_bonus(employee: pd.DataFrame, bonus: pd.DataFrame) -> pd.DataFrame:
    df = employee.merge(bonus, how = 'left', on='empId')
    df = df[(df['bonus'] < 1000) | (df['bonus'].isna() == True)][['name','bonus']]
    return df


#24 1280. Students and Examinations
import pandas as pd

def students_and_examinations(students: pd.DataFrame, subjects: pd.DataFrame, examinations: pd.DataFrame) -> pd.DataFrame:
    d1 = students.merge(subjects, how = 'cross')
    d2 = examinations.groupby(['student_id','subject_name']).size().reset_index(name='attended_exams')
    df = d1.merge(d2, how='left', on=['student_id','subject_name'])
    df['attended_exams'].fillna(0, inplace = True)
    df.sort_values(by=['student_id','subject_name'], ascending=True, inplace = True)
    return df


#25 570. Managers with at Least 5 Direct Reports
import pandas as pd

def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    result = employee.groupby('managerId').size().reset_index(name='reporting_count')
    result = result[result['reporting_count']>=5]
    df = employee[employee['id'].isin(result['managerId'])][['name']]
    return df


#26 1934. Confirmation Rate
import pandas as pd

def confirmation_rate(signups: pd.DataFrame, confirmations: pd.DataFrame) -> pd.DataFrame:
    total = confirmations.groupby('user_id').size().reset_index(name='total_attempts')
    confirmed = confirmations[confirmations['action']=='confirmed'].groupby('user_id').size().reset_index(name='confirmed_attempts')
    d1 = total.merge(confirmed, how='left', on='user_id')
    df = signups.merge(d1, how = 'left', on='user_id')
    df['confirmation_rate'] = (df['confirmed_attempts']/df['total_attempts']).round(2)
    df.fillna(0,inplace=True)
    return df[['user_id','confirmation_rate']]


#27 620. Not Boring Movies
import pandas as pd

def not_boring_movies(cinema: pd.DataFrame) -> pd.DataFrame:
    cinema = cinema[(cinema['id']%2 !=0) & (cinema['description'].ne('boring'))]
    cinema.sort_values(by='rating', ascending=False, inplace = True)
    return cinema


"""2nd February 2026"""
#28 1251. Average Selling Price
import pandas as pd
import numpy as np

def average_selling_price(prices: pd.DataFrame, units_sold: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(prices, units_sold, how='left', on = 'product_id')
    df = df[(df['purchase_date'].isna() == True) | df['purchase_date'].between(df['start_date'], df['end_date'])]
    df['total_price'] = df['price']*df['units']
    df.fillna(0, inplace = True)
    result = df.groupby('product_id').aggregate(final_price = ('total_price', 'sum'), final_count = ('units','sum')).reset_index()
    result['average_price'] = np.where(result['final_count']==0,0,(result['final_price']/result['final_count'])).round(2) 
    
    return result[['product_id','average_price']]


#29 1075. Project Employees I
import pandas as pd

def project_employees_i(project: pd.DataFrame, employee: pd.DataFrame) -> pd.DataFrame:
    df = project.merge(employee, on='employee_id', how='left')
    result = df.groupby('project_id').aggregate(average_years = ('experience_years','mean')).round(2).reset_index()
    return result


#30 1633. Percentage of Users Attended a Contest
import pandas as pd

def users_percentage(users: pd.DataFrame, register: pd.DataFrame) -> pd.DataFrame:
    unique_users = users['user_id'].nunique()
    contest_users = register.groupby('contest_id').aggregate(contest_user = ('user_id','size')).reset_index()
    contest_users['percentage'] = (contest_users['contest_user']/unique_users*100).round(2)
    contest_users.sort_values(by=['percentage','contest_id'], ascending = [False,True], inplace = True)
    return contest_users[['contest_id','percentage']]


#31 1211. Queries Quality and Percentage
import pandas as pd
import numpy as np

def queries_stats(queries: pd.DataFrame) -> pd.DataFrame:
    queries['qr_ratio'] = (queries['rating']/queries['position'])
    queries['is_poor'] = queries['rating']<3

    final = queries.groupby('query_name').aggregate(quality = ('qr_ratio', 'mean'), poor_query_percentage = ('is_poor', lambda x : x.mean()*100)).sort_values(by='query_name').reset_index()

    #to handle rounding issue
    final['quality'] = np.floor(final['quality'] * 100 + 0.5) / 100
    final['poor_query_percentage'] = np.floor(final['poor_query_percentage'] * 100 + 0.5) / 100

    return final


""" 3rd February 2026 """
#32 1193. Monthly Transactions I
import pandas as pd
import numpy as np

def monthly_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    transactions['month'] = pd.to_datetime(transactions['trans_date']).dt.strftime('%Y-%m')
    transactions['approved'] = transactions['state'] == 'approved'
    transactions['approved_amount'] = np.where(transactions['state'] == 'approved', transactions['amount'], 0)
    
    result = transactions.groupby(['month','country'], dropna = False).aggregate(trans_count = ('trans_date','size'), approved_count = ('approved','sum'), trans_total_amount = ('amount', 'sum'), approved_total_amount = ('approved_amount','sum')).reset_index()
    return result


#33 1174. Immediate Food Delivery II
import pandas as pd
import numpy as np

def immediate_food_delivery(delivery: pd.DataFrame) -> pd.DataFrame:
    first_order_dates = delivery.groupby('customer_id')['order_date'].min().reset_index(name = 'first_date')
    result = delivery.merge(first_order_dates, left_on=['customer_id','order_date'], right_on=['customer_id','first_date'])
    
    immediate_orders = len(result[result['order_date']==result['customer_pref_delivery_date']])
    total_orders = len(first_order_dates)

    immediate_percentage = round(immediate_orders/total_orders*100,2)
    
    df = pd.DataFrame({'immediate_percentage' : [immediate_percentage]})
    return df


import pandas as pd

def immediate_food_delivery(delivery: pd.DataFrame) -> pd.DataFrame:    
    delivery.sort_values(by = ['customer_id','order_date'], ascending = [True,True], inplace = True)
    delivery.drop_duplicates(subset = ['customer_id'],keep = 'first', inplace = True)
    delivery['is_immediate'] = delivery['order_date'] == delivery['customer_pref_delivery_date']

    return pd.DataFrame({'immediate_percentage' : [delivery['is_immediate'].mean().round(4)*100]})


#34 550. Game Play Analysis IV
