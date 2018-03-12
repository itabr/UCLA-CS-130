import json
import pickle
import re
import pandas
import keras
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing.text import hashing_trick
from keras.models import load_model

from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import svm

from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.naive_bayes import GaussianNB

import nltk
from nltk import word_tokenize          
from nltk.stem.porter import PorterStemmer

from sklearn.model_selection import GridSearchCV

tfidf_labels = ["math", "dp", "datastructure", "greedy", "graphs", "probabilities", "sortings", "strings", "numbertheory"]
nn_labels = ["combinatorics", "games", "geometry", "search"]
hashing_trick_max_features = 20000
nn_features_max_size = 5000
confidence_threshold = .5


class TFIDFMapper(object):
	def __init__(self, prefix):
		data = pandas.read_csv(prefix + 'data.csv')
		data = data.dropna()

		self.vectorizer = TfidfVectorizer(stop_words="english", analyzer = 'word')
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
	def __init__(self, name, mapper_fn, prefix=""):
		f = open(prefix + name + ".dump")
		self.clf = pickle.loads(f.read())
		f.close()
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))


class KerasClassifier(object):
	def __init__(self, name, mapper_fn, prefix=""):
		self.clf = load_model(prefix + name + ".h5")
		self.mapper_fn = mapper_fn

	def predict(self, sample):
		return self.clf.predict(self.mapper_fn(sample))


class TagPredictor(object):
	def __init__(self, parameters_path = ""):
		self.tfidf_mapper = TFIDFMapper(prefix = parameters_path)
		self.nn_mapper = NNMapper()

		self.label_classifiers = {}
		failure = False
		for label in tfidf_labels:
			try:
				self.label_classifiers[label] = SKLClassifier(label, self.tfidf_mapper.map_sample, parameters_path)
				print "SKL Classifier Loaded: " + label
			except Exception, e:
				failure = True
				print "SKL Classifier Load Failed: " + label + ";     " + str(e)
		for label in nn_labels:
			self.label_classifiers[label] = KerasClassifier(label, self.nn_mapper.map_sample, parameters_path)
		exit("done")

	def predict(self, sample):
		predictions = []

		for label in self.label_classifiers:
			if self.label_classifiers[label].predict(sample) >= confidence_threshold:
				predictions.append(label)

		return predictions
