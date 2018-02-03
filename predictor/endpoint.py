from flask import Flask
app = Flask(__name__)

def predict():
	return "Nothing, because prediction is not implemented!"

@app.route('/', methods=['POST'])
def responder():
	response_str = '<h1>Your reponse is below:</h1><br>'
	response_str += ("<p>" + predict() + "<p>")
	return response_str
