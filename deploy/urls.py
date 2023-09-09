from django.urls import path

from . import views

urlpatterns = [
    path('', views.trans, name='trans'),
    path('output/', views.op, name='op'),
]