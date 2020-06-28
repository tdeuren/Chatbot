""" This is a simple chatbot in the command line.
There are a few things you can ask him.
You can play games and open programs. """
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import json
from sklearn.neural_network import MLPClassifier
import re
import string
from joblib import dump, load
from Webscraping import getweathertoday, gettimenow
import HighwayRider
import Snake
import SpaceInvaders
import mail_functions
import os
import sklearn.utils._cython_blas

stemmer = LancasterStemmer()

class Chatbot:
        def __init__(self, filename):
                self.filename = filename
                try:
                        self.model = load("%s.joblib" %self.filename)
                        self._loadfile()
                except:
                        self.train(filename)

        def _initialize(self):
                for intent in self.data["intents"]:
                        for question in intent["questions"]:
                                #words from question without punctuation and lower
                                words = [re.sub ('[%s]' % re.escape(string.punctuation), '', stemmer.stem(w.lower())) for w in nltk.word_tokenize(question)]
                                while words.count("") > 0:
                                        words.remove("")
                                self.words.extend(words)
                                self.questions.append(words) #normaal question
                                self.questions_tag.append(intent["tag"])
                        self.tags.append(intent["tag"])

                        responses = []
                        for respons in intent["responses"]:
                                responses.append(respons)
                        self.responses.append(responses)

                self.words = sorted(list(set(self.words)))

                for i, question in enumerate(self.questions):
                        # 1 for word in question, 0 if not
                        training_question = [0 for _ in range(len(self.words))]
                        # 1 for tag of question
                        output_label = [0 for _ in range(len(self.tags))]
                        for word in question:
                                training_question[self.words.index(word)] = 1
                        output_label[self.tags.index(self.questions_tag[i])] = 1
                        self.training.append(training_question)
                        self.output.append(output_label)
        
        def _loadfile(self):
                with open(self.filename) as file:
                        self.data = json.load(file) #the data
                self._initialize()
        
        def train(self, filename):
                self.filename = filename
                self.data = {} #all the data
                self.words = [] #all words
                self.tags = [] #all tags
                self.responses = [] #all responses for every tag
                self.questions = [] #all questions
                self.questions_tag = [] #all tags from questions
                self.training = [] #all questions in right format for training
                self.output = [] #all question tags in right format for training
                self.classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(30, 20), random_state=1)
                self._loadfile()
                self.classifier.fit(self.training, self.output)
                dump(self.classifier, "%s.joblib" %self.filename)
                self.model = load("%s.joblib" %self.filename)

        def _answer(self, inp):
                words = [re.sub ('[%s]' % re.escape(string.punctuation), '', stemmer.stem(w.lower())) for w in nltk.word_tokenize(inp)]
                input_array = [0 for _ in range(len(self.words))]
                for word in words:
                        if self.words.count(word) > 0:
                                input_array[self.words.index(word)] = 1
                output = self.model.predict_proba([input_array])
                #print(output)
                index = np.argmax(output[0])
                if output[0][index] > 0.8:
                        print("Bot: ", random.choice(self.responses[index]))
                        if self.tags[index] == "Quit":
                                return True
                        if self.tags[index] == "Time":
                                gettimenow()
                                return False
                        if self.tags[index] == "Weather":
                                getweathertoday()
                                return False
                        if self.tags[index] == "Highway Rider":
                                HighwayRider.main()
                                return False
                        if self.tags[index] == "Snake":
                                Snake.main()
                                return False
                        if self.tags[index] == "Space Invaders":
                                SpaceInvaders.main()
                                return False
                        if self.tags[index] == "Read Email":
                                username = input("Enter your username: ")
                                password = input("Enter your password: ")
                                mail_functions.show_inbox(username, password)
                                return False
                        if self.tags[index] == "Word":
                                os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\WinWord.exe')
                                return False
                        if self.tags[index] == "Excel":
                                os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\Excel.exe')
                                return False
                        if self.tags[index] == "Powerpoint":
                                os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.exe')
                                return False
                        if self.tags[index] == "Outlook":
                                os.startfile(r'C:\Program Files (x86)\Microsoft Office\root\Office16\Outlook.exe')
                                return False
                else:
                        print("Bot: I don't understand")
                return False
        
        def chat(self):
                print("Start talking with the bot")
                print("Type quit to stop")
                print("The main topics you can ask the bot about are: greetings, feelings, age, food, games, apps, email, time and weather")
                q = False
                while not q:
                        inp = input("You: ")
                        q = self._answer(inp)
                
if __name__ == '__main__':
        chatbot = Chatbot("TrainData.json")
        chatbot.train("TrainData.json")
        chatbot.chat()
