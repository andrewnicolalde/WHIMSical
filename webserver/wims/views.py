from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import event

def index(request):
    events = event.objects.order_by('-created')
    output = ', '.join([e.label for e in events])
    return HttpResponse(output)
