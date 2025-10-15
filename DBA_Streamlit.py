from langgraph.graph import StateGraph,MessagesState,START,END
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage,AIMessageChunk
from typing_extensions import Annotated,TypedDict
from DB_Agent_System_Prompt import FR_SYSTEM_PROMPT,MULTIPLE_DATASETS_SYSTEM_PROMPT,db_metadata
import pandas as pd
import json
import streamlit as st
from cryptography.fernet import Fernet
from datetime import datetime

key="5KmTdJ2hsmenGZVlb-gAAqg8GWstwbkKAo7uRNKAMRE="
access_key1=b'gAAAAABot9zz3KX7jY0lj_aWcW0nrVuyOMt9q2gMXh0VaaNBcBvMZ3ln490Z-LtJ3Rav69Jnps09KtYDVJ0Ca-XGaqBqMQxGlkzj5yPk4XNh-Yu2xbOSFRU='
access_key2=b'gAAAAABot9zzWbdFdJiATMHWGrqkJOSNYQ_sYAdaB7Kt9caQl6xHryiS5iEyO7VdYzVHLKYRvBEPHUKSkWNHNmAFouHIK9NM-_6d7bW3SSC6YeWCFlchtYx-lOfuCScihgasCaoQl03P'

cipher = Fernet(key)

laad_df=pd.read_excel("LAAD_Data_v2.xlsx")
xponent_df=pd.read_excel("Xponent_Data_v3.xlsx")
weekly_sales_crediting_df=pd.read_excel("weekly_sales_crediting_file_v2.xlsx")
territory_mapping_df=pd.read_excel("Territory_Mapping.xlsx")
zip_to_territory_mapping_df=pd.read_excel("Zip_To_Terr.xlsx")
roster_df=pd.read_excel("Roster_Data_v2.xlsx")
ic_goals_df=pd.read_excel("IC_goals_data_v2.xlsx")
segmentation_df=pd.read_excel("Segmentation Data v2.xlsx")
rdtr_df=pd.read_excel("RDTR.xlsx")
plan_df=pd.read_excel("Plan_Data.xlsx")
hcp_master_df=pd.read_excel("HCP_Master_v2.xlsx")
ic_national_summary_df=pd.read_excel("IC National Summary.xlsx")
ic_summary_df=pd.read_excel("IC Summary v2.xlsx")
national_summary_performance_df=pd.read_excel("National Summary (YTD Performance) v2.xlsx")
zip_level_sales_df=pd.read_excel("ZIP LEVEL SALES DATA.xlsx")
pay_curve_df=pd.read_excel("Pay Curve.xlsx")

repl_variables={}

def python_repl_tool(llm_gen_code):
    """
    Execute a snippet of Python code in a given namespace and return the updated namespace.

    This function allows dynamic execution of Python code strings within a
    persistent REPL-style environment. The caller provides both the code to
    run and a dictionary of variables (namespace) that will serve as the
    execution context. After running, any new or modified names in that
    context are returned for inspection or further use.

    
    Args:
        code_to_be_executed: The string containing Python code to execute.
        repl_variables: A dictionary representing the execution namespace.
    """
     
    repl_variables["laad_df"]=laad_df
    repl_variables["xponent_df"]=xponent_df
    repl_variables["weekly_sales_crediting_df"]=weekly_sales_crediting_df
    repl_variables["territory_mapping_df"]=territory_mapping_df
    repl_variables["zip_to_territory_mapping_df"]=zip_to_territory_mapping_df
    repl_variables["roster_df"]=roster_df
    repl_variables["ic_goals_df"]=ic_goals_df
    repl_variables["segmentation_df"]=segmentation_df
    repl_variables["rdtr_df"]=rdtr_df
    repl_variables["plan_df"]=plan_df
    repl_variables["hcp_master_df"]=hcp_master_df
    repl_variables["ic_national_summary_df"]=ic_national_summary_df
    repl_variables["ic_summary_df"]=ic_summary_df
    repl_variables["national_summary_performance_df"]=national_summary_performance_df
    repl_variables["zip_level_sales_df"]=zip_level_sales_df
    repl_variables["pay_curve_df"]=pay_curve_df
    repl_variables["pd"]=pd
    
    try:
        exec(llm_gen_code,repl_variables)
        tool_result=repl_variables.get("result")
        if isinstance(tool_result,pd.DataFrame) or isinstance(tool_result,pd.Series):
            tool_result=tool_result.to_json()
        else:
            tool_result=str(tool_result)
    
    except Exception as e:
        tool_result=str(e)
    
    return tool_result

llm=ChatBedrockConverse(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                        temperature=0,
                        max_tokens=10000,
                        disable_streaming=False,
                        aws_access_key_id=cipher.decrypt(access_key1).decode(),
                        aws_secret_access_key=cipher.decrypt(access_key2).decode(),
                        region_name="us-east-1")

llm_agent=llm.bind_tools([python_repl_tool])

current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class db_graph_state(MessagesState):
    #messages:Annotated[AnyMessage,add_messsage]
    pass

def llm_node(state):
    multi_df_system_prompt=MULTIPLE_DATASETS_SYSTEM_PROMPT.format(db_metadata=db_metadata,current_datetime=current_datetime)

    return {"messages":llm_agent.invoke([SystemMessage(content=multi_df_system_prompt)]+state.get("messages"))}

