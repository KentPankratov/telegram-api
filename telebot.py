#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Bot which accepts following coomands:
     /start - hello message
     /ping - answers 'pong' 
     /time - show what time is it now
     /idme - check out your id in telegram
     /imdb <arguments> - pass as arguments actor names, films etc. and find out a wide answer at your request
     /exg cur1 cur2 - excahnge rates for how much is worth 1 cur1 in cur2
     /weather town - temperature in celsius in your town
     /horoscope sign - find out your today horoscope
     /end - say goodbye to @Talk2MeBot
'''
from datetime import timedelta, datetime
from time import sleep
from twx.botapi import TelegramBot
import json
import requests
import urllib
#import uptime
import imdb
import pyowm
from horoscope import Horoscope

BOT_API_KEY = '***********************************' #your personal token 

last_update = 0
checkervar = 1
bot = TelegramBot(BOT_API_KEY)
bot.update_bot_info().wait()
print"Running TeleBot as %s" % bot.username

#this block goes to prevent cycling over previous updates
updates = bot.get_updates().wait()
if updates is not None:
    for update in updates:
        if update.update_id > last_update:
            last_update = update.update_id


def loop():
    global last_update
    global bot
    global checkervar #1111
    updates = bot.get_updates().wait()
    if updates is not None:
        for update in updates:
            if update is None:
                continue
            if update.update_id is None:
                continue
            if update.update_id <= last_update:
                continue
            if update.message.text is None:
                continue

            print update
            last_update = update.update_id
            text_split = update.message.text.split(' ')
            cmd = text_split[0]
            args = text_split[1:] or None
            chat_id = update.message.chat.id
            sender = update.message.sender
	    if cmd=='/start':
		bot.send_message(chat_id, 'Hi, %s!'%(sender.first_name)).wait()
            if cmd == '/ping':
                bot.send_message(chat_id, 'Pong!').wait()

            if cmd == '/time':
                #bot.send_message(chat_id, str(timedelta(seconds=uptime.uptime())).rsplit('.', 1)[0]).wait()
                bot.send_message(chat_id, str(datetime.now().time())).wait()

            if cmd == '/idme':
                bot.send_message(chat_id, '%s, your user ID is %s' % (sender.first_name, sender.id)).wait()

            '''if cmd == '/mcstatus':
                status = requests.get('http://status.mojang.com/check').text
                status = json.loads(status)
                message = '-- Mojang Service Status --\n\n'
                for i in status:
                    k, v = list(i.items())[0]
                    message += "%s: %s\n" % (k, v.replace('green', u'✅').replace('red', u'🚫').replace('yellow', u'⚠️'))
                bot.send_message(chat_id, message, True).wait()'''

            if cmd == '/imdb': #IMDB INFORMATION ABOUT FILMS, ATCORS, DIRECTORS ETC. 
                if args is None:
                    bot.send_message(chat_id, "Usage: /imdb <search_terms>").wait()
                    continue
                search_terms = ''.join(args)
                ia = imdb.IMDb()
                s_result = ia.search_movie(search_terms)
                movie = s_result[0]
                ia.update(movie)
                bot.send_message(chat_id, movie.summary()).wait()
            if cmd == '/exg':  #CURRENCY RATES
		if args is None:
		    bot.send_message(chat_id, "Usage: /exg cur1 cur2").wait()
                    continue
		url = 'https://currency-api.appspot.com/api/'+args[0].upper()+'/'+args[1].upper()+'.json'
		url = urllib.urlopen(url)
		result = url.read()
		url.close()
		result = json.loads(result)
		#if result['success']:
		bot.send_message(chat_id, '1 %s is worth %.2f %s' % (args[0].upper(), float(result['rate']), args[1].upper())).wait()
	    if cmd == '/weather':
		owm = pyowm.OWM()
		observation = owm.weather_at_place(args[0])
		w = observation.get_weather()
		tempnow = w.get_temperature('celsius')['temp']
		bot.send_message(chat_id,'Temperature in %s at the moment %.2f C'%(args[0], tempnow)).wait()
	    if cmd == '/horoscope':
		your_horoscope = Horoscope.get_todays_horoscope(args[0]) 
		bot.send_message(chat_id, 'Your horoscope for today:\n %s'%(your_horoscope['horoscope'])).wait()
	    if cmd == '/end':
		bot.send_message(chat_id, 'See you next time, %s!'%(sender.first_name)).wait()
		checkervar=0


if __name__ == '__main__':
    while checkervar!=0:
        sleep(0.5)
        try:
            loop()
        except:
            continue
    print 'Bye'
