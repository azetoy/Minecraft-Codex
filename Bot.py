from chatterbot import ChatBot
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from Scrapper import Scrapper
from PIL import Image
import requests
from io import BytesIO


# create chatbot class


class Bot:
    def __init__(self, html_link):
        self.scrapper = Scrapper(html_link)
        self.chatbot = ChatBot("Herobrine", response_selection_method=get_first_response,
                               logic_adapters=[{
                                   "import_path": "chatterbot.logic.BestMatch",
                                   "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance"
                               }])
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer.train("chatterbot.corpus.french.conversations")

    def run(self):
        while True:
            user_input = input("You: ")
            if user_input == "Bye":
                print("Herobrine: Bye")
                break

            elif self.scrapper.check_recipe(user_input):
                print("Herobrine: " + " Yes of course here are all the information about the recipe ")
                print("For the material you need " + self.scrapper.data[self.scrapper.last_recipe][0])
                print("and here a quick description : " + self.scrapper.data[self.scrapper.last_recipe][2])
                response = requests.get(self.scrapper.data[self.scrapper.last_recipe][1])
                Image.open(BytesIO(response.content)).show()
                print("Also you may need this link to see how to build it : " +
                      self.scrapper.data[self.scrapper.last_recipe][1])

            else:
                response = self.chatbot.get_response(user_input)
                print("Herobrine: ", response)
