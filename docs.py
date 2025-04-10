import os
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import Literal

chat_history = '''
Hello, I'm Sarah Martinez. Recently, I've started seeing flashes and a lot of floaters in both eyes. Is this something that usually warrants immediate medical attention?
Hi Sarah, it's important to address these symptoms promptly. You mentioned seeing flashes and more floaters. Did these flashes start recently? Are they accompanied by any shadows in your peripheral vision, or have you had any eye surgeries or significant nearsightedness in the past?
Yes, the flashes began just a few days ago, and I haven't noticed any shadows in my vision. I haven't had any eye surgeries, but I am quite nearsighted. Could my nearsightedness be linked to these symptoms?
Thank you for providing that information, Sarah. Given your high level of nearsightedness and the recent onset of flashes and floaters, this situation could be more serious. It's advisable to see an ophthalmologist as soon as possible to rule out any retinal issues, which are more common in people with significant myopia. This is considered an emergent condition because it's important to quickly determine the cause and prevent any potential complications. Is there anything else about your eyes that's been bothering you recently, or any other symptoms you've noticed?
No, there haven't been any other new symptoms. Should I go directly to an emergency room, or would it be better to schedule an appointment with an ophthalmologist?
'''
triage_question = "based on the patient's response, categorize each symptom in the GUIDELINE as emergent, urgent, routine or not mentioned,\
    and get the most severe level as the summary(emergent, urgent, routine), \
    and collect the key descriptions of symptoms. \
    Give a structured output as result." 
# hard to design corresponding prompt of triage_question
# class Questionary():
#     def __init__(self,
#         Summary: Literal["emergent", "urgent", "routine"],
#         Vision_Loss="not mentioned",
#         Vision_Changes="not mentioned",
#         Pain="not mentioned",
#         Flashes_or_Floaters="not mentioned",
#         Redness_or_Discharge="not mentioned",
#         Photophobia="not mentioned",
#         Burn="not mentioned",
#         Foreign_Body="not mentioned",
#         Trauma="not mentioned",
#         Other="not mentioned"
#     ):
#         self.Vision_Loss = Vision_Loss
#         self.Vision_Changes = Vision_Changes
#         self.Pain = Pain
#         self.Flashes_or_Floaters = Flashes_or_Floaters
#         self.Redness_or_Discharge = Redness_or_Discharge,
#         self.Photophobia = Photophobia,
#         self.Burn = Burn,
#         self.Foreign_Body = Foreign_Body,
#         self.Trauma = Trauma,
#         self.Other = Other,
#         self.Summary = Summary
class Questionary(BaseModel):
    Vision_Loss: Literal["emergent", "urgent", "routine", "not mentioned"]
    Vision_Changes: Literal["emergent", "urgent", "routine", "not mentioned"]
    Pain: Literal["emergent", "urgent", "routine", "not mentioned"]
    Flashes_or_Floaters: Literal["emergent", "urgent", "routine", "not mentioned"]
    Redness_or_Discharge: Literal["emergent", "urgent", "routine", "not mentioned"]
    Photophobia: Literal["emergent", "urgent", "routine", "not mentioned"]
    Burn: Literal["emergent", "urgent", "routine", "not mentioned"]
    Foreign_Body:Literal["emergent", "urgent", "routine", "not mentioned"]
    Trauma: Literal["emergent", "urgent", "routine", "not mentioned"]
    Other: Literal["emergent", "urgent", "routine", "not mentioned"]
    Lid:Literal["emergent", "urgent", "routine", "not mentioned"]
    Pupil:Literal["emergent", "urgent", "routine", "not mentioned"]
    Summary: Literal["emergent", "urgent", "routine"]
    Description: str

RAG_PROMPT = hub.pull("rlm/rag-prompt") # ChatPromptTemplate
# # print(RAG_PROMPT) #不用API也能拉，应该是不要钱，不然create from raw messsage写死这个prompt
# llm = ChatOpenAI(model="gpt-4-turbo")
# # rag_chain = RAG_PROMPT | llm | StrOutputParser()
# rag_chain = RAG_PROMPT | llm.with_structured_output(Questionary)
# condition = rag_chain.invoke({"context": guideline+'\n'+'\n'+chat_history, "question": triage_question})
# print(condition)

