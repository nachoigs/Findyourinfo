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
        self.facebook_work = []
        self.facebook_studies = []
        type(self).counter += 1

    def __del__(self):
        type(self).counter -= 1
