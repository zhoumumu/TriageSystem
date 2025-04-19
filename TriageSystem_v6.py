import os, random
from dotenv import load_dotenv
import openai
# from docs import patient_prompt, nurse_prompt
from prompts import patient_prompt, nurse_prompt_without_guidance
from util import read_profiles
load_dotenv()
print(os.getenv('OPENAI_BASE_URL'))

# def read_profiles(num_start, num_end):
#     profiles = []
#     with open("profiles_4o.txt", 'r') as file:
#         doc = file.readlines()
#     temp = ""
#     for line in doc:
#         if "Caller Information" in line:
#             profiles.append(temp)
#             temp = line
#         else:
#             temp += line
#     profiles.append(temp)
#     return profiles[num_start:num_end]

class ChatMimicApp:
    def __init__(self, nurse_sys, caller_sys):
        self.nurse_history = [{"role": "system", "content": nurse_sys}] #2208
        self.caller_history = [{"role": "system", "content": caller_sys}] #913
        self.client = openai.OpenAI()
        self.nurse_completion_tokens = 0
        self.nurse_prompt_tokens = 0
        self.caller_completion_tokens = 0
        self.caller_prompt_tokens = 0

    def nurse_speak(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.nurse_history
        )
        res = response.choices[0].message.content
        print(res)
        idx = res.find('Talking to the Caller:')
        if idx != -1: res = res[idx+23:]

        self.nurse_history.append({"role": "user", "content": "Nurse: "+res})
        self.caller_history.append({"role": "user", "content": "Nurse: "+res})
        self.nurse_completion_tokens += response.usage.completion_tokens
        self.nurse_prompt_tokens += response.usage.prompt_tokens
        return response.choices[0].message.content
    
    def caller_speak(self):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.caller_history
        )
        res = response.choices[0].message.content
        self.nurse_history.append({"role": "user", "content": "Caller: "+res})
        self.caller_history.append({"role": "user", "content": "Caller: "+res})
        self.caller_completion_tokens += response.usage.completion_tokens
        self.caller_prompt_tokens += response.usage.prompt_tokens
        print(res)
        return res

    def chat(self):
        whoisspeaking = random.randint(0, 1)
        res = ""
        while "[Hang Up]" not in res:
            whoisspeaking = 1 - whoisspeaking
            if whoisspeaking == 0:
                res = self.nurse_speak()
            else:
                res = self.caller_speak()
        return self.nurse_history


if __name__ == "__main__":
    for i, profile in read_profiles(99):
        app = ChatMimicApp(nurse_prompt_without_guidance, patient_prompt.format(profile=profile))
        messages_history = app.chat()
        print(app.nurse_prompt_tokens, app.nurse_completion_tokens)
        print(app.caller_prompt_tokens, app.caller_completion_tokens)
        with open("prompt_4o/prompt_%d.txt"%(i), "w") as file:
            for s in messages_history[1:]:
                file.write(s["content"]+'\n')
        del app
