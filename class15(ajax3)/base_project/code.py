import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import random
import time

# This object will hold our simple notes.
class Note(db.Model) :
  id = db.StringProperty()
  title = db.StringProperty()
  text = db.StringProperty()
  

# This function will just render our template into our HTML.
def render_template(handler, templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

  
# Our main page doesn't do much except output our HTML.
class MainPage(webapp2.RequestHandler) :
  def get(self) :
    render_template(self, 'index.html', {})


# This will create JSON output that has all of our note titles and IDs.
class GetNoteTitles(webapp2.RequestHandler) :
  def get(self) :
    self.post()
    
  def post(self) :
    notes = list()
    
    q = Note.all()
    for note in q.run() :
      notes.append(note)
      
    values = {
      'notes' : notes
    }
    render_template(self, 'note_titles.json', values)
    

# This will return all of the note detail for a particular ID.
class GetNoteDetail(webapp2.RequestHandler) :
  def post(self) :
 
    notes = list()
    
    id = self.request.get('id')
    q = Note.all()
    q.filter('id =', id)
    for note in q.run(limit=1) :
      notes.append(note)
        
    values = {
      'notes' : notes
    }
    render_template(self, 'notes.json', values)


# This will save the note.  
class SaveNote(webapp2.RequestHandler) :
  def post(self) :
    
    id = self.request.get('id')
    title = self.request.get('title')
    text = self.request.get('text')
    
    # If we don't have a defined ID, we'll create one and save a new note.
    if (id == None or id == '') :
      note = Note()
      id = str(time.time()) + str(random.random())
      note.id = id
      note.text = text
      note.title = title
      note.put()
      
    # If we do have a defined ID, we'll update the existing note.
    else :
      q = Note.all()
      q.filter('id =', id)
      for note in q.run(limit=1) :
        note.title = title
        note.text = text
        note.put()
        
    # We don't have to use a template to output JSON; we can just do it inline.
    # Note that we're returning the ID here, in case this was a "create" operation - 
    # Our JavaScript will be able to identify the newly created ID.
    self.response.out.write('{"result":"OK","id":"' + id + '"}')
    

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/titles', GetNoteTitles),
  ('/detail', GetNoteDetail),
  ('/save', SaveNote)
])







