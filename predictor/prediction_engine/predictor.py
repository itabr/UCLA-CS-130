import json
import pickle
import re
import pandas
import keras
from sklearn.linear_model import RidgeClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import hashing_trick
from keras.models import load_model

tfidf_labels = ["math", "dp", "geometry", "combinatorics", "datastructures",
	"games", "graphs", "probabilities", "sortings", "strings", "twopointers"]
nn_labels = ["implementation", "search", "greedy"] # games? numbertheory? strings?
hashing_trick_max_features = 20000
nn_features_max_size = 5000
confidence_threshold = .5


class TFIDFMapper(object):
	def __init__(self, prefix):
		data = pandas.read_csv(prefix + 'data.csv')
		data = data.dropna()

		vectorizer = TfidfVectorizer(stop_words="english", analyzer = 'word')
		l = (data['input-spec'].astype(str) + (data['problem-statement'].astype(str) + data['output-spec'])) .tolist()
		res = []
		self.regex = re.compile("^a-zA-Z0-9\ '" )
		for i in range(len(l)):
		    try:
		        res.append(self.regex.sub(' ', l[i]))
		    except:
		        res.append("")
		self.vectorizer.fit(res)

	def map_sample(self, sample):
		return self.vectorizer.transform([sample])


class NNMapper(object):
	def map_sample(self, sample):
		features = hashing_trick(sample, hashing_trick_max_features)
		return features + [0] * (nn_features_max_size - len(features))


class SKLClassifier(object):
	def __init__(self, name, prefix="", mapper_fn):
		f = open(prefix + name + ".dump")
		self.clf = pickle.loads(f.read())
		f.close()
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))


class KerasClassifier(object):
	def __init__(self, name, prefix="", mapper_fn):
		self.clf = load_model(prefix + name + ".dump")
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))


class TagPredictor(object):
	def __init__(self, parameters_path = ""):
		self.tfidf_mapper = TFIDFMapper(prefix = parameters_path)
		self.nn_mapper = NNMapper(prefix=parameters_path)

		self.label_classifiers = {}
		for label in tfidf_labels:
			self.label_classifiers[label] = SKLClassifier(label, parameters_path, self.tfidf_mapper.map_sample)
		for label in nn_labels:
			self.label_classifiers[label] = KerasClassifier(label, parameters_path, self.nn_mapper.map_sample)

	def predict(self, sample):
		predictions = []

		for label in self.label_classifiers:
			if self.label_classifiers[label].predict(sample) >= confidence_threshold:
				predictions.append(label)

		return predictions
