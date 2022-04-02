from django.conf import settings
from rest.models import Highscore
import tibiapy
import time
from django.utils import timezone
from datetime import datetime
import asyncio
import requests
import json
import sys

# Asynchronously
import aiohttp

def get_character():
    url = tibiapy.Character.get_url("Alee Mau")

    r = requests.get(url)
    content = r.text
    character = tibiapy.Character.from_content(content)
    print(character)
    return character

async def mainRq():
    async with aiohttp.ClientSession() as session:
        url = tibiapy.WorldEntry.get_list_url()
        async with session.get(url) as resp:
            print(resp.status)
            print(await resp.text())

async def get_character_async(session, url):
    for x in range(1, 11):
        try:
            async with session.get(url) as resp:
                status = resp.status
                if (status != 200):
                    await asyncio.sleep(1/5)
                    continue
                content = await resp.text()
                char_url_list.remove(url)
                character = tibiapy.Character.from_content(content)
                return character
        except (
          aiohttp.ClientConnectionError,
          aiohttp.ClientError,
          aiohttp.ServerDisconnectedError,
          asyncio.IncompleteReadError,
        ) as ex:
            print("Error: ", ex)
            await asyncio.sleep(1)

    return "Failed"

async def check_all_nicknames(char_url_list):
    async with create_session() as session:
        tasks = []
        for charname in char_url_list:
            tasks.append(asyncio.ensure_future(get_character_async(session, charname)))
            #await asyncio.sleep(1/25)

        char_list = await asyncio.gather(*tasks)
        filtered_char_list = filter(lambda char: char != "Failed", char_list)
        return char_list

def char_urls_list(char_list):
    urls = []
    for char in char_list:
        url = tibiapy.Character.get_url(char.name)
        urls.append(url)
    return urls[:100]

def blacklisted_worlds(world):
    return not world.experimental and not world.tournament_world_type

async def fetch_htmls(urls):
    async with create_session() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(fetch_html(session, url)))

        return await asyncio.gather(*tasks)

def create_session():
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=10, force_close=True)
    timeout = aiohttp.ClientTimeout(total=60*60)
    headers = {
        "User-Agent": "Tibiagraphs",
        "Accept-Encoding": "gzip, deflate"
    }
    session = aiohttp.ClientSession(connector=connector, timeout=timeout, headers=headers, trust_env=True)
    return session

async def fetch_html(session, url):
    for x in range(1, 100):
      try:
        async with session.get(url) as resp:
            if (resp.status != 200):
                await asyncio.sleep(1/20)
                continue
            content = await resp.text()
            return content
      except (
        aiohttp.ClientConnectionError,
        aiohttp.ClientError,
        aiohttp.ServerDisconnectedError,
        asyncio.IncompleteReadError,
      ) as ex:
          print("Error: ", ex)
          await asyncio.sleep(1)

    return url

def prep_url_list():
    url = tibiapy.WorldEntry.get_list_url()
    asyncio.run(mainRq)
    # url_list = []
    # url_list.append(url)
    # cnt = asyncio.run(fetch_htmls(url_list))
    # for item in cnt:
    #     print(cnt)
    headers = {
        "User-Agent": "Tibia.py/%s (+https://github.com/Galarzaa90/tibia.py)",
        "Accept-Encoding": "gzip, deflate"
    }
    r = requests.get(url, headers=headers)
    content = r.text
    worlds = tibiapy.WorldEntry.list_from_content(content)
    worlds = list(filter(blacklisted_worlds, worlds))
    # get number of hs pages for each world
    url_list = []
    for world in worlds:
        url = tibiapy.Highscores.get_url(world=world.name)
        url_list.append(url)
    content = asyncio.run(fetch_htmls(url_list))
    worlds_hs = []
    for html in content:
        hs = tibiapy.Highscores.from_content(html)
        worlds_hs.append(hs)
    # num of worlds is ~85 each world has 20 hs pages. Total of ~1600 reqs
    url_list = []
    for world_hs in worlds_hs:
        for n in range(0, world_hs.total_pages):
            url = tibiapy.Highscores.get_url(world=world_hs.world,page=n+1)
            url_list.append(url)
    return url_list

def get_hs_as():
    url_list = prep_url_list()
    list_main = []
    content = asyncio.run(fetch_htmls(url_list))
    for html in content:
        hs = tibiapy.Highscores.from_content(html)
        list_main.extend(hs.entries)
    #print(datetime.now(), "reqs list: ", len(url_list))
    # if hr < 10:
        # timedelta hours 10-hr 
        # get previous day date and set it to 10 am
        # delete all entries from the day AND the day before from 10 am
    #date from string
    hr = datetime.now(tz=timezone.utc).hour
    if hr >= 10:
        target_dt = datetime.now(tz=timezone.utc).replace(hour=10, minute=00)
        print(target_dt)
        query = Highscore.objects.filter(created_at__gte=target_dt)
        query.delete()
    for hs in list_main:
        h = Highscore(nick=hs.name, world=hs.world, vocation=hs.vocation, level=hs.level, exp=hs.value)
        h.save()
    return list_main

start_time = time.time()

st = datetime.now()
print(st, "get_hs_as fnc start")
#get_hs_as()
# char_url_list = char_urls_list(lmain)

# while len(char_url_list) > 0:
#     content = asyncio.run(check_all_nicknames(char_url_list))
#     print(datetime.now(), "char_url_list: ", len(char_url_list))
#     time.sleep(1)

print("script started: ", st)
print("--- %s seconds ---" % (time.time() - start_time))
#hs = tibiapy.Highscores.from_content(content)
#print(hs.entries[49])