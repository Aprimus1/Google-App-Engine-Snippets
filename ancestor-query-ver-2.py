#-- Model--
class Job(ndb.Model):
    job_title = ndb.StringProperty()
    
#-- Put data in datastore--

class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("hello.html", params=params)

    def post(self):
        user = users.get_current_user()

        job_title = self.request.get('job_title')

        job = Job(parent=ndb.Key('User', user.nickname()))
        job.job_title = job_title

        job.put()

        self.redirect('/')
        
  #-- retrieve data from datastore--
  
  class ResultHandler(BaseHandler):

    def get(self):
    
        jobs = Job.query().fetch()

        params = {'jobs': jobs}

        return self.render_template('result.html', params=params)
        
#--- html results.html----------------

{% block content %}
{% for job in jobs %}
    <li>{{ job.job_title }} -- Author: {{ job.key.parent().id() }}</li>
{% endfor %}
{% endblock content %}