def tool_call_check(state):
    ai_message=(state.get("messages"))[-1]
    if len(ai_message.tool_calls)>0:
        return "Tool Executor"
    else:
        return "Response Generator"
    
def tool_executor(state):
    ai_message=(state.get("messages"))[-1]
    tool_call_list=ai_message.tool_calls
    tool_messages_list=[]
    for tool_call in tool_call_list:
        function_name=eval(tool_call.get("name"))
        function_arguments=tool_call.get("args")
        function_id=tool_call.get("id")
        function_result=function_name(**function_arguments)
        tool_message=ToolMessage(content=function_result,tool_call_id=function_id)
        tool_messages_list.append(tool_message)
    
    return {"messages":tool_messages_list}

def final_response_llm(state):
    message_history=state.get("messages")
    return {"messages":llm_agent.invoke([SystemMessage(content=FR_SYSTEM_PROMPT)]+message_history+[HumanMessage(content="Answer the the question initially asked by the user based on the previous chathistory")])}

builder=StateGraph(db_graph_state)
builder.add_node("LLM",llm_node)
builder.add_node("Tool Executor",tool_executor)
builder.add_node("Response Generator",final_response_llm)

builder.add_edge(START,"LLM")
builder.add_conditional_edges("LLM",tool_call_check,["Tool Executor","Response Generator"])
builder.add_edge("Tool Executor","LLM")
builder.add_edge("Response Generator",END)

graph=builder.compile()

print("\nLangGraph Compiled!\n")

st.set_page_config(page_title="Conversational Agent", page_icon="🤖")

# --- Conversation history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 F.A.C.T DB Agent")

# --- User input ---
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            # Thought
            with st.expander("💭 Agent Thought Process", expanded=False):
                st.markdown(msg["content"]["thought"])
            # Tool
            with st.expander("🛠️ Tool Call", expanded=False):
                st.markdown(msg["content"]["tool"])
            # Final Answer
            st.markdown(msg["content"]["final"])
        else:
            st.markdown(msg["content"])

# --- Agent simulation ---
if user_prompt:
    with st.chat_message("assistant"):
        llm_thought_text_stream_flag=False
        final_response_markdown_container_flag=False

        thought_stream = st.empty()
        thought_text = ""

        final_response_stream=st.empty()
        final_response_text=""

        tool_call_text=""
        data=""
        data_flag=0

        for chunk in graph.stream({"messages":HumanMessage(content=user_prompt)},{"recursion_limit":60},stream_mode="messages"):
            raw_chunk=chunk[0]
            raw_chunk_metadata=chunk[1]
            if isinstance(raw_chunk,AIMessageChunk):
                if raw_chunk_metadata.get("langgraph_node")=="LLM":
                    if len(raw_chunk.content)>0:
                        if "type" in raw_chunk.content[0] and "text" in raw_chunk.content[0]:
                            chunk_text=raw_chunk.content[0].get("text")
                            if chunk_text!="":
                                data={"type":"thought","chunk":chunk_text}
                                data_flag=1
                               
                                print({"type":"thought","chunk":chunk_text})
                        
                        elif "type" in raw_chunk.content[0] and "input" in raw_chunk.content[0]:
                            chunk_text=raw_chunk.content[0].get("input")
                            tool_call_text=tool_call_text+chunk_text
                        
                    elif "stopReason" in raw_chunk.response_metadata:
                            if raw_chunk.response_metadata.get("stopReason")=="tool_use":
                                try:
                                    tool_call_actual_text=json.loads(tool_call_text)
                                    tool_call_actual_text=tool_call_actual_text.get("llm_gen_code")
                                    
                                    data={"type":"tool_call","chunk":tool_call_actual_text}
                                    data_flag=1
                            
                                    print({"type":"tool_call","chunk":tool_call_actual_text})
                                    tool_call_text=""

                                except Exception as e:
                                    print("Converting Tool Call Dict to Text Failed while Streaming")
                                    print(e)

                if raw_chunk_metadata.get("langgraph_node")=="Response Generator":
                    if len(raw_chunk.content)>0:
                        if "text" in raw_chunk.content[0]:        
                            data={"type":"final_response","chunk":raw_chunk.content[0].get("text")}

                            data_flag=1
                    
                            print({"type":"final_response","chunk":raw_chunk.content[0].get("text")})
                
                if data_flag==1: 
                    if data.get("type")=="thought":
                        if llm_thought_text_stream_flag==False:
                            with st.expander("💭 Agent Thought Process", expanded=True):
                                thought_stream=st.empty()
                                thought_text=thought_text+data.get("chunk")
                                thought_stream.markdown(thought_text)
                                llm_thought_text_stream_flag=True
                        else:
                            thought_text=thought_text+data.get("chunk")
                            thought_stream.markdown(thought_text)

                    elif data.get("type")=="tool_call":
                        with st.expander("🛠️ Tool Call", expanded=True):
                            st.code(data.get("chunk"))
                        llm_thought_text_stream_flag=False
                        thought_text=""

                    elif data.get("type")=="final_response":
                        if final_response_markdown_container_flag==False:
                            final_response_stream=st.empty()
                            final_response_text=final_response_text+data.get("chunk")
                            final_response_stream.info(final_response_text)
                            final_response_markdown_container_flag=True
                        else:
                            final_response_text=final_response_text+data.get("chunk")
                            final_response_stream.info(final_response_text)

                    data_flag=0

        # Save structured response
        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "final": final_response_text,
                "thought": "",
                "tool": ""
            }
        })















