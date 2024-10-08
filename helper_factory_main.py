import streamlit as st 

overview_page = st.Page("helper_overview.py", title = "🧭 Overview")
questions_page = st.Page("helper_prototype.py", title = "🤖 Build your bot")
personas_page = st.Page("helper_personas.py", title = "🕵🏻‍♀️ Finetune your personas")
chatbot_page = st.Page("helper_conversation_bot.py", title = " 🧐 Test data collection")
# testing_page = st.Page("helper_testing.py", title = "Step 3: Test your bot")


pg = st.navigation([overview_page, questions_page, personas_page, chatbot_page])

pg.run()