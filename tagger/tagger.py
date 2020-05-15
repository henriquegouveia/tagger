import nl_core_news_sm
from spacy.symbols import NOUN, VERB
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask import Response

app = Flask(__name__)
api = Api(app)

def extract_tag(text):
		nouns = []
		nlp = nl_core_news_sm.load()
		doc = nlp(text)
		for token in doc:
			if token.head.pos == NOUN:
				nouns.append("%s %s" % (token.text, token.head.text))

		return nouns

class Tagger(Resource):
	@api.representation('application/json')
	def post(self):
		text = request.json['text']
		nouns = extract_tag(text)
		response = jsonify(nouns)
		return response

api.add_resource(Tagger, '/tagger')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
