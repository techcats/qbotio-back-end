from mongoengine import Document, fields

class Question(Document):
    """
    Model for a Question
    """
    value = fields.StringField(required=True)

class Answer(Document):
    """
    Model for a Question Answer
    """
    value = fields.StringField(required=True)
    origin = fields.StringField()
    source = fields.StringField(required=True)
    tags = fields.ListField()

class QuestionResult:
    """
    Transient model for ES Question result
    """
    def __init__(self, value, score):
        self.value = value
        self.score = score


class AnswerResult:
    """
    Transient model for ES Answer results
    """
    def __init__(self, value, source, origin, score):
        self.value = value
        self.source = source
        self.origin = origin
        self.score = score
