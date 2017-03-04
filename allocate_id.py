class MainHandler(BaseHandler):
    def get(self):

        params = {}

        user = users.get_current_user()

        if user is not None:
            logout_url = users.create_logout_url(self.request.uri)
            params['user'] = user.nickname()
            params['logout_url'] = logout_url

        else:
            login_url = users.create_login_url(self.request.uri)
            params['login_url'] = login_url

        return self.render_template("hello.html", params=params)

    def post(self):
        company_name = self.request.get('company_name')
        job_title = self.request.get('job_title')

        ids = Company.allocate_ids(size=1)
        company = Company(id=ids[0])
        company.company_name = company_name



        job = Job()
        job.job_title = job_title
        job.company_key = company.key


        ndb.put_multi([company, job])


        self.redirect('/')
