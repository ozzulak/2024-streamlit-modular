import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
import os

smith_client = Client()
## The assumption here is that users have gone through step 1 -- i.e., we have questions and example answer to insert into the bot now 

## TODO insert the check for this this 

DEBUG = False


st.session_state['ready'] = False

generation_prompt = """{persona}

Example:
{scenario}

Your task:
Create scenario based on the following questions and answers: 
{history}

Create a scenario based on these responses, using parent-friendly language. 
Return your answer as a JSON file with a single entry called 'new_scenario'

"""

init_questions = """Q1: What was the win or breakthrough situation you experienced?
Q2: I’d like to know more about the situation. What was happening at the time that was making the situation tricky? 
Q3: What did you do or say to manage the situation and how did your child react?
Q4: How did that make you feel?
Q5: What would you tell a younger version of you who is trying to manage this tricky situation?
"""


init_persona = """You're an expert sociologist who is collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""


init_persona2 = """You're an expert medievalist who only speaks with a scottish lingo. You are collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""

init_persona3 = """You're a parenting coach who works with low-SES populations. You only use simple language and short sentences. You are collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""


init_example_set = """
Q1: What was the win or breakthrough situation you experienced? 
Human:  Child was upset after school as they weren’t selected for the school play
 
Q2: I’d like to know more about the situation. What was happening at the time that was making the situation tricky? 
Human:  In the car on the way home from school, Sam looked upset and said that all his friends had a part in the show but he wasn’t selected.
 
Q3: What did you do or say to manage the situation and how did your child react? 
Human:  I was driving so couldn’t give full attention but I remembered something I’d read about acknowledging feelings. I told him that it must have made him feel really sad. He then opened up and told me more about the situation. 
 
Q4: How did that make you feel? 
Human:  It was a win to know I didn’t need to solve everything and that Sam was willing to open up instead of bottling it in.
 
Q5: What would you tell a younger version of you who is trying to manage this tricky situation? 
Human:  Don’t try to always fix stuff. Kids go through tough times and they need to learn how to deal with them. As a parent I can be there to support them with those tough times.
 
 
 The scenario based on these responses: Recently, I encountered a parenting moment that felt like a small victory in understanding my child's emotions. After school one day, my child, Sam, seemed visibly upset during our drive home. He shared that he was disappointed because he wasn't selected for the school play, while all his friends had secured roles. As I was driving, I couldn't give him my full attention, but I remembered reading about the importance of acknowledging children's feelings. I told Sam that it must have made him feel really sad, and to my relief, he began to open up more about how he was feeling. This experience taught me that I don't always need to have solutions ready; sometimes, just being there to listen is enough. It was reassuring to see that Sam was willing to share his feelings rather than keeping them bottled up. If I could offer advice to a younger version of myself, it would be to resist the urge to fix everything. Children will face challenges, and it's crucial for them to learn how to navigate these experiences. As a parent, my role is to support them through these tough times, providing a safe space for them to express their emotions.
"""

def story_ready(): 
    st.session_state['ready'] = True

def persona_updates():
    """ Called when user clicks Update personas button. Will update the st.session_state.package['personas'] and run the three LLM calls. 
    """

    st.session_state.package['personas']['p1'] = st.session_state['persona1']
    st.session_state.package['personas']['p2'] = st.session_state['persona2']
    st.session_state.package['personas']['p3'] = st.session_state['persona3']

    with test_container: 
        st.write(":green[updated!]")

@traceable
def create_scenario(history,persona, one_shot):
    chat = ChatOpenAI(temperature=0.3, model="gpt-4o", openai_api_key = st.secrets.openai_api_key)

    # start by setting up the langchain chain from our template (defined in lc_prompts.py)
    scenario_template = PromptTemplate(input_variables = ["history", "persona", 'scenario'], template = generation_prompt)
    # st.write(scenario_template)

    # add a json parser to make sure the output is a json object
    json_parser = SimpleJsonOutputParser()

    # connect the prompt with the llm call, and then ensure output is json with our new parser
    chain = scenario_template | chat | json_parser

    scenario = chain.invoke({"history" : history, "persona" : persona, "scenario": one_shot})

    return(scenario)



def generate_story(persona):
    if st.session_state['ready']:
        st.write(":red[please add your testing conversation!]")
    else:
        answer = create_scenario(st.session_state['persona_user_history'], st.session_state[persona], st.session_state.package['example_set'])
        return answer['new_scenario']

# st.write("### :male-factory-worker: :female-factory-worker: In development, please check in later  :female-factory-worker::male-factory-worker: ")

## Let's start by setting out the main page structure -- info, three columns, and user dialogue (as callout? )
st.sidebar.write("This page is here for you to explore & finalise possible personas. We assume you already went through Step 1 -- the bot knows your questions and you already provided an example answers set.")

st.sidebar.text_input("Persona 1 label", key = "label_p1", value = "Persona 1")
st.sidebar.text_input("Persona 2 label", key = "label_p2", value = "Persona 2")
st.sidebar.text_input("Persona 3 label", key = "label_p3", value = "Persona 3")

test_container = st.container()

exp_history = st.expander("User answers")
exp_persona = st.expander("Persona definitions")
exp_stories = st.expander("Resulting stories")

with exp_history:
    ## build the conversation history string and questions string 
    convo = ""
    qs = st.session_state.package['questions_str']
    lines = qs.splitlines()
    nq = st.session_state.package['questions_num']
    for n in range(1, nq + 1):
        convo += (f"{lines[n-1].strip()} \nHuman:  \n \n") 
    
    st.text_area("fill in your conversation here:", value = convo, height= 400, key = "persona_user_history", label_visibility= "hidden")

    st.button("Ready", on_click = story_ready)


with exp_persona: 
## create 3 text boxes for personas
    st.text_area(st.session_state['label_p1'], value = init_persona, key = "persona1", height = 150)
    st.text_area(st.session_state['label_p2'], value = init_persona2, key = "persona2", height = 150)
    st.text_area(st.session_state['label_p3'], value = init_persona3, key = "persona3", height = 150)

    st.button("Update personas", key = "button_persona_update", on_click = persona_updates)

with exp_stories: 
    column_stories = st.container()
    follow_up = st.container()

    
    ## is this the first run? 
    if 'p_run' not in st.session_state:
        if st.session_state['ready']:
            st.session_state['temp_stories'] = {
                'p1': generate_story('persona1'),
                'p2': generate_story('persona2'),
                'p3': generate_story('persona3')
            }
            st.session_state['p_run'] = True
        else:
             st.session_state['temp_stories'] = {
                'p1': 'add your story',
                'p2': 'add your story',
                'p3': 'add your story'
            }

    with follow_up:
        st.button("Regenerate stories", key = 'regenerate')
        
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
    
    if st.session_state['regenerate']:
        st.session_state['temp_stories'] = {
            'p1': generate_story('persona1'),
            'p2': generate_story('persona2'),
            'p3': generate_story('persona3')
        }