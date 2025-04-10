from dotenv import load_dotenv
load_dotenv()
from prompts import (
    patient_prompt, nurse_prompt, recommendator, symptom_converter
)
from guideline import switcher
from typing import Annotated, Sequence, List, Dict
from typing_extensions import TypedDict
import operator

from langchain_core.messages import ToolMessage, HumanMessage, BaseMessage, AIMessage, convert_to_messages
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START, add_messages
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

#RAG
# from langchain_community.vectorstores import Chroma
# from langchain_core.documents import Document
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.retrievers import BaseRetriever
# from langchain_text_splitters import RecursiveCharacterTextSplitter

llm = ChatOpenAI(model="deepseek-chat")
class AgentState(TypedDict): # data stream in the graph, input of each node
    messages: Annotated[Sequence[BaseMessage], operator.add]
    profile: str
    symptom_curr: Annotated[str, "symptom which should be inquiry at this round"]
    inquiry_progress: Dict
    during_inquiry: Annotated[bool, "A flag, set to True while Nurse agent detect new symtom, reset to False after triage."]
    

def read_profiles():
    profiles = []
    with open("profiles_4o.txt", 'r') as file:
        doc = file.readlines()
    temp = ""
    for line in doc:
        if "Caller Information" in line:
            profiles.append(temp)
            temp = line
        else:
            temp += line
    profiles.append(temp)
    return profiles[84:]


# def get_retriever() -> BaseRetriever:
#     vectorstore = Chroma.from_documents(
#         documents=nurse_guideline,
#         collection_name="pandas-rag-chroma",
#         embedding=OpenAIEmbeddings(),
#     )
#     retriever = vectorstore.as_retriever()
#     return retriever
# retriever = get_retriever()

def triage(inquiry_progress): #get the most severe level as the triage result
    most_severe_level = 'Routine'
    for _, level in inquiry_progress.items():
        if level == 'E':
            return 'Emergent' # condition1: if any 'E', return immediately
        elif level == 'U':
            most_severe_level = 'Urgent' # condition2: all 'R' and 'U', most_severe_level would be updated to 'U' and continue checking
    return most_severe_level # condition3: all 'R', most_severe_level would never be updated

def inquiry_node(state: AgentState):
    '''
    接管过来的中间重复步骤可以抽象为def inqury(state, answer): ->next question，是一个调用字典的纯工具过程。
    接管之时要做的操作包括抽出具体病症，根据病症取出第一个问题，将<symtom, 1>的初始态append进state里。
    nurse_agent无法判断一个症状是否结束inquiry，因此接管必须直到所有症状inquiry结束。
    接管最末的操作是：如果返回的next question是个字符，调用triage()取最终一级的分级作为最终分级。
    
    有三种情况：1.开始一轮inquiry（条件是开始谈论第一个病症/上个病症谈论结束）；2.继续之前的inquiry；3.结束inquiry；
    对应的输出分别是：1.Q1；2.Q_next；3.下一个症状的Q1/分诊结果（所有病症都问询完毕）
  
    输出行为抽象出两个操作：getQuestion(Symp_curr, num)->Q;
    getNextNum(Symp_curr, ans)->Q or Triage_result {
        parse ans to yes or no;
        if isinstance(ans, int): getQuestion(Symp_curr, Num_next)
        else:
            if no new Symp: Triage()
            else: getQuestion(Symp_next, 1)
    }
    getQuestion这个方法去掉了，直接用序号访问问题列表即可
    '''
    new_state = state

    # Check new symptom every round, assuming all new symptoms are in patient's most recent answer
    new_symptoms = symptom_converter.invoke({"message": new_state["messages"][-1].content})
    for symptom in new_symptoms.valid_symptom:
        if symptom not in new_state["inquiry_progress"]:
            new_state["inquiry_progress"][symptom] = 0
        
    # at very first of first symptom's inquiry
    if "symptom_curr" not in new_state:
        new_state["symptom_curr"] = "trauma_injury" # TODO: at least 'R' on this symptom while patient could probably don't have it
        
        if "trauma_injury" in new_state["inquiry_progress"]:# if patient report injury initiatively, inquiry about injury first
            new_state["inquiry_progress"]["trauma_injury"] = 1 # as if we already inquiried Q1
            new_state["messages"].append(BaseMessage("Yes, patient have trauma or injury.")) # as if patient answered yes
        else:
            new_state["inquiry_progress"]["trauma_injury"] = 0

    symptom_curr = new_state["symptom_curr"]
    # condition 1: start Q1 of symptom_curr
    if new_state["inquiry_progress"][symptom_curr] == 0:
        new_state["inquiry_progress"][symptom_curr] = 1
        new_state["messages"] = [HumanMessage(content=switcher.get(symptom_curr).question_list[1], name="InquiryAgent")]
    # condition 2: continue inquiring
    else:
        question_curr = new_state["inquiry_progress"][symptom_curr]
        question_next = switcher.get(symptom_curr).getNextNum(question_curr, ans=new_state["messages"][-1].content)
        new_state["inquiry_progress"][symptom_curr] = question_next
        # condition 2-1: continue inquiring
        if isinstance(question_next, int):
            new_state["messages"] = [HumanMessage(content=switcher.get(symptom_curr).question_list[question_next], name="InquiryAgent")]
        # condition 2-2: finished inquiring on symptom_curr
        else: # char
            # condition 2-2-1: start inquiring on next symptom
            for k,v in new_state["inquiry_progress"].items():
                if v == 0:
                    new_state["symptom_curr"] = k
                    new_state["inquiry_progress"][k] = 1
                    new_state["messages"] = [HumanMessage(content=switcher.get(symptom_curr).question_list[1], name="InquiryAgent")]
                    return new_state
            # condition 2-2-2: finished all sympton's inquiry (finished loop without returning)
            level = triage(new_state["inquiry_progress"])
            new_state["messages"] = [HumanMessage(content=recommendator.invoke({"level": level}), name="InquiryAgent")]
            new_state["during_inquiry"] = False

    return new_state

