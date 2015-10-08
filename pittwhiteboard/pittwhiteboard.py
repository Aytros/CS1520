import webapp2
import datetime
import json
from DB_Methods_And_Classes import *
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from webapp2_extras import sessions

db = DB_Methods()
assignment_types = [
        {
        'id' : 1234,
        'name' : 'Exams',
        'quantity' : 2,
        'percent_of_total' : 20
        },
        {
        'id' : 3456,
        'name' : 'Projects',
        'quantity' : 5,
        'percent_of_total' : 8
        },
        {
        'id' : 4567,
        'name' : 'Quiz',
        'quantity' : 2,
        'percent_of_total' : 5
        },
        {
        'id' : 5678,
        'name' : 'Participation',
        'quantity' : 1,
        'percent_of_total' : 10
        }
    ]

class BaseHandler(webapp2.RequestHandler):
  def dispatch(self):
    self.session_store = sessions.get_store(request=self.request)
    try:
      webapp2.RequestHandler.dispatch(self)
    finally:
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session(self):
    return self.session_store.get_session()

class LoginHandler(BaseHandler):
  def get(self):
    path = 'templates/draft2.html'
    self.response.out.write(template.render(path, None))

  def post(self):
    if self.request.get('formId')=='userLog':
        uname=self.request.get('username')
        pwd=self.request.get('pwd')
        if db.check_login(uname, pwd)==1:
            self.session['uid'] = uname
            self.redirect('/userpage.html')
        else:
            self.response.out.write('''<script>alert("Username/Password combo is incorrect.  If you are not a member please register.");</script>''')
            self.response.out.write(template.render('templates/draft2.html', None))
    if self.request.get('formId')=='userReg':
        fname=self.request.get('first')
        lname=self.request.get('last')
        pword=self.request.get('pass')
        uni=self.request.get('uni')
        email=self.request.get('studId')
        regname=email.split('@')[0]

        if db.does_user_exist(regname):
            self.response.out.write('''<script>alert("Username is already taken.  PLease choose another.");</script>''')
            self.response.out.write(template.render('templates/draft2.html', None))
        else:
            db.register_user(pword, email, fname, lname, uni)
            self.session['uid'] = regname
            self.redirect('/userpage.html')

class AccountHandler(BaseHandler):
    def get(self):
        path = 'templates/accountinfo.html'
        user = db.fetch_user_by_login(self.session['uid'])
        user_id = user.key.integer_id()

        template_values={
            'user' : db.fetch_user_by_login(self.session['uid']),
            'courses' : AccountHandler.get_courses(self,user_id)
        }
        self.response.out.write(template.render(path, template_values))

    def get_courses(self, user_id) :
        formatted_courses = []
        courses = db.get_courses_for_user(user_id)
        for c in courses:
            url = '/coursepage.html?courseid='+ str(c.key.integer_id())
            formatted_c = {
                'url' : url,
                'number' : c.number,
                'title' : c.name,
                'professor' : c.professor_name
            }
            formatted_courses.append(formatted_c)
        return formatted_courses

    def post(self):
        user = db.fetch_user_by_login(self.session['uid'])
        user_id = user.key.integer_id()

        template_values={
            'user' : db.fetch_user_by_login(self.session['uid']),
            'courses' : AccountHandler.get_courses(self,user_id)
        }

        if self.request.get('formId')=='infoblock':
            fname=self.request.get('first')
            lname=self.request.get('last')
            uni=self.request.get('uni')
            db.update_user(user_id, user.password, user.email, fname, lname, uni)
            template_values={
                'user' : db.fetch_user_by_login(self.session['uid'])
            }
            self.response.out.write(template.render('templates/accountinfo.html', template_values))
            #self.redirect('/accountinfo.html')

        if self.request.get('formId')=='mailblock':
            currmail=self.request.get('currmail')
            newmail=self.request.get('newmail')
            conmail=self.request.get('conmail')
            
            if (newmail=="") or (conmail==""):
                self.response.out.write('''<script>alert("Required fields missing")</script>''')
                self.redirect('/accountinfo.html')
            else:
                if newmail==conmail:
                    db.update_user(user_id, user.password, newmail, user.first, user.last, user.university)
                    template_values={
                        'user' : db.fetch_user_by_login(self.session['uid'])
                    }
                    self.response.out.write(template.render('templates/accountinfo.html', template_values))
                else:
                    self.response.out.write('''<script>alert("New email and confirmation do not match!")</script>''')
                    self.redirect('/accountinfo.html')
            #self.redirect('/accountinfo.html')

        if self.request.get('formId')=='passblock':
            currpass=self.request.get('currpass')
            newpass=self.request.get('newpass')
            conpass=self.request.get('conpass')

            if (newpass=="") or (conpass==""):
                self.response.out.write('''<script>alert("Required fields missing")</script>''')
                self.redirect('/accountinfo.html')
            else:
                if newpass==conpass:
                    db.update_user(user_id, newpass, user.email, user.first, user.last, user.university)
                    template_values={
                        'user' : db.fetch_user_by_login(self.session['uid'])
                    }
                    self.response.out.write(template.render('templates/accountinfo.html', template_values))
                else:
                    self.response.out.write('''<script>alert("New password and confirmation do not match!")</script>''')
                    self.redirect('accountinfo.html')
            #self.redirect('/accountinfo.html')


