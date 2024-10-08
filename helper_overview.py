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
1. **the core questions** you want the system to ask ... and the answers to which will combine into a *good* story! This is the heart of a good micro-narrative, and the ability for the researcher to 'inject' some psychological theory into the story creation.
2. **example answers set & scenario**, which teaches the LLM how to combine your questions into a linear narrative 
3. **three personas**, which guides how the system fills in the 'connective tissue' in between the user's answers. 

Note that the :violet[core questions] are going to be different to what you would normally use in interviews -- the idea here is that you use each question to uncover another key facet of the story you think the participant can tell; while ensuring that putting these all facets together creates a coherent story. 

In our experience, the best micro-narratives happen when the questions ask about parts of participants' experience that they might not consider necessarily important, but that pull out something crucial about their perspective about the world. 

As a team, we are still trying to understand how best to generate such templates, and how to help others to do so too ... thus also this :robot_face::factory:.
""")



st.markdown("""### What now? 

The rest of this system is created to help you make all three steps of the template, one at a time. 

1. First, we will look at identifying the *questions* you think the bot should be asking, give some answers that mirror what you think your users could say; and see how the narratives shape up (or not). This then also creates your *answer set*. Please do expect that this *could be an iterative process, as getting the questions right is what makes or breaks your micro-narrative bot*!

2. Second, we will then allow you to try your questions & suggested answer set to test your three *personas* you would like your system to use. 

3. Third, you will get to experience a test run of how your bot could work and get the underlying config file ... Note that in ~ weeks we should be also able **spit out the python code that you can run on your own server** (-- this still in progress""")

st.button("I'm ready")



