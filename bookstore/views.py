from django.http import JsonResponse

# As per Django Documentation, A view function is a Python function
# that takes a Web request and returns a Web response.


def ping(request):
    # data = {"status": "success!!!"}
    data = {"ping": "pong!"}
    return JsonResponse(data)