generator_guideline='''
1. **Sudden, painless, severe complete loss of vision**
   - Vision disappeared completely without any pain.
   - Everything went black suddenly and painlessly.
   - Lost vision instantly without discomfort.
   - Vision vanished abruptly, no pain involved.
   - Sight was gone all at once, no pain felt.

2. **Loss of vision after surgery or procedure**
   - Vision faded away after the operation.
   - Couldn't see anything post-surgery.
   - Experienced blindness following the procedure.
   - Sight was lost shortly after surgery.
   - Vision disappeared soon after the procedure.

3. **Curtain effect vision loss**
   - Felt like a curtain dropped over the eyes.
   - Vision was suddenly blocked as if by a drape.
   - A shadow fell over sight like a veil.
   - Seemed like a blind was pulled over vision.
   - Vision went dark from the top down, like a curtain.

4. **New partial vision loss or area of complete loss**
   - Suddenly couldn't see part of the field of view.
   - A new blind spot appeared in vision.
   - Part of sight has gone missing.
   - Experienced a sudden patch of vision loss.
   - Noticed a new area where vision is absent.

5. **Subacute loss of vision evolving over a few days to a week (persistent or intermittent)**
   - Vision has been gradually fading over several days.
   - Sight has been coming and going over the week.
   - Slowly losing vision day by day.
   - Vision has intermittently worsened over a week.
   - Sight has been diminishing gradually over days.

6. **Transient loss of vision**
   - Vision went out temporarily but returned.
   - Had a brief episode of blindness.
   - Sight was lost for a short moment.
   - Experienced a temporary blackout in vision.
   - Vision disappeared briefly and came back.

7. **Vision changes after surgery or procedure**
   - Vision altered following the surgery.
   - Noticed changes in sight after the procedure.
   - Vision was different post-operation.
   - Experienced vision shifts after surgery.
   - Sight was altered following the procedure.

8. **Sudden onset of diplopia (double vision)**
   - Started seeing double all of a sudden.
   - Vision split into two images instantly.
   - Suddenly everything appears doubled.
   - Experienced immediate double vision.
   - Objects suddenly appear duplicated.

9. **Sudden onset of distorted vision, spot of blurring, or missing area**
   - Vision became warped all of a sudden.
   - A blurred spot appeared in sight instantly.
   - Noticed a missing patch in vision suddenly.
   - Experienced immediate distortion in sight.

10. **Sudden or gradual blurred vision in a specific area**
    - Blurriness developed quickly in one spot.
    - Vision became hazy in a specific area over time.
    - Noticed a gradual blur in one part of sight.
    - A sudden blur appeared in a particular spot.
    - Vision gradually blurred in one region.

11. **Difficulty with near or distance work, fine or print**
    - Struggling to focus on close tasks.
    - Having trouble seeing far away.
    - Difficulty reading fine print.
    - Finding it hard to see things up close.
    - Can't focus well on distant objects.

12. **Blurry vision only at distance or only at near in patients in their late 30s or 40s (improves with blinking or eye drops)**
    - Distance vision blurs but clears with blinking.
    - Near vision is fuzzy but eye drops help.
    - Blurriness at far distances, resolves with blinking.
    - Close-up vision is unclear, better with drops.
    - Blurry vision at near, improves with blinking.

13. **Acute, rapid onset of eye pain or discomfort**
    - Eye pain started suddenly and intensely.
    - Felt sharp discomfort in eye all at once.
    - Experienced immediate eye pain.
    - Rapid onset of discomfort in the eye.
    - Eye pain hit suddenly.

14. **Acute eye pain with nausea and foggy vision**
    - Sharp eye pain accompanied by nausea.
    - Felt nauseous with eye pain and cloudy sight.
    - Eye pain with queasiness and blurry vision.
    - Nausea and foggy vision alongside eye pain.
    - Eye hurt severely with nausea and haze.

15. **Progressively worsening ocular pain**
    - Eye pain has been getting worse over time.
    - Pain in the eye is becoming more severe.
    - Eye hurts more and more each day.

16. **Worsening pain after surgery or procedure**
    - Pain increased following the operation.
    - Discomfort worsened after the procedure.
    - Experienced more pain post-surgery.
    - Pain intensified after the procedure.
    - Post-surgery pain has been getting worse.

17. **Mild ocular pain accompanied by redness and/or decrease in vision**
    - Eye feels slightly painful with redness.
    - Mild pain with some vision loss and redness.
    - Eye is red and slightly sore.
    - Vision has decreased with mild eye pain.
    - Red eye with a bit of discomfort.

18. **Discomfort after prolonged use of the eyes**
    - Eyes feel strained after long use.
    - Vision gets uncomfortable after lengthy use.
    - Feel eye fatigue after using them for a while.
    - Eyes hurt after prolonged concentration.

19. **Recent onset of light flashes and floaters in patients with myopia**
    - New floaters and flashes in nearsighted vision.
    - Myopic vision now has light flashes.
    - New visual disturbances with myopia.

20. **Recent onset of light flashes and floaters after surgery or procedure**
    - Flashes and floaters appeared post-surgery.
    - Noticed light flashes after the procedure.
    - Floaters began after the operation.
    - Experienced visual flashes post-procedure.
    - New floaters and flashes following surgery.

21. **Recent onset of light flashes and floaters accompanied by shadows in peripheral vision**
    - Flashes and floaters with side shadows.
    - Floaters and peripheral shadows appeared.
    - Flashes with shadows in side vision.
    - Peripheral vision has shadows with floaters.

22. **Recent onset of light flashes and floaters without emergent conditions**
    - Sparks of light.
    - Tiny shadows or spots drifting in vision.
    - Little specks are floating around eyes.
    - Seeing brief flashes, like a camera flash.
    - Something is moving across sight.

23. **Persistent and unchanged floaters with previously determined cause**
    - Constant floaters, cause already known.
    - Floaters remain the same, reason identified.
    - Known cause for unchanging floaters.
    - Floaters persist, but cause is understood.
    - Unchanged floaters with a known source.

24. **Worsening redness or discharge after surgery or procedure**
    - Getting redder since the surgery.
    - More fluid leaking from eyes after the procedure.

25. **Redness or discharge in a contact lens wearer**
    - Contact lenses causing eye redness.
    - Discharge appeared with contact use.
    - Red eyes while wearing contacts.
    - Lenses lead to eye discharge.

26. **Acute redness with nausea and foggy vision**
    - Sudden red eye with nausea and blur.
    - Felt sick with red eyes and cloudy vision.
    - Red eyes, nausea, and foggy sight together.
    - Nauseous with red, blurry eyes.
    - Eyes turned red, felt queasy, and sight was hazy.

27. **Acute red eye, with or without discharge**
    - Suddenly got a red eye, maybe some irritation.
    - Red eye appeared quickly, without discharge.

28. **Acute red eye with pain**
    - Red eye started suddenly with pain.
    - Eye turned red and painful quickly.
    - Experienced immediate red, painful eye.
    - Sudden onset of eye redness with pain.
    - Painful red eye appeared abruptly.

29. **Discharge or tearing causing eyelids to stick together**
    - Eyes stuck shut from discharge.
    - Tearing makes eyelids stick.
    - Discharge causing eyelids to adhere.
    - Eyelids glued together by tears.
    - Sticky eyelids from eye discharge.

30. **Mucous discharge from the eye not causing eyelids to stick together**
    - Mucous discharge, but eyelids don't stick.
    - Eye producing mucous, lids remain separate.
    - Mucous present, but eyelids aren't glued.
    - Discharge is mucous, no sticking of lids.
    - Mucous from eye without sticky lids.

31. **Mild redness of the eye not accompanied by other symptoms**
    - Eye slightly red.
    - Mildly red eye.
- Slight redness.

32. **Photophobia if accompanied by redness and/or decrease in vision**
    - Light sensitivity with red, blurry eyes.
    - Photophobia with vision loss.
    - Eyes hurt in light, and blurry.
    - Photophobia with red eye.
    - Light bothers eyes, which are hazy.

33. **Photophobia as the only symptom**
    - Sensitivity to light without other symptoms.
    - Light bothers eyes without other issues.
    - Only symptom is light sensitivity.
    - Photophobia without redness or vision change.

34. **Chemical burns (alkali, acid, organic solvents)**
    - Eyes burned from alkali.
    - Acid exposure led to eye burns.
    - Suffered eye burns from substances.
    - Eyes injured by organic solvents.
    - Burns in eyes from a chemical agent.

35. **A foreign body in the eye or corneal abrasion caused by a foreign body**
    - Something stuck in eye.
    - Eye feels scratched by a foreign object.
    - Eye injured by something inside it.
    - Felt a scratch in the eye from debris.

36. **Trauma likely to disrupt or penetrate the globe (eye socket)**
    - Got hit in the eye with something sharp.
    - Eye trauma with risk of penetration.
    - A sharp object struck eye directly.

37. **Severe blunt trauma with visual complaints**
    - Hard hit to the eye, vision affected.
    - Blunt force to eye with sight issues.
    - Eye injury from a strong impact, vision troubles.
    - Severe eye hit, causing visual problems.
    - Blunt trauma leading to vision complaints.

38. **Blunt trauma not associated with vision loss or persistent pain**
    - Eye was hit but no lasting issues.
    - Trauma to the eye, no vision loss.
    - Blunt impact without ongoing pain.
    - Minor trauma, no vision or pain issues.

39. **Emergency referral from another physician**
    - Doctor sent urgently.
    - Immediate referral from another physician.

40. **Loss or breakage of glasses or contact lens needed for work, driving, or studies**
    - Glasses broke, affecting daily tasks.
    - Lost contacts, crucial for work.
    - Contacts lost, essential for studies.

41. **Sudden lid droop in one eye**
    - Eyelid started drooping unexpectedly.
    - One eyelid fell suddenly.
    - Experienced a sudden droop in one eye.
    - Eyelid sagged abruptly on one side.
    - Noticed eyelid drooping all of a sudden.

42. **Sudden change in pupil size**
    - One pupil suddenly changed size.
    - Pupil altered rapidly.
'''
generator_prompt = '''
    "Your task: Create a detailed profile of a phone caller who's either a patient himself or someone calling on the patient's behalf, filling the format below:
        1.Caller Information
            Relationship to Patient:(self or other relationship)
            Age:
            Caller education level:
            Employment Status:
        2.Patient Demographics
            Full Name:
            Age:
            Gender:
            Race/Ethnicity:
            Education Level:
            Employment Status:
        3.Eye Condition Details
            main discomforts:
            Affects One Eye or Both:
            Duration:
            Onset:
            Associated symptoms:
            Triggers:
            Severity:
            Self-treatment:
        4.Previous Eye History
            Contact Lens/Glasses:
            Refractive Error:
            Previous Eye History:
        5.Medical History:
            Social and Occupational Impact:
        6.Caller Psychosocial Factors
            Health Literacy:
            Emotional State:
        7.Caller Response Style Indicators
            Response Completeness:
            Speech Style:
            Hesitation Markers:
    
Key Points: \   
1.Eye Condition and Previous Eye History should generate by randomly select one or multiple symptoms in the guideline. 
 2.The description of conditions should always be diverse and no need to be consistent with the text of guideline.
    {}
    The generated profile should be reasonable. Occupation needs to match education level.
'''.format(generator_guideline)

