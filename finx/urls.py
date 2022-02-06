from django.urls import path
from . views import MyView, parallel_calls_to_databases


urlpatterns = [
    path('test_url', MyView.as_view(), name='test_url'),
    path('parallel_calls_to_databases', parallel_calls_to_databases, name='parallel_calls_to_databases'),
]
