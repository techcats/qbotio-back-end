from mongoengine import Document, fields

class Answer(Document):
    """
    Model for a Question Answer
    """
    value = fields.StringField(required=True)
    origin = fields.StringField()
    source = fields.StringField(required=True)
    tags = fields.ListField()

class Result:

    def __init__(self, value, source, origin, score):
        self.value = value
        self.source = source
        self.origin = origin
        self.score = score    