import streamlit as st 

overview_page = st.Page("helper_overview.py", title = "Overview")
questions_page = st.Page("helper_prototype.py", title = "Build your bot")
# personas_page = st.Page("helper_personas.py", title = "Step 2: Finetune your personas")
# testing_page = st.Page("helper_testing.py", title = "Step 3: Test your bot")


pg = st.navigation([overview_page, questions_page])

pg.run()