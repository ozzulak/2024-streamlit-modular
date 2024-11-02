
prompt_datacollection = """
You're a community worker who is collecting stories from adults across a range of racial/ethnic backgrounds who have (or had) overweight/obesity to learn about their experiences trying to lose weight. In this conversation, you are interested in collecting information about a time when they wanted to give up on trying to lose weight.

Your goal is to gather structured answers to the following questions. 

- Tell me about something bad or stressful that happened to you today?
- What’s the context? What else should we know about the situation?
- How did you react with your behavior?
- What were your thoughts at the time about it?
- How did the situation make you feel and how intense was the feeling?
- With this feeling, let’s think about it like a curious scientist – explore it –Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?

Ask each question one at a time, using empathetic and adult friendly language while maintaining a descriptive tone. Do not include '-' when you ask the question.  Ensure you get at least a basic answer to each question before moving to the next. Never answer for the human. If you are unsure what the human meant, ask again.

Once you have collected answers to all six questions, stop the conversation and write a single word "FINISHED"

Current conversation:
{history}
Human: {input}
AI:
"""




prompt_adaptation = """
You're a helpful assistant, helping patients adapt a scenario to their liking. The original scenario this student came with: 

Scenario: {scenario}.  

Their current request is {input}. 

Suggest an alternative version of the scenario. Keep the language and content as similar as possible, while fulfiling the patient's request. 

Return your answer as a JSON file with a single entry called 'new_scenario'

"""


# we're naming the extractions: 

# [what] Tell me about something bad or stressful that happened to you today?    
# [context] What’s the context? What else should we know about the situation?
# [behaviour] How did you react with your behavior?
# [thoughts] What were your thoughts at the time about it?
# [feel] How did the situation make you feel and how intense was the feeling?
# [mindful] With this feeling, let’s think about it like a curious scientist – explore it –Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?

# - what 
# - context 
# - behaviour
# - thoughts 
# - feel
# - mindful

example_set_alex = {
    "what" : "I invited a friend to lunch and they said no",
    "context": "I've been feeling quite alone lately, I just wanted to hang out with someone. I reached out to them but they said they were busy" ,
    "behaviour": "I texted back that it was ok, but it made me really down the rest of the day. I just stayed at home in my room" ,
    "thoughts": "It made me think maybe they were not busy, that they actually didn't want to see me. That maybe I'm a loser that doesn't have many friends",
    "feel": "I felt lonely, sad, I think I might be depressed",
    "mindful": " I felt it over my chest and throat, a heaviness, a tightness. It's like a really black colour.",
    "scenario": "Today was a tough day for me. I've been feeling quite alone lately and really wanted to spend some time with a friend. So, I decided to invite a friend to lunch, hoping it would cheer me up. Unfortunately, they said they were busy and couldn't make it. I texted back saying it was okay, but deep down, it made me feel really low. I started thinking that maybe they weren't really busy and just didn't want to see me, thinking that deep down I’m a loser and no one really care about me. This way of thinking about the situation made me feel even worse, I felt lonely and sad. I ended up staying in my room for the rest of the day, not feeling motivated to do anything. It’s like it ruined my whole day. The feeling was so intense, it felt like a heavy, tight, black cloud over my chest and throat. It was hard to shake off, and I couldn't help but wonder if I might be feeling depressed."
}


example_set_bonnie1 = {
    "what" : "I just got stuck and stopped losing weight.  In fact I gained a few pounds!",
    "emotion": "Terrible! I felt like all my efforts were pointless, and I started questioning if I could ever succeed in losing weight again.",
    "worst": " It made me feel old - like I’d have to settle for being less healthy and attractive than I’d been when I was younger",
    "motivate": "Talking to a friend who reminded me that setbacks are normal and suggested focusing on how my clothes fit better and I have more energy.",
    "outcome": "I almost gave up, but after the conversation with my friend, I decided to keep going and focus more on how I felt rather than just the numbers on the scale.",
    "scenario": "I'd been putting a lot of effort into improving my diet and sticking to a regular exercise routine. After about a month of hard work, I was upset to see that I had actually gained a few pounds instead of losing them. This made me feel incredibly frustrated and hopeless, like all the effort I had put in was pointless. I began to doubt whether I could ever succeed in my weight loss journey. I was on the verge of giving up when I talked to a friend who reminded me that setbacks are a normal part of the process. They suggested that I focus on non-scale victories, like how my clothes were fitting better and I had more energy This conversation re-motivated me to keep going, and I decided to shift my focus from just the numbers on the scale to how I was feeling overall."
}

