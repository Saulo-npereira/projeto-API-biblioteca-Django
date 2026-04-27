from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .services.api import adicionar_livro_api, quantos_usuarios, deletar_livro_api, listar_livros, editar_estoque, buscar_emprestimo, buscar_livro
from .services.api import listar_usuario, deletar_usuario_api, buscar_usuario, buscar_usuario_id, listar_emp_ativo, listar_emp_atrasados, buscar_emprestimo_livro
from .services.api import renovar_emprestimo_api

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
        acao = request.POST.get('acao')

        if acao == 'adicionar':
            titulo = request.POST.get('titulo')
            autor = request.POST.get('autor')
            descricao = request.POST.get('desc')
            isbn = request.POST.get('isbn')
            categoria = request.POST.get('cate')
            quant_disp = request.POST.get('quant_disp')
            response = adicionar_livro_api(titulo=titulo, autor=autor, descricao=descricao, isbn=isbn, categoria=categoria, quant_disp=quant_disp, request=request)
            return render(request, 'manipularlivros.html', {'response': response, 'livros': livros.get('livros')})
        elif acao == 'buscar':
            livro = request.POST.get('titulo')
            response = buscar_livro(request, livro)
            if response.get('livro'):

                return render(request, 'manipularlivros.html', {'livros': [response.get('livro')]})
            return render(request, 'manipularlivros.html', {'livros': livros.get('livros'), 'message': response.get('detail')})
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

@admin_required
def manipular_usuario(request):
    usuarios = listar_usuario(request)
    if request.method == 'POST':
        email = request.POST.get('usuario')
        usuario = buscar_usuario(request, email)
        if usuario.get('detail'): 
            return render(request, 'manipularusuario.html', {'usuarios': usuarios.get('usuarios'), 'message': usuario.get('detail')})
        return redirect('usuario', usuario['usuario'].get('id'))
    return render(request, 'manipularusuario.html', usuarios)

@admin_required
def deletar_usuario(request, id_usuario):
    deletar_usuario_api(request, id_usuario)
    return redirect('manusuario')

@admin_required
def usuario(request, id_usuario):
    usuario = buscar_usuario_id(request, id_usuario)
    return render(request, 'usuario.html', usuario)

@admin_required
def manipular_emprestimo(request):
    emps_ativos = listar_emp_ativo(request)
    emps_atrasados = listar_emp_atrasados(request)
    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'usuario':
            email = request.POST.get('email')
            usuario = buscar_usuario(request, email)
            if usuario.get('detail'):
                return render(request, 'manipularemprestimo.html', {'emps_ativos': emps_ativos.get('emprestimos_ativos'),
                                                            'emps_atrasados': emps_atrasados.get('emprestimos_atrasados'),
                                                            'message': emps_atrasados.get('message'),
                                                            'detail': usuario.get('detail')})
            emprestimos = buscar_emprestimo(request, usuario['usuario'].get('id'))
            if emprestimos.get('detail'):
                return render(request, 'manipularemprestimo.html', {'emps_ativos': emps_ativos.get('emprestimos_ativos'),
                                                            'emps_atrasados': emps_atrasados.get('emprestimos_atrasados'),
                                                            'message': emps_atrasados.get('message'),
                                                            'detail': emprestimos.get('detail')})
            return render(request, 'emprestimosalguem.html', emprestimos)
        elif acao == 'livro':
            titulo = request.POST.get('titulo')
            emprestimos = buscar_emprestimo_livro(request, titulo)
            if emprestimos.get('detail'):
                messages.error(request=request, message=emprestimos.get('detail'))
                return redirect('manemprestimo')
            return render(request, 'emprestimoslivro.html', emprestimos)



    return render(request, 'manipularemprestimo.html', {'emps_ativos': emps_ativos.get('emprestimos_ativos'),
                                                         'emps_atrasados': emps_atrasados.get('emprestimos_atrasados'),
                                                         'message': emps_atrasados.get('message')})

        

def renovar(request, emp_id):
    response = renovar_emprestimo_api(request, emp_id)
    messages.success(request, response.get('detail'))
    return redirect('manemprestimo')

        