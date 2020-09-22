from edit_distance import EditDistance
from telex import Telex
from teencode import Teencode

class Candidate():
    def __init__(self, dictionary):
        self.edit_distance = EditDistance(dictionary)
        self.telex = Telex()
        self.teencode = Teencode(dictionary)
    def generate_candidate(self, word):
        word_candidates =  list(self.edit_distance.candidates_e1(word))
        fix_telex = self.telex.uni2telex(word)
        if fix_telex != word:
            word_candidates.insert(0,fix_telex)
        candidates_acr = self.teencode.candidate_acronym(word)
        candidates_teen = self.teencode.candidate_teen(word)
        word_candidates += candidates_acr
        word_candidates += candidates_teen
        return word_candidates