class UserPageHandler(BaseHandler) :
	def get_assignments(self, user_id) :
		formatted_assignments = []
		assignments = db.get_all_assignments_for_user(user_id)
		for a in assignments:
			course = db.get_course_by_id(a.course_id)
			
			formatted_a = {
				'title' : a.name,
				'course' : course.number,
				'year' : a.due_date.year,
                'month': a.due_date.month,
                'day'  : a.due_date.day,
				'details' : a.details
			}
			formatted_assignments.append(formatted_a)
		return formatted_assignments
	
	def get_courses(self, user_id) :
		formatted_courses = []
		courses = db.get_courses_for_user(user_id)
		for c in courses:
			url = '/coursepage.html?courseid='+ str(c.key.integer_id())
			formatted_c = {
				'url' : url,
				'number' : c.number,
				'title' : c.name,
				'professor' : c.professor_name
			}
			formatted_courses.append(formatted_c)
		return formatted_courses
	
	def get(self):
		path = 'templates/userpage.html'
		user = db.fetch_user_by_login(self.session['uid'])
		if user == None:
			self.redirect('/userpage.html')
		else:
			user_id = user.key.integer_id()
		
			template_values = {
				'user' : db.fetch_user_by_id(user_id),
				'courses' : UserPageHandler.get_courses(self,user_id)
			}
			self.response.out.write(template.render(path, template_values))
	
	def post(self):
		if self.request.get('submit'):
			coursenum = self.request.get('classnumber')
			coursename = self.request.get('classname')
			courselocation = self.request.get('courselocation')
			if courselocation == "":
				courselocation = None
			coursetime = self.request.get('coursetime')
			if coursetime == "":
				coursetime = None
			reclocation = self.request.get('reclocation')
			if reclocation == "":
				reclocation = None
			rectime = self.request.get('rectime')
			if rectime == "":
				rectime = None
			
			proffirst = self.request.get('prof-fname')
			proflast = self.request.get('prof-lname')
			profname = proffirst + ' ' + proflast
			profoffice = self.request.get('prof-office')
			if profoffice == "":
				profoffice = None
			profofficehour = self.request.get('prof-office-hours')
			if profofficehour == "":
				profofficehour = None
			profemail = self.request.get('prof-email')
			if profemail == "":
				profemail = None
			
			tafirst = self.request.get('ta-fname')
			if tafirst == "":
				tafirst = None
			talast = self.request.get('ta-lname')
			if talast == "":
				talast = None
			if (tafirst == None) and (talast == None):
				taname = None
			elif (tafirst == None) and (talast != None):
				taname = talast
			elif (tafirst != None) and (talast == None):
				taname = tafirst
			else:
				taname = tafirst + ' ' + talast
			taoffice = self.request.get('ta-office')
			if taoffice == "":
				taoffice = None
			taofficehour = self.request.get('ta-office-hours')
			if taofficehour == "":
				taofficehour = None
			taemail = self.request.get('ta-email')
			if taemail == "":
				taemail = None
			
			user_id = db.fetch_user_by_login(self.session['uid']).key.integer_id()
			new = db.create_course(user_id, coursename, coursenum, courselocation, coursetime, reclocation, rectime, profname, profemail, profoffice, profofficehour, taname, taemail, taoffice, taofficehour, None, None, None)
			new_course=new.get()
			redirectString = '/coursepage.html?courseid='+str(new_course.key.integer_id())
			self.redirect(redirectString)
		else:
			self.response.out.write(template.render('templates/userpage.html', None))

