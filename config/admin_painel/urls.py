from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeadmin, name='homeadmin'),
    path('livros/', views.manipular_livro, name='manlivro'),
    path('deletar_livro/<int:id_livro>/', views.deletar_livro, name='dellivro'),
    path('edestoque_livro/<int:id_livro>/', views.editar_estoque_livro, name='edestoque'),
    path('usuarios/', views.manipular_usuario, name='manusuario'),
    path('delusuario/<int:id_usuario>/', views.deletar_usuario, name='delusuario'),
    path('usuario/<int:id_usuario>/', views.usuario, name='usuario'),
    path('emprestimos/', views.manipular_emprestimo, name='manemprestimo'),
    path('renovar/<int:emp_id>/', views.renovar, name='renovar')
]
