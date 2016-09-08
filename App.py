# Findyourinfo

from flask import Flask, url_for, render_template, request
import requests  #, sys
import json
import re
from info import info
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# sys.path.append('env/Lib/)


app = Flask(__name__)


@app.route('/')
def hello_world():

	return render_template("index.html")

@app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user
	return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
	# show the post with the given id, the id is an integer
	return 'Post %d' % post_id

@app.route('/about')
def about():
	return 'The about page ' + url_for('hello_world') + url_for('projects') + url_for('index', prueba='hello') + url_for('show_user_profile', username='prueba')
 

@app.route('/bing')
def bing():
	bingheader = {'Ocp-Apim-Subscription-Key': '9ed77606931144cca303b3bbffc23c63'}
	binglink = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=%%2B{searchterm}"
	searchterm = request.args.get('search', '')
	firstterm = searchterm.split()[0]
	searchterm = searchterm.replace(" ", "+")
	binglink = binglink.format(searchterm=searchterm)
	bing = requests.get(binglink, headers=bingheader)
	bingprejson = bing.content.decode('utf-8')
	bingjson = json.loads(bingprejson)
	infolist = []

	for x in bingjson['webPages']['value']:
		link = x['displayUrl']
		linkparsed = urlparse(link)
		schemenetloc = linkparsed.scheme + "://" + linkparsed.netloc
		text = x['snippet']
		infolist.append(info(schemenetloc, link, text, ''))

	result = ''
	for x in infolist:
		if re.search('twitter.com/'+searchterm, x.link):
			soup = BeautifulSoup(requests.get('http://twitter.com/' + searchterm).content, 'html5lib')
			x.twitter_name = soup.find(class_="ProfileHeaderCard-nameLink").string if soup.find(class_="ProfileHeaderCard-nameLink") else x.twitter_name
			x.twitter_location = soup.find(class_="ProfileHeaderCard-locationText u-dir").string if soup.find(class_="ProfileHeaderCard-locationText u-dir") else x.twitter_location
			x.twitter_birth = soup.find(class_="ProfileHeaderCard-birthdateText u-dir").span.string if soup.find(class_="ProfileHeaderCard-birthdateText u-dir") else x.twitter_birth
			x.twitter_bio = ''.join(text for text in soup.find(class_="ProfileHeaderCard-bio u-dir").find_all(string=True)) if soup.find(class_="ProfileHeaderCard-bio u-dir") else x.twitter_bio

		if re.search("https://www.facebook.com/(?!public)[\w\W]*" + firstterm, x.link, re.IGNORECASE):
			print(x.link)
			soup = BeautifulSoup(requests.get(x.link).content, 'html5lib')
			x.facebook_location = soup.find(id='current_city').find(class_='_50f5 _50f7').string + '. ' if soup.find(id='current_city') else x.facebook_location
			x.facebook_location = soup.find(id='hometown').find(class_='_50f5 _50f7').string + '. ' if soup.find(id='current_city') else x.facebook_location

			
			for y in soup.find("", {"data-pnref":"edu"}).find_all(class_="_42ef"):
				x.facebook_studies.append(' - '.join(y.find_all(string=True)))

			for y in soup.find("", {"data-pnref":"work"}).find_all(class_="_42ef"):
				x.facebook_work.append(' - '.join(y.find_all(string=True)))
	# print(json.dumps(bingjson, sort_keys=True, indent=4, separators=(',', ': ')))

	return render_template("index.html", infolist=infolist)


@app.route('/google')
def google():
	# Uses Google Custom Search
	google = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyAivBHuR6rQLfFFzYZPsFKoW6NEu2uf178&cx=014899431841328080285:dgyb9nv0qd0&exactTerms={searchterm}&q=")
	searchterm = request.args.get('search', '')
	google = google.format(searchterm=searchterm)
	googlejson = google.json()

	infolist = []

	for x in googlejson['items']:
		link = x['link']
		linkparsed = urlparse(link)
		schemenetloc = linkparsed.scheme + "://" + linkparsed.netloc
		text = x['snippet']

		infolist.append(info(schemenetloc, link, text, ''))

	for x in infolist:
		if re.search('twitter.com/'+searchterm, x.link):
			soup = BeautifulSoup(requests.get('http://twitter.com/' + searchterm).content, 'html5lib')
			x.twitter_name = soup.find(class_="ProfileHeaderCard-nameLink").string if soup.find(class_="ProfileHeaderCard-nameLink") else x.twitter_name
			x.twitter_location = soup.find(class_="ProfileHeaderCard-locationText u-dir").string if soup.find(class_="ProfileHeaderCard-locationText u-dir") else x.twitter_location
			x.twitter_birth = soup.find(class_="ProfileHeaderCard-birthdateText u-dir").span.string if soup.find(class_="ProfileHeaderCard-birthdateText u-dir") else x.twitter_birth
			x.twitter_bio = ''.join(text for text in soup.find(class_="ProfileHeaderCard-bio u-dir").find_all(string=True)) if soup.find(class_="ProfileHeaderCard-bio u-dir") else x.twitter_bio
			
		if re.search("https://www.facebook.com/[\w\W]*"+firstterm, x.link, re.IGNORECASE):
			soup = BeautifulSoup(requests.get(x.link).content, 'html5lib')
			x.facebook_location = soup.find(id='current_city').a.string + '. ' if soup.find(id='current_city') else x.facebook_location

			for y in soup.find("", {"data-pnref":"edu"}).find_all(class_="_42ef"):
				x.facebook_studies.append(' - '.join(y.find_all(string=True)))

			for y in soup.find("", {"data-pnref":"work"}).find_all(class_="_42ef"):
				x.facebook_work.append(' - '.join(y.find_all(string=True)))

	return render_template("index.html", infolist=infolist)
