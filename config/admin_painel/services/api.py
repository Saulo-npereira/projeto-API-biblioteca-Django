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
