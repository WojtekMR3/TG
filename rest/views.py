from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest.models import World, Highscore
import datetime

import tibiapy
import requests
import json

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>Time is now %s.</body></html>" % now
    return HttpResponse(html)

def db(request):
    entries = World.objects.filter(created_at__gte="2022-01-25")
    data = list(entries.values())
    return JsonResponse(data, safe=False)

def dbSave(request):
    for x in range(500):
      w = World(name='SampleWorld', onlineCount='9000', created_at='2017-04-16 04:55:51+00')
      w.save()
    return HttpResponse("DB Saving done")

def dbDelete(request):
    World.objects.filter(name='SampleWorld').delete()
    return HttpResponse("DB Deleting done")

def get_highscores(request, world):
    query = Highscore.objects.filter(created_at__gte="2022-03-01", world=world)
    data = list(query.values())
    return JsonResponse(data, safe=False)

def get_worlds(request):
    url = tibiapy.WorldEntry.get_list_url()
    r = requests.get(url)
    content = r.text
    worlds = tibiapy.WorldEntry.list_from_content(content)
    worlds = list(filter(lambda world: not world.experimental and not world.tournament_world_type, worlds))
    worldsList = []
    for world in worlds:
      wrldList = {
        "name": world.name,
        "location": str(world.location),
      }
      worldsList.append(wrldList)
    return JsonResponse(worldsList, safe=False)