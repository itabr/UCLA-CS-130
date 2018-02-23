from sklearn.linear_model import RidgeClassifierCV
from sklearn.preprocessing import MultiLabelBinarizer
import pandas
import pickle
import sys
import re

if len(sys.argv) < 2:
	exit("ERROR: Pass one argument to this program, the path of the data file.")

input_df = pandas.read_csv(sys.argv[1])
labels = input_df['FEATURE_LABELS'].get_values()
features = input_df.drop(columns=["FEATURE_LABELS"]).get_values()

def string_to_vector(s):
	try:
		cleaned_s = re.sub("[\ ]", '', s)
	except:
		return []
	return cleaned_s.split(",")

labels = list(map(string_to_vector, labels))

y = MultiLabelBinarizer()
clf = RidgeClassifierCV()
clf.fit(features, y.fit_transform(labels))

f = open("ridge_clf.txt", 'w')
f.write(pickle.dumps(clf))
f.close()

f = open("binarizer.txt", 'w')
f.write(pickle.dumps(y))
f.close()
