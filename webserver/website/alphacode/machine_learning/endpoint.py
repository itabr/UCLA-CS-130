from flask import Flask, request, jsonify
from prediction_engine.predictor import TagPredictor
app = Flask(__name__)
predictor = TagPredictor("ridge/vsm", parameters_path = "prediction_engine/")

@app.route('/', methods=['POST'])
def responder():
	req_data = request.get_json()
	try:
		if req_data['test'] == 200 or int(req_data['test']) == 200:
			return jsonify({'test': 'all clear'})
	except:
		pass
	try:
		prob_st = req_data['data']
	except:
		return jsonify({'error': "incorrect input format: input key must be 'data', and input value must be a string"}), 400
	try:
		if type(prob_st) is str or type(prob_st) is unicode:
			return jsonify({"prediction": str(predictor.predict(prob_st))})
		else:
			return jsonify({'error': 'incorrect input format: input value must be a string'}), 400
	except Exception as e:
		return jsonify({'error': 'internal server error: ' + str(e)}), 500
