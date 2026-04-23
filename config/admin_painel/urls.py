from django.urls import path
from . import views

urlpatterns = [
    path('', views.adicionar_livro, name='adicionar_livro')
]
