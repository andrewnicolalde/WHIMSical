from django.shortcuts import render

import json

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import *

def index(request):
    events = Event.objects.all().order_by('-created')[:20]

    eventsList = []

    for event in events:
    	items = Item.objects.filter(event=event)

    	itemsList = []

    	for item in items:
    		itemDict = {
    			"label": item.label,
    			"box": item.box,
    			"confidence": item.confidence
    		}

    		itemsList.append(itemDict)

    	missing_items = Missing_items.objects.filter(event=event)

    	missing_itemsList = []
    	for item in missing_items:
    		itemDict = {
    			"label": item.label
    		}

    	missing_itemsList.append(itemDict)

    	eventDict = {
    		"created": event.created.strftime("%m/%d/%Y, %H:%M:%S"),
    		"img_src": event.img_src,
    		"items": itemsList,
    		"missing_items": missing_itemsList
    	}

    output = json.dumps(eventDict)
    return HttpResponse(output)
