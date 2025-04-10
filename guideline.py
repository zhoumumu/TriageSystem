############### Single-Qs Version ########################
trauma_injury = {
1: "Wait, was there trauma or injury to the eye?",
2: "Have you experienced any penetration of the globe, severe blunt trauma, foreign body exposure, chemical burns, or recent eye surgery?",
3: "Does the visual complaints persistent?",
4: "Was there surgery or procedure on the eye recently?",
}
trauma_injury_trans = {
    1:(2, 4), 2:('E', 3), 3:('E', 'U'), 4:('E', 'R')
}

vision_loss = {
1: "Have the symptoms been present for a new onset, or for less than a few days, or for many months?",
2: "Is it total darkness or part of the vision missing?"
}
vision_loss_trans = {
   1:(2, 'U', 'R'), 2:('E', 'U')
}

vision_changes = {
1: "Have the symptoms been present for a new onset to a week, or longer than few weeks?",
}
vision_changes_trans = {1:('U', 'R')}

eye_pain = {
1: "Have the symptoms been present for a new onset, or longer than few days?",
2: "Is the symptom worsening in nature?",
3: "Is the eye pain accompanied by eye redness?",
4: "Is the eye pain accompanied by a decrease in vision?",
5: "Is the patient a contact lens wearer?"
}
eye_pain_trans = {
   1:('E', 2), 2:('E', 3), 3:(5, 4), 4:('U', 'R'), 5:('E', 'U')
}

flashes_floaters = {
1: "Have the symptoms been present for a new onset to a week, or longer than few weeks?",
2: "Is the patient myopic (nearsighted)?",
3: "Has the patient had LASIK or refractive surgery?",
4: "Are the light flashes and floaters accompanied by shadows in the peripheral vision?"
}
flashes_floaters_trans = {
   1:(2, 'R'), 2:('E', 3), 3:('E', 4), 4:('E', 'U')
}

redness = {
1: "Have the symptoms been present for a new onset to a week, or longer than few weeks?",
2: "Is the patient a contact lens wearer?",
3: "Is the redness accompanied by nausea and foggy vision?",
4: "Is the red eye accompanied by pain?",
5: "Is the pain worsening in nature?"}
redness_trans = {
   1:(2, 'R'), 2:('E', 3), 3:('E', 4), 4:(5, 'U'), 5:('E', 'U')
}

discharge = {
1: "Have the symptoms been present for a new onset to a week, or longer than few weeks?",
2: "Is the patient a contact lens wearer?",
3: "Is the discharge accompanied by eye redness?",
4: "Is the redness accompanied by nausea and foggy vision?",
5: "Is the red eye accompanied by pain?",
6: "Is the pain worsening in nature?",
7: "Is the discharge accompanied by pain and vision loss?",
8: "Does the discharge or tearing cause the eyelids to stick together?"
}
discharge_trans = {
   1:(2, 'R'), 2:('E', 3), 3:(4, 7), 4:('E', 5),
   5:(6, 'U'), 6:('E', 'U'), 7:(6, 8), 8:('U', 'R')
}

photophobia = {
1: "Is the photophobia accompanied by redness?",
2: "Is the patient a contact lens wearer?",
3: "Is the photophobia accompanied by a decrease in vision?",
4: "Does the patient have any other eye symptoms?"
}
photophobia_trans = {
    1:(2, 3), 2:('E', 'U'), 3:('U', 4), 4:('R', 'R')
}

lid = {
    1: "Is there a sudden drooping of the eyelid in one eye?",
    2: "Are there bumps, lumps or swelling on the eyelid in one eye?",
    3: "Is the symptom accompanied by pain or vision loss?"
}
lid_trans = {
    1:('U', 2), 2:(3, 'R'), 3:('U', 'R')
}

burns = {1: "Does the patient have any other eye symptoms?"}
burns_trans = {1:('R', 'R')}

itching = {1: "Does the patient have any other eye symptoms?"}
itching_trans = {1:('R', 'R')}

tearing = {1: "Does the patient have any other eye symptoms?"}
tearing_trans = {1:('R', 'R')}

white_pupil = {1: "Let me check, is the patient a child?"}
white_pupil_trans = {1:('E', 'R')}

pupil_size_trans = {1:('E', 'R')}
referral_trans = {1:('E', 'U')}
glasses_lenses_trans = {1:('U', 'U')}


# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# llm = ChatOpenAI(model="deepseek-r1")
# level_parsing_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Give the <answer> a integer representation in a range given by the options in the <question>. \
#                 For example, \
#                 <question>: Have the symptoms been present for a new onset, or for less than a few days, or for many months? \
#                 <answer>: I have my eye pain suddenly in this morning. \
#                 You should return just a 0(no any other words), ranking the options 0,1,2 one by one. \
#                 If the question is a yes-no question, return 0 for a yes-answer, return 1 for a no-answer."),
#     ("human", "<question>: {question} \n <answer>: {answer}"),
# ])
# answer_converter = level_parsing_prompt | llm

# class SymtomDAG():
#     def __init__(self, trans, symtom=None):
#         self.question_list = symtom
#         self.conditional_graph = trans

#     def getNextNum(self, last_Q, ans):
#         option = answer_converter.invoke({
#             "question": self.question_list[last_Q],
#             "answer": ans
#         })
#         return self.conditional_graph[last_Q][int(option.content)]

# switcher = {
#     "vision_loss": SymtomDAG(vision_loss_trans, vision_loss),
#     "vision_changes": SymtomDAG(vision_changes_trans, vision_changes),
#     "eye_pain": SymtomDAG(eye_pain_trans, eye_pain),
#     "flashes_floaters": SymtomDAG(flashes_floaters_trans, flashes_floaters),
#     "redness": SymtomDAG(redness_trans, redness),
#     "discharge": SymtomDAG(discharge_trans, discharge),
#     "trauma_injury": SymtomDAG(trauma_injury_trans, trauma_injury),
#     "photophobia": SymtomDAG(photophobia_trans, photophobia),
#     "lid": SymtomDAG(lid_trans, lid),
#     "burns": SymtomDAG(burns_trans, burns),
#     "itching": SymtomDAG(itching_trans, itching),
#     "tearing": SymtomDAG(tearing_trans, tearing),
#     "white_pupil": SymtomDAG(white_pupil_trans, white_pupil),
#     "pupil_size": SymtomDAG(pupil_size_trans),
#     "referral": SymtomDAG(referral_trans),
#     "glasses_lenses": SymtomDAG(glasses_lenses_trans)
# }

################# Decision-tree Version #############################
basic_questions = '''
Q1: Does the patient has any eye complaints? 
Yes →  Q2
No →  Q10

Q2:Is the issue affecting one eye or both? left or right eye?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Do you have any other symptoms in listed('vision_loss_change', 'eye_pain', 'flashes_floaters', 'redness_discharge', 'photophobia', 'lid', 'pupil')?
Yes → Should not see this condition
No → Q8

Q8: Have the symptoms been present for a new onset(within last few day), or for many weeks or months? Are the symtoms comes and goes?
within last few days → Q9
Longer than few weeks→ Q10

Q9: Is the symptom severe and worsening? 
Yes → Emergent
No →  Urgent

Q10: Are there any other eye related problems?
patient lost or broken glasses or contact lenses -> URGENT
patient been judged Emergent from another physician → EMERGENT
Other eye-related issues → Artificial transposon
'''

vision_loss_change = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Is patient's vision change or loss accompanied by pain?
Yes→ Q8
No → Vision Loss → Q9
No →Vision Changes → Q11

Q8: Is the pain worsening?
Yes → Emergent
No → Urgent

Q9: Have the symptoms been present for a new onset, or for less than a few days, or for many months? Are the symtoms comes and goes?
New onset → Q10
Few days to a week → Urgent
Longer than few weeks→ Q16

Q10: Is it total darkness or part of the vision missing?
Total → EMERGENT
Part → Urgent

Q11: What is the problem of vision change?
Blurriness →  Q12
Diplopia (double vision) or other distorted vision → Q13

Q12:Does the vision change affect only near or distance work, or both?
Both →Q13
Only at distance or only at near →Q16

Q13: Have the symptoms been present for a new onset, or for less than a few days, or for many months? 
New onset to a week → Q14
Longer than few weeks→  Q16

Q14: Are the symptoms constant or do they come and go? Do they occur under certain conditions?
Constant → Q15
come and go → Q16


Q15: Is the vision change accompanied by acute eye redness or headache? 
Yes → EMERGENT
No →  Urgent

Q16: Is the vision change accompanied by light sensitivity?
Yes → URGENT
No → Q17

Q17: Are there any other symptoms?
whatever condition → ROUTINE
'''

eye_pain = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset → EMERGENT   
Few days to few weeks→ Q8

Q8: Is the symptom worsening? 
Yes→ EMERGENT  
No → Q9

Q9: Is the eye pain accompanied by eye redness and/or a decrease in vision? 
Redness/both→ Q10
Only a decrease in vision → Urgent  
Neither→  Q11

Q10: Is the patient a contact lens wearer?
Yes→ EMERGENT
No → Urgent

Q11: Are there bumps, lumps or swelling on the eyelid in one eye?  
Yes → URGENT
No → Q12

Q12: What's the area of pain and how severe it is?
Moderate to severe → URGENT
Mild → Q13

Q13: Are there any other symptoms?
whatever condition → Routine
'''

