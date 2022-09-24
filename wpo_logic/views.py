# Python
import sys

# Django Rest Framework
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# wpo_logic
from wpo_logic.serializers import CodigosPostalesSerializer, SportsLocationSerializer
from wpo_logic.controllers import get_all_codigos_postales


class SportsLocationAPIView(APIView):
    """Create a Sports Location."""

    def post(self, request, *args, **kwargs):
        try:
            serializer = SportsLocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    {"message": f"Room {request.data['room']} not available"},
                    status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            exc_tb = sys.exc_info()[2]
            return Response({"message": "something bad occurred!",
                             "error": f"{str(e)} line: {exc_tb.tb_lineno}"
                             },
                            status=status.HTTP_400_BAD_REQUEST)


class CodigosPostalesAPIView(APIView):
    """Get Codigos postales from Mexico"""

    def get(self, request, *args, **kwargs):
        key_word = request.query_params["string"]
        try:
            codigos_postales_result = get_all_codigos_postales(key_word)
            data = CodigosPostalesSerializer(codigos_postales_result, many=True)
            return Response(data.data, status=status.HTTP_200_OK)

        except Exception as e:
            exc_tb = sys.exc_info()[2]
            return Response({"message": "something bad occurred!",
                             "error": f"{str(e)} line: {exc_tb.tb_lineno}"
                             },
                            status=status.HTTP_400_BAD_REQUEST)
