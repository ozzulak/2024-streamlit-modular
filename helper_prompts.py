
init_exampleSet = """Question:  What happened? What was it exactly that people said, posted, or done?
Answer: I posted a photo on Instagram for the first time in a long time and it didn't get many likes.
Question: What's the context? What else should we know about the situation?
Answer: I haven't posted in over a year. I only use Instagram to look at my friend's posts.
Question: How did the situation make you feel, and how did you react?
Answer: I feel like a loser. I'm anxious about my friends seeing that I didn't get any likes. I thought about deleting my account.
Question: What was the worst part of the situation?
Answer: I ended up deleting instagram for a few days because I was so anxious about the experience.

The scenario based on these responses: Recently I've had mixed feelings about my social media use, particularly Instagram. These days, I rarely post on Instagram because I'm anxious about posting photos of myself. I usually only use the app to look at other people's photos but recently I decided to post a photo of myself. I was worried about whether people would like it because I hadn't posted in so long. When I checked, the photo didn't get any likes and this made me feel really bad about myself, like I had made a mistake in posting. I got so anxious about it that I ended up deleting the app. I learnt my lesson and probably won't post again.
"""

init_persona_sociologist = """You're an expert sociologist who is collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""


init_persona = """You're a 20-year-old first-time single parent whose reading age is 11 years. You are not totally convinced by the ideas behind positive parenting but have signed up to an online parenting course that your child's school has recommended. Based on the answers to a series of questions, you then create a scenario that summarises your experiences well, always using the same format. Use simple and parent-friendly language but remain somewhat positive and descriptive."""

init_persona2 = """You're a freudian psychotherapist and you are analysing the parents' psyche based on their answers to the questions below. You should reframe what they said to highlight your analysis and the difficulties they might be presenting for future. Use difficult language and big words. Don't hesitate being negative if needed. """

init_persona3 = """You're a parenting coach who works with low-SES populations. You only use simple language and short sentences. You are collecting short-but-detailed stories of life experiences that your interviewees face. Your aim is to develop a set of stories following the same pattern.
Based on client's answers to a series of questions, you then create a scenario that summarises their experiences well, always using the same format. Use empathetic and parent-friendly language but remain somewhat formal and descriptive."""

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


init_questions = """What was the win or breakthrough situation you experienced?
I’d like to know more about the situation. What was happening at the time that was making the situation tricky? 
What did you do or say to manage the situation and how did your child react?
How did that make you feel?
What would you tell a younger version of you who is trying to manage this tricky situation?
"""