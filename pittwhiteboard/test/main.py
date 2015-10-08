#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div><textarea name="content" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name:
      <input value="%s" name="guestbook_name">
      <input type="submit" value="switch">
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

#This should ensure they're all in the same entity group
#...I have no idea what that means
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	#This has something to do with datastore keys
	return ndb.Key('Guestbook', guestbook_name)

# we'll create a simple Model class here.
class Greeting(ndb.Model) :  
  author = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  #auto_now_add makes the time auto-add to the present time
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name',
        					DEFAULT_GUESTBOOK_NAME)

        greetings_query = Greeting.query(
        	ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        for greeting in greetings:
        	if greeting.author:
        		self.response.write(
        			'<b>%s</b> wrote: ' %greeting.author.nickname())
        	else:
        		self.response.write('Anonymous wrote:')
        	self.response.write('<blockquote>%s</blockquote>' %
        							cgi.escape(greeting.content)) 
        if users.get_current_user():
        	url = users.create_logout_url(self.request.uri)
        	url_linktext = 'Logout'
        else:
        	url = users.create_login_url(self.request.uri)
        	url_linktext = 'Login'

        sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE %(sign_query_params, cgi.escape(guestbook_name),
        					url, url_linktext))

#This another page, so we'll need to add it to the app
class Guestbook(webapp2.RequestHandler):
	def post(self):
		#Should grab the default guestbook
		guestbook_name = self.request.get('guestbook_name',
								DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		#If we're not anonymous, we want to store an author
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = self.request.get('content')
		#Also, because date is not set, it's automatically the present time
		greeting.put()	#add it to the base

		query_params = {'guestbook_name' : guestbook_name}
		self.redirect('/?' + urllib.urlencode(query_params))



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign', Guestbook),
], debug=True)
