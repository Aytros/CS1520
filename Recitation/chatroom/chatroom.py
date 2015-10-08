import cgi
import urllib
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
import json

import webapp2


def get_key():
    return ndb.ro

# defining type Comment
class UserInfo(ndb.Model):
	user = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

    #  defining type 
class Post(ndb.Model):
	content = ndb.StringProperty()	# a string attribute
	user = ndb.StringProperty();
	date = ndb.DateTimeProperty(auto_now_add=True) # a a date time attribute set to be initialized by the server automatically so I won't have to set value myself


# my handler for the main page. The only page that shows content
class MainPage(webapp2.RequestHandler):
	
	def registerUser(self):
		user = users.get_current_user()
		userFetched=UserInfo.query(UserInfo.user==user.nickname()).fetch(1)	
		if  len(userFetched) == 0:
			u = UserInfo()
			u.user = user.nickname()
			u.date=datetime.now()
			u.put()

	def get(self):
		user = users.get_current_user()

		if user:
			self.registerUser()
		# 	# creating the path for the tempalte
			path = os.path.dirname(__file__)+ '/templates/index.html'		
		# 	# defining a dictionary to pass variables to tempalte
			template_values = {}	
		# 	# reading and rendering the template
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect(users.create_login_url('/'))

	



# # handler for the post Post request 
class LogoutHandler(webapp2.RequestHandler):

	def get(self):		
		user = users.get_current_user()
		userFetched=UserInfo.query(UserInfo.user==user.nickname()).fetch(1)
		if  len(userFetched)>0:
			userFetched[0].key.delete()
			# redirecting to google logout page
		self.redirect(users.create_logout_url("/"))


		



# handler for post Comment request
class ChatHandler(webapp2.RequestHandler):
	def get(self):
		lasttime = self.request.get('lasttime')
		if not lasttime=="0":
			lastdate=datetime.strptime(lasttime, '%m-%d-%Y_%I:%M:%S')
			posts =Post.query(Post.date > lastdate).order(Post.date).fetch()
		else:
			posts =Post.query().order(Post.date).fetch()
		data = {}
		data['time'] = datetime.now().strftime('%m-%d-%Y_%I:%M:%S');
		postlist = []
		for post in posts:
			postlist= postlist+ [{'user':post.user,'content':post.content}]
		data['posts'] = postlist			
		self.response.write(json.dumps(data));	
	# its a post request
	def post(self):
		content = self.request.get('postcontent')
		post = Post()
		post.content = content
		user = users.get_current_user()
		post.user=user.nickname()
		post.put()

		self.updateUser()
		self.redirect("/")

	def updateUser(self):
		user = users.get_current_user()
		userFetched=UserInfo.query(UserInfo.user==user.nickname()).fetch(1)
		if  len(userFetched)>0:
			userFetched[0].date = datetime.now()
			userFetched[0].put()

class TimeHandler(webapp2.RequestHandler):
	
	def get(self):
		self.response.write(datetime.now().strftime('%m-%d-%Y_%I:%M:%S'))

class UsersHandler(webapp2.RequestHandler):
	
	def get(self):
		
		users = UserInfo.query().fetch()
		tmp=""
		for user in users:
			tmp+='<li class="useritem"><img src="'+self.getimage(user)+'" >'+user.user+'</li>\n'

		self.response.write(tmp)

	def getimage(self,user):
		current = datetime.now()
		last = user.date	
		dif = (current-last).total_seconds()
		
		if dif > 3*60:
			return "img/offline.png"
		if dif > 1*60:
			return "img/inactive.png"
		return "img/online.png"
	



# adding three handlers to the application for each request address
application = webapp2.WSGIApplication([
	('/',MainPage),
	('/logout',LogoutHandler),
	('/chat',ChatHandler),
	('/time',TimeHandler),
	('/users',UsersHandler),

], debug=True)