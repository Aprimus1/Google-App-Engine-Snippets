from google.appengine.ext import ndb


class Company(ndb.Model):
    company_name = ndb.StringProperty()
    
class Job(ndb.Model):
    job_title = ndb.StringProperty()
    
    
    
# Put data in Datastore:
#------------------------------------------------------
class MainHandler(BaseHandler):
    def get(self):
        # ...

    def post(self):
        company_name = self.request.get('company_name')
        job_title = self.request.get('job_title')


        company = Company()
        company.company_name = company_name
        company.put()

        job = Job(parent=company.key)
        job.job_title = job_title

        job.put()
        self.redirect('/')
        
        
        
# Retrieve data from Datastore
#----------------------------------------------------------
class ResultHandler(BaseHandler):
    def get(self):
        companies_id = map(lambda key: key.id(), Company.query().fetch(keys_only=True))

        jobs = [Job.query(ancestor=ndb.Key(Company, element_id)).fetch() for element_id in companies_id]

        params = {'companies': [Company.get_by_id(comp_id) for comp_id in companies_id],
                  'jobs': jobs}

        return self.render_template('result.html', params=params)
        
        
""" Template result.html

{% extends 'base.html' %}

{% block content %}
{% for company, jobs in zip(companies, jobs_list) %}
    <li>{{ company.company_name }}</li>
    {% for job in jobs %}
        {{ job.job_title }}
    {% endfor %}
{% endfor %}
{% endblock content %}

"""
