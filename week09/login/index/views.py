from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .form import LoginForm


def index(request: HttpRequest):
    return render(request, 'index/index.html')


@require_http_methods(['GET', 'POST'])
def login(request: HttpRequest):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'index/form.html', locals())
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            form_data = login_form.cleaned_data
            user = authenticate(username=form_data['username'], password=form_data['password'])
            if user:
                return render(request, 'index/success.html', locals())
            else:
                return render(request, 'index/failed.html')
