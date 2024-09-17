from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def about(request: HttpRequest) -> HttpResponse:
    """Рассказ о проекте."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """Отображений правил проекта."""
    template = 'pages/rules.html'
    return render(request, template)


def page_not_found(request, exception):
    """Сообщение о том, что страница не найдена"""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Сообщение об ошибке проверки CSRF, запрос отклонён"""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Сообщение об ошибке сервера"""
    return render(request, 'pages/500.html', status=500)
