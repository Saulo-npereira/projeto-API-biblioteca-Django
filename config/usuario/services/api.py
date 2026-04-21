import requests

BASE_URL = 'http://127.0.0.1:8000/'

def fazer_request(request, metodo, url, **kwargs):
    token = request.session.get('token')

    headers = kwargs.get("headers", {})
    headers["Authorization"] = f"Bearer {token}"
    kwargs["headers"] = headers

    response = requests.request(metodo, url, **kwargs)

    # 🔥 se token expirou
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

def pegar_headers(request):
    token = request.session.get('token')

    return {
        "Authorization": f"Bearer {token}"
    }

def criar_usuario(nome: str, email: str, senha: str):
    try:
        response = requests.post(f'{BASE_URL}usuarios/criar_usuario',
                                 json={
                                     "nome": nome,
                                     "email": email,
                                     "senha": senha,
                                     "admin": False
                                 }, timeout=5)
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        return {
            'success': False,
            'error': response.json().get('detail')
        }
    except requests.exceptions.RequestException:
        return {
            'success': False,
            'error': "Erro na conexão com a API"
        }

def logar_usuario(email: str, senha: str):
    try:
        response = requests.post(f'{BASE_URL}usuarios/login',
                                 json={
                                     "email": email,
                                     "senha": senha,
                                 }, timeout=5)
        if response.status_code == 200:
            return {
                'success': True,
                'data': response.json()
            }
        return {
            'success': False,
            'error': response.json().get('detail')
        }
    except requests.exceptions.RequestException:
        return {
            'success': False,
            'error': "Erro na conexão com a API"
        }


def listar_livros():
    response = requests.get(f"{BASE_URL}bibliotecas/listar_livros")
    return response.json().get("livros", [])


def buscar_livro_por_titulo(titulo):
    response = requests.get(f"{BASE_URL}bibliotecas/buscar_livro_titulo/{titulo}")
    return response.json().get("livro")

def pegar_livro_por_id(id):
    response = requests.get(f"{BASE_URL}bibliotecas/buscar_livro_id/{id}")
    return response.json()

def pegar_emprestado(id, request):
    refresh_token(request)
    response = fazer_request(request, 'POST', f'{BASE_URL}bibliotecas/pegar_emprestado/{id}')
    return response.json()

def listar_emprestimos(request):
    refresh_token(request)
    response = fazer_request(request, 'GET', f'{BASE_URL}emprestimos/ativos_logado')
    return response.json()

def devolver_livro(id, request):
    response = fazer_request(request, 'POST', f'{BASE_URL}bibliotecas/devolver_livro/{id}')
    return response.json()

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

def renovar_emprestimo(request, id_emprestimo):
    response = fazer_request(
        request,
        'POST',
        f'{BASE_URL}emprestimos/renovar_emprestimo/{id_emprestimo}'
    )
    return response.json().get("message")

