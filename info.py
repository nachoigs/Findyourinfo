class info:
    counter = 0

    def __init__(self, domain, link, pagetext, urlimg):
        self.domain = domain
        self.link = link
        self.pagetext = pagetext
        self.urlimg = urlimg
        self.twitter_name = ''
        self.twitter_age = ''
        self.twitter_location = ''
        self.twitter_birth = ''
        self.twitter_bio = ''
        self.facebook_location = ''
        self.facebook_birthloc = ''
        self.facebook_work = []
        self.facebook_infos = []
        self.linkedin_infos = []
        type(self).counter += 1

    def __del__(self):
        type(self).counter -= 1

class linkedin_info:
    def __init__(self, topcard='', experience='', schools='', awards='', languages='', certifications=''):
        self.topcard = topcard
        self.experience = experience
        self.schools = schools
        self.awards = awards
        self.languages = languages
        self.certifications = certifications

class linkedin_topcard:
    def __init__(self, picture='', name='', headline='', location='', sector=''):
        self.picture = picture
        self.name = name
        self.headline = headline
        self.location = location
        self.sector = sector

class linkedin_experience:
    def __init__(self, title='', subtitle='', date_range='', location=''):
        self.title = title
        self.subtitle = subtitle
        self.date_range = date_range
        self.location = location

class linkedin_school:
    def __init__(self, name='', studies='', period='', description=''):
        self.name = name
        self.studies = studies
        self.period = period
        self.description = description

class linkedin_awards:
    def __init__(self, title='', subtitle='', description=' '):
        self.title = title
        self.subtitle = subtitle
        self.description = description

class linkedin_languages:
    def __init__(self, language='', proficiency=''):
        self.language = language
        self.proficiency = proficiency

class linkedin_certifications:
    def __init__(self, title='', subtitle=''):
        self.title = title
        self.subtitle = subtitle
