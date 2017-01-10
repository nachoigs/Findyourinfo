# Findyourinfo

from flask import Flask, url_for, render_template, request
import requests  #, sys
import json
import re
from info import *
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tinfoleak as tinfoleak
from flask_sqlalchemy import SQLAlchemy



# sys.path.append('env/Lib/)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\nacho_000\\Desktop\\Pagina con FLASK\\Database\\testdb.db' # Change for whatever path you want

db = SQLAlchemy(app)

@app.route('/')
def index():
	searchterm = request.args.get("search", "")

	if (searchterm):
		infolist = search(searchterm)

		return render_template("index.html", infolist=infolist)

	return render_template("index.html")

@app.route('/tinfoleak')
def tinfoleakfunction():
	# Show Twitter info using TinfoLeak

	user = request.args.get('user', '')

	if (user == ''):
		return

	templatedata = tinfoleak.main([user, "-i"])

	#tinfoleak.main([user, "-i"])

	return render_template("tinfoleak.html", **templatedata)

## FUNCTIONS ##

def search(searchterm):
	infolist = []

	google_search(searchterm, infolist)

	# bing_search(searchterm, infolist)

	firstterm = searchterm.split()[0]
	for x in infolist:
		if re.search("www.facebook.com/[\w\W]*"+firstterm, x.link, re.IGNORECASE):
			linkdb = relevants_links(searchterm, x.link, "Facebook" )
			db.session.add(linkdb)
			db.session.commit()
			facebook_search(x, x.link)

		if re.search('twitter.com/'+searchterm, x.link):
			linkdb = relevants_links(searchterm, x.link, "Twitter" )
			db.session.add(linkdb)
			db.session.commit()
			twitter_search(x, x.link)

		if re.search("linkedin.com/in/[\w\W]*"+firstterm, x.link, re.IGNORECASE):
			linkdb = relevants_links(searchterm, x.link, "Linkedin" )
			db.session.add(linkdb)
			db.session.commit()
			linkedin_search(x, x.link)

	return infolist


def google_search(searchterm, infolist):
	search = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAivBHuR6rQLfFFzYZPsFKoW6NEu2uf178&cx=014899431841328080285:dgyb9nv0qd0&exactTerms={searchterm}&q="
	search = search.format(searchterm=searchterm)
	google = requests.get(search)

	googlejson = google.json()

	for x in googlejson['items']:
		link = x['link']
		linkparsed = urlparse(link)
		schemenetloc = linkparsed.scheme + "://" + linkparsed.netloc
		text = x['snippet']

		infolist.append(info(schemenetloc, link, text, ''))

	return

def bing_search(searchterm, infolist):
	bingheader = {'Ocp-Apim-Subscription-Key': '9ed77606931144cca303b3bbffc23c63'}
	binglink = "https://api.cognitive.microsoft.com/bing/v5.0/search?q=%%2B{searchterm}"
	
	searchterm = searchterm.replace(" ", "+")
	binglink = binglink.format(searchterm=searchterm)
	bing = requests.get(binglink, headers=bingheader)
	bingprejson = bing.content.decode('utf-8')
	bingjson = json.loads(bingprejson)
	infolist = []
	print(bingjson)

	for x in bingjson['webPages']['value']:
		link = x['displayUrl']
		linkparsed = urlparse(link)
		schemenetloc = linkparsed.scheme + "://" + linkparsed.netloc
		text = x['snippet']
		infolist.append(info(schemenetloc, link, text, ''))


def twitter_search(x, link):
	soup = BeautifulSoup(requests.get(link).content, 'html5lib')
	profilecard = soup.find(class_="ProfileHeaderCard")

	profilecard_name = profilecard.find(class_="ProfileHeaderCard-name")

	twitter_urlimg = ''
	twitter_name = ''
	twitter_user = ''
	twitter_bio = ''
	twitter_location = ''
	twitter_birth = ''
	twitter_joindate = ''

	profileavatar = soup.find(class_="ProfileAvatar")

	if profileavatar:
		twitter_urlimg = profileavatar.find(class_="ProfileAvatar-image")['src']

	if profilecard_name:
		twitter_name = profilecard_name.a.string

	profilecard_user = profilecard.find(class_="ProfileHeaderCard-screenname")

	if profilecard_user:
		twitter_user = ''.join(profilecard_user.a.find_all(string=True))

	profilecard_bio = profilecard.find(class_="ProfileHeaderCard-bio u-dir")

	if profilecard_bio:
		twitter_bio = ''.join(profilecard_bio.find_all(string=True))

	profilecard_location = profilecard.find(class_="ProfileHeaderCard-location")

	if profilecard_location:
		twitter_location = profilecard_location.find(class_="ProfileHeaderCard-locationText").string

	profilecard_birth = profilecard.find(class_="ProfileHeaderCard-birthdate")

	if profilecard_birth:
		twitter_birth = profilecard_birth.find(class_="ProfileHeaderCard-birthdateText").string

	profilecard_joindate = profilecard.find(class_="ProfileHeaderCard-joinDate")

	if profilecard_joindate:
		twitter_joindate = profilecard_joindate.find(class_="ProfileHeaderCard-joinDateText")['title']

	x.twitter_infos.append(twitter_info(twitter_urlimg, twitter_name, twitter_user, twitter_joindate, twitter_location, twitter_birth, twitter_bio))


