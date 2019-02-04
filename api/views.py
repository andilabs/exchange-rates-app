from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CurrencyRateConverterSerializer


class CurrencyRateConverterApiView(APIView):

    def get(self, request, base_currency_code, target_currency_code, amount):
        serializer = CurrencyRateConverterSerializer(data={
            'input_base_currency': base_currency_code,
            'input_target_currency': target_currency_code,
            'base_amount': amount
        })
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
