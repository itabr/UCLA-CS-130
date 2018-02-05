import pandas
import math
import re
import numpy
import sys

if len(sys.argv) < 2:
	exit("ERROR: Pass one argument to this program, the path of the file to analyze.")

df = pandas.read_csv(sys.argv[1])
labels = df['labels']
prob_statements = df['problem-statement']

def string_to_words(input_str):
	cleaned_str = re.sub("[^abcdefghijklmnopqrstuvwxyz'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\ ]", ' ', input_str)
	return filter(lambda w: len(w) > 0, cleaned_str.split(" "))

word_counts = {}
for statement in prob_statements:
	try:
		words = string_to_words(statement)
	except:
		continue
	uniques = set(words)
	for word in uniques:
		try:
			word_counts[word] += 1
		except:
			word_counts[word] = 1
idf = {}
num_probs = len(prob_statements)
for key in word_counts:
	idf[key] = math.log10(num_probs / word_counts[key])

def get_counts(words_arr):
	ret = {}
	for word in words_arr:
		try:
			ret[word] += 1
		except:
			ret[word] = 1
	return ret

def get_vsm(input_str):
	try:
		words = string_to_words(input_str)
		if len(words) == 0:
			return [0 for word in word_counts]
	except:
		return [0 for word in word_counts]

	counts = get_counts(words)
	un_normed_vsm = [counts[word] * idf[word] if word in counts else 0 for word in idf]
	tot = un_normed_vsm[0]**2 - un_normed_vsm[0] + reduce((lambda x, y: x + y**2), un_normed_vsm)
	factor = tot**.5
	return list(map(lambda x: x / factor, un_normed_vsm))

features = list(map(get_vsm, prob_statements))
df_columns = [word for word in idf]
output_df = pandas.DataFrame(data=features, columns=df_columns)
output_df['labels'] = labels

filename = "".join(sys.argv[1].split(".")[:1])
output_df.to_csv(filename + "_features.csv", index=False)