def facebook_search(x, link):
	soup = BeautifulSoup(requests.get(x.link).content, 'html5lib')

	facebook_bio = ""
	facebook_name = ""
	facebook_studies = []
	facebook_works = []
	facebook_urlimg = ""
	facebook_locations = []

	ProfileCover = soup.find(id="fbProfileCover")

	if ProfileCover:
		facebook_name = ProfileCover.find(id="fb-timeline-cover-name").string

	ProfileAvatar = soup.find(class_="profilePicThumb")

	if ProfileAvatar:

		facebook_urlimg = soup.find(class_="profilePic img")['src']

	page_eduwork = soup.find(id="pagelet_eduwork")

	if page_eduwork:

		page_work = page_eduwork.find(attrs={"data-pnref": "work"})

		if page_work:
			works = page_work.find_all(class_="fbEditProfileViewExperience")
			for work in works:
				title = page_work.find(class_="_2lzr _50f5 _50f7").a.string
				subtitlediv = page_work.find(class_="fsm fwn fcg")
				subtitle = ""
				if subtitlediv:
					subtitle = ' '.join(subtitlediv.find_all(string=True))
				descriptiondiv = page_work.find(class_="_3-8w _50f8")
				description = ""
				if descriptiondiv:
					description = description.string
				facebook_works.append(facebook_work(title, subtitle, description))

		page_edu = page_eduwork.find(attrs={"data-pnref": "edu"})

		if page_edu:
			studies = page_edu.find_all(class_="fbEditProfileViewExperience")
			for study in studies:
				school = study.find(class_="_2lzr _50f5 _50f7").a.string
				school_location = study.find(class_="_173e _50f8 _50f3").div.string
				facebook_studies.append(facebook_study(school, school_location))

	page_hometown = soup.find(id="pagelet_hometown")

	if page_hometown:

		page_cities = page_hometown.find_all(class_="_3pw9 _2pi4 _2ge8")

		for page_city in page_cities:

			location = page_city.find(class_="_50f5 _50f7").a.string
			state = page_city.find(class_="fsm fwn fcg").string

			facebook_locations.append(facebook_location(location, state))

		page_cities2 = page_hometown.find_all(class_="_43c8 _5f6p")

		for page_city in page_cities2:

			location = page_city.find(class_="_50f5 _50f7").a.string
			state = page_city.find(class_="fsm fwn fcg").string

			facebook_locations.append(facebook_location(location, state))

	page_bio = soup.find(id="pagelet_bio")

	if page_bio:
		facebook_bio = page_bio.find(class_="_c24 _50f4").string

	x.facebook_infos.append(facebook_info(facebook_urlimg, facebook_name, facebook_locations, facebook_studies, facebook_works, facebook_bio))


def linkedin_search(x, link):
	headers = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)'}
	r = requests.get(link, headers=headers)
	soup = BeautifulSoup(r.content, 'html5lib')

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
			description = position.find(class_="description").string or ""
			experience_info.append(linkedin_experience(title, subtitle, date_range, location, description))


	education = profile.find(id="education")
	schools_info = []
	if education:
		schools = education.find_all(class_="school")
		for school in schools:
			title = school.find(class_="item-title").string or ""
			subtitle = school.find(class_="item-subtitle").find(class_="original translation").string or ""
			period = "".join(school.find(class_="date-range").find_all(string=True)) or ""
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

# Models

class relevants_links(db.Model):

	id = db.Column('id', db.Integer, primary_key = True)
	query = db.Column(db.String(100))
	link = db.Column(db.String(100))
	service = db.Column(db.String(50))

	def __init__(self, query, link, service):
		self.query = query
		self.link = link
		self.service = service

db.create_all()