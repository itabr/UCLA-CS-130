from flask import Flask, request, jsonify
from prediction_engine.predictor import TagPredictor
app = Flask(__name__)
predictor = TagPredictor("ridge/vsm", parameters_path = "prediction_engine/")

@app.route('/', methods=['POST'])
def responder():
	req_data = request.get_json()
	#print "Request JSON:"
	#print req_data
	return jsonify({"prediction": str(predictor.predict(req_data['data']))})
