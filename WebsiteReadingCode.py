import os
from google import genai
from google.genai import types
import io
import pandas as pd
import time
import csv
from datetime import date

#https://ai.google.dev/gemini-api/docs
my_api_key=os.environ['GEMINI_API_KEY']

open_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/01Raw_Website_Snapshots/"
exit_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/02Processed_Website_Schedules/"
error_path="C:/Users/hoppe/Documents/SchedulingApp/SchedulingAppLive/Errors/"

#initialize lists for error log
Error_file=[]
Error_type=[]
Error_date=[]
Error_message=[]
current_date=str(date.today())

client = genai.Client(api_key=my_api_key)


prompt="Please help me generate a csv file of all the events from the website shown in the attached image. "
prompt+="Each row should represent a separate event. "
prompt+="For each event, there should be four columns: the title of the concert or event,"
prompt+="the month as a number (ie 1 for January, 8 for August),"
prompt+="the day (ie, 15 for the 15th, 2 for the 2nd),"
prompt+="and the time as military time (ie, 20:40 for 8:40 PM, 10:15 for 10:15 AM). (Always )"
prompt+="If the time cannot be found, please put *Unknown*. If the month or day cannot be included, please ignore it."
prompt+="Under no circumstances should you respond with anything other than the csv. Do not include ```csv!!! " #eg ```csv was included once
prompt+="Only use ASCII characters. Do not use any unusual characters."
#prompt+="A perfect example of what I want is the following csv structure:"
#prompt+="Title, Month, Day, Time, \n"
#prompt+="Ion Prototyping Lab Office Hours, 4, 1, 13:00, \n"
#prompt+="DJ Night DJ Python, 5, 23, 22:00, \n"
#prompt+="SBC Central Meeting, 2, 19, 18:00"

for file in os.listdir(open_path):
    attempts_remaining_counter=3
    error_prompt_addon=""
    file_name=file[:-4]
    output_file_name=exit_path+file[:-4]+".csv"
    while attempts_remaining_counter>0 and os.path.isfile(output_file_name)==False:
        try:
        #Get the image
            current_image=client.files.upload(file=open_path+file)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[current_image, prompt+error_prompt_addon],
                #https://ai.google.dev/gemini-api/docs/thinking
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                )
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
                df.to_csv(output_file_name, index=False)
                print(file[:-4]+" successful")
                attempts_remaining_counter=0
            except Exception as e:
                print(file+" failed. "+str(attempts_remaining_counter)+" attempts remaining")
                print("Error code: "+str(e))
                error_prompt_addon+="The previous attempt failed. While trying to convert this to a pandas dataframe in python, the following error occured: "
                error_prompt_addon+=str(e)
                attempts_remaining_counter=attempts_remaining_counter-1
                Error_file.append(output_file_name)
                Error_type.append("Failed at csv step")
                Error_date.append(current_date)
                Error_message.append(str(e))
                time.sleep(60)
#                if attempts_remaining_counter==0:
#                    with open(exit_path+file[:-4]+"ERROR"+".csv", "w") as file:
#                        file.write(csv_clean_data)
        except Exception as e:
            print("Gemini model failed!")
            print("Error code: "+str(e))
            attempts_remaining_counter=attempts_remaining_counter-1
            Error_file.append(output_file_name)
            Error_type.append("Failed at csv step")
            Error_date.append(current_date)
            Error_message.append(str(e))
            time.sleep(60)
        time.sleep(60)

df=pd.DataFrame({
    "Error_file": Error_file,
    "Error_type": Error_type,
    "Error_date": Error_date,
    "Error_message": Error_message
})

df.to_excel(error_path+"Errors.xlsx", index=False)