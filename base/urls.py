from django.urls import path
from .views import home_page, detail_page

urlpatterns = [
    path('', home_page, name='home_url'),
    path('detail/<int:pk>', detail_page, name='detail_url'),
]   