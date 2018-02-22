import json
import pickle
import re
from sklearn.linear_model import RidgeClassifierCV
from sklearn.preprocessing import MultiLabelBinarizer

class VSMSampleMapper(object):
	def __init__(self, prefix = "", idf_file_type = 'pickle'):
		if idf_file_type == "pickle":
			f = open(prefix + "idf.txt")
			self.idf = pickle.loads(f.read())
			f.close()
		else:
			f = open(prefix + "idf.txt")
			self.idf = json.loads(f.read())
			f.close()

	def _string_to_words(self, input_str):
		cleaned_str = re.sub("[^abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\ ]", ' ', input_str)
		return filter(lambda w: len(w) > 0, cleaned_str.split(" "))

	def _get_word_counts(self, words_arr):
		ret = {}
		for word in words_arr:
			try:
				ret[word] += 1
			except:
				ret[word] = 1
		return ret

	def _norm_magnitude_vector(self, input_vec):
		sum_squares = sum(map(lambda x: x**2, input_vec))
		magnitude = sum_squares**.5
		if magnitude == 0:
			return [0 for i in input_vec]
		return list(map(lambda x: x / magnitude, input_vec))

	def map_sample(self, sample):
		word_counts = self._get_word_counts(self._string_to_words(sample))
		conversion = [word_counts[word] * self.idf[word] if word in word_counts else 0 for word in self.idf]
		return self._norm_magnitude_vector(conversion)

class RidgeCLF(object):
	def __init__(self, prefix = ""):
		f = open(prefix + "ridge_clf.txt")
		self.clf = pickle.loads(f.read())
		f.close()
		f = open(prefix + "binarizer.txt")
		self.binarizer = pickle.loads(f.read())
		f.close()

	def predict(self, sample_vec):
		pred = self.clf.predict([sample_vec])[0]
		return self.binarizer.classes_[int(pred)]

class TagPredictor(object):
	def __init__(self, algorithm = "ridge/vsm", parameters_path = False):
		if parameters_path:
			self.mapper = VSMSampleMapper(prefix = parameters_path)
			self.predictor = RidgeCLF(prefix = parameters_path)
		else:
			self.mapper = VSMSampleMapper()
			self.predictor = RidgeCLF()

	def predict(self, sample):
		sample_features = self.mapper.map_sample(sample)
		return self.predictor.predict(sample_features)
