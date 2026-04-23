from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services.api import adicionar_livro_api

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user')
        

        if not user or not user.get('admin'):
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def adicionar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        descricao = request.POST.get('desc')
        isbn = request.POST.get('isbn')
        categoria = request.POST.get('cate')
        quant_disp = request.POST.get('quant_disp')
        response = adicionar_livro_api(titulo=titulo, autor=autor, descricao=descricao, isbn=isbn, categoria=categoria, quant_disp=quant_disp, request=request)
        return render(request, 'homeadmin.html', response)

    return render(request, 'homeadmin.html')