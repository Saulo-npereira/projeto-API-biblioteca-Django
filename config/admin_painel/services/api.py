import requests

BASE_URL = 'http://127.0.0.1:8000/'

def fazer_request(request, metodo, url, **kwargs):
    token = request.session.get('token')

    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers

    response = requests.request(metodo, url, **kwargs)

    if response.status_code == 401:
        sucesso = refresh_token(request)

        if not sucesso:
            return response

        # novo token
        token = request.session.get('token')
        headers["Authorization"] = f"Bearer {token}"

        # tenta de novo
        response = requests.request(metodo, url, **kwargs)

    return response

def refresh_token(request):
    refresh = request.session.get('refresh_token')

    response = requests.post(
        "http://127.0.0.1:8000/usuarios/refresh",
        json={"refresh_token": refresh}
    )

    if response.status_code == 200:
        data = response.json()

        request.session['token'] = data['access_token']
        request.session['refresh_token'] = data['refresh_token']

        return True

    return False


def adicionar_livro_api(titulo:str, autor:str, descricao: str, isbn: str, categoria: str, quant_disp: int, request):
    response = fazer_request(request, 'POST', f'{BASE_URL}bibliotecas/adicionar_livro', json={
    "titulo": titulo,
    "autor": autor,
    "descricao": descricao,
    "isbn": isbn,
    "categoria": categoria,
    "quantidade_disponivel": quant_disp
        })
    return response.json()

def quantos_usuarios(request):
    response = fazer_request(request, 'GET', f'{BASE_URL}usuarios/quantos_usuario')
    return response.json()

def deletar_livro_api(request, id_livro):
    response = fazer_request(request, 'DELETE', f'{BASE_URL}bibliotecas/deletar_livro/{id_livro}')
    return response.json()

def listar_livros():
    response = requests.get(f"{BASE_URL}bibliotecas/listar_livros")
    return response.json()

def editar_estoque(request, id_livro, quantidade):
    response = fazer_request(request, 'POST', f'{BASE_URL}bibliotecas/editar_estoque/{id_livro}/{quantidade}')
    return response.json()

def listar_usuario(request):
    response = fazer_request(request, 'GET', f'{BASE_URL}usuarios/listar_usuarios')
    return response.json()

def deletar_usuario_api(request, id_usuario):
    response = fazer_request(request, 'DELETE', f'{BASE_URL}usuarios/deletar_usuario/{id_usuario}')
    return response.json()

def buscar_usuario(request, email):
    response = fazer_request(request, 'GET', f'{BASE_URL}usuarios/buscar_usuario_email/{email}')
    return response.json()

def buscar_usuario_id(request, id_usuario):
    response = fazer_request(request, 'GET', f'{BASE_URL}usuarios/buscar_usuario_id/{id_usuario}')
    return response.json()

def listar_emp_ativo(request):
    response = fazer_request(request, 'GET', f'{BASE_URL}emprestimos/listar_emprestimos_ativos')
    return response.json()

def listar_emp_atrasados(request):
    response = fazer_request(request, 'GET', f'{BASE_URL}emprestimos/listar_atrasados')
    return response.json()

def buscar_emprestimo(request, id):
    response = fazer_request(request, 'GET', f'{BASE_URL}emprestimos/emprestimos_usuario/{id}')
    return response.json()

def buscar_livro(request, titulo):
    response = fazer_request(request, 'GET', f'{BASE_URL}bibliotecas/buscar_livro_titulo/{titulo}')
    return response.json()