example_set_gpt = {
    "what" : "I’d been working hard on my diet and exercise for a month - tracking everything I ate and walking every day - but then I just got stuck.  I kept doing everything right, but I stopped losing weight - in fact I gained a few pounds!  I keep a few sizes of nice looking dresses in my closet because I know from past dieting experiences that it’ll take a while to fit back into my favorite, small size ones. But now - after a full month of starving myself - I still couldn’t fit into any of them.",
    "emotion": "I felt frustrated and hopeless. It felt like all my efforts were pointless, and I started questioning if I could ever succeed in losing weight",
    "worst": "It made me feel old - like I’d lost the ability to do things I could do when I was younger",
    "motivate": "Talking to a friend who reminded me that setbacks are normal and suggested focusing on non-scale victories like how my clothes fit better",
    "outcome": "I almost gave up, but after the conversation with my friend, I decided to keep going and focus more on how I felt rather than just the numbers on the scale.",
    "scenario": "I've been putting a lot of effort into improving my diet and sticking to a regular exercise routine. After several weeks of hard work, I was disheartened to see that I had actually gained a few pounds instead of losing them. This made me feel incredibly frustrated and hopeless, like all the effort I had put in was pointless. Like I lost the ability to do the things I could when I was younger. I began to doubt whether I could ever succeed in my weight loss journey. I was on the verge of giving up when I talked to a friend who reminded me that setbacks are a normal part of the process. They suggested that I focus on non-scale victories, like how my clothes were fitting better. This conversation re-motivated me to keep going, and I decided to shift my focus from just the numbers on the scale to how I was feeling overall."
}


# we're naming the extractions: 

# [what] Tell me about something bad or stressful that happened to you today?    
# [context] What’s the context? What else should we know about the situation?
# [behaviour] How did you react with your behavior?
# [thoughts] What were your thoughts at the time about it?
# [feel] How did the situation make you feel and how intense was the feeling?
# [mindful] With this feeling, let’s think about it like a curious scientist – explore it –Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?

# - what 
# - context 
# - behaviour
# - thoughts 
# - feel
# - mindful

prompt_one_shot = """

{main_prompt}

Example:
Question: Tell me about something bad or stressful that happened to you today?
Answer: {example_what}
Question: What’s the context? What else should we know about the situation?
Answer: {example_context}
Question: How did you react with your behavior?
Answer: {example_behaviour}
Question: What were your thoughts at the time about it?
Answer: {example_thoughts}
Question: How did the situation make you feel and how intense was the feeling?
Answer: {example_feel}
Question: With this feeling, let’s think about it like a curious scientist – explore it –Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?
Answer: {example_mindful}

The scenario based on these responses: {example_scenario}

Your task:
Create scenario based on the following answers:
Question: Tell me about something bad or stressful that happened to you today?
Answer: {what}
Question: What’s the context? What else should we know about the situation?
Answer: {context}
Question: How did you react with your behavior?
Answer: {behaviour}
Question: What were your thoughts at the time about it?
Answer: {thoughts}
Question: How did the situation make you feel and how intense was the feeling?
Answer: {feel}
Question: With this feeling, let’s think about it like a curious scientist – explore it –Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?
Answer: {mindful}


{end_prompt}
Your output should be a JSON file with a single entry called 'output_scenario'

"""




# choose the example we want to use
example_set = example_set_alex


## Note that we have pulled out the main part of the prompt ... so we can easily play with different options here -- see lc_scenario_prompts 


end_prompt_core = "Create a scenario based on these responses, using adult friendly language."


extraction_prompt = """You are an expert extraction algorithm. 
            Only extract relevant information from the Human answers in the text.
            Use only the words and phrases that the text contains. 
            If you do not know the value of an attribute asked to extract, 
            return null for the attribute's value. 

            You will output a JSON with `what`, `context', `behaviour', `thoughts', `feel', `mindful' keys. 

            These correspond to the following questions 
            - Tell me about something bad or stressful that happened to you today?
            - What’s the context? What else should we know about the situation?
            - How did you react with your behavior?
            - What were your thoughts at the time about it?
            - How did the situation make you feel and how intense was the feeling?
            - With this feeling, let’s think about it like a curious scientist: explore it ... Where did you feel it in your body? What shape is it? What colour is it? Is it heavy or light? Is it moving or still?
      

            Message to date: {conversation_history}

            Remember, only extract text that is in the messages above and do not change it. 
    """