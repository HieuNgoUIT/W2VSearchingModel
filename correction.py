import numpy as np
import fasttext
from candidate import Candidate

class Correction():
    def __init__(self, path_model, path_dictionary):
        self.model = fasttext.load_model(path_model) #TODO
        self.dictionary = self.load_dictionary(path_dictionary)
        self.candidate = Candidate(self.dictionary)
    
    def load_dictionary(self, path):
        with open(path, 'r') as f:
            data = f.read()

        rows = data.split("\n")
        my_dict = {}
        for i in rows:
            if i not in my_dict:
                my_dict[i] = 1
        return my_dict

    def comp_sum(self,vectors):
        """
        Composes a single vector representation out of several vectors using summing with reciprocal weighting.
        :param vectors: vectors to be composed
        :return: composed vector representation
        """
        weight_vector = np.reciprocal(np.arange(1., len(vectors) + 1))
        weighted_vectors = []
        for i, weight in enumerate(weight_vector):
            weighted_vectors.append(vectors[i] * weight)
        composed_vector = np.sum(weighted_vectors, axis=0)

        return composed_vector

    def normalize(self,vector):
        """
        Normalizes a vector.
        :param vector: a numpy array or list to normalize.
        :return: a normalized vector.
        """
        if not vector.any():
            return vector

        return vector / np.linalg.norm(vector)

    def vectorize(self, sequence, remove_oov=True):
        """
        :param sequence: sequence to be vectorized
        :param remove_oov: whether to vectorize oov tokens
        :return: vectorized sequence
        """
        if remove_oov:
            sequence = [x for x in sequence if x in self.model.words]

        return [np.array(self.model[x]) for x in sequence] #TODO
    
    def context_ranking(self, candidates, misspelling, left_context, right_context, window_size):
        """
        Context-sensitive ranking model
        :param candidates_list: list of candidate list per misspelling
        :return: list with corrections or k-best corrections
        """
        left_context, right_context = left_context[::-1][:window_size], right_context[:window_size]
        left_window = self.vectorize(left_context, remove_oov=True)  # take only in-voc tokens for context
        right_window = self.vectorize(right_context, remove_oov=True)  # take only in-voc tokens for context

        if left_window:
            vectorized_left_window = self.comp_sum(left_window)
        else:
            vectorized_left_window = np.zeros(300)

        if right_window:
            vectorized_right_window = self.comp_sum(right_window)
        else:
            vectorized_right_window = np.zeros(300)

        if not vectorized_left_window.any() and not vectorized_right_window.any():
            return misspelling  # no context to correct the misspelling

        vectorized_context = self.normalize(np.sum((vectorized_left_window, vectorized_right_window), axis=0))

        current_target_vector = self.normalize(np.array(self.model[misspelling])) #TODO
        current_target_score = np.dot(vectorized_context, current_target_vector) ##  NOT COSINE ??

        candidate_vectors = []
        # make vector representations of candidates
        for candidate in candidates:
            candidate_vectors.append(self.normalize(np.array(self.model[candidate]))) #TODO
        # calculate cosine similarities
        distances = [np.dot(vectorized_context, candidate) for candidate in candidate_vectors]

        # output
        try:
            best_score = distances[np.argmax(distances)]
        except:
            best_score = 0

        if best_score > current_target_score:
            return candidates[np.argmax(distances)]
        else:
            return misspelling

    def test_realword(self, model):
        total = 0
        with open("realword_error.txt", 'r') as f:
            count = 0
            for line in f:
                total += 1
                print(total)
                data = line.split("_") 
                realword = data[0]
                left = data[1].split()
                right = data[2].split()
                label = data[3].replace("\n","")
                word_candidates = model.candidate.generate_candidate(realword)
                result = self.context_ranking(candidates = word_candidates ##TODO
                                , misspelling = realword
                                , left_context= left
                                , right_context= right
                                , window_size = 10)
                if result == label:
                    count += 1
        print(count/total*100)

        ### two things :
        ### accuracy
        ### is there wanted canidadate