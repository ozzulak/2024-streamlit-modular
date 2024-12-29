import streamlit as st 

## get all the prompts needed 
from helper_prompts import *


overview_page = st.Page("helper_overview.py", title = "🧭 Overview")
questions_page = st.Page("helper_questions.py", title = "💡 Design your questions")
chatbot_page = st.Page("helper_conversation_bot.py", title = "🧪 Test data collection")
personas_page = st.Page("helper_personas.py", title = "🕵🏻‍♀️ Finetune your personas")
prototype_page = st.Page("helper_prototype.py", title = "⚙️ Build your bot")
export_page = st.Page("helper_export.py", title = "🚀 Export your config")


# testing_page = st.Page("helper_testing.py", title = "Step 3: Test your bot")





def init_package():
    # we are setting up a single 'package' that will include all the information needed for config file
    st.session_state['package'] = {
        'stage' : 'step1',
        'questions_intro': "a time you were able to connect with your child today. Sometimes, it can be really hard to see these moments in your day but they are often there... even if they are really, really small!",
        'questions_num': 5,
        'questions_str' : init_questions,
        'current_example_set' : init_exampleSet,
        'new_example_set': "",
        'persona': init_persona,
        'convo': "Copy & paste a dialogue, or create one in the 'Test data collection' step on the left. ",
        'convo_extract': "Write your own dialogue, or create on in the 'Test data collection' step on the left. ",
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


pg = st.navigation([overview_page, questions_page, chatbot_page, prototype_page, personas_page, export_page])

pg.run()