
from django.urls import path
from .views import home_view, scan_view

urlpatterns = [
    path('', home_view, name='home'),
    path('scan/', scan_view, name='scan'),
]
