import os, glob, time
from dotenv import load_dotenv
load_dotenv()
from typing import Annotated, Sequence, Dict
from typing_extensions import TypedDict
import operator
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END, StateGraph, START

from prompts import patient_agent, nurse_agent, recommendator, symptom_converter
from guideline import basic_questions, switcher
from util import read_profiles

class AgentState(TypedDict): # data stream in the graph, input of each node
    all_messages: Annotated[Sequence[BaseMessage], operator.add]
    messages: Annotated[Sequence[BaseMessage], operator.add]
    profile: str
    symptom_curr: Annotated[str, "symptom which should be inquiry at this round"]
    decision_tree_curr: Annotated[str, "guide of current sympton"]
    inquiry_progress: Dict
    URGENCY_LEVEL: str

def triage(inquiry_progress): #get the most severe level as the triage result
    if VERBOSE: print("\nInquiry Results:")
    ret = 'ROUTINE'
    for sym, level in inquiry_progress.items():
        if VERBOSE: print(sym, level)
        if level == "EMERGENT":
            return level # condition1: if any 'E', return immediately
        elif level == "URGENT":
            ret = level # condition2: all 'R' and 'U', most_severe_level would be updated to 'U' and continue checking
    return ret # condition3: all 'R', most_severe_level would never be updated


def nurse_node(state: AgentState):
    result = nurse_agent.invoke(state)
    response = result.content.replace("Nurse: ", '').replace("\"", '')
    if VERBOSE: print(response)
    new_state = state

    idx = result.content.find('Talking to the Caller:')
    if idx != -1:
        response = result.content[idx+23:].strip()
        # end of inquiry of current symptom
        level = next((l for l in ["EMERGENT", "URGENT", "ROUTINE"] if l in response), 0)

        while level != 0:
            flag_finished_in_advance = False
            flag_finshed = True # wrong init value that need to be alter
            if len(new_state["inquiry_progress"].keys()) > 0:
                new_state["inquiry_progress"][new_state["symptom_curr"]] = level
            else:
                flag_finished_in_advance = True
                flag_finshed = False
                final_level = level

            for k,v in new_state["inquiry_progress"].items():
                if v == 0:
                # update symptom_curr and corresponding guide desision tree, and inquiry again to decide the right inquiry question of this round
                    flag_finshed = False
                    new_state["symptom_curr"] = k
                    new_state["decision_tree_curr"] = switcher[k]
                    result = nurse_agent.invoke(new_state)
                    
                    idx = result.content.find('Talking to the Caller:')
                    if idx == -1: break
                    response = result.content[idx+23:].strip().replace("Nurse: ", '').replace("\"", '')
                    level = next((l for l in ["EMERGENT", "URGENT", "ROUTINE"] if l in response), 0)
                    break # go check again whether reach the end of new symptom, if not go to position1

            if flag_finshed: # finish all the symptoms' inquiry
                final_level = triage(new_state["inquiry_progress"])
                
            if flag_finshed or flag_finished_in_advance:
                new_state["URGENCY_LEVEL"] = final_level
                final_response = recommendator.invoke({"level": final_level})
                # new_state["all_messages"].append(HumanMessage(content="Nurse: "+final_response, name="Nurse"))
                new_state["messages"].append(HumanMessage(content="Nurse: "+final_response+"\n[Hang Up]", name="Nurse"))
                return new_state

        # position1
        # new_state["all_messages"].append(HumanMessage(content="Nurse: "+result.content.replace("Nurse: ", '').replace("\"", ''), name="Nurse"))
        new_state["messages"].append(HumanMessage(content="Nurse: "+response, name="Nurse"))
        return new_state 
        
    # at begining or later sometime, might doesn't do inquiry so won't find 'Talking to the Caller:'
    # new_state["all_messages"].append(HumanMessage(content="Nurse: "+result.content.replace("Nurse: ", '').replace("\"", ''), name="Nurse"))
    new_state["messages"].append(HumanMessage(content="Nurse: "+response, name="Nurse"))
    return new_state

def patient_node(state):
    new_state = state
    result = patient_agent.invoke(state)
    # new_state["all_messages"] = [HumanMessage(content="Caller: "+result.content.replace("Caller: ", '').replace("\"", ''), name="Caller")]
    new_state["messages"] = [HumanMessage(content="Caller: "+result.content.strip().replace("Caller: ", '').replace("\"", ''), name="Caller")]

    # check new symptom every round
    new_symptoms = symptom_converter.invoke({"message": result.content})
    if VERBOSE: print("\n Symptoms in this words: ", new_symptoms)
    for symptom in new_symptoms.valid_symptom:
        if "symptom_curr" not in new_state: # at very first start
            new_state["symptom_curr"] = symptom
            new_state["decision_tree_curr"] = switcher[symptom]
        if symptom not in new_state["inquiry_progress"]:
            new_state["inquiry_progress"][symptom] = 0 # boolean, 0 for inquiry unfinished, would be set to be level by nurse

    return new_state


def nurse_edge_mapping_func(state: AgentState):
    if "[Hang Up]" in state["messages"][-1].content or "[Hang Off]" in state["messages"][-1].content:
        return END
    else: return "Caller"

def caller_edge_mapping_func(state: AgentState):
    if "[Hang Up]" in state["messages"][-1].content or "[Hang Off]" in state["messages"][-1].content:
        return END
    else: return "Nurse"


VERBOSE = False
if __name__ == "__main__":
    skipped = [364]
    for i, profile in read_profiles(specify=skipped):
        workflow = StateGraph(AgentState)
        workflow.add_node("Nurse", nurse_node)
        workflow.add_node("Caller", patient_node)
        workflow.add_edge(START, "Caller")
        workflow.add_conditional_edges("Nurse", nurse_edge_mapping_func, ["Caller", END])
        workflow.add_conditional_edges("Caller", caller_edge_mapping_func, ["Nurse", END])
        graph = workflow.compile()
        
        try:
            ret = ""
            for s in graph.stream(
                {"all_messages": [], "messages": [], "inquiry_progress": {},
                    "profile": profile, "decision_tree_curr": basic_questions, "URGENCY_LEVEL": 'Routine'},# TODO: bug, profile 13, this is not updated
                {"configurable": {"thread_id": "thread-1", "recursion_limit": 50}}
            ):
                name = list(s.keys())[0]
                if VERBOSE: s[name]['messages'][-1].pretty_print()

                if 'messages' in s[name]:
                    ret += s[name]['messages'][-1].content+'\n\n'
            ret += "Triage Result: "+s[name]['URGENCY_LEVEL']+'\nDetected Symptoms: \n'
            for k, v in s[name]['inquiry_progress'].items():
                ret += k+': '+v+'\n'
        except Exception as e:
            print(e)
            print("broken and skip at Number", i)
            time.sleep(60)
            continue

        # bad_file = glob.glob("reddit_train/reddit_%d_*.txt"%i)
        # if len(bad_file) == 1:
        #     os.remove(bad_file[0])
        #     print(bad_file[0], "has been removed")

        with open("profiles_genBy4o/%d_%s.txt"%(i, s[name]['URGENCY_LEVEL']), "w") as file:
            file.write(ret)
        del(graph)
        del(workflow)
        if VERBOSE: print("\n\n\n\n")
