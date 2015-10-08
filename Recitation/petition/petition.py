import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

HEADER = """
	<html>
		<head>
			<link href="css/style.css">
			<script href="js/app.js"></script>
			<title> Crazy Todo List </title>
		</head>
		<body>
			<h1> Sign if you want :D </h1>
			<form action="/" method="post">				
				<input type="submit" name="sign">
			</form>

"""

FOOTER = """
		</body>
	</html>
"""

def get_key():
    return ndb.Key('petition', 'signatures')
    
class Signature(ndb.Model):
    user = ndb.UserProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.write(HEADER)

			query = Signature.query(ancestor=get_key())
			signatures =query.fetch();

			self.response.write("<ul>")
			for sign in signatures:
				self.response.write("<li>"+sign.user.nickname()+"</li>")
			self.response.write("</ul>")

			self.response.write(FOOTER)
		else:
			self.redirect(users.create_login_url(self.request.uri))

	def post(self):
		
		s = Signature(parent=get_key())
		s.user = users.get_current_user()
		s.put()
		self.redirect("/")


application = webapp2.WSGIApplication([
	('/',MainPage),
], debug=True)