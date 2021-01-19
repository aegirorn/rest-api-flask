from db import db


class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    content = db.Column(db.Text)

    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    language = db.relationship('LanguageModel')

    def __init__(self, title, content, language_id):
        self.title = title
        self.content = content
        self.language_id = language_id

    def json(self):
        return {'name': self.title, 'content': self.content}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()