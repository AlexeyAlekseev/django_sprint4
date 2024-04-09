from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)


def permission_denied(request, reason=''):
    return render(request, 'pages/403.html', status=HTTPStatus.FORBIDDEN)


def server_error(request, reason=''):
    return render(request,
                  'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR
                  )