class CoursePageHandler(BaseHandler):

  def get_assignment_type_by_id(self, at_id):
    for at in assignment_types:
        if at['id'] == at_id:
            return at
    return None

  # Format the assignments to json parsable object for display
  def get_formatted_assignments(self, course_id):
    formatted_assignments = []
    raw_assignments = db.get_all_assignments_for_course(course_id)
    for raw_a in raw_assignments:
        #a_type = db.get_assignment_type_by_id(raw_a.assignment_type_id)
        a_type = CoursePageHandler.get_assignment_type_by_id(self, raw_a.assignment_type_id)
        formatted_a = {
            'id' : raw_a.key.id(),
            'assignment_type' : {
                'id' : a_type['id'],
                'name' : a_type['name']
            },
            'complete' : raw_a.complete,
            'current_grade' : raw_a.current_grade,
            'details' : raw_a.details,
            'due_date': {
                'year' : raw_a.due_date.year,
                'month': raw_a.due_date.month,
                'day'  : raw_a.due_date.day
            },
            'name' : raw_a.name,
            'link' : raw_a.link,
            'total_grade' : raw_a.total_grade
        }
        if raw_a.reminder_date != None:
            formatted_a['reminder_date'] = {
                'year' : raw_a.reminder_date.year,
                'month': raw_a.reminder_date.month,
                'day'  : raw_a.reminder_date.day,
                'hour' : raw_a.reminder_date.hour,
                'minute': raw_a.reminder_date.minute
            }
        formatted_assignments.append(formatted_a)
    return formatted_assignments

  def get_formatted_assignment_types(self, assig_types):
    formatted_ats = []
    for at in assig_types:
        f_at = {
            'id' : at['id'],
            'name' : at['name'],
            'percent_of_total' : at['percent_of_total'],
            'quantity' : at['quantity']
        }
        formatted_ats.append(f_at)
    return json.dumps(formatted_ats)

  def get(self):
    path = 'templates/coursepage.html'

    # Get the user_id and course_id
    user = db.fetch_user_by_login(self.session['uid'])
    user_id = int(user.key.id())
    course_id = int(self.request.get('courseid'))

    #db.get_assignment_types_for_course(course_id)

    template_values = {
      'user' : db.fetch_user_by_id(user_id),
      'course' : db.get_course_by_id(course_id),
      'courses' : db.get_courses_for_user(user_id),
      'assignments_json' : json.dumps(CoursePageHandler.get_formatted_assignments(self,course_id)), # want to be able to access from js
      'assignment_types' : assignment_types,
      'assignment_types_json' : CoursePageHandler.get_formatted_assignment_types(self, assignment_types) # want to be able to access from js
    }
    self.response.out.write(template.render(path, template_values))

  def post(self):
    a = json.loads(self.request.body)
    course_id = int(a['course_id'])
    name = a['name']
    at_id = int(a['assignment_type']['id'])
    r_date = datetime.datetime(int(a['reminder_date']['year']), int(a['reminder_date']['month']), int(a['reminder_date']['day']), int(a['reminder_date']['hour']), int(a['reminder_date']['minute']))
    d_date = datetime.date(int(a['due_date']['year']), int(a['due_date']['month']), int(a['due_date']['day']))
    details = a['details']
    tot_grade = int(a['tot_grade'])
    link = a['link']

    db.create_assignment(course_id, name, at_id, d_date, r_date, details, tot_grade, link)
    self.response.write(json.dumps(a))
	
