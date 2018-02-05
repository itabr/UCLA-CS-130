from flask import Flask, request, jsonify
#from .predict import DummyResponse
app = Flask(__name__)

class DummyResponse(object):
	def respond(self):
		return "Tag1 Tag2 Tag3"

def predict():
	resp = DummyResponse()
	return resp.respond()

@app.route('/', methods=['POST'])
def responder():
	req_data = request.get_json()
	#print "Request JSON:"
	#print req_data
	response_str = '<h1>Your reponse is below:</h1><br>'
	response_str += ("<p>" + predict() + "<p>")
	return jsonify({"prediction": str(predict())})
