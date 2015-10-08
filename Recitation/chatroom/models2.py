import cgi
import urllib
from google.appengine.ext import ndb
import webapp2
# defining type Comment
class UserInfo(ndb.Model):
	user = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

    #  defining type 
class Post(ndb.Model):
	content = ndb.StringProperty()	# a string attribute
	user = ndb.StringProperty();
	date = ndb.DateTimeProperty(auto_now_add=True) # a a date time attribute set to be initialized by the server automatically so I won't have to set value myself