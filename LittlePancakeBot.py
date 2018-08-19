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

eightBall = ["It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "As I see it, yes", 
	    "Most likely", "Yes", "The answer is exactly what you think it is", "Signs point to a yes", "Better not tell you now", 
	     "That is up for you to decide", "I don't think you should know", "Don't count on it", "My reply is no", "My sources say no", 
	     "Unlikely", "Very doubtful", "No", "Signs point to no", "Not a chance"]

client = discord.Client()

@client.event
async def on_ready():
	print("Logged in as")
	print(client.user.name)
	print(client.user.id)
	print('--------')
	client.change_presence(game=discord.Game(type=0, name=">help"))

@client.event
async def on_member_join(member):
	await sendEmbed(member.server.default_channel, "Welcome, " + str(member.name) + " <:yayshark:327870025878732800>")

@client.event
async def on_member_remove(member):
	await sendEmbed(client.get_channel("443112151339499560"), str(member.name) + " has left the server.")

@client.event
async def on_message(message):
	if message.content.startswith(">hello"):
		await sendEmbed(message.channel, "Good day.")

	elif message.content.startswith(">help"):
		await sendEmbed(message.channel, mainTitle="List of Commands:", desc="\n>roll (Rolls a random number between 0 and 100" + 
			"\n>roll x (Rolls a random number between 0 and x)" +
			"\n>8ball (Will answer a yes or no question with blistering accuracy)" +
			"\n\n>left or right (Greatly improves your T2 skill, screenshot optional)" + 
			"\n>which class (If you need help deciding which class to play on T2)" +
			"\n\n>shadowlog (grabs relevant data from shadowlog, can specify class and/or format)" +
			"\n    eg. >shadowlog forest (Grabs Forest's stats in rotation)" +
			"\n        >shadowlog sword unlimited (Grabs Sword's stats in unlimited)" + 
			"\n        >shadowlog unlimited (Grabs all relevant stats in unlimited)" +
			"\n\n>anime (Searches MAL for specified anime)" + 
			"\n>anime tv (For only TV search)" +
			"\n>anime movie (For only movie search)" +
			"\n>anime random (Grabs a random anime out of the best 1500 on MAL)" +
			"\n>manga (Searches MAL for specified manga)" +
			"\n>manga random (Grabs a random manga out of the best 1000 on MAL)", footer=True)

	elif message.content.startswith(">roll"):
		try:
			maxrand = int(message.content[6:])
			if maxrand > 0:
				await sendEmbed(message.channel, desc="You rolled " + str(randint(0, maxrand)))
		except:
			await sendEmbed(message.channel, desc="You rolled " + str(randint(0, 100)))
			
	elif message.content.startswith(">which class"):
		await sendEmbed(message.channel, desc="You should choose " + choice(["the 1st one", "the 2nd one", "the 3rd one"]))

	elif message.content.startswith(">left or right") or message.content.startswith(">right or left"):
		await sendEmbed(message.channel, desc="You should choose " + choice(["Left", "Right"]))

	elif message.content.startswith(">anime "):
		if message.content.startswith(">anime random"):
			randomNumber = randint(0, 1499)
			soup_page = getSoup("https://myanimelist.net/topanime.php?limit=" + str(randomNumber))

			anime = soup_page.find('a', class_="hoverinfo_trigger fl-l fs14 fw-b")
			await client.send_message(message.channel, anime['href'])
			return

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
			await sendEmbed(message.channel, desc="Please add a search term at the end.")
			return

		search.replace(" ", "%20")
		soup_page = getSoup("https://myanimelist.net/anime.php?q=" + search + searchType)

		anime = soup_page.find('a', class_="hoverinfo_trigger fw-b fl-l")
		await client.send_message(message.channel, anime['href'])

	elif message.content.startswith(">manga "):
		if message.content.startswith(">manga random"):
			randomNumber = randint(0, 1000)
			soup_page = getSoup("https://myanimelist.net/topmanga.php?limit=" + str(randomNumber))

			manga = soup_page.find('a', class_="hoverinfo_trigger fs14 fw-b")
			await client.send_message(message.channel, manga['href'])
		else:
			search = message.content[7:]

			if search == "":
				await sendEmbed(message.channel, desc="Please add a search term at the end.")
				return

			search.replace(" ", "%20")
			soup_page = getSoup("https://myanimelist.net/manga.php?q=" + search)

			manga = soup_page.find('a', class_="hoverinfo_trigger fw-b")
			await client.send_message(message.channel, manga['href'])

	elif message.content.startswith(">shadowlog"):
		if " sword" in message.content:
			await classShadowlogMessage(message, "Sword", "2")
		elif " rune" in message.content:
			await classShadowlogMessage(message, "Rune", "5")
		elif " portal" in message.content:
			await classShadowlogMessage(message, "Portal", "8")
		elif " haven" in message.content:
			await classShadowlogMessage(message, "Haven", "7")
		elif " blood" in message.content:
			await classShadowlogMessage(message, "Blood", "6")
		elif " dragon" in message.content:
			await classShadowlogMessage(message, "Dragon", "3")
		elif " forest" in message.content:
			await classShadowlogMessage(message, "Forest", "1")
		elif " shadow" in message.content:
			await classShadowlogMessage(message, "Shadow", "4")
		else:
			await classShadowlogMessage(message)

	elif message.content.startswith("Who's the best shadowverse player"):
		await sendEmbed(message.channel, desc="Why " + os.environ.get("BEST_PLAYER") + " of course <:smug:302980339444350976>")
		
	elif message.content.startswith(">8ball "):
		await sendEmbed(message.channel, desc=choice(eightBall))

