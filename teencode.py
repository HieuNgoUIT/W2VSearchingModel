class Teencode():
    def __init__(self, dictionary):
        self.dictionary = dictionary
    def candidate_acronym(self, word):
        acronym = {
            "ko" : "không",
            "a" : "anh",
            "e" : "em",
            "bít": "biết",
            "h" : "giờ",
            "j" : "gì",
            "mún" : "muốn",
            "hok" : "học",
            "iu" : "yêu",
            "ck" : "chồng",
            "vk" : "vợ",
            "ô" : "ông",
            "đc" : "được",
            "t" : "tôi"
        }
        candidates = []
        for i in acronym:
            if i in word:
                temp_text = word.replace(i, acronym[i])
                if temp_text in self.dictionary:
                    candidates.append(temp_text)
        return candidates

    def candidate_teen(self, word):
        teen = {
            "ck":"ch",
            "f":"ph",
            "tk":"th",
            "nk":"nh"
        }
        candidates = []
        for t in teen:
            if t in word:
                temp_text = word.replace(t, teen[t])
                if temp_text in self.dictionary:
                    candidates.append(temp_text)
        return candidates


