import json
import pickle
import re
import pandas
import keras
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import hashing_trick
from keras.models import load_model
from sklearn.externals import joblib
from keras.preprocessing import sequence


tfidf_labels = ["math", "dp", "datastructure", "greedy", "graphs", "probabilities", "sortings", "strings", "numbertheory"]
nn_labels = ["combinatorics", "games", "geometry", "search"]
hashing_trick_max_features = 5000
nn_features_max_size = 5000
confidence_threshold = .5


class TFIDFMapper(object):
	def __init__(self, prefix):
		data = pandas.read_csv(prefix + 'data.csv')
		data = data.dropna()

		self.vectorizer = TfidfVectorizer(stop_words="english", analyzer = 'word')
		l = data['ps'] = (data['problem-statement'].astype(str) + data['output-spec']) .tolist()
		res = []
		self.regex = re.compile("^a-zA-Z0-9\ '" )
		for i in range(len(l)):
		    try:
		        res.append(self.regex.sub(' ', l[i]))
		    except:
		        res.append("")
		self.vectorizer.fit(res)

	def clean_string(self, input_str):
		return self.regex.sub(' ', input_str)

	def map_sample(self, sample):
		return self.vectorizer.transform([self.clean_string(sample)])


class NNMapper(object):
	def map_sample(self, sample):
		features = hashing_trick(sample, hashing_trick_max_features)
		return sequence.pad_sequences([features], nn_features_max_size)


class SKLClassifier(object):
	def __init__(self, name, mapper_fn, prefix=""):
		self.clf = joblib.load(prefix + name + ".dump")
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))[0]


class KerasClassifier(object):
	def __init__(self, name, mapper_fn, prefix=""):
		self.clf = load_model(prefix + name + ".h5")
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))[0][0]


class TagPredictor(object):
	def __init__(self, parameters_path = ""):
		self.tfidf_mapper = TFIDFMapper(prefix = parameters_path)
		self.nn_mapper = NNMapper()

		self.label_classifiers = {}
		failure = False
		for label in tfidf_labels:
			self.label_classifiers[label] = SKLClassifier(label, self.tfidf_mapper.map_sample, parameters_path)
		for label in nn_labels:
			self.label_classifiers[label] = KerasClassifier(label, self.nn_mapper.map_sample, parameters_path)

	def predict(self, sample):
		predictions = []

		for label in self.label_classifiers:
			if self.label_classifiers[label].predict(sample) >= confidence_threshold:
				predictions.append(label)

		return predictions
