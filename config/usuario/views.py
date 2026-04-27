from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services.api import criar_usuario, logar_usuario, listar_livros, renovar_emprestimo
from .services.api import buscar_livro_por_titulo, pegar_livro_por_id, pegar_emprestado, listar_emprestimos, devolver_livro
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('token')

        if not token:
            return redirect('login')

        return view_func(request, *args, **kwargs)


    return wrapper

def cadastrar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        data = criar_usuario(nome, email, senha)
        if data.get('error') == 'Já existe um usuario com esse email':
            return render(request, 'cadastrar.html', data)
        return redirect('login')
    return render(request, 'cadastrar.html')

def logar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        data = logar_usuario(request, email, senha)

        if data.get('message') == 'Login feito com sucesso':
            request.session['token'] = data['access_token']
            request.session['refresh_token'] = data['refresh_token']
            user = {
            "id": data.get('id_usuario'),
            "username": data.get('nome_usuario'),
            "admin": data.get('admin')
            }

            request.session['user'] = user
            if user['admin']:
                return redirect('homeadmin')
            return redirect('home')
        
        return render(request, 'login.html', {'error': data['detail']})
    
    return render(request, 'login.html')

@login_required
def home(request):
    livros = listar_livros()
    emprestimos = listar_emprestimos(request)

    if request.method == "POST":
        busca = request.POST.get("livro")

        if busca:
            resultados = buscar_livro_por_titulo(busca)

            if resultados:
                return redirect('livro', resultados['id'])
    return render(request, 'home.html', {'livros': livros, 'emprestimos': emprestimos.get('emprestimos')})



@login_required
def livro(request, id):
    livro = pegar_livro_por_id(id)

    if request.method == "POST":
        acao = request.POST.get("acao")

        if acao == "pegar":
            resultado = pegar_emprestado(request=request, id=id)

        elif acao == "devolver":
            resultado = devolver_livro(request=request, id=id)


        return render(request, 'livro.html', {'message': resultado['detail'], 'livro': livro['livro']})

    return render(request, 'livro.html', {'livro': livro['livro']})

@login_required
def renovar(request, id_emprestimo):
    resultado = renovar_emprestimo(request, id_emprestimo)

    messages.success(request=request, message=resultado)
    return redirect('home')
