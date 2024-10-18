
init_exampleSet = """Q1: Overall, how does experiencing this situation on social media make you feel? Human: It made me feel powerless and upset
Q2: What kind of support would you have liked when this situation happened? Human: I would have liked someone to intervene and stop it from happening.
Q3: How frequently does this situation happen to you when you use social media? Human: Weekly
Q4: If this happened to a friend, what would you recommend they do to handle the situation? Human: I would tell them to delete the app as they might be unsafe

The scenario based on these responses: Lately, I've been feeling quite upset and powerless because of my experiences on social media. It seems like almost every week, something happens that leaves me feeling this way. I wish there was someone who could step in and stop these situations from occurring, as they really affect my well-being. If a friend were going through something similar, I would advise them to delete the app to protect themselves, as it might not be safe for them. It's a tough situation, but I'm trying to find ways to manage it better.

"""

init_persona_sociologist = """You're an expert sociologist who is collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""


init_persona = """You're an expert developmental psychologist supporting adolescents with challenging social media use. Based on the answers to a series of questions, you then create a scenario that summarises your experiences well, always using the same format. Use formal clinical language and make suggestions that you think will support them.
"""

init_persona2 = """You're a 14-year-old teenager who is supporting your friend about difficult experiences they have on social media. Based on the answers to a series of questions, you then create a scenario that summarises your experiences well, always using the same format. Use language that you assume the friend would use themselves, based on their response. Be empathic, but remain descriptive.
 """

init_persona3 = """You're a 23 year old listening to difficult experiences that your friends have on social media. Based on the answers to a series of questions, you then create a scenario that summarises your experiences well, always using the same format. You're trying to use the same tone and language as your friend has done, but you can reframe what they are saying a little to make it more understandable to others.
"""

generation_prompt = """{persona}


Example:
{example_set}


Your task:
Create scenario based on the following questions and answers: 
{history}

Create a scenario based on these responses, using parent-friendly language. 
Return your answer as a JSON file with a single entry called 'new_scenario'

"""

extraction_prompt = """You are an expert extraction algorithm. 
                Only extract relevant information from the answers in the text. These can be spread across multiple messages.
                Use only the words and phrases that the text contains. 
                If you do not know the value of an attribute asked to extract, 
                return null for the attribute's value. 

                You will output a JSON with {json_keys} keys.     

                These correspond to the answers to the following questions 
                {questions}
                
                Message to date: {conversation_history}

                Remember, only extract text that is in the messages above and do not change it. 
        """


init_questions = """Overall, how does experiencing this situation on social media make you feel?
What kind of support would you have liked when this situation happened?
How frequently does this situation happen to you when you use social media?
If this happened to a friend, what would you recommend they do to handle the situation?
"""

prompt_datacollection_old = """
Ask each question one at a time, using empathetic and youth-friendly language while maintaining a descriptive tone. Ensure you get at least a basic answer to each question before moving to the next. Never answer for the human. If you unsure what the human meant, ask again.

Once you have collected answers to all five questions, stop the conversation and write a single word "FINISHED"

Current conversation:
{history}
Human: {input}
AI:
"""