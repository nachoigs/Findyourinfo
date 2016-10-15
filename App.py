# Findyourinfo

from flask import Flask, url_for, render_template, request
import requests  #, sys
import json
import re
from info import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tinfoleak as tinfoleak



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


	for x in infolist:
		if re.search('twitter.com/'+searchterm, x.link):
			twitter_search(x, searchterm)

		if re.search("https://www.facebook.com/(?!public)[\w\W]*" + firstterm, x.link, re.IGNORECASE):
			facebook_search(x, x.link)


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

@app.route('/tinfoleak')
def tinfoleakfunction():
	# Show Twitter info using TinfoLeak

	user = request.args.get('user', '')

	if (user == ''):
		return

	templatedata = tinfoleak.main([user, "-i"])

	#tinfoleak.main([user, "-i"])

	return render_template("tinfoleak.html", **templatedata)

@app.route('/testlinkedin')
def linkedintest():
	link = request.args.get('link', '')

	if (link == ''):
		return

	infolist = []
	infolist.append(info('', link, '' , ''))

	for x in infolist:
		linkedin_search(x, x.link)

		for y in x.__dict__:
			print('{}: {}'.format(y, x.__dict__[y]))
			if isinstance(x.__dict__[y], list):
				for z in x.__dict__[y]:
					for t in z.__dict__:
						print('{}: {}'.format(t, z.__dict__[t]))
						if isinstance(z.__dict__[t], list):
							for j in z.__dict__[t]:
								for i in j.__dict__:
									print('{}: {}'.format(i, j.__dict__[i].encode('utf-8')))



						
	return render_template("index.html", infolist=infolist)


## FUNCTIONS ##


def twitter_search(x, searchterm):
	soup = BeautifulSoup(requests.get('http://twitter.com/' + searchterm).content, 'html5lib')
	x.twitter_name = soup.find(class_="ProfileHeaderCard-nameLink").string if soup.find(class_="ProfileHeaderCard-nameLink") else x.twitter_name
	x.twitter_location = soup.find(class_="ProfileHeaderCard-locationText u-dir").string if soup.find(class_="ProfileHeaderCard-locationText u-dir") else x.twitter_location
	x.twitter_birth = soup.find(class_="ProfileHeaderCard-birthdateText u-dir").span.string if soup.find(class_="ProfileHeaderCard-birthdateText u-dir") else x.twitter_birth
	x.twitter_bio = ''.join(text for text in soup.find(class_="ProfileHeaderCard-bio u-dir").find_all(string=True)) if soup.find(class_="ProfileHeaderCard-bio u-dir") else x.twitter_bio


def facebook_search(x, link):
	soup = BeautifulSoup(requests.get(x.link).content, 'html5lib')
	x.facebook_location = soup.find(id='current_city').find(class_='_50f5 _50f7').string + '. ' if soup.find(id='current_city') else x.facebook_location
	x.facebook_location = soup.find(id='hometown').find(class_='_50f5 _50f7').string + '. ' if soup.find(id='current_city') else x.facebook_location

	for y in soup.find("", {"data-pnref":"edu"}).find_all(class_="_42ef"):
		x.facebook_studies.append(' - '.join(y.find_all(string=True)))

	for y in soup.find("", {"data-pnref":"work"}).find_all(class_="_42ef"):
		x.facebook_work.append(' - '.join(y.find_all(string=True)))


def linkedin_search(x, link):
	headers = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)'}
	r = requests.get(link, headers=headers)
	soup = BeautifulSoup(r.content, 'html5lib')
	print(link)

	#print(soup.encode('utf-8'))

	profile = soup.find(id="profile")

	topcard = profile.find(id="topcard")
	topcard_info = ''
	if topcard:
		picture = topcard.find("div", class_="profile-picture").a["href"] or ""
		profileoverview = topcard.find("div", class_="profile-overview-content") or ""
		name = profileoverview.find(id="name").string or ""
		headline = profileoverview.find("p", class_="headline title").string or ""
		location = profileoverview.find("span", class_="locality").string or "" 
		sector = profileoverview.find("dd", class_="descriptor").string or "" 
		topcard_info = linkedin_topcard(picture, name, headline, location, sector)

	experience = profile.find(id="experience")
	experience_info = []
	if experience:		
		for position in experience.find_all(class_="position"):
			title = position.find(class_="item-title").string or ""
			subtitle = position.find(class_="item-subtitle").string or ""
			date_range = "".join(position.find(class_="date-range").find_all(string=True)) or ""
			location = position.find(class_="location").string or ""


	education = profile.find(id="education")
	schools_info = []
	if education:
		schools = education.find_all("li", class_="school")
		for school in schools:
			print(school.encode('utf-8'))
			title = school.find(class_="item-title").string or ""
			subtitle = school.find(class_="item-subtitle").find(class_="original translation").string or ""
			period = " ".join(school.find(class_="date-range").find_all(string=True)) or ""
			## Reminder: Check this, I have to try it ASAP ##
			descriptionsoup = school.find(class_="description") or ""
			description = " - "
			if (descriptionsoup):
				description = description.join(descriptionsoup.find_all(string=True)) or ""

			schools_info.append(linkedin_school(title, subtitle, period, description))

	awards = profile.find(id="awards")
	awards_info = []
	if awards:
		for award in awards.find_all(class_="award"):
			title = award.find(class_="item-title").string or ""
			subtitle = award.find(class_="item-subtitle").string or ""
			description = award.find(class_="description").string or ""

			awards_info.append(linkedin_awards(title, subtitle, description))

	languages = profile.find(id="languages")
	languages_info = []
	if languages:
		for language in languages.find_all(class_="language"):
			name = language.find(class_="name").string or ""
			proficiency = language.find(class_="proficiency").string or ""

			languages_info.append(linkedin_languages(name, proficiency))

	certifications = profile.find(id="certifications")
	certifications_info = []
	if certifications:
		for certification in certifications.find_all(class_="certification"):
			title = certification.find(class_="item-title").string or ""
			subtitle = certification.find(class_="item-subtitle").string or ""

			certifications_info.append(linkedin_certifications(title, subtitle))

	x.linkedin_infos.append(linkedin_info(topcard_info, experience_info, schools_info, awards_info, languages_info, certifications_info))

