# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .tasks import sendEmail
from django.views.decorators.cache import cache_page
import requests


def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")

# a view for test caching via redis:
@cache_page(400)
def test_cache(request):
    response = requests.get("https://b2a3bf75-0773-48c8-be89-468d58a79c66.mock.pstmn.io/test/delay/5")
    return JsonResponse(response.json())