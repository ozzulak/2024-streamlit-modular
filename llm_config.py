import tomllib

class LLMConfig:

    def __init__(self, filename):

        with open(filename, "rb") as f:
            config = tomllib.load(f)

        self.questions_intro = config["questions"]["intro"]
        self.questions_prompt = self.generate_questions_prompt(config["questions"])
        self.questions_outro = "Great, I think I got all I need -- but let me double check!"

        self.extraction_task = f"Create a scenario based on these responses. {config['summaries']['language_type']}"
        self.extraction_prompt = self.generate_extraction_prompt(config["summaries"])
        self.extraction_adaptation_prompt = self.generate_adaptation_prompt()

        self.personas = list(config["summaries"]["personas"].values())
        self.example_messages = config["example"]["messages"]
        self.example_summary = config["example"]["summary"]
        self.one_shot = self.generate_one_shot(config["questions"]["specific"], config["example"]["summary"])


    def generate_questions_prompt(self, questions):

        questions_prompt = f"{questions['persona']}\n\nYour goal is to gather structured answers to the following questions.\n\n"

        n_general = len(questions["general"])
        if questions["general"]:
            questions_prompt += f"You start with {n_general} general question{'s' if n_general > 1 else ''}:\n"
            for count, question in enumerate(questions["general"]):
                questions_prompt += f"{count+1}. {question}\n"

        n_specific = len(questions["specific"])
        questions_prompt += f"\nYou proceed to ask the following {n_specific} questions about a specific experience they had:\n"
        for count, question in enumerate(list(questions["specific"].values())):
            questions_prompt += f"{n_general+count+1}. {question}\n"

        questions_prompt += f"\nAsk each question one at a time. {questions['language_type']} "\
            "Ensure you get at least a basic answer to each question before moving to the next. "\
            "Never answer for the human. "\
            "If you unsure what the human meant, ask again."

        n_total = n_general + n_specific
        questions_prompt += f'\n\nOnce you have collected answers to all {n_total} question{"" if n_total == 1 else "s"}, stop the conversation and write a single word "FINISHED".\n\n'\
            "Current conversation:\n{history}\nHuman: {input}\nAI:"

        return questions_prompt


    def generate_extraction_prompt(self, summaries):

        keys = list(summaries['questions'].keys())
        keys_string = f"`{keys[0]}`"
        for key in keys[1:-1]:
            keys_string += f", `{key}`"
        if len(keys_string):
            keys_string += f", and `{keys[-1]}`"

        extraction_prompt = "You are an expert extraction algorithm. " \
            "Only extract relevant information from the Human answers in the text. " \
            "Use only the words and phrases that the text contains. " \
            "If you do not know the value of an attribute asked to extract, return null for the attribute's value.\n\n" \
            f"You will output a JSON with {keys_string} keys.\n\n" \
            f"These correspond to the following question{'s' if len(keys) else ''}:\n"

        
        for count, question in enumerate(summaries["questions"].values()):
            extraction_prompt += f"{count+1}: {question}\n"
            

        extraction_prompt += "\nMessage to date: {conversation_history}\n\n" \
            "Remember, only extract text that is in the messages above and do not change it. "
        
        return extraction_prompt
    

    def generate_adaptation_prompt(self):

        prompt_adaptation = "You're a helpful assistant, helping students adapt a scenario to their liking. The original scenario this student came with:\n\n" \
            "Scenario: {scenario}.\n\n" \
            "Their current request is {input}.\n\n" \
            "Suggest an alternative version of the scenario. Keep the language and content as similar as possible, while fulfilling the student's request.\n\n" \
            "Return your answer as a JSON file with a single entry called 'new_scenario'."

        return prompt_adaptation


    def generate_one_shot(self, questions, example_answers):

        one_shot = "{main_prompt}\n\nExample:\n"

        for key, question in questions.items():
            one_shot += f"Question: {question}\n"
            one_shot += f"Answer: {example_answers[key]}\n"

        one_shot += "\nThe scenario based on these responses: {example_scenario}\n\n" \
            "Your task:\n Create scenario based on the following answers:\n\n"

        for key, question in questions.items():
            one_shot += f"Question: {question}\n"
            one_shot += f"Answer: {{{key}}}\n"

        one_shot += "\n{end_prompt}\n\nYour output should be a JSON file with a single entry called 'output_scenario'"

        return one_shot
