from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services.api import adicionar_livro_api, quantos_usuarios, deletar_livro_api, listar_livros, editar_estoque

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user')
        

        if not user or not user.get('admin'):
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def homeadmin(request):
    qnts_usuarios_e_livros = quantos_usuarios(request)
    return render(request, 'homeadmin.html', qnts_usuarios_e_livros)

@admin_required
def manipular_livro(request):
    livros = listar_livros()
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        descricao = request.POST.get('desc')
        isbn = request.POST.get('isbn')
        categoria = request.POST.get('cate')
        quant_disp = request.POST.get('quant_disp')
        response = adicionar_livro_api(titulo=titulo, autor=autor, descricao=descricao, isbn=isbn, categoria=categoria, quant_disp=quant_disp, request=request)
        return render(request, 'manipularlivros.html', {'response': response, 'livros': livros.get('livros')})
    return render(request, 'manipularlivros.html', {'livros': livros.get('livros')})

@admin_required
def deletar_livro(request, id_livro):
    deletar_livro_api(request, id_livro)
    return redirect('manlivro')

@admin_required
def editar_estoque_livro(request, id_livro):
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        response = editar_estoque(request, id_livro, quantidade)
        if response.get('detail'):
            return render(request, 'edestoque.html', response)
        return redirect('manlivro')
    return render(request, 'edestoque.html')
        
        