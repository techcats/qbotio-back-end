from datetime import datetime
from haystack import indexes
from search.models import Result

class ResultIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index for Result model
    """
    answer = indexes.CharField(document=True)

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return obj.answer[:15]

    def get_model(self):
        return Result

    def index_queryset(self, using=None):
        """
        Get new non future items that should be indexed
        """
        return self.get_model(self).objects.filters(pub_date__lte=datetime.now())
