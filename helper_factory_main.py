import streamlit as st 

overview_page = st.Page("helper_overview.py", title = "Overview")
questions_page = st.Page("helper_prototype.py", title = "Step 1: Find your questions")
personas_page = st.Page("helper_personas.py", title = "Step 2: Find personas")
testing_page = st.Page("helper_testing.py", title = "Step 3: Test your bot")


pg = st.navigation([overview_page, questions_page, personas_page, testing_page])

pg.run()