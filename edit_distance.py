from collections import defaultdict

class EditDistance():
    def __init__(self, dictionary):
        self.word = dictionary

    def candidates(self, word): 
        "Generate possible spelling corrections for word."
        return self.known([word]).union(self.known(self.edits1(word)), self.known(self.edits2(word)), [word])

    def candidates_e1(self, word): 
        "Generate possible spelling corrections for word."
        return self.known([word]).union(self.known(self.edits1(word)))

    def known(self, words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.word)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters    = 'aáàạãảăắằẵẳặâấầẩậẫbcdđeéèẻẽẹêếềểệễghiíìịĩỉjklmnoóòọõỏôốồổộỗơớờợỡởpqrstuúùủụũưứừửữựvxy'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
