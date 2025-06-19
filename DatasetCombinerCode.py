import pandas as pd
import os

open_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/02Processed_Website_Schedules/"
exit_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/03Final_Dataset/"

col_names=['Event', 'Month', "Day", 'Time', 'Location']
master_df=pd.DataFrame(columns=col_names)

for file in os.listdir(open_path):
    current_df=pd.DataFrame(columns=col_names)
    try:
        current_df=pd.read_csv(open_path+file)
        current_df['Location']=file[:-4]
        current_df.columns=col_names
        master_df=pd.concat([master_df, current_df], ignore_index=True)
    except:
        print(file+" failed")
        if len(current_df.columns)>5:
            print("Too many columns")

master_df.to_csv(exit_path+"Final.csv", index=False)