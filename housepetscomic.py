import requests
import praw
import sys
import json
import datetime

file = open("oldtitlecomic.txt","r+")
reddit = praw.Reddit(client_secret="redditsecret",client_id="redditid",user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")
url = 'comicwebhook'
subreddit = reddit.subreddit("housepetscomic")
oldtitle = file.read()
file.close()

data = {}
data["content"] = "New post in r/HousepetsComic!"
data["embeds"] = []
embed = {}
embed["color"] = 16733952

for submission in subreddit.new(limit=1):
	print(submission.title)
	author = "u/" + submission.author.name
	if submission.selftext == "":
		print("No selftext")
		description = "Image post"
	else:
		description = submission.selftext
	if submission.title == oldtitle:
		print("Post already posted.")
		sys.exit(-1)
	else:
		print("New post!")
		file = open("oldtitlecomic.txt","w")
		file.write(submission.title)
		file.close()
	embed["title"] = submission.title
	embed["description"] = description
	embed["url"] = "https://reddit.com" + submission.permalink
	embed["timestamp"] = datetime.datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ')
	embed["footer"] = {"icon_url":"https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png","text":author}
	embed["thumbnail"] = {"url":submission.preview['images'][0]['resolutions'][-1]['url']}
	
data["embeds"].append(embed)

result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
try:
	result.raise_for_status()
except requests.exceptions.HTTPError as err:
	print(err)
else:
	print("Payload delivered successfully, code {}.".format(result.status_code))
