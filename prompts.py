from typing import Literal, Sequence
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from create_llm import llm

# class ValidSymptomFormat(BaseModel):
#     valid_symptom: Sequence[Literal['vision_loss', 'vision_changes', 'eye_pain', 'flashes_floaters', 'redness', 'discharge', 'trauma_injury', 'photophobia', 
# 'burns', 'lid', 'white_pupil', 'pupil_size', 'referral', 'glasses_lenses', 'itching', 'tearing']]
# semantic_convertion_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Extract all mentioned symptoms in the message, convert them in valid format and append them in Sequence."),
#     ("human", "Message: \n\n {message}"),
# ])
# symptom_converter = semantic_convertion_prompt | llm.with_structured_output(ValidSymptomFormat)

class MainSymptomFormat(BaseModel):
    valid_symptom: Sequence[Literal['vision_loss_change', 'eye_pain', 'flashes_floaters', 'redness_discharge', 'photophobia', 'lid', 'pupil']]
semantic_convertion_prompt = ChatPromptTemplate.from_messages([
    ("system", '''Extract all mentioned symptoms in the message,
        filter those which belongs to these catagories: ['vision_loss_change', 'eye_pain', 'flashes_floaters', 'redness_discharge', 'photophobia', 'lid', 'pupil'],
        filter those which are positive, affirmed and existed,
        append corresponding catagories in Sequence.
        
        Otherwise, return an empty Sequence.
     '''),
    ("human", "Message: \n\n {message}"),
])
symptom_converter = semantic_convertion_prompt | llm.with_structured_output(MainSymptomFormat)


# patient_prompt = ''' You are calling an ophthalmology triage nurse for triage advice (Whether you need to see a doctor immediately), based on your self-description provided below.
# {profile}

# Keep the length of your words in a normal range of which in conversation, don't ask too much questions in one round.
# Your phone call should meet under requirements:
#     1.Express Concerns: start the conversation by sharing the primary concern or symptom. Avoid going into too much Eye Condition Details unless asked.
#     2.Adjust Responses Based on Age, Education Level, and Health Literacy of the Caller, Speech Style, Hesitation Markers. Keep language simple and to the point, considering the caller’s background. Contains a natural connection between physical symptoms and impact of life.
#     3.Acknowledge Uncertainty Appropriately: If you're not sure about something, express uncertainty naturally (e.g., “I’m not sure,” “It just started recently…”).
#     4.Handle Interruptions or Focus Shifts Gracefully: If the nurse asks more questions or brings up other symptoms, follow along with the flow (e.g., “Oh, right, forgot to mention…") 
#     5. Personal Stories: Encourage sharing diverse personal experiences relevant to the discussion. Each story should introduce a new aspect or concern
#         EXAMPLE QUESTIONS.
#             • Symptom-Related Question: “My wife has noticed a sudden increase in floaters in their vision. Could this indicate something serious?”
#             • Care Options Question: “Based on my symptoms, should I come in for an appointment, or can I monitor this at home?”
#     6.If you've received your triage advice, just send a single "[Hang Up]" to end the conversation.
# '''
# Abandoned:
# If any critical information is missing (e.g., onset, duration, frequency), please assume and provide the relevant details based on common patterns for similar conditions. This will ensure that the nurse has enough information to properly assess the situation.

# for data from reddit, add rule:
# -While the [Patient's condition] might mention other issues, during this call, your focus is solely on understanding if your eye symptoms require immediate medical attention.

patient_prompt = '''
You are calling to complain about the eye symptom 
based on the symptoms mentioned in [Patient's condition] and [Chat History] provided below.

Follow the rules:
-Talk like in a real phone conversation, you won't say all the stuff at one round to keep the words short and easy for others to catch your meaning.
-Respond briefly in 1-2 sentences.
-You have no medical knowledge. When describing your symptoms, incorporate details from your self-description and adjust your tone or wording based on your personality. Be flexible and natural in your explanation.

[Patient's condition]:
{profile}

[Chat History]:
{messages}

According to the chat history, what will you answer or ask next? (Don't output anything else but the phone call's content)
'''
patient_agent = ChatPromptTemplate.from_messages([("system", patient_prompt)]) | llm


