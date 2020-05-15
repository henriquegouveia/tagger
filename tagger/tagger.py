import nl_core_news_sm
import redis
import json
import pickle
from spacy.symbols import NOUN, VERB
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from flask import Response

app = Flask(__name__)
api = Api(app)

client = redis.StrictRedis('redis', 6379, charset="utf-8", decode_responses=True)

def key_builder(texts):
	key = ""
	for text in texts:
		key += "%s" % (text)

	return key

def count_tags_occurrences_by_product(tag, productId, language):
    indice_key = key_builder([language, productId])
    client.sadd(indice_key, tag)
    tag_key = key_builder([language, productId, tag])
    client.hincrby(tag_key, "count", 1)

def get_tags_by_occurrence(language, productId):
	name = key_builder([language, productId])
	byFilter = "%s*->count" % (name)

	return client.sort(name, by=byFilter, desc=True)

def save_reviewsId_by_tag(tag, productId, language, reviewId):
	key = key_builder([language, productId, tag, "reviews"])
	client.rpush(key, reviewId)

def extract_tag(text):
		nouns = []
		nlp = nl_core_news_sm.load()
		doc = nlp(text)
		for token in doc:
			if validateTag(token) == True:
				nouns.append(("%s %s" % (token.text, token.head.text)).lower())

		return nouns

def validateTag(token):
    return ((token.pos_ == 'PROPN' and token.head.pos_ == 'PROPN') or
            (token.pos_ == 'ADJ' and token.head.pos_ == 'NOUN') or
            (token.pos_ == 'NUM' and token.head.pos_ == 'PROPN') or
            (token.pos_ == 'NOUN' and token.head.pos_ == 'NOUN') and
            (token.text != token.head.text))

@api.resource('/tagger')
class Tagger(Resource):
	def get(self):
		productId = request.args.get('productId')
		language = request.args.get('language')

		return get_tags_by_occurrence(language, productId)

	def post(self):
		review = request.json['review']
		productId = request.json['productId']
		reviewId = request.json['reviewId']
		language = request.json['language']
        
		nouns = extract_tag(review)
		for noun in nouns:
			count_tags_occurrences_by_product(noun, productId, language)
			save_reviewsId_by_tag(noun, productId, language, reviewId)

		response = jsonify(nouns)
		return response

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
