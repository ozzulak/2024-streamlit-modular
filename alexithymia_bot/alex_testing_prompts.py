test_messages = """
    
            Message to date: AI: Let's talk about how your day went! 

  Let me know when you're ready!
Human: ready
AI: Tell me about something bad or stressful that happened to you today.
Human: I have test due tomorrow that is worth a lot of marks, I haven't been studying properly for it and am not ready
AI: What’s the context? What else should we know about the situation?
Human: I've been doing this course for awhile, it's important I pass - my parents are putting pressure on me
AI: How did you react with your behavior when you realized you weren't ready for the test?
Human: I think I've just given up, I haven't really tried to study since, there is no point, not enough time
AI: What were your thoughts at the time about not being ready for the test?
Human: Basically that I'm screwed, I reckon I'm going to fail the course. It's going to be a disaster
AI: How did the situation make you feel and how intense was the feeling?
Human: I'm not sure, I just feel bad
AI: With this feeling of feeling bad, let's think about it like a curious scientist and explore it. Where did you feel it in your body? What shape is it? What color is it? Is it heavy or light? Is it moving or still?
Human: A lot of it seems to be in my chest, really heavy. Maybe a bit in my head
AI: What shape and color would you say this feeling in your chest and head is? Is it moving or still?
Human: I don't think it has a colour, it's pretty still
    """


# create an answer set -- which we can use a separate interactive agent to get to:


answer_set = {
    "what": "I have test due tomorrow that is worth a lot of marks, I haven't been studying properly for it and am not ready",
    "context": "I've been doing this course for awhile, it's important I pass - my parents are putting pressure on me",
    "behaviour": "I think I've just given up, I haven't really tried to study since, there is no point, not enough time",
    "thoughts": "Basically that I'm screwed, I reckon I'm going to fail the course. It's going to be a disaster",
    "feel": "I just feel bad",
    "mindful": "A lot of it seems to be in my chest, really heavy. Maybe a bit in my head. I don't think it has a colour, it's pretty still"
}

answer_set_emotional = {
  "what": "I sent a report to my boss, and they said it wasn't good enough and I need to redo it",
  "context": "I'd been working on that report for a while, so it was disappointing to hear it wasn't good enough. I'm quite new to this job, so I want to impress people, but it's going badly",
  "behaviour": "I stayed pretty quiet in the meeting, I just said sorry and that I'd try to improve it. I haven't really looked at the document since then, it's hard to look at",
  "thoughts": "It surprized me. I thought the report was ok, so to hear I needed to fix a bunch of things was a surprize. It made me feel anxious, and embarrassed. Like I can't be sure anymore about my work, maybe I'm not good enough to work there",
  "feel": "anxious and embarrassed, quite intense",
  "mindful": "I think mainly in my head and chest. It was like a pressure. No colour. I think like a big blob at the top of my body, it felt heavy, tight"
}