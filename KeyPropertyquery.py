from google.appengine.ext import ndb


class Company(ndb.Model):
    company_name = ndb.StringProperty()
    
class Job(ndb.Model):
    job_name = ndb.StringProperty()
    job_description = ndb.TextProperty()
    job_requirement = ndb.StringProperty()
    company_key = ndb.KeyProperty(kind=Company)





class MainHandler(BaseHandler):
    def get(self):
        params = {}

        jobs = Job.query().fetch()

        for job in jobs:
            params['job'] = job
            params['company'] = job.company_key.get()

        return self.render_template("main.html", params=params)
