import os
import webapp2
from google.appengine.ext.webapp import template

# This function will just render our template into our HTML.
def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
class MainPage(webapp2.RequestHandler) :
  def get(self) :
    render_template(self, 'index.html', {})
    
    
class TestJson(webapp2.RequestHandler) :
  def post(self) :
    render_template(self, 'test.json', {})
    
    
class TestXml(webapp2.RequestHandler) :
  def get(self) :
    self.post()
    
  def post(self) :
    self.response.headers['Content-Type'] = 'text/xml'
    render_template(self, 'myxml.xml', {})


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/getjson', TestJson),
  ('/getxml', TestXml)
])







