from django.urls import path
from admin_panel.views import home
urlpatterns = [
    path('', home),
]