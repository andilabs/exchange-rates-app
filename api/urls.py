from django.urls import path

from api.views import (
    CurrencyRateConverterApiView
)

app_name = 'api'

urlpatterns = [
    path('convert/<base_currency_code>/<target_currency_code>/<amount>/',
         CurrencyRateConverterApiView.as_view(), name='currency-converter')
]