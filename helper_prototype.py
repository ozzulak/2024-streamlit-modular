import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
import os


# Using streamlit secrets to set environment variables for langsmith/chain
os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']
os.environ["LANGCHAIN_API_KEY"] = st.secrets['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_PROJECT"] = st.secrets['LANGCHAIN_PROJECT']
os.environ["LANGCHAIN_TRACING_V2"] = 'true'


st.set_page_config(page_title="Step 1: design your questions", page_icon="🤷🏻‍♂️")
# st.title("Step 1: Design your questions")

st.write("""Hello and welcome. This first step will help you find the right questions for micro-narrative bot. You can do this in three steps: 
1. Start by listing your questions in the sidebar on the left. 
2. Provide sample answers in the expander below. 
3. Check how a resulting narrative could look like by pressing Ready""")

init_persona = """You're an expert sociologist who is collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""

generation_prompt = """{persona}


Example:
Question:  What happened? What was it exactly that people said, posted, or done?
Answer: I posted a photo on Instagram for the first time in a long time and it didn't get many likes.
Question: What's the context? What else should we know about the situation?
Answer: I haven't posted in over a year. I only use Instagram to look at my friend's posts.
Question: How did the situation make you feel, and how did you react?
Answer: I feel like a loser. I'm anxious about my friends seeing that I didn't get any likes. I thought about deleting my account.
Question: What was the worst part of the situation?
Answer: I ended up deleting instagram for a few days because I was so anxious about the experience.

The scenario based on these responses: Recently I've had mixed feelings about my social media use, particularly Instagram. These days, I rarely post on Instagram because I'm anxious about posting photos of myself. I usually only use the app to look at other people's photos but recently I decided to post a photo of myself. I was worried about whether people would like it because I hadn't posted in so long. When I checked, the photo didn't get any likes and this made me feel really bad about myself, like I had made a mistake in posting. I got so anxious about it that I ended up deleting the app. I learnt my lesson and probably won't post again.


Your task:
Create scenario based on the following questions and answers: 
{history}

Create a scenario based on these responses, using parent-friendly language. 
Return your answer as a JSON file with a single entry called 'new_scenario'

"""

extraction_prompt = """You are an expert extraction algorithm. 
                Only extract relevant information from the answers in the text.
                Use only the words and phrases that the text contains. 
                If you do not know the value of an attribute asked to extract, 
                return null for the attribute's value. 

                You will output a JSON with {json_keys}

                These correspond to the following questions 
                {questions}
                
                Message to date: {conversation_history}

                Remember, only extract text that is in the messages above and do not change it. 
        """

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
def create_scenario(history,persona):
    chat = ChatOpenAI(temperature=0.3, model="gpt-4o", openai_api_key = st.secrets.openai_api_key)

    # start by setting up the langchain chain from our template (defined in lc_prompts.py)
    scenario_template = PromptTemplate(input_variables = ["history", "persona"], template = generation_prompt)
    # st.write(scenario_template)

    # add a json parser to make sure the output is a json object
    json_parser = SimpleJsonOutputParser()

    # connect the prompt with the llm call, and then ensure output is json with our new parser
    chain = scenario_template | chat | json_parser

    scenario = chain.invoke({"history" : history, "persona" : persona})

    return(scenario)





# Define your CSS
style = """
<style>
.stTextArea>div>div>textarea {
    font-size: 12px;
}
</style>
"""

# Inject CSS with markdown
st.markdown(style, unsafe_allow_html=True)


init_questions = """What was the win or breakthrough situation you experienced?
I’d like to know more about the situation. What was happening at the time that was making the situation tricky? 
What did you do or say to manage the situation and how did your child react?
How did that make you feel?
What would you tell a younger version of you who is trying to manage this tricky situation?
"""


st.sidebar.text_area("I want to collect stories about a time when ...", value = "[example - change me!]\n ... a parent had a breakthrough with a parenting technique ", height = 20)

st.sidebar.text_area("Possible questions that bot should ask -- one per line", value = init_questions, key = "questions", height = 250)


st.sidebar.select_slider("How many of the Qs above should the bot ask? \n(first N will be used)", options = [ 3, 4, 5, 6], value = 5, key = "questions_num")

st.sidebar.text_area("Persona", value = init_persona, key = "persona", height = 250)

exp_qs = st.expander("**Insert your example answers here and press Ready when done**", expanded = False)
exp_llm = st.container()

# assuming the user input some questions already
if st.session_state['questions'] is not None:
    qs = st.session_state['questions'] 
    lines = qs.splitlines()

    nq = st.session_state['questions_num']

    with exp_qs:
        if len(lines) < nq:
            st.write("Add more questions on the left please!")
        else: 
            ## build the conversation history string: 
            convo = ""
            for n in range(1, nq + 1):
                
                convo += (f"Q{n}: {lines[n-1].strip()} \nHuman:  \n \n")
                # st.text_input(f"Q{n} answer", key = f"ans_Q{n}", label_visibility = "hidden")
            st.text_area("fill in your conversation here:", value = convo, height= 400, key = "convo_history", label_visibility= "hidden")
            st.button("Ready!", key = "ready_llm")
# Langsmith set-up 
smith_client = Client()

## check that we have the button visualised 
if 'ready_llm' in st.session_state: 
    ## now wait for it to be pressed:
    if st.session_state['ready_llm']:
        with exp_llm:
            st.write("**This is what LLM extracts:**")
            
            ## create the JSON keys / questions: 
            question_pairs = {}
            for n in range (1, nq + 1):
                question_pairs[f'Q{n}'] = f"Q{n}: {lines[n-1].strip()}"

            # Collecting all keys and values in separate lists
            json_keys = list(question_pairs.keys())
            questions = list(question_pairs.values())

            # choices = extractChoices(json_keys, questions, st.session_state['convo_history'])
            with st.spinner('Creating your scenario...'):
                scenario = create_scenario(st.session_state['convo_history'], st.session_state['persona'])
            st.write(scenario['new_scenario'])
            # st.write(choices)

            

