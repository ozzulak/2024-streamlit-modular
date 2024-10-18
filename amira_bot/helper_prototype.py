import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
import os

## get all the prompts needed 
from helper_prompts import *


# Using streamlit secrets to set environment variables for langsmith/chain
os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']
os.environ["LANGCHAIN_API_KEY"] = st.secrets['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_PROJECT"] = st.secrets['LANGCHAIN_PROJECT']
os.environ["LANGCHAIN_TRACING_V2"] = 'true'


st.set_page_config(page_title="Step 1: design your questions", page_icon="🤷🏻‍♂️")
# st.title("Step 1: Design your questions")

# Langsmith set-up 
smith_client = Client()


def init_package():
    # we are setting up a single 'package' that will include all the information needed for config file
    st.session_state['package'] = {
        'stage' : 'step1',
        'questions_intro': """the story you shared with me today: \n\n "Recently, I've been struggling with something that happened on social media. Someone posted a really unflattering picture of me, and it was clear they did it just to make fun of me. This made me feel incredibly powerless, like I had no control over how people saw me. I tried to ignore the situation, hoping it would just go away. But the worst part was feeling like I was being bullied. It was a tough experience, and it made me question how safe I really am online." 
        """,
        'questions_num': 4,
        'questions_str' : init_questions,
        'current_example_set' : init_exampleSet,
        'new_example_set': "",
        'persona': init_persona,
        'convo': "Please update your questions on the left. ",
        'personas' : {
            'p1' : "",
            'p2' : "",
            'p3' : ""
        }
    }
    st.session_state['ready'] = False


# init if this is run for the first time
if 'package' not in st.session_state:
    init_package()

@traceable
def extractChoices(json_keys, questions, msgs):
    """Uses bespoke LLM prompt to extract answers to given questions from a conversation history into a JSON object. 

    Arguments: 
    msgs (str): conversations history to extract from -- this can be streamlit memory, or a dummy variable during testing
    json_keys (str): a list of keys, likely being 'Q1', 'Q2', 'Q3' ... 
    questions (str): a list of questions, starting with Q1, Q2 ... 

    """

    ## set up our extraction LLM -- low temperature for repeatable results
    extraction_llm = ChatOpenAI(temperature=0.1, model="gpt-4o", openai_api_key=st.secrets.openai_api_key)

    
    extraction_template = PromptTemplate(input_variables=["json_keys", "questions", "conversation_history"], template = extraction_prompt)

    ## set up the rest of the chain including the json parser we will need. 
    json_parser = SimpleJsonOutputParser()
    extractionChain = extraction_template | extraction_llm | json_parser

    
    # allow for testing the flow with pre-generated messages -- see testing_prompts.py
    extractedChoices = extractionChain.invoke({"conversation_history" : msgs, "json_keys" : json_keys, "questions" : questions})
    

    return(extractedChoices)



@traceable
def create_scenario(history,example_set,persona):
    chat = ChatOpenAI(temperature=0.3, model="gpt-4o", openai_api_key = st.secrets.openai_api_key)

    # start by setting up the langchain chain from our template (defined in lc_prompts.py)
    scenario_template = PromptTemplate(input_variables = ["history", "example_set", "persona"], template = generation_prompt)
    # st.write(scenario_template)

    # add a json parser to make sure the output is a json object
    json_parser = SimpleJsonOutputParser()

    # connect the prompt with the llm call, and then ensure output is json with our new parser
    chain = scenario_template | chat | json_parser

    scenario = chain.invoke({"history" : history, "persona" : persona, "example_set" : example_set})

    return(scenario)



## called once the "update questions and persona" button is pressed: 
def update_qp():
    qs = st.session_state['questions'] 
    nq = st.session_state['questions_num']
    
    # update the questions in the package    
    st.session_state.package['questions_str'] = qs  # save current questions
    st.session_state.package['questions_num'] = nq
    st.session_state.package['questions_intro'] = st.session_state['questions_intro']

    # update the conversation: 
    
    lines = qs.splitlines()
    
    if len(lines) < nq:
        st.session_state.package['convo'] = "Add more questions on the left please!"
    else: 
        
        
        convo = ""
        ## build the conversation history string and questions string 
        for n in range(1, nq + 1):    
            convo += (f"Q{n}: {lines[n-1].strip()} \nHuman:  \n \n") 
        
        # now insert to be presented  
        st.session_state.package['convo'] = convo

def setupSidebar(): 
    ## set up side bar content
    st.sidebar.button("Update questions and persona", key = 'q_updated', on_click = update_qp)

    st.sidebar.text_area("I want to collect stories about ...", key = 'questions_intro', value = st.session_state.package['questions_intro'], height = 15)

    st.sidebar.text_area("questions that bot should ask -- one per line", value = st.session_state.package["questions_str"], key = "questions", height = 200)

    st.sidebar.select_slider("How many of the Qs above should the bot ask? \n(first N will be used)", options = [ 3, 4, 5, 6], value = st.session_state.package["questions_num"], key = "questions_num")

    st.sidebar.text_area("Persona", value = st.session_state.package["persona"], key = "persona", height = 200)


def toggle_ready():
    st.session_state['ready'] = not st.session_state['ready'] 



# Define your CSS and inject it -- ensuring smaller font in the text areas. 
style = """
<style>
.stTextArea>div>div>textarea {
    font-size: 12px;
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

setupSidebar()

# load up initial questions
if 'firstRun' not in st.session_state:
    st.session_state['firstRun'] = True
    update_qp()
    


## set up basic structure of the page: 
# Prepare two tabs, one tab to explore in, the other to finalise and move on. 
tab1, tab2, tab3 = st.tabs(['👷‍♀️ Build / test your Qs', '🔎 Update your example', '🔮 See current configuration'])


## First working with tab1 -- helping the user identify their questions
with tab1: 
    st.write("""Hello and welcome. This first step will help you find the right questions for micro-narrative bot. You can do this in three steps: 
1. Start by listing your questions in the sidebar on the left. 
2. Provide sample answers in the expander below. 
3. Check how a resulting narrative could look like by pressing Ready""")

    exp_qs = st.expander("**Insert your example answers here and press Ready when done**", expanded = False)
    exp_llm = st.container()  # insert container to show the LLM in

# write the recent value of convo 
with exp_qs:
    st.text_area("fill in your conversation here:", value = st.session_state.package['convo'], height= 400, key = "convo_history", label_visibility= "hidden")
    st.button("Ready!", key = "ready_llm")


## check that we have the button visualised 
if 'ready_llm' in st.session_state: 
    ## now wait for it to be pressed:
    if st.session_state['ready_llm']:

        # once pressed, let's save the current convo & persona first: 
        st.session_state.package['convo'] = st.session_state['convo_history']
        st.session_state.package['persona'] = st.session_state['persona']

        # load up the data from package: 
        lines = st.session_state.package['questions_str'].splitlines()
        nq = st.session_state.package['questions_num']
        with exp_llm:
            st.write("**This is what LLM extracts:**")
            
            ## create the JSON keys / questions: 
            question_pairs = {}
            for n in range (1, nq + 1):
                question_pairs[f'Q{n}'] = f"Q{n}: {lines[n-1].strip()}"

            # Collecting all keys and values in separate lists
            json_keys = list(question_pairs.keys())
            questions = list(question_pairs.values())

            with st.spinner('Creating your scenario...'):
                scenario = create_scenario(st.session_state['convo_history'], st.session_state.package['current_example_set'], st.session_state['persona'])

            if 'new_scenario' in scenario:  # assuming that the LLM call went well!
                # save the current version of the example in the config-package
                example_set = f"{st.session_state['convo_history']} \n \n The scenario based on these responses: {scenario['new_scenario']}"
                st.session_state.package['new_example_set'] = example_set
                
                # show to the user 
                st.write(scenario['new_scenario'])
            else: 
                st.write("Error in scenario generation: ", scenario)
            # st.write(choices)

## Moving onto the second tab -- now adapting & finalising the scenario examples. 
with tab2: 
    st.write("This tab will help you finalise your example answers set, based on your questions. This will guide your bot as the _'One shot'_ example -- so it is crucial that you have it right, and take a neutral tone.")

    st.write("This is what you have so far ... feel free to edit the answers & resulting scenario, but **do not alter the questions themselves** -- you would need to go back to the `Build your Qs' tab to do that.")

    st.text_area("Finalise your example answers set here:", value = st.session_state.package['new_example_set'], height= 400, key = "fix_answer_set", label_visibility= "hidden") 

    st.button("Save the example above into the bot", key = "fix_answer_set_button")

    # if update clicked  
    if st.session_state['fix_answer_set_button']:
        st.session_state.package['current_example_set'] = st.session_state['fix_answer_set']
        st.write(":green[Perfect, you can get back to the previous tab]")
        st.button("OK")

with tab3: 
    
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
    st.markdown(f"**Your current persona:** \n")
    st.write(st.session_state.package['persona'])