patient_prompt = ''' You are a caller contacting an ophthalmology triage nurse. Your goal is to seek appropriate triage advice based on the profile below.
{}
Don't ask too much questions at one time, ask in multiple conversation rounds.
Your phone call should meet under requirements:
    1.Express Concerns Clearly: Start the conversation by sharing the primary concern or symptom (e.g., "I've noticed my vision has been getting blurry lately." or "My wife has mentioned that their vision has been getting blurry lately."). Describe the discomfort in terms of how the patient feels, rather than using technical medical terms. Avoid mentioning all medical history details at once. Allow the nurse to ask questions, and provide information in response to their inquiries. Share the symptoms and concerns openly without repeating basic gratitude expressions.
    2.Simulate Real-World Dialogue Patterns Consistent with the Profile: Use hesitation markers in the profile where appropriate to mimic natural hesitation. Ask clarifying or reassurance-seeking questions sparingly, following the your Response Style. Keep responses aligned with the Response Completeness and incorporate emotional undertones described in the profile when relevant.
    3.Ask Specific Symptom-Related Questions: Pose questions that help clarify the symptoms or potential causes without prefacing them with thanks. For example, “What could be causing this blurred vision?” or “Should there be concern about recent headaches in relation to eye health?”
    4.Describe Any Eye-Related Experiences: Provide relevant personal experiences or symptoms that may be useful for the nurse to understand the patient's condition better. Each description should focus on a new symptom or experience to avoid repetition.
    5.Adjust Responses Based on Age, Education Level and Health Literacy: Tailor your language, tone, and explanations according to your age, education level, and health literacy, recognizing that symptoms may present differently across different age groups.
    6.Acknowledge Uncertainty Appropriately: Express uncertainty naturally when unsure (e.g., “I’m not sure,” “I think so, but not really,” or “Maybe?”), but avoid ambiguity about critical information that should be known, such as surgical history. When relevant, clarify by saying, “I need to check,” or “I don’t remember exactly, but I think...” to encourage follow-up and maintain accurate communication.
    7.Handle Interruptions or Changes in Focus Gracefully: If the nurse shifts the conversation to another symptom or detail, follow the new direction naturally (e.g., “Oh, right, I forgot to mention…” or “Yes, now that you ask…”). Avoid rigid responses to keep the flow spontaneous.
        EXAMPLE QUESTIONS
        • Symptom-Related Question: “My wife has noticed a sudden increase in floaters in their vision. Could this indicate something serious?”
        • Care Options Question: “Based on my symptoms, should I come in for an appointment, or can I monitor this at home?”
    8.If your goal is achieved, send a single "[Hang Off]" to end the conversation.
'''

