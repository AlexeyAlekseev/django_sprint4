from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def about(request: HttpRequest) -> HttpResponse:
    """Handles requests for the 'About' page."""
    template: str = 'pages/about.html'
    return render(request, template)


def rules(request: HttpRequest) -> HttpResponse:
    """Handles requests for the 'Rules' page."""
    template: str = 'pages/rules.html'
    return render(request, template)