def func():
    "an occupation func"
nurse_agent = create_react_agent(llm, tools=[func], state_modifier=nurse_prompt, checkpointer=MemorySaver())
def nurse_node(state: AgentState):
    result = nurse_agent.invoke(state)
    # for mess in result["messages"]:
    #     if isinstance(mess, ToolMessage):
    #         # print(mess)
    #         mess.pretty_print()
    # print('nurse', result["messages"][-1].usage_metadata)
    if "[Inquiry]" in result["messages"][-1].content: return {"during_inquiry": True}

    return {"messages": [HumanMessage(content=result["messages"][-1].content, name="Nurse")]}


def nurse_edge_mapping_func(state: AgentState):
    if "during_inquiry" in state and state["during_inquiry"] == True:
        return "InquiryAgent"
    elif "[Hang Off]" in state["messages"][-1].content:
        return END
    else: return "Caller"
def caller_edge_mapping_func(state: AgentState):
    if "during_inquiry" in state and state["during_inquiry"] == True:
        return "InquiryAgent"
    elif "[Hang Off]" in state["messages"][-1].content:
        return END
    else: return "Nurse"

##################
def run(i, profile):
    patient_agent = create_react_agent(llm, tools=[func], state_modifier=patient_prompt.format(profile), checkpointer=MemorySaver())
    def patient_node(state):
        result = patient_agent.invoke(state)
        # print('caller', result["messages"][-1].usage_metadata)
        return {"messages": [HumanMessage(content=result["messages"][-1].content, name="Caller")]}

    workflow = StateGraph(AgentState)
    workflow.add_node("Nurse", nurse_node)
    workflow.add_node("Caller", patient_node)
    workflow.add_node("InquiryAgent", inquiry_node)
    workflow.add_edge(START, "Caller")
    workflow.add_edge("InquiryAgent", "Caller")
    workflow.add_conditional_edges("Caller", caller_edge_mapping_func, ["Nurse", "InquiryAgent", END])
    workflow.add_conditional_edges("Nurse", nurse_edge_mapping_func, ["Caller", "InquiryAgent", END])
    graph = workflow.compile()
    # with open("TriageCalling/example_%d.txt"%i, "w") as file, callback_handler as cb:
    with open("example_%d.txt"%i, "w") as file:
        for s in graph.stream(
            {"messages": [], "inquiry_progress": {}},
            {"configurable": {"thread_id": "thread-1", "recursion_limit": 50}}
        ):
            name = list(s.keys())[0]
            print(s[name])
            # s[name]['messages'][-1].pretty_print()
            if 'messages' in s[name]:
                file.write(name+": "+s[name]['messages'][-1].content+'\n')

    del(graph)
    del(workflow)
    del(patient_agent)

####################
for i, profile in enumerate(read_profiles()):
    run(i+84, profile)
    break
