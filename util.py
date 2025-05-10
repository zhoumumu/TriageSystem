import os, re
import pandas as pd

def read_profiles(num_start=1, num_end=-1, specify=None): # start from 1
    # 1.get [start:end], closed range
    # 2.get [start:]
    # 3.get specified
    # 4.get all
    # with open("profiles_reddit-train.txt", 'r', encoding='utf-8') as file:
    with open("profiles_4o.txt", 'r', encoding='utf-8') as file:
        doc = file.read()
    # profiles = doc.split("\n##########\n")
    profiles = doc.split("\n---\n")
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
#     os.listdir('reddit_4onurse+dspatient'),
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
#dsv3 + 4o-mini converter: [7, 8, 10, 11, 12, 14, 15, 17, 21, 23, 26, 29, 31, 32, 34, 35, 36, 37, 38, 40, 41, 42, 43, 45, 48, 54, 60, 63, 65, 67, 76, 80, 82, 83, 87, 92, 93]
#reddit_4onurse+dspatient:[0, 6, 8, 9, 11, 12, 14, 15, 19, 25, 26, 29, 30, 31, 32, 34, 36, 40, 41, 43, 45, 62, 63, 67, 68, 70, 76, 79, 82, 83, 90, 91, 92, 93, 99, 100]

################# check skipped inquiry
# skipped = []
# for f in os.listdir("reddit_train"):
#     with open("reddit_train/"+f, 'r') as file:
#         content = file.read()
#         if content.count("Nurse:") == 1: skipped.append(int(f.split('_')[1]))
# print(skipped)
# [108, 157, 174, 18, 203, 211, 23, 244, 250, 300, 315, 337, 397, 39, 402, 416, 423, 438, 442, 451, 461, 484, 516, 524, 529, 575, 584, 586, 58, 60, 628, 662, 675, 688, 70, 717, 718, 737, 748, 758, 773, 8]

################# check restart
# abnormal = []
# marks = ["hi", "hey", "hello"]
# for f in os.listdir("reddit_train"):
#     with open("reddit_train/"+f, 'r') as file:
#         content = file.read()
#         count = 0
#         for word in marks:
#             match = re.findall(fr'\b{word}\b', content, re.IGNORECASE)
#             count += len(match)
#         if count > 2: abnormal.append(int(f.split('_')[1]))
# print(abnormal)
# [102, 109, 120, 147, 149, 154, 155, 158, 15, 160, 162, 164, 171, 177, 17, 183, 187, 199, 1, 201, 204, 208, 218, 228, 229, 233, 239, 256, 258, 25, 263, 269, 26, 270, 274, 275, 278, 282, 283, 284, 288, 291, 301, 303, 306, 313, 325, 327, 336, 341, 355, 360, 371, 375, 398, 401, 405, 410, 415, 421, 439, 43, 444, 446, 454, 460, 465, 467, 468, 475, 47, 485, 490, 492, 4, 
# 506, 510, 526, 52, 532, 543, 545, 547, 564, 571, 57, 587, 588, 591, 605, 606, 60, 621, 624, 626, 627, 645, 654, 656, 671, 672, 674, 680, 681, 687, 688, 68, 690, 691, 697, 698, 69, 702, 704, 706, 70, 710, 712, 713, 714, 718, 721, 728, 72, 732, 747, 759, 761, 765, 77, 787, 82, 84, 97]

################# test API key
# from dotenv import load_dotenv
# import os
# load_dotenv()
# print(os.getenv('OPENAI_BASE_URL'))
# # Way 1
# from openai import OpenAI
# client = OpenAI()
# completion = client.chat.completions.create(
#   model="deepseek-v3",
#   messages=[
#       {
#           "role": "user",
#           "content": "Hi"
#       }
#   ]
# )
# print(completion)
# # Way 2
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model='deepseek-v3', api_key="", base_url="")
# print(llm.invoke("Hi, who are you"))

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