import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

class HistoryTeacherChat(Command):
    def __init__(self):
        super().__init__()
        self.name = "history"
        self.description = "This agent is pretending to be a history teacher of ancient Rome"
        self.history = []
        load_dotenv()
        API_KEY = os.getenv('API-KEYXX')
        # you can try GPT4 but it costs a lot more money than the default 3.5
        # self.llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-4-0125-preview")  # Initialize once and reuse
        # This is default 3.5 chatGPT
        # self.llm = ChatOpenAI(openai_api_key=API_KEY)  # Initialize once and reuse

    def calculate_tokens(self, text):
        # More accurate token calculation mimicking OpenAI's approach
        return len(text)

    def interact_with_ai(self, user_input, character_name):
        # Generate a more conversational and focused prompt
        era = '17th century england'
        prompt_text = f"Imagine you are a distinguished teacher with a deep knowledge of {era}, tasked with guiding a learner's exploration of this subject. Begin the interaction by posing an initial question that covers a foundational aspect of {era} history, ensuring it is accessible for a broad range of knowledge levels. Based on the learner's response, if they answer correctly, increase the complexity of the next question to challenge them further. Conversely, if the answer is incorrect, maintain or slightly decrease the difficulty to build their confidence and understanding. Proceed with this adaptive approach through three questions, each time providing feedback that includes corrections or additional insights as necessary. After the third question, offer a comprehensive assessment of their performance, highlighting their strengths, areas for improvement, and encouragement for their continued learning and curiosity about {era} history."
        prompt = ChatPromptTemplate.from_messages(self.history + [("system", prompt_text)])
        
        output_parser = StrOutputParser()
        chain = prompt | self.llm | output_parser

        response = chain.invoke({"input": user_input})

        # Token usage logging and adjustment for more accurate counting
        tokens_used = self.calculate_tokens(prompt_text + user_input + response)
        logging.info(f"OpenAI API call made. Tokens used: {tokens_used}")
        return response, tokens_used

    def execute(self, *args, **kwargs):
        character_name = kwargs.get("character_name", "Movie Expert")
        print(f"This your Roman history teacher")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Thank you for using the Movie Expert Chat. Goodbye!")
                break

            self.history.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Movie Expert: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.history.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")

