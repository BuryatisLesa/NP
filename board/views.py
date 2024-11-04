from django.http import HttpResponse
from django.views import View
from .tasks import hello, printer

class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')