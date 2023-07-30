import re 
import pandas as pd
from datetime import datetime

def preprocess(data):
    
    patt='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # patt='\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} (?:am|pm)'
    msgs= re.split(patt, data)[1:]
    date= re.findall(patt, data)

    dates = [datetime.strptime(date, '%m/%d/%y, %H:%M - ') for date in date]
    df=pd.DataFrame({'user_msg': msgs, 'msg_dates': dates})
    df['msg_dates'] = pd.to_datetime(df['msg_dates'], format='%m/%d/%y, %H:%M - ')
    df.rename(columns={'msg_dates': 'date'}, inplace=True)
    users=[]
    msgs=[]
    for msg in df['user_msg']:
        entry=re.split('([\w\W]+?):\s', msg)
        if(entry[1:]):
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_noti')
            msgs.append(entry[0])

    df['users']=users
    df['message']=msgs
    df.drop(columns=['user_msg'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year']=df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    return df