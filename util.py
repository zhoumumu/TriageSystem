import os, re
import pandas as pd

def read_profiles(num_start=1, num_end=-1, specify=None): # start from 1
    # 1.get [start:end], closed range
    # 2.get [start:]
    # 3.get specified
    # 4.get all
    with open("profiles_reddit.txt", 'r', encoding='utf-8') as file:
        doc = file.read()
    profiles = doc.split("\n##########\n")
    if specify: return [(i, profiles[i-1]) for i in specify]
    if num_end == -1: num_end = len(profiles)
    return [(i, profiles[i-1]) for i in range(num_start, num_end+1)]


# def search_and_rename_files(folder_path):
#     keywords = ['immediate', '24 hours', 'next available']
#     levels = ['Emergent', 'Urgent', 'Routine']

#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         found_keywords = []
        
#         with open(file_path, 'r') as file:
#             content = file.read()    
#             # Search for each keyword (case-sensitive)
#             for keyword in keywords:
#                 if re.search(r'\b' + re.escape(keyword) + r'\b', content):
#                     found_keywords.append(keyword)
            
#         if len(found_keywords) == 0: continue
#         # if len(found_keywords) > 1: # no example like this
#         #     print(f"File {filename} contains multiple keywords: {', '.join(found_keywords)}")

#         # Rename the file with the keyword as suffix
#         name, ext = os.path.splitext(filename)
#         level = levels[keywords.index(found_keywords[0])]
#         new_name = f"{name}_{level}{ext}"
#         new_path = os.path.join(folder_path, new_name)
#         os.rename(file_path, new_path)
            
# search_and_rename_files("prompt_4o")

################## check accuracy
# df = pd.read_excel('add_time_filtered_reddit_info.xlsx')
# answer = df['分诊分级'].tolist()
# pred = sorted(
#     os.listdir('prompt_4o'),
#     # key=lambda x: os.path.getmtime(os.path.join('reddit_qwen2.5-32b-instruct', x)),
#     key=lambda x: int(x.split('_')[1]),
#     reverse=False
# )
# # print(pred)
# pred = [p.split('_')[-1][:-4] for p in pred]
# # print(answer)
# correct = 0
# wrong = []
# for i in range(101):
#     if answer[i][0] == pred[i][0]: correct += 1
#     else: wrong.append(i)
# print(correct)
# print(wrong)
#qwen: [8, 10, 11, 12, 14, 15, 17, 19, 25, 26, 29, 32, 34, 36, 37, 38, 39, 41, 42, 47, 48, 53, 61, 65, 66, 67, 71, 72, 73, 74, 80, 82, 84, 88, 89, 91, 95, 96, 97, 100]
#gpt_4o pure prompt: [0, 6, 7, 9, 10, 12, 13, 14, 16, 17, 19, 20, 23, 24, 25, 26, 28, 29, 31, 32, 33, 36, 38, 40, 41, 42, 43, 45, 48, 50, 56, 58, 61, 62, 63, 64, 65, 66, 68, 69, 70, 72, 73, 77, 78, 80, 81, 82, 83, 84, 85, 86, 88, 89, 90, 91, 95, 99]

################# test API key
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# load_dotenv()
# print(os.getenv('OPENAI_BASE_URL'))
# # Way 1
# client = OpenAI()
# completion = client.chat.completions.create(
#   model="gpt-4o",
#   messages=[
#       {
#           "role": "user",
#           "content": "Hi"
#       }
#   ]
# )
# print(completion)
# Way 2
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model='gpt-4o', api_key="", base_url="")
# print(llm.invoke("Hi, who are you"))
# Way 3
# import requests
# import json
# 使用中转链接可以和特定的API可以不必向openai发起请求，且请求无须魔法
# 调用方式与openai官网一致，仅需修改baseurl
# Baseurl = "xxx"
# Skey = "xxx"

# payload = json.dumps({
#    "model": "gpt-4o",
#    "messages": [
#       {
#          "role": "system",
#          "content": "You are a helpful assistant."
#       },
#       {
#          "role": "user",
#          "content": "hello, who are you"
#       }
#    ]
# })
# headers = {
#    'Accept': 'application/json',
#    'Authorization': f'Bearer {Skey}',
#    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
#    'Content-Type': 'application/json'
# }

# response = requests.request("POST", Baseurl, headers=headers, data=payload)
# data = response.json()
# print(data)

###########################level validation######################
# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# load_dotenv()
# print(os.getenv('OPENAI_BASE_URL'))
# from prompts import validation_prompt, symptom_converter
# from guideline import basic_questions, switcher
# client = OpenAI()
# def validate(main_complain, guideline):
#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{
#             "role": "user",
#             "content": validation_prompt.format(main_complain=main_complain, guideline=guideline) 
#         }]
#     )
#     return completion.choices[0].message.content
# ret = []
# for i, profile in read_profiles(67):
#     guidelines = "Basic Questions \n" + basic_questions
#     symptoms = symptom_converter.invoke({"message": profile})
#     for symptom in symptoms.valid_symptom:
#         guidelines = guidelines + "\n"+symptom.replace('_', ' ').title()+"\n" + switcher[symptom]
#     level = validate(profile, guidelines)
#     ret.append(level)
#     print(level)
# print(ret)

# output
# ret = [
#     "Urgent", "Routine", "Routine", "Routine", "Emergent", "Emergent", 
#     "Routine", "Urgent", "Routine", "Urgent", "Urgent", "Urgent", 
#     "Urgent", "Urgent", "Emergent", "Emergent", "Routine", "Urgent", 
#     "Routine", "Routine", "Urgent", "Routine", "Emergent", "Emergent", 
#     "Routine", "Emergent", "Urgent", "Emergent", "Routine", "Emergent", 
#     "Urgent", "Routine", "Urgent", "Routine", "Routine", "Emergent", 
#     "Urgent", "Urgent", "Routine", "Routine", "Routine", "Urgent", 
#     "Routine", "Routine", "Emergent", "Emergent", "Routine", "Routine", 
#     "Emergent", "Emergent", "Routine", "Routine", "Emergent", "Emergent", 
#     "Routine", "Emergent", "Routine", "Emergent", "triggering Azure OpenAI's content management policy", "Urgent",
#     "Urgent", "Routine", "Urgent", "Urgent", "Routine", "Routine",
#     'Routine', 'Routine', 'Emergent', 'Routine', 'Routine', 'Routine',
#     'Routine', 'Routine', 'Routine', 'Routine', 'Urgent', 'Routine',
#     'Routine', 'Urgent', 'Urgent', 'Routine', 'Routine', 'Routine',
#     'Urgent', 'Urgent', 'Emergent', 'Routine', 'Urgent', 'Routine',
#     'Urgent', 'Urgent', 'Routine', 'Routine', 'Routine', 'Routine',
#     'Urgent', 'Emergent', 'Urgent', 'Urgent', 'Routine'
# ]
# df = pd.read_excel('add_time_filtered_reddit_info.xlsx')
# answer = df['分诊分级'].tolist()
# correct = 0
# wrong = []
# for i in range(101):
#     if answer[i][0] == ret[i][0]: correct += 1
#     else: wrong.append(i)
# print(correct)
# print(wrong)