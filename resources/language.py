from flask_restful import Resource
from models.language import LanguageModel

#Add voice

class Language(Resource):
    def get(self, name):
        store = LanguageModel.find_by_title(name)
        if store:
            return store.json()
        return {'message': 'Language not found'}, 404

    def post(self, name, voice):
        if LanguageModel.find_by_name(name):
            return {'message': "A language with name '{}' already exists.".format(name)}, 400

        language = LanguageModel(name, voice)
        try:
            language.save_to_db()
        except:
            return {"message": "An error occurred creating the language."}, 500

        return language.json(), 201

    def delete(self, name):
        language = LanguageModel.find_by_name(name)
        if language:
            language.delete_from_db()

        return {'message': 'Language deleted'}


class LanguageList(Resource):
    def get(self):
        return {'languages': list(map(lambda x: x.json(), LanguageModel.query.all()))}