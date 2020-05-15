import nl_core_news_sm
import redis
from spacy.symbols import NOUN, VERB
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask import Response

app = Flask(__name__)
api = Api(app)

client = redis.Redis(db=0, host='redis', port='6379')

def count_tags_occurrences_by_product(tag, productId, language):
    key = "%s:%s:%s" % (language, productId, tag)
    client.incr(key)

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
		review = request.json['review']
		productId = request.json['productId']
		reviewId = request.json['reviewId']
		language = request.json['language']
        
		nouns = extract_tag(review)
		for noun in nouns:
			count_tags_occurrences_by_product(noun, productId, language)

		response = jsonify(nouns)
		return response

api.add_resource(Tagger, '/tagger')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
