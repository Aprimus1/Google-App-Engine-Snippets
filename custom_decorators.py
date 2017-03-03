# Login Required

from google.appengine.api import users

def login_required(handler):
    def wrapper(self,*args, **kwargs):
        user = users.get_current_user()

        if user:
            return handler(self,*args, **kwargs)
        else:
            return self.write('Please Login first')
    return wrapper
