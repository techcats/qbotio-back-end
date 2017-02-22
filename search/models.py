from mongoengine import Document, fields

class Result(Document):
    answer = fields.StringField(required=True)
    pub_date = fields.DateTimeField('date published')
