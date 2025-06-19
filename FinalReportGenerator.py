import pandas as pd
import numpy as np
import datetime

output_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/04Final_Report/"

output_string=""
df=pd.read_csv("C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/03Final_Dataset/Final.csv", index_col=False)
df.loc[df['Event']=="*Unknown*", "Event"]=np.nan
df.loc[df['Month']=="*Unknown*", "Month"]=np.nan
df.loc[df['Day']=="*Unknown*", "Day"]=np.nan
df=df.dropna(how="any")


#clean up time
TimeSort=[]
TimeChar=[]
for rowVal in df["Time"]:
    raw_time=str(rowVal)
    Unknown_Flag=False
    for char in raw_time:
        if char not in '0123456789':
            Unknown_Flag=True
    if Unknown_Flag==True:
        TimeSort.append(9999)
        TimeChar.append(raw_time)
    elif len(raw_time)<=4:
        raw_time+="0"*(4-len(raw_time))
        TimeSort.append(int(raw_time))
        TimeChar.append(raw_time[:2]+":"+raw_time[2:])
    else:
        print("Odd Value")
        print(raw_time)
df['TimeSort']=TimeSort
df['TimeChar']=TimeChar


#clean up date
TimeDateTime=[]
for i in range(len(df.index)):
    raw_month=str(df['Month'].iloc[i])
    raw_day=str(df['Day'].iloc[i])
    if raw_month.find(".")>=0:                  #find returns -1 if the char isn't in the string
        float_index=raw_month.find(".")         #Sometimes we get floats instead of integers
        clean_month=int(raw_month[:float_index])
    else:
        clean_month=int(raw_month)
    if raw_day.find(".")>=0:                  #find returns -1 if the char isn't in the string
        float_index=raw_day.find(".")         #Sometimes we get floats instead of integers
        clean_day=int(raw_day[:float_index])
    else:
        clean_day=int(raw_day)
    current_date=datetime.datetime(2025, clean_month, clean_day)
    TimeDateTime.append(current_date.date())

df['TimeSort']=TimeSort
df['TimeChar']=TimeChar
df['Date']=TimeDateTime


start_date=datetime.date.today()+datetime.timedelta(days=1)
end_date=datetime.date.today()+datetime.timedelta(days=8)

output_df=df[(df['Date']>=start_date) & (df['Date']<=end_date)]
output_df=output_df.sort_values(by=['Date', 'TimeSort'], ascending=True, na_position='last')
output_df=output_df[["Event", "Date", "TimeChar", "Location"]]

output_df.to_csv(output_path+"FinalReport.csv")



