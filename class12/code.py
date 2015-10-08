import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

# We only need to create a db.Model class to save values to the datastore.
class MyAnswer(db.Model) :
  answer = db.StringProperty()
  correct = db.BooleanProperty()
  user = db.StringProperty()


def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
class MainPage(webapp2.RequestHandler) :
  def post(self) :
    answer = self.request.get('answer')
    correct = self.request.get('correct')
    
    # retrieving the current user is simple.
    user = users.get_current_user()
    
    # if this object is defined now, we can assume a valid user is signed in.
    if user :
      # we can populate this object...
      my_answer = MyAnswer()
      my_answer.answer = answer
      if correct == 'TRUE' :
        my_answer.correct = True
      else :
        my_answer.correct = False
      my_answer.user = user.email()
      
      # ... then save it to the datastore with the db.Model put() method.
      my_answer.put()
      
    self.response.out.write("everything worked out ok.")
      
  
  def get(self) :
  
    user = users.get_current_user()
  
    login_url = ''
    logout_url = ''
    
    email = ''
    name = ''
    
    if user :
      # it's easy to get basic details from our user, as well as a URL to sign out.
      # the parameter to the create_logout_url method just identifies where to redirect after logout.
      logout_url = users.create_logout_url('/')
      email = user.email()
      name = user.nickname()
    else :
      login_url = users.create_login_url('/')
    
    template_values = {
      'login' : login_url,
      'logout' : logout_url,
      'email' : email,
      'nickname' : name,
    }
  
    render_template(self, 'index.html', template_values)


# we'll use this to retrieve the values from the datastore.
class ShowAnswers(webapp2.RequestHandler) :
  def get(self) :
  
    answers = []
    
    # we'll get the current user... 
    user = users.get_current_user()
    if user :
    
      # ... then build a query based on that users's entries.
      q = MyAnswer.all()
      q.filter('user =', user.email())
      
      # we'll run the query and save all the results.
      for answer in q.run() :
        answers.append(answer)
      
    template_values = {
      'answers' : answers
    }
    render_template(self, 'answers.html', template_values)


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/answers', ShowAnswers)
])





