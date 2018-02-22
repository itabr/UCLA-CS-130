import sys
import os
import pickle
sys.path.append("../") #this allows imports from neighboring directories

#test VSMSampleMapper
try:
	from prediction_engine.predictor import VSMSampleMapper

	stub_idf = {"This": 1.,"is": 1.,"a": 1.,"test": 1.,"problem": 1.,"statement": 1., "not": 1.,"representative": 1.,"of": 1.,"true": 1.}
	os.makedirs("tmp")
	f = open("tmp/idf.txt", 'w')
	f.write(pickle.dumps(stub_idf))
	f.close()
	mapper = VSMSampleMapper(prefix="tmp/")
	os.remove("tmp/idf.txt")
	os.rmdir("tmp")

	sample_str = "This is a test problem statement.  This is not representative of a true problem statement!"
	sample_mapped_str = mapper.map_sample(sample_str)
	correct_mapped_str = [0.4, 0.4, 0.2, 0.4, 0.2, 0.2, 0.4, 0.2, 0.4, 0.2]
	if sample_mapped_str == correct_mapped_str:
		print("Success: VSMSampleMapper")
	else:
		print("Failure: VSMSampleMapper - mapped string is not correct!")
except Exception, e:
	print("Failure: VSMSampleMapper - " + str(e))

#test RidgeCLF
try:
	from prediction_engine.predictor import RidgeCLF
	from prediction_engine.predictor import VSMSampleMapper
	sample_text = "This is a test problem statement.  This is not representative of a true problem statement!"
	mapper = VSMSampleMapper(prefix="prediction_engine/")
	clf = RidgeCLF(prefix="prediction_engine/")
	prediction = clf.predict(mapper.map_sample(sample_text))

	if prediction == "implementation":
		print("Success: RidgeCLF")
	else:
		print("Failure: RidgeCLF - prediction is not correct!")
except Exception, e:
	print("Failure: RidgeCLF - " + str(e))

#test TagPredictor
try:
	from prediction_engine.predictor import TagPredictor
	pred = TagPredictor("ridge/vsm", "prediction_engine/")
	sample_problem_statement = "This is a test problem statement.  This is not representative of a true problem statement!"
	sample_prediction = pred.predict(sample_problem_statement)
	if sample_prediction == "implementation":
		print("Success: TagPredictor")
	else:
		print("Failure: TagPredictor - prediction is not correct!")
except Exception, e:
	print("Failure: TagPredictor - " + str(e))

#test endpoint.py (assumed to be running)
try:
	#run tests
	pass
except Exception, e:
	print("Failure: " + str(e))

