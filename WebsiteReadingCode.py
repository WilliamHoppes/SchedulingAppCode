import os
from google import genai
import io
import pandas as pd
import time
import csv

#https://ai.google.dev/gemini-api/docs
my_api_key="AIzaSyABpmNdLcZhnAduMWBpDob8gaeq2BUWtsI"

open_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/01Raw_Website_Snapshots/"
exit_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/02Processed_Website_Schedules/"

client = genai.Client(api_key="AIzaSyABpmNdLcZhnAduMWBpDob8gaeq2BUWtsI")


prompt="Please help me generate a csv file of all the events from the website shown in the attached image. "
prompt+="Each row should represent a separate event. "
prompt+="For each event, there should be four columns: the title of the concert or event,"
prompt+="the month as a number (ie 1 for January, 8 for August),"
prompt+="the day (ie, 15 for the 15th, 2 for the 2nd),"
prompt+="and the time as military time (ie, 20:40 for 8:40 PM, 10:15 for 10:15 AM). (Always )"
prompt+="If the time cannot be found, please put *Unknown*. If the month or day cannot be included, please ignore it."
prompt+="Under no circumstances should you respond with anything other than the csv. Do not include ```csv!!! " #eg ```csv was included once
prompt+="Only use ASCII characters. Do not use any unusual characters."

for file in os.listdir(open_path):
    attempts_remaining_counter=3
    error_prompt_addon=""
    while attempts_remaining_counter>0:
        #Get the image
        file_name=file[:-4]
        current_image=client.files.upload(file=open_path+file)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[current_image, prompt+error_prompt_addon],
        )
        csv_raw_data=str(response.text)
        #Basic Cleaning
        csv_raw_data=csv_raw_data.replace("``` csv", "")     #The model insists on inlcuding this
        csv_raw_data=csv_raw_data.replace("csv", "") 
        safe_characters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*(),   \n"
        csv_clean_data=""
        for char in csv_raw_data:
            if char in safe_characters:
                csv_clean_data+=char
        #We need to add pandas for file checking
        #https://www.statology.org/pandas-read-csv-from-string/
        try:
            df=pd.read_csv(io.StringIO(csv_clean_data), sep=",")
            df["Location"]=file[:-4]
            df.to_csv(exit_path+file[:-4]+".csv", index=False)
            print(file[:-4]+" successful")
            attempts_remaining_counter=0
        except Exception as e:
            print(file+" failed. "+str(attempts_remaining_counter)+" attempts remaining")
            print("Error code: "+str(e))
            error_prompt_addon+="The previous attempt failed. While trying to convert this to a pandas dataframe in python, the following error occured: "
            error_prompt_addon+=str(e)
            attempts_remaining_counter=attempts_remaining_counter-1
            time.sleep(5)
        time.sleep(10)


