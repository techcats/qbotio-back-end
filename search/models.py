from mongoengine import Document, fields

class Answer(Document):
    """
    Model for a Question Answer
    """
    value = fields.StringField(required=True)
    origin = fields.StringField()
    source = fields.StringField(required=True)
