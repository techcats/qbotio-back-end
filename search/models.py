from mongoengine import Document, fields

class Result(Document):
    answer = fields.StringField(required=True)