flashes_floaters = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset to a week →  Q9
Longer than few weeks→ Q8

Q8: Have these flash or floaters increased in amount or size? 
Yes→ Q9
No→ Q12

Q9:Is the patient myopic (nearsighted)? 
Yes → EMERGENT
No →  Q10

Q10: Has the patient had LASIK or refractive surgery?  
Yes → EMERGENT
No →  Q11

Q11: Are the light flashes and floaters accompanied by shadows in the peripheral vision? 
Yes → EMERGENT
No → URGENT

Q12: Are there any other symptoms?
whatever condition → Routine
'''

redness_discharge = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset to a week →  Q8
Longer than few weeks→ Q16

Q8: Is the patient a contact lens wearer?  
Yes → EMERGENT
No, and patient has redness → Q9
Else → Q14

Q9: Is the redness accompanied by nausea and foggy vision? 
Yes → EMERGENT
No → Q10

Q10: Is the red eye accompanied by pain?
Yes →  Q11
No →  Q12

Q11: Is the pain worsening?
Yes → Emergent
No → Urgent

Q12: Is the redness accompanied by photophobia?
YES → URGENT
No, and patient has discharge → Q14
Else → Q13

Q13: Is the redness severe or getting worse?
YES → URGENT
No → Q15

Q14: Is the discharge accompanied by pain and vision loss?
Yes →  Q11
No →  Q15

Q15: Does the discharge or tearing cause the eyelids to stick together?
Yes → URGENT
No → Q16

Q16: Are there any other symptoms?
whatever condition → Routine
'''

photophobia = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Is the photophobia accompanied by redness?
YES → Q8
NO → Q9

Q8: Is the patient a contact lens wearer?  
Yes → EMERGENT
No → URGENT

Q9: Is the photophobia accompanied by a decrease in vision?
Yes →URGENT
No →  Q10

Q10: Are there any other symptoms?
whatever condition → Routine
'''

lid = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7: Is there a sudden drooping of the eyelid in one eye?  
Yes → URGENT 
No →  Q8

Q8: Are there bumps, lumps or swelling on the eyelid in one eye?  
Yes →  Q9
No → Q11

Q9: Is the symptom accompanied by pain or vision loss?
Pain → Q10  
Vision loss → Q11
Both→ Q12
No other symptom accompanied → Q13

Q10: Is the pain worsening? 
Yes→ EMERGENT  
No →  URGENT

Q11: Is there a sudden and complete loss of vision?
Yes → EMERGENT  
No → Urgent 

Q12: Is the pain worsening?And Is there a sudden and complete loss of vision?
Either or both → EMERGENT  
Neither → Urgent 

Q13: Are there any other symptoms?
whatever condition → Routine
'''

pupil = '''
Q1: Does the patient have any eye complaints?
Yes →  Q2
patient been judged Emergent from another physician → EMERGENT
patient lost or broken glasses or contact lenses -> URGENT

Q2:Is the issue affecting one eye or both?
whatever condition → Q3

Q3: Has there been any eye injury, foreign body entry, or chemical burn within last few days?
Yes, trauma or injury → Q4
Yes, foreign body go into eye → Emergent
Yes, chemical burn → Emergent and give burn instructions
None of them → Q6

Q4: What type of eye injury occurred, and how it happened?
Globe penetration or severe blunt trauma → EMERGENT
Blunt trauma → Q5

Q5: Are the patient still experiencing visual problems or ongoing pain?
Yes→ EMERGENT
No → Urgent

Q6: Was there surgery or procedure on the eye in last few weeks? Are the symptoms persistent post-operative symptoms?
Both Yes→ EMERGENT
Any no (e.g., the surgery was not recent) → Q7

Q7:  Is there a sudden change in the size of one pupil?  
Yes → EMERGENT
No → Q8

Q8: Is the pupil abnormal with persistent visual symptoms?
Yes → Urgent
No → Q9

Q9: Are there any other symptoms?
whatever condition → Routine
'''

switcher = {
    'vision_loss_change': vision_loss_change,
    'eye_pain': eye_pain,
    'flashes_floaters': flashes_floaters,
    'redness_discharge': redness_discharge,
    'photophobia': photophobia,
    'lid': lid,
    'pupil': pupil
}