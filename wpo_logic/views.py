import sys

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from wpo_logic.serializers import CodigosPostalesSerializer
from wpo_logic.controllers import get_all_codigos_postales


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
