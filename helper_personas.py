import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
import os
from helper_prompts import *


smith_client = Client()
## The assumption here is that users have gone through step 1 -- i.e., we have questions and example answer to insert into the bot now 

## TODO insert the check for this this 



def story_ready(): 
    st.session_state['ready'] = True

def persona_updates():
    """ Called when user clicks Update personas button. Will update the st.session_state.package['personas'] and run the three LLM calls. 
    """

    st.session_state.package['personas']['p1'] = st.session_state['persona1']
    st.session_state.package['personas']['p2'] = st.session_state['persona2']
    st.session_state.package['personas']['p3'] = st.session_state['persona3']

@traceable
def create_scenario(history,persona, one_shot):
    chat = ChatOpenAI(temperature=0.3, model="gpt-4o", openai_api_key = st.secrets.openai_api_key)

    # start by setting up the langchain chain from our template (defined in lc_prompts.py)
    scenario_template = PromptTemplate(input_variables = ["history", "persona", 'example_set'], template = generation_prompt)
    # st.write(scenario_template)

    # add a json parser to make sure the output is a json object
    json_parser = SimpleJsonOutputParser()

    # connect the prompt with the llm call, and then ensure output is json with our new parser
    chain = scenario_template | chat | json_parser

    scenario = chain.invoke({"history" : history, "persona" : persona, "example_set": one_shot})

    return(scenario)



def generate_story(persona):
    answer = create_scenario(st.session_state['persona_user_history'], st.session_state[persona], st.session_state.package['current_example_set'])
    return answer['new_scenario']


def regenerate_stories():
    st.session_state['temp_stories'] = {
        'p1': generate_story('persona1'),
        'p2': generate_story('persona2'),
        'p3': generate_story('persona3')
    }
    # print(st.session_state['temp_stories'])

def setup_first_run(): 
        st.session_state.package['personas']['p1'] = init_persona
        st.session_state.package['personas']['p2'] = init_persona2
        st.session_state.package['personas']['p3'] = init_persona3
        st.session_state['ready'] = False
        st.session_state['temp_stories'] = {
                    'p1': 'add your story and click ready',
                    'p2': 'add your story and click ready',
                    'p3': 'add your story and click ready'
                }

if 'package' not in st.session_state:
    st.write("Please go to the previous page and provide the questions and example answers first.")
else:

    ## is this the first run -- set up personas from init values
    if 'p_run' not in st.session_state:
        setup_first_run()
        st.session_state['p_run'] = True
        
    ## Let's start by setting out the main page structure -- info, three columns, and user dialogue (as callout? )
    st.sidebar.write("This page is here for you to explore & finalise possible personas. We assume you already went through Step 1 -- the bot knows your questions and you already provided an example answers set.")

    st.sidebar.text_input("Persona 1 label", key = "label_p1", value = "Parent")
    st.sidebar.text_input("Persona 2 label", key = "label_p2", value = "Psychoanalyst")
    st.sidebar.text_input("Persona 3 label", key = "label_p3", value = "Parenting coach")

    test_container = st.container()

    # exp_history = st.expander("Insert user answers")
    # exp_persona = st.expander("Persona definitions")
    # exp_stories = st.expander("Resulting stories")
    

    exp_history, exp_persona, exp_stories, exp_config = st.tabs(["🗣 Insert user answers", "🧞 Persona definitions", "📚 Resulting stories", "🔮 Current config"])

    with exp_history:
        ## build the conversation history string and questions string 
        if not st.session_state['ready']: 
            convo = ""
            qs = st.session_state.package['questions_str']
            lines = qs.splitlines()
            nq = st.session_state.package['questions_num']
            for n in range(1, nq + 1):
                convo += (f"{lines[n-1].strip()} \nHuman:  \n \n") 
        else:
            convo = st.session_state['persona_user_history']            
        st.text_area("fill in your conversation here:", value = convo, height= 400, key = "persona_user_history", label_visibility= "hidden")

        st.button("Ready", on_click = story_ready)


    with exp_persona: 
    ## create 3 text boxes for personas
        st.text_area(st.session_state['label_p1'], value = st.session_state.package['personas']['p1'], key = "persona1", height = 150)
        st.text_area(st.session_state['label_p2'], value = st.session_state.package['personas']['p2'], key = "persona2", height = 150)
        st.text_area(st.session_state['label_p3'], value = st.session_state.package['personas']['p3'], key = "persona3", height = 150)

        st.button("Update personas", key = "button_persona_update", on_click = persona_updates)

    with exp_stories: 
        column_stories = st.container()
        follow_up = st.container()

        
        ## is this the first run? 

        with follow_up:
            st.button("Regenerate stories", key='regenerate', on_click=regenerate_stories)
            
        with column_stories: 
            col1, col2, col3 = st.columns(3)

            with col1: 
                    st.header("Scenario 1") 
                    st.write(st.session_state.temp_stories['p1'])

            with col2: 
                    st.header("Scenario 2") 
                    st.write(st.session_state.temp_stories['p2'])

            with col3: 
                    st.header("Scenario 3") 
                    st.write(st.session_state.temp_stories['p3'])
        

with exp_config: 
    
    ## build the conversation history string and questions string 
    lines = st.session_state.package['questions_str'].splitlines()
    nq = st.session_state.package['questions_num']
    qs = ""
    for n in range(1, nq + 1):    
        qs += (f"- Q{n}: {lines[n-1].strip()}\n \n") 
    

    st.write("This tab just shows you what configuration your bot has right now.")
    st.divider()

    st.markdown(f"**Your questions:** \n")
    st.write(qs)
    st.divider()
    st.markdown(f"**Your one-shot example:** \n")
    st.write(st.session_state.package['current_example_set'])
    st.divider()
    st.markdown(f"**Your current personas:** \n")
    st.write(st.session_state.package['personas'])