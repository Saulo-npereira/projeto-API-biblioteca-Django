from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', views.logar, name='login'),
    path('', views.home, name='home'),
    path('livro/<int:id>/', views.livro, name='livro'),
    path('renovar/<int:id_emprestimo>/', views.renovar, name='renovar')
]
