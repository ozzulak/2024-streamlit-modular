import streamlit as st 

st.set_page_config(page_title="Export your current configuration", page_icon="🤷🏻‍♂️")
st.title("Export your current configuration")



## build the conversation history string and questions string 
lines = st.session_state.package['questions_str'].splitlines()
nq = st.session_state.package['questions_num']
qs = ""
for n in range(1, nq + 1):    
    qs += (f"- Q{n}: {lines[n-1].strip()}\n \n") 




st.write("Your :green[current configuration] is shown below. You can use this to copy&paste this information into the config file you will use to run your bot.")
st.divider()

st.markdown(f"**Your questions:** \n")
st.write(qs)
st.divider()
st.markdown(f"**Your one-shot example:** \n")
st.write(st.session_state.package['current_example_set'])
st.divider()
st.markdown(f"**Your current personas:** \n")
st.write(st.session_state.package['personas'])


