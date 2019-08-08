from .exceptions import *
import random

class GuessAttempt(object): 
    def __init__(self, character, hit=None, miss=None):
        self.character = character
        if hit and miss:
                raise InvalidGuessAttempt()
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit:
            return True
        return False
    def is_miss(self):
        if self.miss:
            return True
        return False


class GuessWord(object):
    def __init__(self,answer):
        self.answer = answer
        self.masked = '*' * len(answer)
        if len(answer) <= 0:
            raise InvalidWordException()
        
#     def unmask(self, character):
#         answer_string = ''
#         for c,l in zip(self.answer.lower(),self.masked):
#             if c == character.lower():
#                 answer_string += c
#             else:
#                 answer_string += l
#         return answer_string
    
    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        if character.lower() in self.answer.lower():
            attempt = GuessAttempt(character, hit=True)
            #self.masked = self.unmask(character)
            new_mask = ''
            for c,l in zip(self.answer.lower(),self.masked):
                if c == character.lower():
                    new_mask += c
                else:
                    new_mask += l
            self.masked = new_mask
        else:
            attempt = GuessAttempt(character, miss=True)
        return attempt


class HangmanGame(object):
    WORD_LIST = ['rmotr','python','awesome']
    
    def __init__(self, list_of_words = None, number_of_guesses = 5):
        if not list_of_words:
            list_of_words = self.WORD_LIST
            
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        answer = self.select_random_word(list_of_words)
        self.word = GuessWord(answer)
        
    
    def guess(self,character):
        if self.is_won() or self.is_lost():
            raise GameFinishedException()
        self.previous_guesses.append(character.lower())
        attempt = self.word.perform_attempt(character)
        if attempt.is_miss() == True:
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        if self.is_won():
            raise GameWonException()
        return attempt 
            
    
    def is_won(self):
        return self.word.answer.lower() == self.word.masked.lower()
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    def is_lost(self):
        return self.remaining_misses < 1
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()

        return random.choice(list_of_words)
            
        
    
