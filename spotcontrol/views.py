from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, TemplateView


def index(request):
    return render(request, 'spotcontrol/index.html', {})


def room(request, room_name):
    return render(request, 'spotcontrol/room.html', {
      'room_name': room_name
    })


def auth_spotify(request):
    print(request)
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    print(
        f'\ncode = {code}\n\n'
        f'state = {state}\n'
    )
    return HttpResponse("Hello.")


class MainPage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        print(f'context: {context}')
        return context


class AuthResult(TemplateView):
    template_name = 'auth/auth_success_or_fail.html'

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        print(f'context: {context}')
        return context
