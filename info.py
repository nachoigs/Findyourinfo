class info:
    counter = 0

    def __init__(self, domain, link, pagetext, urlimg):
        self.domain = domain
        self.link = link
        self.pagetext = pagetext
        self.urlimg = urlimg
        self.twitter_infos = []
        self.facebook_infos = []
        self.linkedin_infos = []
        type(self).counter += 1

    def __del__(self):
        type(self).counter -= 1

class twitter_info:
    def __init__(self, urlimg, name, user, joindate, location, birth, bio):
        self.type = "Twitter"
        self.urlimg = urlimg
        self.name = name
        self.user = user
        self.joindate = joindate
        self.location = location
        self.birth = birth
        self.bio = bio

class facebook_info:
    def __init__(self, urlimg, name, locations, studies, works, bio):
        self.type = "Facebook"
        self.name = name
        self.urlimg = urlimg
        self.locations = locations
        self.studies = studies
        self.works = works
        self.bio = bio

class facebook_work:
    def __init__(self, title, subtitle, description):
        self.title = title
        self.subtitle = subtitle
        self.description = description

class facebook_study:
    def __init__(self, school, school_location):
        self.school = school
        self.school_location = school_location

class facebook_location:
    def __init__(self, location, state):
        self.location = location
        self.state = state

class linkedin_info:
    def __init__(self, topcard, experiences, schools, awards, languages, certifications):
        self.type = "Linkedin"
        self.topcard = topcard
        self.experiences = experiences
        self.schools = schools
        self.awards = awards
        self.languages = languages
        self.certifications = certifications

class linkedin_topcard:
    def __init__(self, picture, name, headline, location, sector):
        self.picture = picture #
        self.name = name #
        self.headline = headline
        self.location = location
        self.sector = sector

class linkedin_experience:
    def __init__(self, title, subtitle, date_range, location, description):
        self.title = title
        self.subtitle = subtitle
        self.date_range = date_range
        self.location = location
        self.description = description

class linkedin_school:
    def __init__(self, name, study, period, description):
        self.name = name
        self.study = study
        self.period = period
        self.description = description

class linkedin_awards:
    def __init__(self, title, subtitle, description=' '):
        self.title = title
        self.subtitle = subtitle
        self.description = description

class linkedin_languages:
    def __init__(self, language, proficiency):
        self.language = language
        self.proficiency = proficiency

class linkedin_certifications:
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
