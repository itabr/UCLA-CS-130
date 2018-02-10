import pandas
import math
import re
import numpy
import sys
import multiprocessing
import pickle

if len(sys.argv) < 2:
	exit("ERROR: Pass one argument to this program, the path of the data file.")

def string_to_words(input_str):
	cleaned_str = re.sub("[^abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\ ]", ' ', input_str)
	return filter(lambda w: len(w) > 0, cleaned_str.split(" "))

def get_word_counts(words_arr):
	ret = {}
	for word in words_arr:
		try:
			ret[word] += 1
		except:
			ret[word] = 1
	return ret

def norm_magnitude_vector(input_vec):
	sum_squares = sum(map(lambda x: x**2, input_vec))
	magnitude = sum_squares**.5
	if magnitude == 0:
		return [0 for i in input_vec]
	return list(map(lambda x: x / magnitude, input_vec))

df = pandas.read_csv(sys.argv[1])
labels = df['labels']
prob_statements = df['problem-statement']

document_frequency = {}
for statement in prob_statements:
	try:
		words = string_to_words(statement)
	except:
		continue
	uniques = set(words)
	for word in uniques:
		try:
			document_frequency[word] += 1
		except:
			document_frequency[word] = 1
idf = {}
num_docs = len(prob_statements)
for key in document_frequency:
	idf[key] = math.log10(num_docs / document_frequency[key])

def get_document_vector(input_str):
	try:
		words = string_to_words(input_str)
		if len(words) == 0:
			return [0 for word in idf]
	except:
		return [0 for word in idf]

	counts = get_word_counts(words)
	un_normed_vec = [counts[word] * idf[word] if word in counts else 0 for word in idf]
	return norm_magnitude_vector(un_normed_vec)

pool = multiprocessing.Pool()
vsm_features = list(pool.map(get_document_vector, prob_statements))
df_columns = [word for word in idf]
output_df = pandas.DataFrame(data=vsm_features, columns=df_columns)
output_df['FEATURE_LABELS'] = labels

filename = sys.argv[1].split("/")
filename = "".join(filename[len(filename)-1].split(".")[:1])
output_df.to_csv(filename + "_features.csv", index=False)

f = open('idf_dump.txt', 'w')
f.write(pickle.dumps(idf))
f.close()