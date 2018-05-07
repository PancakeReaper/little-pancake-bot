import discord
import asyncio

import os
from random import randint
from random import choice
import time
	
import bs4 as bs
from urllib import request as uRequest

translate = {"ロイヤル":"Sword", "ウィッチ":"Rune", "ネメシス":"Portal", "ビショップ":"Haven", 
			 "ヴァンパイア":"Blood", "ドラゴン":"Dragon", "エルフ":"Forest", "ネクロマンサー":"Shadow"}

eightBall = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it", "As I see it, yes", 
	    "Most likely", "Outlook good", "Yes", "Signs point to yes", "Reply hazy try again", "Ask again later", 
	     "Better not tell you now", "Cannot predict now", "Concentrate and ask again", "Don't count on it", 
	     "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

client = discord.Client()

@client.event
async def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print('------')
	client.change_presence(game=discord.Game(name=">help"))

@client.event
async def on_member_join(member):
	await client.send_message(member.server.default_channel, "Welcome, " + str(member.name) + " <:yayshark:327870025878732800>")
	
@client.event
async def on_member_remove(member):
	await client.send_message(member.server.default_channel, str(member.name) + " has left the server <:thesaddest:357950212096131072>")

@client.event
async def on_message(message):
	if message.content.startswith(">hello"):
		await client.send_message(message.channel, "Good day.")

	elif message.content.startswith(">help"):
		await client.send_message(message.channel,
			"```" +
			"\n>roll (Rolls a random number between 0 and 100" + 
			"\n>roll x (Rolls a random number between 0 and x)" +
			"\n>flip (Flips a coin)" + 
			"\n>shadowlog (grabs relevant data from shadowlog, can specify class and/or format)" +
			"\n    eg. >shadowlog forest (Grabs Forest's stats in rotation)" +
			"\n        >shadowlog sword unlimited (Grabs Sword's stats in unlimited)" + 
			"\n        >shadowlog unlimited (Grabs all relevant data in unlimited)" +
			"\n>anime (Searches MAL for specified anime)" + 
			"\n>anime tv (For only TV search)" +
			"\n>anime movie (For only movie search)" +
			"\n>anime random (Grabs a random anime out of the best 1500 on MAL)" +
			"\n>manga (Searches MAL for specified manga)" +
			"\n>manga random (Grabs a random manga out of the best 1000 on MAL)" + "\n```")

	elif message.content.startswith(">roll"):
		try:
			maxrand = int(message.content[6:])
			if maxrand > 0:
				await client.send_message(message.channel, "You rolled " + str(randint(0, maxrand)))
		except:
			await client.send_message(message.channel, "You rolled " + str(randint(0, 100)))

	elif message.content.startswith(">flip"):
		await client.send_message(message.channel, "You flipped a " + choice(["Heads.", "Tails."]))

	elif message.content.startswith(">anime random"):
		randomNumber = randint(0, 1499)
		uClient = uRequest.urlopen("https://myanimelist.net/topanime.php?limit=" + str(randomNumber))
		sauce = uClient.read()
		uClient.close()
		soup_page = bs.BeautifulSoup(sauce, 'html.parser')

		anime = soup_page.find('a', class_="hoverinfo_trigger fl-l fs14 fw-b")
		await client.send_message(message.channel, anime['href'])

	elif message.content.startswith(">anime "):

		if message.content.startswith(">anime movie "):
			search = message.content[13:]
			searchType = "&type=3"
		elif message.content.startswith(">anime tv "):
			search = message.content[10:]
			searchType = "&type=1"
		else:
			search = message.content[7:]
			searchType = "" 

		if(search == ""):
			await client.send_message(message.channel, "Please add a search term at the end.")
			return

		search.replace(" ", "%20")
		uClient = uRequest.urlopen("https://myanimelist.net/anime.php?q=" + search + searchType)
		sauce = uClient.read()
		uClient.close()
		soup_page = bs.BeautifulSoup(sauce, 'html.parser')

		anime = soup_page.find('a', class_="hoverinfo_trigger fw-b fl-l")
		await client.send_message(message.channel, anime['href'])

	elif message.content.startswith(">manga "):
		if message.content.startswith(">manga random"):
			randomNumber = randint(0, 1000)
			uClient = uRequest.urlopen("https://myanimelist.net/topmanga.php?limit=" + str(randomNumber))
			sauce = uClient.read()
			uClient.close()
			soup_page = bs.BeautifulSoup(sauce, 'html.parser')

			manga = soup_page.find('a', class_="hoverinfo_trigger fs14 fw-b")
			await client.send_message(message.channel, manga['href'])
		else:
			search = message.content[7:]

			if search == "":
				await client.send_message(message.channel, "Please add a search term at the end.")
				return

			search.replace(" ", "%20")
			uClient = uRequest.urlopen("https://myanimelist.net/manga.php?q=" + search)
			sauce = uClient.read()
			uClient.close()
			soup_page = bs.BeautifulSoup(sauce, 'html.parser')

			manga = soup_page.find('a', class_="hoverinfo_trigger fw-b")
			await client.send_message(message.channel, manga['href'])

	elif message.content.startswith(">shadowlog"):
		r = "r"
		if "unlimited" in message.content:
			r = ""
		week = int(time.strftime("%W", time.gmtime()))-1
		uClient = uRequest.urlopen("https://shadowlog.com/trend/2018/" + str(week) + "/4/" + r)
		sauce = uClient.read()
		uClient.close()
		soup_page = bs.BeautifulSoup(sauce, 'html.parser')

		data = []
		table = soup_page.find("table", id="table1")
		table_body = table.find("tbody")

		rows = table_body.findAll("tr")
		i = 0
		for row in rows:
			data.append([])
			cols = row.findAll("td")
			for col in cols:
				data[i].append(col.text)
			i+=1

		t = "```\n"
		if " sword" in message.content:
			t += getShadowlogMessage(data, "Sword") + "\n```"
		elif " rune" in message.content:
			t += getShadowlogMessage(data, "Rune") + "\n```"
		elif " portal" in message.content:
			t += getShadowlogMessage(data, "Portal") + "\n```"
		elif " haven" in message.content:
			t += getShadowlogMessage(data, "Haven") + "\n```"
		elif " blood" in message.content:
			t += getShadowlogMessage(data, "Blood") + "\n```"
		elif " dragon" in message.content:
			t += getShadowlogMessage(data, "Dragon") + "\n```"
		elif " forest" in message.content:
			t += getShadowlogMessage(data, "Forest") + "\n```"
		elif " shadow" in message.content:
			t += getShadowlogMessage(data, "Shadow") + "\n```"
		else:
			t += getShadowlogMessage(data) + "```"
		await client.send_message(message.channel, t)

	elif message.content.startswith("Who's the best shadowverse player"):
		await client.send_message(message.channel, "Why " + os.environ.get("BEST_PLAYER") + " of course <:smug:302980339444350976>")
		
	elif message.content.startswith(">8ball "):
		randomNumber = randint(0, 19)
		await client.send_message(message.channel, eightBall[randomNumber])

def getShadowlogMessage(data, target=""):
	if target != "":
		for row in data:
			if translate[row[0]] == target:
				return target + " has a playrate of " + row[1] + " at a winrate of " + row[4] + " (" + row[5] + " first, " + row[6] + " second)\n"
	s = ""
	for row in data:
		s += translate[row[0]] + " has a playrate of " + row[1] + " at a winrate of " + row[4] + " (" + row[5] + " first, " + row[6] + " second)\n"
	return s

client.run(os.environ.get("BOT_TOKEN"))
