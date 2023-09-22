import requests
from random import randint, choice
import time

class Speed_Test():
    def __init__(self):
        self.sentence = self.sentence_creator()

    #grabs word_count words from api
    def sentence_grabber(self, word_count):
        random_word_api = f'https://random-word-api.herokuapp.com/word?number={word_count}'
        random_sentence_response = requests.get(random_word_api)
        random_sentence_response.raise_for_status()
        return random_sentence_response.json()
    
    #scores wpm
    def words_per_minute(self, minutes):
        wpm = round( self.short_list / minutes)
        cpm = round( self.shorter_string / minutes, 2)
        adjusted_wpm = round(cpm / 5, 2)
        print(f'Congrats! You typed {adjusted_wpm} words per minute with {self.word_accuracy}% accuracy, {self.char_accuracy}% character accuracy  ({cpm} characters, {wpm} actual words)')
    
    #scores the test
    def score_test(self, typed_string, elapsed_time):
        self.accuracy_scores(typed_string)
        minutes = elapsed_time / 60
        self.words_per_minute(minutes)

    def word_accuracy(self, typed_string):
        typed_list = typed_string.split()
        sentence_list = self.sentence.split()
        self.short_list = min(len(typed_list), len(sentence_list))
        correct = 0
        for word in typed_list:
            if word in sentence_list:
                correct += 1
        self.word_accuracy = round(correct / len(sentence_list) * 100, 2)

    def character_accuracy(self, typed_string):
        correct = 0
        for sentence_char, typed_char in zip(self.sentence, typed_string):
            if sentence_char == typed_char:
                correct += 1
        self.shorter_string = min(len(typed_string), len(self.sentence))
        self.char_accuracy = round((correct/ self.shorter_string) * 100, 2)
        

    def accuracy_scores(self, typed_string):
        self.character_accuracy(typed_string)
        self.word_accuracy(typed_string)

    #starts the timers and test
    def start_test(self):
        start = time.time()
        self.print_sentence()
        typed = input('Retype sentence: ')
        stop = time.time()
        elapsed_time = stop - start
        self.score_test(typed, elapsed_time)

    #adds words from json into a string
    def json_to_string(self, json):
        sentence = ''
        for word in json:
            sentence += f'{word} '
        sentence = sentence.strip()
        sentence += choice(['.', '!', '?'])
        return sentence

    #creates sentence of random words for speed test
    def sentence_creator(self):
        self.random_word_count = randint(40,60)
        random_sentence_json = self.sentence_grabber(self.random_word_count)
        sentence = self.json_to_string(random_sentence_json)
        return sentence
    
    def print_sentence(self):
        print(self.sentence)