class ReportProblemHandler(BaseHandler) :
	def get(self):
		path='templates/reportproblem.html'
		self.response.out.write(template.render(path,None))
	
	def post(self):
		name=self.request.get('name')
		email=self.request.get('email')
		problem=self.request.get('problem')
		
		mail.send_mail(sender="Whiteboard Support <support@pittwhiteboard.com>", to="<cs1520pitt@gmail.com>", subject="Problem Reported", body="Name: "+name+"\nContact Email: "+email+"\nReported Problem: "+problem+"\n")
		
		path='templates/reportproblem2.html'
		self.response.out.write(template.render(path,None))
	
class LogOutHandler(BaseHandler) :
	def get(self):
		self.session['uid']=None
		self.redirect('/')
	

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my_secret_key',
}

app = webapp2.WSGIApplication([
  ('/', LoginHandler),
  ('/userpage.html', UserPageHandler),
  ('/coursepage.html', CoursePageHandler),
  ('/reportproblem', ReportProblemHandler),
  ('/logout.html', LogOutHandler),
  ('/accountinfo.html', AccountHandler)
], debug=True, config=config)


# --------------- CREATE ENTITIES ---------------------------
#user_key = db.register_user('badass', 'fonz', 'Arthur','Fonzarelli', 'University of Pittsburgh')

# c1_key = db.create_course(user_key, 'Programming for Web Applications', 'CS 1520', '5120 Sennott Square', 'T/H: 6:00pm - 7:15pm', 
#     '5120 Sennott Square', 'T: 12:00pm - 12:50pm', 'Timothy James', 'trjames@pitt.edu', '', 'By appointment',
#     'Salim Malakouti', 'sem156@pitt.edu', '5501 Sennott Square', 'F: 1:00pm - 2:00pm', 'doc1.pdf', 'https://my.pitt.edu',
#     'http://salimm.me/courses/cs1520/fall-2014/')
# c2_key = db.create_course(user_key, 'Busting Heads', 'BS 1654', '121 Sennott Square', 'M/W/F: 4pm - 5:15pm', 
#     '254 Sennott Square', 'T: 9:30am - 10:20am', 'Frank Dux', 'frd101@pitt.edu', '789 Sennott Square', 'H: 2:00pm - 4:00pm',
#     'Norman from Mighty Max', 'nmm24@pitt.edu', 'Hillman Cafe', 'T: 1:00pm - 2:00pm', 'doc1.pdf', 'cs.pitt.edu/~jmisurda.com',
#     None)
# c3_key = db.create_course(user_key, 'Picking Up Chicks', 'PC 1501', '1675 Sennott Square', 'M/W/F: 3pm - 4:15pm', 
#     '289 Sennott Square', 'T: 8:30am - 9:20am', 'James Kirk', 'jtk@pitt.edu', '1600 Sennott Square', 'H: 12:00pm - 2:00pm',
#     'Danny Zucco', 'ddz12@pitt.edu', '568 Sennott Square', 'F: 2:00pm - 4:00pm', 'doc1.pdf', None,
#     None)

# course = db.get_course_by_id(4889528208719872)
# db.create_assignment_type('Midterm Exam', course.key, 1, 25)
# db.create_assignment_type('Final Exam', course.key, 1, 25)
# db.create_assignment_type('Project 1', course.key, 1, 10)
# db.create_assignment_type('Project 2', course.key, 1, 15)
# db.create_assignment_type('Project 3', course.key, 1, 15)
# db.create_assignment_type('Quizzes', course.key, 5, 10)

# date1 = datetime.date(2014, 10, 15)
# date2 = datetime.date(2014, 10, 25)
# datetime1 = datetime.datetime(2014, 10, 13, 9, 30)
# ass1 = db.create_assignment(6296903092273152, 'Exam 1', 5593215650496512, date1, datetime1, 'The first exam for this class.', 100, 'https.my.pitt.edu')
# ass2 = db.create_assignment(6296903092273152, 'Project 1', 5698768766763008, date2, None, 'The first project for this class.', 100, None)
# --------------- END CREATE ENTITIES -----------------------
