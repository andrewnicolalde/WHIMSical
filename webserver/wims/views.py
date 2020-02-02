from django.shortcuts import render
from django.http import JsonResponse
import json

# Create your views here.
from .models import *

def events(request):
    events = Event.objects.all().order_by('-created')[:20]

    eventsList = []

    for event in events:
    	# Build items list
    	items = Item.objects.filter(event=event)

    	itemsList = []

    	for item in items:
    		itemDict = {
    			"label": item.label,
    			"box": item.box,
    			"confidence": item.confidence
    		}

    		itemsList.append(itemDict)

    	# Build missing items list
    	missing_items = Missing_items.objects.filter(event=event)

    	missing_itemsList = []
    	for item in missing_items:
    		itemDict = {
    			"label": item.label
    		}

    		missing_itemsList.append(itemDict)

    	# Build event object
    	eventDict = {
    		"created": event.created.strftime("%m/%d/%Y, %H:%M:%S"),
    		"img_src": event.img_src,
    		"items": itemsList,
    		"missing_items": missing_itemsList
    	}

    	eventsList.append(eventDict)

    #output = json.dumps(eventDict)
    return JsonResponse(eventsList, safe=False)

def index(request):
	return render(request, "wims/index.html")