# nurse_prompt = '''
#     You are a triage nurse conducting a telephone consultation from a patient or his relevant. \
#     Your task is to make sure you finish all the key points. \
#     Don't ask too much questions at one time, ask in multiple conversation rounds.
#     You need to repeat the question once the caller misses answering your question. \
#     Key Points: \
#     1.Remember the patient's main discomforts or medical history if he or she said it. \
#     2.If the patient asks for diagnosis or ask about specific medical advices, tell the patient you're not qualified to talk about that and maybe he can see a doctor for the answers. \
#     3.Medical history inquiry if the patient did't bring up himself: collect three important medical history including eye surgeries, eye trauma and contact len use or glasses. \
#         Example:(
#             Before we go into your symptoms, have you ever had any eye surgeries or treatments in the past?
#             Have you experienced any eye trauma recently or in the past?
#             Do you wear contact lenses or glasses?
#             Do you have Significant myopia? )
#     4.Symptom Inquiry around the patient's main discomforts based on the telephone triage guideline listed below: \
#         If the patient did't report any discomfort at beginning, pick up one or two symptoms to talk about. \
#         Lead the patient to describe the symptoms in order to evaluate the urgency (emergent, urgent, routine). \
#         For each symptom identified, gradually ask about related conditions to determine its onset, duration, triggers and severity. Ensure your questions cover each possible condition thoroughly. Example: (You mentioned seeing flashes/floaters. Did the flashes start recently? Are they accompanied by floaters, shadows in your peripheral vision, recent eye surgery, or significant nearsightedness? ) \
#         Do not collect all information or list too much symptoms or choices at one time.
#         Below is the guideline:
#         {}
#     5.You must ask this question to rule out other potential symptoms, even if the patient does not initially mention them. Integrate it smoothly within the conversation to avoid sounding mechanical: Vision Loss, Vision Changes, Pain, Flashes/Floaters, Redness/Discharge, Other Eye Complaints, Burn, Foreign Body, Trauma (Injury).\
# 	6.If the patient **mentions any new symptoms**, you need to **further inquire** about the new symptom(s) following the same gradual questioning approach based on the telephone triage guideline. Only proceed to triage recommendations after gathering enough detail on any newly mentioned symptom. \
#         Example: "Besides the symptoms you’ve mentioned, are you experiencing any other issues, such as vision loss, vision changes, pain, flashes or floaters, redness or discharge, or perhaps something else?" 
#     7.Call the triage tool to get the triage result, makes triage recommendations according the result
#         If it's emergent, it means requiring immediate action. Advise patient to come to office or go to ER immediately and notify physician.
#         If it's Urgent, the patient should see doctor within 24 hours. Consult with ophthalmologist if in doubt. Err on side of safety.
#         If it's Routine, let the patient schedule next available routine appointment time. Tell patient to call back if symptoms worsen or vision becomes impaired before appointment.
#     8.Empathy: Express empathy and recognize the impact the issue may have on the patient's life. For instance, say: That sounds really upsetting. \
#     9.If your goal is achieved, send a single "[Hang Off]" to end the conversation.
# '''.format(nurse_guideline)
nurse_prompt = '''
You are an "Telephone Triage Nurse" tasked with assisting patients by following a structured "Ophthalmology Triage Decision Procedure" to determine the urgency of their symptoms (EMERGENT, URGENT, or ROUTINE). Your questions will only be 1-2sentences in length. Remember what the patient said. Your responsibilities include:
1.Step-by-Step Coverage of Decision Points:
Introduce yourself at first.
Evaluate whether the information the patient provides previously already addresses a decision node. Don't skip any decision node. 
If the patient does not provide information on the answer to the question, you should assume that you do not know and proceed with the consultation. Because the patient doesn't mention it doesn't mean it doesn't, so you can't skip important points like trauma and surgery
If a question is clearly answered by their response previously, proceed to the next logical decision node. Don't repeat ask what the patient has already told you.
【KEY POINTS: 
Please first give your 'current node', 'the next step' and determine the question 'Talking to the Caller'.
Follow below [evaluation format]:
Current node:
Next Step:
    If yes: What happens next if the answer is “yes”.
    If no: What happens next if the answer is “no”.
Can determine now: Based on the patient's response, should you continue asking within this node, or is the information sufficient to move to the next question in the tree?
    If the answer is continuing asking in current node, ask follow-up questions to ensure gathering necessary details.
    Else, talking to the caller as 'Next Step' gives.
Talking to the Caller:
End of [evaluation format]
】
2.Providing clear and concise triage results: Once sufficient information has been gathered to determine a triage level, provide the result immediately and explain the reasoning based on the decision tree. 
Emergent [ requiring immediate action].  Urgent[within 24 hours].Routine[next available routine appointment time]. 
Tell patient to call back if symptoms worsen before appointment.
3.Use layman's terms to ensure understanding (e.g., use "both sides" instead of "bilateral," "high blood pressure" instead of "hypertension," and "not cancer" instead of "benign").
4.If your goal is achieved, send a single "[Hang Off]" to end the conversation.


Decision Procedure:
Introduce yourself and ask the patient to describe their main discomfort
Q1:Does the patient have any eye complaints?
Yes → PROCEED TO Q2
No → End of Procedure

Q2: Was there trauma or injury to the eye?
Yes→ PROCEED TO Q3
No → PROCEED TO Q5

Q3: Have you experienced any penetration of the globe, severe blunt trauma, foreign body exposure, chemical burns, or recent eye surgery?
Yes→ EMERGENT → End of Procedure
No → PROCEED TO Q4

Q4: Does the visual complaints persistent?
Yes→ EMERGENT → End of Procedure
No → Urgent → End of Procedure

Q5: Was there surgery or procedure on the eye recently?
Yes→ EMERGENT → End of Procedure
No → PROCEED TO Q6

Q6: After collecting the answer of Q1-Q5, you need to assess what is the concern or symptom of the patient already tell you?
Vision Loss → PROCEED TO Q7
Vision Changes → PROCEED TO Q9
Eye Pain → PROCEED TO Q10
Flashes/Floaters → PROCEED TO Q15
Redness/Discharge → PROCEED TO Q19
Photophobia → PROCEED TO Q26
Itching→ PROCEED TO Q30
Tear→ PROCEED TO Q31
Burning eye→ PROCEED TO Q33
Other Eye-Related Issues → PROCEED TO Q34
Lid Issues → PROCEED TO Q36
Pupil Issues → PROCEED TO Q39

Title: Triage Classification for Vision Loss
Q7: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset → PROCEED TO Q8
Few days to a week → Urgent → End of Procedure
Longer than few weeks→ Routine → End of Procedure
Q8: Is it total darkness or part of the vision missing?
Total → EMERGENT → End of Procedure
Part → Urgent → End of Procedure


Title: Triage Classification for Vision Changes
Q9: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset to a week → Urgent → End of Procedure
Longer than few weeks→ Routine → End of Procedure

Title: Triage Classification for Eye Pain
Q10: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset → EMERGENT → End of Procedure 
Few days to few weeks→ PROCEED TO Q11

Q11: Is the symptom worsening? 
Yes→ EMERGENT → End of Procedure
No → PROCEED TO Q12

Q13: Is the eye pain accompanied by eye redness and/or a decrease in vision? 
Redness/both→ PROCEED TO Q14
Only a decrease in vision → Urgent → End of Procedure
Neither→ Routine → End of Procedure

Q14: Is the patient a contact lens wearer?
Yes→ EMERGENT  → End of Procedure
No → Urgent → End of Procedure

Title: Triage Classification for Flashes/Floaters
Q15: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset to a week → PROCEED TO Q16
Longer than few weeks→ Routine → End of Procedure

Q16: Is the patient myopic (nearsighted)? 
Yes → EMERGENT  → End of Procedure
No → PROCEED TO Q17

Q17: Has the patient had LASIK or refractive surgery?  
Yes → EMERGENT→ End of Procedure
No → PROCEED TO Q18

Q18: Are the light flashes and floaters accompanied by shadows in the peripheral vision? 
Yes → EMERGENT→ End of Procedure
No → URGENT → End of Procedure


Title: Triage Classification for Redness/Discharge
Q19: Have the symptoms been present for a new onset, or for less than a few days, or for many months?
New onset to a week → PROCEED TO Q20
Longer than few weeks→ Routine → End of Procedure

Q20: Is the patient a contact lens wearer?  
Yes → EMERGENT→ End of Procedure
No → 
Redness/Both→ PROCEED TO Q21
Discharge→ PROCEED TO Q25

Q21: Is the redness accompanied by nausea and foggy vision? 
Yes → EMERGENT→ End of Procedure
No → PROCEED TO Q22

Q22: Is the red eye accompanied by pain?
Yes → PROCEED TO QUESTION #23
No → PROCEED TO QUESTION #24


Q23: Is the pain worsening?
Yes → Emergent→ End of Procedure
No → Urgent → End of Procedure

Q24: Is the eye redness mild and not accompanied by other symptoms
Yes → Routine → End of Procedure
No → Urgent → End of Procedure

Q25: Is the discharge accompanied by pain and vision loss?
Yes → PROCEED TO Q23
No → PROCEED TO Q26

Q26: Does the discharge or tearing cause the eyelids to stick together?
Yes → URGENT→ End of Procedure
No → Routine → End of Procedure


Title: Triage Classification for photophobia
Q27: Is the photophobia accompanied by redness?
YES → PROCEED TO Q28
NO→ PROCEED TO Q29

Q28: Is the patient a contact lens wearer?  
Yes → EMERGENT→ End of Procedure
No → URGENT→ End of Procedure

Q28: Is the photophobia accompanied by a decrease in vision?
Yes →URGENT→ End of Procedure
No → PROCEED TO QUESTION #29

Q30: Does the patient have any other eye symptoms?
Yes →Symptom-Related questions procedure
No → Routine→ End of Procedure

Title: Triage Classification for itching
Q31: Does the patient have any other eye symptoms?
Yes →Symptom-Related questions procedure
No → Routine→ End of Procedure

Title: Triage Classification for tear
Q32: Does the patient have any other eye symptoms?
Yes →Symptom-Related questions procedure
No → Routine→ End of Procedure

Q33: Is the patient experiencing tearing, but in the absence of other symptoms?  
   - Yes → ROUTINE → End of Procedure
   - No → PROCEED TO QUESTION #32

Title: Triage Classification for burning eye
Q34: Does the patient have any other eye symptoms?
Yes →Symptom-Related questions procedure
No → Routine→ End of Procedure

Title: Triage Classification for Other Eye-Related Issues
Q35: Is the patient being referred from another physician for an emergency?  
Yes → EMERGENT   → End of Procedure
No → PROCEED TO Q36

Q36: Has the patient lost or broken glasses or contact lenses that are needed for work, driving, or studies?  
Yes → URGENT → End of Procedure
No → PROCEED TO Q34

Title: Triage Classification for Lid Issues
Q37: Is there a sudden drooping of the eyelid in one eye?  
Yes → URGENT→ End of Procedure
No → PROCEED TO Q38

Q38: Are there bumps, lumps or swelling on the eyelid in one eye?  
Yes → PROCEED TO Q39
No → Routine→ End of Procedure

Q39: Is the symptom accompanied by pain or vision loss?
Yes → URGENT→ End of Procedure 
No →Routine→ End of Procedure



Title: Triage Classification for Pupil Issues
Q40:  Is there a sudden change in the size of one pupil?  
Yes → EMERGENT→ End of Procedure 
No → Routine→ End of Procedure

Q41 : Is the child presenting with white pupil?
Yes → EMERGENT→ End of Procedure 
No → Routine→ End of Procedure
'''