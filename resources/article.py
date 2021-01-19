from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.article import ArticleModel


class Article(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('language_id',
                        type=int,
                        required=True,
                        help="Every article needs a language_id."
                        )

    @jwt_required()
    def get(self, title):
        article = ArticleModel.find_by_title(title)
        if article:
            return article.json()
        return {'message': 'Article not found'}, 404

    def post(self, title):
        if ArticleModel.find_by_title(title):
            return {'message': "An article with title '{}' already exists.".format(title)}, 400

        data = Article.parser.parse_args()

        article = ArticleModel(title, **data)

        try:
            article.save_to_db()
        except:
            return {"message": "An error occurred inserting the article."}, 500

        return article.json(), 201

    def delete(self, title):
        article = ArticleModel.find_by_title(title)
        if article:
            article.delete_from_db()
            return {'message': 'Article deleted.'}
        return {'message': 'Article not found.'}, 404

    def put(self, title):
        data = Article.parser.parse_args()

        article = ArticleModel.find_by_title(title)

        if article:
            article.price = data['price']
        else:
            article = ArticleModel(title, **data)

        article.save_to_db()

        return article.json()


class ArticleList(Resource):
    def get(self):
        return {'articles': list(map(lambda x: x.json(), ArticleModel.query.all()))}