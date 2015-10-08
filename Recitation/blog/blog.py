import cgi
import urllib
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2


# just returning a simple key. This type of key definition is not appropriate however, its a good practice. Will talk about this next recitation.
def get_key():
    return ndb.Key('blog', 'posts')

# defining type Comment
class Comment(ndb.Model):
	content = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

    #  defining type 
class Post(ndb.Model):
	title = ndb.StringProperty() # a string attribute
	content = ndb.StringProperty()	# a string attribute
	date = ndb.DateTimeProperty(auto_now_add=True) # a a date time attribute set to be initialized by the server automatically so I won't have to set value myself
	comments = ndb.StructuredProperty(Comment, repeated=True) # repeated means that I'm keeping an array. Comment is the type of that array


# my handler for the main page. The only page that shows content
class MainPage(webapp2.RequestHandler):
	def get(self):
		# a query to get the list of posts ordered descending based on their date. Note that I'm getting posts that are withing/(jave subkey) ("blog","post")
		query = Post.query(ancestor=get_key()).order(-Post.date)
		# fetching results
		posts = query.fetch()
		# creating the path for the tempalte
		path = os.path.dirname(__file__)+ '/templates/index.html'
		
		# adding post keys to the objects to use in the tempalte
		for post in posts:
			post.k = post.key.urlsafe()
		# defining a dictionary to pass variables to tempalte
		template_values = {
			"posts": posts,
		}	
		# reading and rendering the template
		self.response.out.write(template.render(path, template_values))


# handler for the post Post request 
class PostHandler(webapp2.RequestHandler):

	def post(self):		
		# reading the content of post
		content = self.request.get('content')
		# creating an instance of Post
		post = Post(parent=get_key())
		# reading and setting value of title
		post.title = self.request.get('title')
		# setting value of content
		post.content = content
		# setting a new emtpy array for the comments attribute (no comments yet for this post)
		post.comments = []
		# calling put to store post in database
		post.put()
		# redirecting to main page to show posts
		self.redirect("/")



# handler for post Comment request
class CommentHandler(webapp2.RequestHandler):
	# its a post request
	def post(self):
		# reading key from the request. The key is in the request within a hidden input tag for each comment for of each posts div tag.
		# I'm doing this because I need to tell the server somehow which post am I posting a new comment for. 
		pkey = self.request.get('post')
		# fetching a post from db using its key
		post = ndb.Key(urlsafe=pkey).get()
		#  creating a new comment
		cmt = Comment()
		# reading content of the comment
		cmt.content = self.request.get('content')
		# appending the new comment to the lsit of the post
		post.comments.append(cmt)
		# updating post by repushing it 
		post.put()
		# redirecting to the main page
		self.redirect("/")
		


# adding three handlers to the application for each request address
application = webapp2.WSGIApplication([
	('/',MainPage),
	('/post',PostHandler),
	('/comment',CommentHandler),
], debug=True)