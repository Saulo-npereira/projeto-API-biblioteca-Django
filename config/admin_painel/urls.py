from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeadmin, name='homeadmin'),
    path('livros/', views.manipular_livro, name='manlivro'),
    path('deletar_livro/<int:id_livro>/', views.deletar_livro, name='dellivro'),
    path('edestoque_livro/<int:id_livro>/', views.editar_estoque_livro, name='edestoque')
]
