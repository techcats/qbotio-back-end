from rest_framework.views import APIView
from rest_framework.response import Response
from search.models import Result
from search.serializers import ResultSerializer


class ResultList(APIView):

    def get(self):
        """
        List all results.
        """
        results = [
            Result(answer="Answer 1"),
            Result(answer="Answer 2"),
            Result(answer="Answer 3"),
        ]
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
