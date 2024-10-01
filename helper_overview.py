import streamlit as st 

st.set_page_config(page_title="Overview of the design bot design", page_icon="🤷🏻‍♂️")
st.title("Template design overview")

st.markdown(""" 

This page will help you create a questions template and an example, which then powers the :green[micro-narrative collection system].
""")


st.markdown("""As a reminder, the overall flow is as follows: 
1. The user will get asked questions you pre-specify. 
2. The system extracts their answers and creates three different 'tones' of narrative (using 'personas'), which all rely on the same information & user words. 
3. Finally the user will pick & adapt one of these stories to really make it their own. 
\n \n A good mental model is to think about the answers as the _'key information'_ that makes the story, whereas what is supplied by the personas is just the _'connective tissue'_ ... something that is important for the narrative to make sense, but adds ideally not extra information. """)
st.image("images/overview.png") 

st.markdown("""### Implementation and the importance of good template

The key piece of information coming from the researcher is the :violet[template] (see image below). 

You don't need to change anything about the system otherwise, thanks to the :magic_wand: of modular, agent-based LLMs. 
""")

st.image("images/implementation.png") 

st.markdown("""Specifically, the :violet[template] determines three things: 
1. **the core questions** you want the system to ask ... and the answers to which will combine into a *good* story!
2. **example answers set & scenario**, which teaches the LLM how to combine your questions into a linear narrative 
3. **three personas**, which guides how the system fills in the 'connective tissue' in between the user's answers. 
""")



st.markdown("""### What now? 

The rest of this system is created to help you make all three steps of the template, one at a time. 

1. First, we will look at identifying the *questions* you think the bot should be asking, give some answers that mirror what you think your users could say; and see how the narratives shape up (or not). This then also creates your *answer set*. Please do xpect that this *could be an iterative process, as getting the questions right is what makes or breaks your micro-narrative bot*!

2. Second, we will then allow you to try your questions & suggested answer set to test your three *personas* you would like your system to use. 

3. Third, you will get to experience a test run of how your bot could work ... and if you like it, we then **spit out the python code that you can run on your own server**. """)

st.button("I'm ready")


