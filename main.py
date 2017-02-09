import os
import webapp2
from webapp2_extras.appengine.users import login_required
from google.appengine.api import users
import jinja2
from models import Message


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=False)
jinja_env.globals['url_for'] = webapp2.uri_for

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))




class MainHandler(BaseHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        if user is not None:

            logout_url = users.create_logout_url(self.request.uri)

            template_context = {'message': "I'm here",

                                'logout_url': logout_url,}
        else:
            login_url = users.create_login_url(self.request.uri)
            template_context = {'login_url': login_url}
        return self.render_template('hello.html', template_context)

class ResultHandler(BaseHandler):
    @login_required
    def get(self):

        return self.render_template('result.html')

    def post(self):
        message = Message()
        if users.get_current_user():
            message.author = users.get_current_user()
        message.title = self.request.get('title')
        message.content = self.request.get('vnos')
        message.put()
        self.redirect('message_list')

class ProductHandler(BaseHandler):
    def get(self, product_id):
        self.write('The product id is {}'.format(product_id))

class MessageLists(BaseHandler):
    def get(self):
        list = Message.query().fetch()
        template_context = {
            'list': list
        }
        return self.render_template('list.html', template_context)

class SingleMessage(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        template_context = {
            'message': message,
        }
        return self.render_template('single_message.html', template_context)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler, name='result'),
    webapp2.Route('/message_list', handler=MessageLists, name='message_list'),
    webapp2.Route('/message/<message_id:\d+>', handler=SingleMessage, name='single_message'),
], debug=True)
