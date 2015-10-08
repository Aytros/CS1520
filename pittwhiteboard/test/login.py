import sys
import webapp2
from google.appengine.ext import ndb
from DB_Methods_And_Classes import *

DEFAULT_UNI_NAME = 'University of Pittsburgh'
def uni_key(uni_name = DEFAULT_UNI_NAME) :
	return ndb.Key('University', uni_name)



#This will get the base login page, we should just need to make sure 
#that your name and password combo match
class MainHandler(webapp2.RequestHandler):
	def get(self):
		result = LOGIN_PAGE_HTML_START
		user_query = User.query(
		 	ancestor=uni_key(DEFAULT_UNI_NAME)).order(-User.date)
		list_of_names = user_query.fetch(10)
		for users in list_of_names:
			u_key = users.key.integer_id()
			result += '<b>' + users.login + '</b><br>'
		result += LOGIN_PAGE_HTML_END
		self.response.write(result)


#This should write all 
class Register(webapp2.RequestHandler):
	def post(self):
		db = DB_Methods()
		password = self.request.get('pass')
		email = self.request.get('email')
		first = self.request.get('first')
		last =  self.request.get('last')
		university = self.request.get('uni')
		db.register_user(password,email,first,last,university)
		#go back to the default login page
		self.redirect('/')

class Login(webapp2.RequestHandler): 
	def post(self):
		#query and fetch the user
		enter_password = self.request.get('pwd')
		login_query = User.query(User.login == self.request.get('username'))
		meth = DB_Methods()
		are_we_good = meth.check_login(self.request.get('username'),self.request.get('pwd'))
		if are_we_good is 0 :
			self.response.write('''
					<script>
						alert("Password is incorrect!");
					</script>
				''')
			return
		else:
			user = meth.fetch_user_by_login(self.request.get('username'))
			self.response.write('''
					<script>
						alert("Password for %s was correct");
					</script>
				'''%self.request.get('username'))
		return






LOGIN_PAGE_HTML_START = """
<html>
<head>
	<script type="text/javascript">
		function toggle(id)
		{
			var e=document.getElementById(id);
			if (e.style.display=='')
				e.style.display='none';
			else
				e.style.display='';
		}
	</script>
	<title>CS1520: Group Project</title>
	<link rel="stylesheet" type="text/css" href="css/draft2style.css">
</head>
<body>
"""
LOGIN_PAGE_HTML_END = """
	<h1>CourseWeb 2.AWESOME!!</h1>
	<div id="signin">
		<a href="#" onclick="toggle('log')">Login</a>
		<div id="log" style="display:none">
			<form action="/login" method="post">
				Username: <input type="text" name="username"><br>
				Password: <input type="password" name="pwd"><br>
				<input type="submit" value="Login" name="sub">
			</form>
		</div><br>
		<a href="#" onclick="toggle('reg')">Register</a>
		<div id="reg" style="display:none">
			<form action="/register" method="post">
				First Name: <input type="text" name="first"><br>
				Last Name: <input type="text" name="last"><br>
				University: <input type="text" name="uni"><br>
				Email: <input type="text" name="email"><br>
				Password: <input type="text" name="pass"><br>
				<input type="submit" value="Register" name="regSub">
			</form>
		</div>
	</div>

</body>
</html>
"""


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', Register),
    ('/login', Login),
], debug=True)