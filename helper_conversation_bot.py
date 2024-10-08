
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
from langsmith.run_helpers import get_current_run_tree
from streamlit_feedback import streamlit_feedback

from functools import partial

import os

import streamlit as st

from helper_prompts import prompt_datacollection_old


# Using streamlit secrets to set environment variables for langsmith/chain
os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']
os.environ["LANGCHAIN_API_KEY"] = st.secrets['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_PROJECT"] = st.secrets['LANGCHAIN_PROJECT']
os.environ["LANGCHAIN_TRACING_V2"] = 'true'


def init_session_stateVars():
    ## initialising key variables in st.sessionstate if first run
    if 'agentState' not in st.session_state: 
        st.session_state['agentState'] = "start"
    if 'consent' not in st.session_state: 
        st.session_state['consent'] = False
    if 'exp_data' not in st.session_state: 
        st.session_state['exp_data'] = True

    ## set the model to use in case this is the first run 
    if 'llm_model' not in st.session_state:
        # st.session_state.llm_model = "gpt-3.5-turbo-1106"
        st.session_state.llm_model = "gpt-4o"

def reset_conversation():
    msgs.clear()
    st.session_state['agentState'] = "start"

def convo_finished():
    st.write("Great, you've finished the data collection. You can review the history below and reset the conversation to start again. _Note that you could copy & paste the conversation history to use it in the next stage of the process._")

    st.button("Reset conversation", key = "reset_convo", on_click = reset_conversation)

    history = ""
    #build the conversation history
    for msg in msgs.messages:
        if msg.type == "ai":
            history += f"AI: {msg.content}\n\n"
        else:
            history += f"Human: {msg.content}\n\n"

    st.expander("Conversation history", expanded = True).write(history)



def getData (testing = False ): 
    """Collects answers to main questions from the user. 
    
    The conversation flow is stored in the msgs variable (which acts as the persistent langchain-streamlit memory for the bot). The prompt for LLM must be set up to return "FINISHED" when all data is collected. 
    
    Parameters: 
    testing: bool variable that will insert a dummy conversation instead of engaging with the user

    Returns: 
    Nothing returned as all data is stored in msgs. 
    """

    ## if this is the first run, set up the intro 
    if len(msgs.messages) == 0:
        msgs.add_ai_message(f"Hi there -- I'm collecting stories about  {st.session_state.package['questions_intro']} \n\n  Let me know when you're ready! ")


   # as Streamlit refreshes page after each input, we have to refresh all messages. 
   # in our case, we are just interested in showing the last AI-Human turn of the conversation for simplicity

    if len(msgs.messages) >= 2:
        last_two_messages = msgs.messages[-1:]
    else:
        last_two_messages = msgs.messages

    for msg in last_two_messages:
        if msg.type == "ai":
            with entry_messages:
                st.chat_message(msg.type).write(msg.content)


    # If user inputs a new answer to the chatbot, generate a new response and add into msgs
    if prompt:
        # Note: new messages are saved to history automatically by Langchain during run 
        with entry_messages:
            # show that the message was accepted 
            st.chat_message("human").write(prompt)
            
            # generate the reply using langchain 
            response = conversation.invoke(input = prompt)
            
            # the prompt must be set up to return "FINISHED" once all questions have been answered
            # If finished, move the flow to summarisation, otherwise continue.
            if "FINISHED" in response['response']:
                st.divider()
                st.chat_message("ai").write("Great, I think I got all I need -- click okay to continue.")

                # call the summarisation  agent
                st.session_state.agentState = "done"
                
                st.button("Okay")
            else:
                st.chat_message("ai").write(response["response"])


def stateAgent(): 
    """ Main flow function of the whole interaction -- keeps track of the system state and calls the appropriate procedure on each streamlit refresh. 
    """

    # Main loop -- selecting the right 'agent' each time: 
    if st.session_state['agentState'] == 'start':
            getData()
            # summariseData(testing)
            # reviewData(testing)
    elif st.session_state['agentState'] == 'done':
            convo_finished()



if 'package' not in st.session_state:
    st.write("Please go to the previous page and provide the questions and example answers first.")
else:

    ## set up UX model 
    st.sidebar.write("This page is here for you to explore how your current questions would be asked by the bot. The questions in your question set are as follows. If you want to change these, please go back to the previous stages .")

    lines = st.session_state.package['questions_str'].splitlines()
    nq = st.session_state.package['questions_num']
    qs = ""
    for n in range(1, nq + 1):    
        qs += (f"- {lines[n-1].strip()}\n \n") 

    st.sidebar.write(qs)

    ## create the UX structure
    entry_messages = st.expander("Collecting your story", expanded = True)

    # create the user input object 
    prompt = st.chat_input()

    # initialise the session state variables
    
    init_session_stateVars()

    # Set up memory for the lanchchain conversation bot
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(memory_key="history", chat_memory=msgs)




    # Set up the LangChain for data collection, passing in Message History
    chat = ChatOpenAI(temperature=0.3, model=st.session_state.llm_model, openai_api_key = st.secrets.openai_api_key)

    prompt_datacollection = f"""You're a trained psychologist. Your goal is to gather structured answers to the following questions. 
    
    {qs}

    {prompt_datacollection_old}
    """
    
    print(prompt_datacollection)

    prompt_updated = PromptTemplate(input_variables=["history", "input"], template = prompt_datacollection)

    conversation = ConversationChain(
        prompt = prompt_updated,
        llm = chat,
        verbose = True,
        memory = memory
        )

    # start the flow agent 
    stateAgent()    