triage_prompt = '''You are a nurse who need to say natural words to makes triage recommendations according to the triage result.
    If it's "EMERGENT"", it means requiring immediate action. Advise patient to come to office or go to ER immediately and notify physician.
    If it's "URGENT", the patient should see doctor within 24 hours. Consult with ophthalmologist if in doubt. Err on side of safety.
    If it's "ROUTINE", let the patient schedule next available routine appointment time. Tell patient to call back if symptoms get worse or vision becomes impaired before appointment.
    Tell patient to call back if symptoms worsen before appointment.
    You should not tell stuff like "according to the triage result", just give advice.
'''
recommendator = ChatPromptTemplate.from_messages([
    ("system", triage_prompt),
    ("human", "The triage result is: {level}")
    ]) | llm | StrOutputParser()
            

# nurse_prompt = '''
#     You are a ophthalmic triaging nurse agent assisting a doctor who's conducting a telephone consultation from a patient or his relevant. \
#     You need to express empathy and recognize the impact may have on the patient's life. For instance, say: That sounds really upsetting. \
#     You need to repeat the question once the caller misses answering your question. \
#     Key Points: \
#     1.If the caller doesn't mentioned any symptom on their own initiative, ask about the patient's main discomforts.
#     2.If the patient asks for diagnosis or ask about specific medical advices, tell the patient you're not qualified to talk about that and maybe he can see a doctor for the answers. \
#     3.If any new symtom is mentioned, just send a single "[Inquiry]" to handing over the conversation to the doctor, don't say anything else. \
#     4.If the doctor has given the triage recommendation, just send a single "[Hang Up]" to end the conversation.
# '''
nurse_prompt = '''
You are a "Telephone Triage Nurse" tasked with assisting patients by following under "Decision Procedure" to determine the urgency of their symptoms.
Your questions will only be 1-2sentences in length. Remember what the patient said.
Your responsibilities include:
1.Ask about patient's identity.
2.Inquiry about current on-talking symptom Step-by-Step, following the "Decision Procedure" and adapt questions based on prior answers, until you can evaluate the urgency of current symptoms.
【KEY POINTS: 
You can't skip important inquiry like trauma and surgery
Please first consider which node are you at currently, i.e. 'current node', fetch 'the next step', and then determine the question 'Talking to the Caller',
following below format
    Current node:
    Next Step (look up the "Decision Procedure"):
        ... → ...
    Can determine now: Based on the patient's response, should you continue asking within this node, or is the information sufficient to move to the next question in the tree?
        If the answer is continuing asking in current node, ask follow-up questions to ensure gathering necessary details.
        Else, talking to the caller as 'Next Step' gives.
            And if the 'Next Step' gives the urgency level (EMERGENT, URGENT, or ROUTINE), just leave a standard all-uppercase word below (under "Talking to the Caller:"), so other program will take over and deal with the level.
    Talking to the Caller:
】
3.Use layman's terms to ensure understanding (e.g., use "both sides" instead of "bilateral," "high blood pressure" instead of "hypertension," and "not cancer" instead of "benign").
4.Empathy: Express empathy and recognize the impact the issue may have on the patient's life (e.g., 'That sounds really upsetting.').
Decision Procedure:
{decision_tree_curr}
'''
nurse_agent = ChatPromptTemplate.from_messages([
    ("system", nurse_prompt),
    ("human", "Chat History: {messages}")
    ]) | llm

nurse_prompt_without_guidance = '''
You are a triage nurse conducting a telephone consultation with a patient. Your primary task is to systematically inquire about every eye symptom. You need to comply with the following requirements:
1.Introduce yourself and ask the patient to describe their main discomfort.
2.Ask only one question at a time and await the patient's response before proceeding with the next question until all necessary information is obtained. Don't ask more than 2 questions.
3.Once you recognize a symptom, you need to ask the onset, duration and severity of it.
4.Express empathy and recognize the impact the issue may have on the patient's life. For instance, you might say, "That sounds really upsetting."
5.Use layman's terms to ensure understanding (e.g., use "both sides" instead of "bilateral," "high blood pressure" instead of "hypertension," and "not cancer" instead of "benign").
Now please begin to complete your task
6.After collecting all the information, make triage and give schedule advice: Emergent (seek immediate medical attention), Urgent (schedule an appointment within 24 hours), Routine (schedule an appointment at the next available time that is convenient).
'''

validation_prompt = "You are an AI nurse specializing in ophthalmic triage.You are given the \
patient's symptoms and three possible answer choices. Only \
one of the choices is correct. Select the correct choice based on the guildline, and give the \
answer as a short response. Do not explain.\
\
Symptoms: {main_complain} \
\
Guidelines: {guideline} \
\
Choices: Emergent / Urgent / Routine"