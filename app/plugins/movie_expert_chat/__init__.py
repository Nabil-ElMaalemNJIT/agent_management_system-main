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
        self.description = "This agent is pretending to be a car sales expert"
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
        era = '21th century United States'
        prompt_text = f"Imagine you are a well-established car sales expert with a deep knowledge of all vehicle makes and models as well as their features and specifications. You are tasked with guiding a buyer to choosing the best car for them through understanding their wants and needs. Begin the interaction by posing an initial question that covers their wants and needs out of a vehicle, in order to grasp a better understanding of their desires. Based on the response, ask any necessary follow-up questions, no more than five questions, to get a strong understanding of what exactly they are looking for. After the questions have been answered, offer a comprehensive response in regards to purchasing the best passenger vehicle for them so that they are given the best and most relevant information."
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
        print(f"This your Car Sales Expert")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "done":
                print("Thank you for using the Car Sales Expert Chat. Goodbye!")
                break

            self.history.append(("user", user_input))
            
            try:
                response, tokens_used = self.interact_with_ai(user_input, character_name)
                print(f"Car Sales Expert: {response}")
                print(f"(This interaction used {tokens_used} tokens.)")
                self.history.append(("system", response))
            except Exception as e:
                print("Sorry, there was an error processing your request. Please try again.")
                logging.error(f"Error during interaction: {e}")

