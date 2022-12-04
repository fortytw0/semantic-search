from django.http import HttpResponse

def hello(request, question_id):
    return HttpResponse("hello world!")