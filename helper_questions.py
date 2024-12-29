import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langsmith import Client
from langsmith import traceable
import os




st.set_page_config(page_title="Step 1: design your questions", page_icon="🤷🏻‍♂️")
# st.title("Step 1: Design your questions")




## called once the "update questions and persona" button is pressed: 
def update_qp():
    qs = st.session_state['questions'] 
    nq = st.session_state['questions_num']
    
    # update the questions in the package    
    st.session_state.package['questions_str'] = qs  # save current questions
    st.session_state.package['questions_num'] = nq
    st.session_state.package['questions_intro'] = st.session_state['questions_intro']
    


def setupSidebar(): 
    ## set up side bar content

    st.sidebar.write("Your currently selected questions are:")
    lines = st.session_state.package['questions_str'].splitlines()
    nq = st.session_state.package['questions_num']
    qs = ""
    for n in range(1, nq + 1):    
        qs += (f"- {lines[n-1].strip()}\n \n") 

    st.sidebar.write(qs)


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

# # load up initial questions
# if 'firstRun' not in st.session_state:
#     st.session_state['firstRun'] = True
#     update_qp()
    


## set up basic structure of the page -- simple set of questions: 

intro_qs = st.container()
collecting_qs = st.container()

with intro_qs:
    st.markdown("""This page is here for you to explore which questions you would like to ask in your bot. You do so in few simple steps: 
1. You outline what kinds of stories you want to collect. 
2. Then you specify the questions you want to ask.
3. You can then test them out in a bot on the next page (and can always return & update them here). 
    """)
    st.divider()


with collecting_qs:    
    st.text_area("I want to collect stories about ...", key = 'questions_intro', value = st.session_state.package['questions_intro'], height = 68)

    st.text_area("Questions to ask -- one per line", value = st.session_state.package["questions_str"], key = "questions", height = 140)

    st.select_slider("How many of the Qs above should the bot ask? \n(first N will be used)", options = [ 3, 4, 5, 6], value = st.session_state.package["questions_num"], key = "questions_num")

    st.button("I've updated questions & want to test them", key = 'q_updated', on_click = update_qp)

    if st.session_state['q_updated']:
        st.switch_page("helper_conversation_bot.py")