def getSoup(link):
	uClient = uRequest.urlopen(link)
	sauce = uClient.read()
	uClient.close()
	return bs.BeautifulSoup(sauce, 'html.parser')

def sendEmbed(channel, desc="", mainTitle="", fTitles=None, fDesc=None, footer=False):
	embed = discord.Embed(title=mainTitle, colour=discord.Colour(0xe21433), 
			description=desc)

	if fTitles != None and fDesc != None:
		for i in range(len(fTitles)):
			embed.add_field(name=fTitles[i], value=fDesc[i])

	if footer:
		embed.set_footer(text="Bot made by PancakeReaper", icon_url="https://i.imgur.com/8jy3d5T.png")
	return client.send_message(channel, "", embed=embed)
	
def classShadowlogMessage(message, name="", class_="", table=1):
	r = "r"
	if "unlimited" in message.content:
		r = ""
	week = int(time.strftime("%W", time.gmtime()))-1
	soup_page = getSoup("https://shadowlog.com/trend/2018/" + str(week+1) + "/4/" + class_ + r)

	if(soup_page.find("div", class_="date-priod") == None):
		soup_page = getSoup("https://shadowlog.com/trend/2018/" + str(week) + "/4/" + class_ + r)

	title = soup_page.find("div", class_="date-priod").text
	if name != "":
		title = name + "'s matchup data, collected from " + title[5:16] + " - " + title[19:30]
	else:
		title = "General data, collected from " + title[5:16] + " - " + title[19:30]

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

	classNames = []
	classStats = []
	for row in data:
		if name == "":
			classNames.append(translate[row[0]])
		else:
			classNames.append("vs" + translate[row[0][2:]])
		classStats.append("Playrate: " + row[1] + "\nRecorded games: " + row[2] + "\nOverall Winrate: " + row[4] + 
			"\nWhen going 1st: " + row[5] + "\nWhen going 2nd: " + row[6])
	return sendEmbed(message.channel, mainTitle=title, fTitles=classNames, fDesc=classStats, footer=True)

client.run(os.environ.get("BOT_TOKEN"))
