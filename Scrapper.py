import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import soundex


# create a class to scrape the data
class Scrapper:

    def __init__(self, url):
        # the url of the scrapper
        self.url = url
        # the data of the scrapper
        self.data = {}
        # call the function to get the data
        self.get_all_recipe()
        # store the last recipe
        self.last_recipe = None

    def get_all_recipe(self):
        # get the data from the url given as the constructor parameter
        request = requests.get(self.url)
        # we use the html5lib because the website is using some tag like td and "tr" that are not supported by the
        # default parser
        soup = BeautifulSoup(request.text, "html5lib")
        # change the select table to iterate over
        content = soup.body.table.tbody.select("tr")[1].select("td")[0].select("table")  # .td.text
        for recipes in content:
            # find all the tag "td" and skip the 4 (Name Ingredients Image Description)
            loops = recipes.find_all("td")[4:]
            # we use the zip function to iterate over multiple elements at the same time
            # we save time by iterating over all the element of the same tag
            for name, resource, recipe, description in zip(loops[::4], loops[1::4], loops[2::4], loops[3::4]):
                # add to the dictionary the name as the key and the resource, recipe and description as the value
                self.data[name.text] = [resource.text,
                                        "https://www.minecraftcrafting.info/" + recipe.img["src"],
                                        description.text]

    # method that take a string as parameter and return the data of the recipe if it exists
    def check_recipe(self, sentence):
        if self.check_similarity(sentence) or self.check_soundex(sentence):
            return True

    # method that take a string as parameter and return true if the word is almost the same
    def check_similarity(self, sentence):
        for word in sentence.split():
            self.last_recipe = process.extractOne(word, self.data.keys(), score_cutoff=80, scorer=fuzz.ratio)
            if self.last_recipe is not None:
                self.last_recipe = self.last_recipe[0]
                return True

    # create a methode that will take a sentence as parameter and check if any recipe match the sentence
    # with the soundex algorithm
    def check_soundex(self, sentence):
        sound = soundex.getInstance()
        # for every word in the sentence
        for word in sentence.split():
            # for every recipe in the dictionary
            for recipe in self.data.keys():
                # if the recipe is in the soundex algorithm
                if sound.soundex(word) == sound.soundex(recipe):
                    self.last_recipe = recipe
                    # return the data of the recipe
                    return True

    # create a method that return the data of the recipe
    def get_recipe(self, recipe_name):
        return self.data[recipe_name]
