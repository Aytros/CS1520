# import the webapp2 module so we can get access to the framework
import webapp2

# import the db module from appengine
from google.appengine.ext import db

# we'll create a simple Model class here.
class PostName(db.Model) :  
  # this model class has just one property - myname
  myname = db.StringProperty()

# This class is a request handler.
class MainPage(webapp2.RequestHandler) :
  # implementing the get method here allows this class to handle GET requests.
  def get(self) :
    # we don't need to set the Content-Type header here, it's just done as an 
    # example.
    # webapp2 provides us with this response object - we can use it to create 
    # our HTTP response.
    self.response.headers['Content-Type'] = 'text/html'
    
    # we'll set up a simple response here.
    myresponse = '<html><body>'
    
    # we're going to iterate over all of our PostName objects and include it in 
    # our response
    for p in PostName.all() :
      myresponse += p.myname + '<br>'

    # we'll complete the response here by including a form, a simple text 
    # field, and a button to submit the form.
    # the "input" tags here just identify form fields - the type="input" for
    # the text box, and the type="submit" for the submit button.
    myresponse += '''<form method="post" action="dopost">
<input type="text" name="name">
<input type="submit">
</form>
</body>
</html>
'''
    
    # we write out our response string here using the built-in capabilities 
    # of the response object.
    self.response.out.write(myresponse)

# we use this second request handler to serve our form's post requests.
class PostHandler(webapp2.RequestHandler) :
  # note that this is handling the "post" request
  def post(self) :
    
    # we're able to just retrieve parameters from the request (note name="name" 
    # in the "input" tag above) using the request.get method
    name = self.request.get('name')
    
    p = PostName(myname=name)
    
    # because our "PostName" class inherits from db.Model, we can simply save 
    # it to the data store.
    p.put()
    self.response.out.write('<html><body>Hello, ' + name + '</body></html>')
    

# we use this to set up the AppEngine app - each of the mappings identifies a 
# URL and the webapp2.RequestHandler class that handles requests to that URL
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/dopost', PostHandler)
], debug=True)