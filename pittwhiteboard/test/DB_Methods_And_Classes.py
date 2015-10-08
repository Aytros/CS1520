from google.appengine.ext import ndb

#For all ndb models we can grab the key by saying model.key.integer_id()

class User(ndb.Model):
	#This'll be your email minus the @...
	login = ndb.StringProperty(indexed=True)
	password = ndb.StringProperty(indexed=True)
	email = ndb.StringProperty(indexed=False)
	first = ndb.StringProperty(indexed=False)
	last = ndb.StringProperty(indexed=False)
	#We can maybe do something with this later
	university = ndb.StringProperty(indexed=False)
	#This will be the date they register
	date = ndb.DateTimeProperty(auto_now_add=True)

class Course(ndb.Model):
	#Give it a name too, while we're at it
	name = ndb.StringProperty(indexed=True)
	number = ndb.StringProperty(indexed=True)
	#now we have a list of any associated user ids
	user_ids = ndb.IntegerProperty(repeated=True)

	course_location = ndb.StringProperty(indexed=False)
	course_day_time = ndb.DateTimeProperty()
	#This stuff is nullable
	recitation_location = ndb.StringProperty(indexed=False)
	recitation_day_time = ndb.DateTimeProperty()
	#Professor info, we could use an object here
	professor_name = ndb.StringProperty(indexed=True)
	professor_email = ndb.StringProperty(indexed=False)
	professor_office_location = ndb.StringProperty(indexed=False)
	professor_office_hours = ndb.StringProperty(indexed=False)
	#TA info, we could use an object here
	ta_name = ndb.StringProperty(indexed=False)
	ta_email = ndb.StringProperty(indexed=False)
	ta_office_location = ndb.StringProperty(indexed=False)
	ta_office_hours = ndb.StringProperty(indexed=False)


class Assignment(ndb.Model):
	course_id = ndb.IntegerProperty()
	name = ndb.StringProperty(indexed=False)
	assignment_type_id = ndb.IntegerProperty()
	due_date = ndb.DateProperty()
	reminder_date = ndb.DateTimeProperty()
	details = ndb.StringProperty(indexed=False)
	current_grade = ndb.FloatProperty()
	total_grade = ndb.FloatProperty()

class Assignment_Link(ndb.Model):
	#auto id
	assignment_ids = ndb.IntegerProperty(repeated=True)
	name = ndb.StringProperty()
	link = ndb.StringProperty()

class Assignment_Type(ndb.Model):
	#auto id
	name = ndb.StringProperty()
	percent_of_total = ndb.FloatProperty()

class DB_Methods:

	# Takes a course and returns a list of assignments. Make
	# sure to check if the returned list is empty! 
	# Arg1: course object (ndb.Model Course)
	def get_assignments_for_course(self, course_id):
		assignment_list = Assignment.query(Assignment.course_id == course_id).fetch(1000)
		return assignment_list

	# Takes a user and returns a list of assignments (course agnostic). 
	# This method is going to be a little more involved, because we take the
	# user, grab all their courses from their id, then use each of course ids
	# to find assignments
	# Make sure to check if the returned list is empty!
	# Arg1: user object (ndb.Model User)
	def get_all_assignments_for_user(self, user):
		course_list = self.get_courses(user)
		assignnment_list = []
		for course in course_list:
			assignment_list.append(
				Assignment.query(
					Assignment.course_id == course.course_id 
					).fetch(1000))

		return assignment_list

	# Creates a new assignment
	# Arg1: course object (ndb.Model Course)
	# Arg2: assignment type (int)
	# Arg3: due date (date property)
	# Arg4: reminder date (date time property)
	# Arg5: details (String)
	# Arg6: grade
	def create_assignment(self, course, name, a_type, d_date, r_date, d, g):
		new_assignment = Assignment()
		new_assignment.course_id = course.key.integer_id()
		new_assignment.name = name
		new_assignment.assignment_type_id = a_type
		new_assignment.due_date = d_date
		new_assignment.reminder_date = r_date
		new_assignment.details = d
		new_assignment.grade = g
		new_assignment.put()

	# Takes an assignment and updates fields
	# Arg1: the assignment object (ndb.Model Assignment)
	# Arg2-7: same as 1-6 in create_assignment
	def update_assingment(self, assign, course, name, a_type, d_date, r_date, d, g):
		assignment.course_id = course.key.integer_id()
		assignment.name = name
		assignment.assignment_type_id = a_type
		assignment.due_date = d_date
		assignment.reminder_date = r_date
		assignment.details = d
		assignment.grade = g
		assignment.put()

	# This method takes a whole shit ton of arguments, some of which we will
	# have to handle null values for, then creates a course entry for it.
	# Here are the args, nullable values will be noted
	# Arg1: user object (ndb.Model User)
	# Arg2: course name (string)
	# Arg3: course location (string)
	# Arg4: course_day_time (DateTimeProperty)
	# Arg5: recitation_location (String, nullable)
	# Arg6: recitation_day_time (DateTimeProperty, nullable)
	# Arg7: professor name (String)
	# Arg8: professor email (String, nullable)
	# Arg9: professor office location (String, nullable)
	# Arg10: professor office hours (DateTimeProperty, nullable)
	# Arg11: ta name (String, nullable)
	# Arg12: ta email (String, nullable)
	# Arg13: ta office location (String, nullable)
	# Arg14: ta office hours (DateTimeProperty, nullable)
	def create_course(self, user, name, number, c_loc, c_day, r_loc, r_day,
						p_name, p_email, p_loc, p_hours, ta_name, ta_email, 
						ta_loc, ta_hours):
		new_user = User(parent=ndb.Key('University', u))	

		new_course = Course(parent=ndb.Key('University', user.university))
		#new_course = Course()
		new_course.name = name
		new_course.number = number
		new_course.user_ids = [user.key.integer_id()]
		new_course.course_location = c_loc
		new_course.course_day_time = c_day

		new_course.recitation_location = r_loc
		new_course.recitation_day_time = r_day

		new_course.professor_name = p_name
		new_course.professor_email = p_email
		new_course.professor_office_location = p_loc
		new_course.professor_office_hours = p_hours

		new_course.ta_name = ta_name
		new_course.ta_email = ta_email
		new_course.ta_office_location = ta_loc
		new_course.ta_office_hours = ta_hours

		new_course.put()

	# Shhhh... Don't tell anyone, but this is pretty much the exact same as
	# create_course, except that it also takes a course object argument, which
	# it updates, instead of creating a new one from scratch
	# Arg1: course object (ndb.Model course)
	# Arg2 - 15: Same as create_course's 1-14
	def update_course(self, course, user, name, number, c_loc, c_day, r_loc, r_day,
						p_name, p_email, p_loc, p_hours, ta_name, ta_email, 
						ta_loc, ta_hours):
		course.name = name
		course.number = number
		course.user_ids = [user.key.integer_id()]
		course.course_location = c_loc
		course.course_day_time = c_day

		course.recitation_location = r_loc
		course.recitation_day_time = r_day

		course.professor_name = p_name
		course.professor_email = p_email
		course.professor_office_location = p_loc
		course.professor_office_hours = p_hours

		course.ta_name = ta_name
		course.ta_email = ta_email
		course.ta_office_location = ta_loc
		course.ta_office_hours = ta_hours

		course.put()

	# This method is really easy! just send it a course and user object 
	# and it'll add the user id to the course's list of ids
	# Arg1: course object
	# Arg2: user object
	def add_user_to_course(self, course, user):
		#append the user id to the course list of user ids
		course.user_ids.append( user.key.integer_id() )
		#Overwrite the db entry
		course.put()

	# Send this method the user object that you want to get the courses for
	# It grabs that user's id, and queries the courses for courses containing
	# that user id, and returns the list of courses. Remember to check if
	# the return value is None!
	# Arg1: user object (ndb.Model User)
	def get_courses(self, user):
		lookup_id = user.key.integer_id()
		course_list = Course.query(Course.user_ids == lookup_id).fetch(1000)
		return course_list


	#	This method takes all the information a user needs to register
	# and creates a new DB entry for it. Returns 0 if things are all good.
	# Arguments are as follows:
	#1: user's password
	#2: user's email
	#3: user's first name
	#4: user's last name
	#5: user's university
	def register_user(self, p, e, fname,lname, u):
		new_user = User(parent=ndb.Key('University', u))	
		new_user.password = p;
		new_user.email = e;
		new_user.first = fname;
		new_user.last = lname;
		new_user.university = u;
		new_user.login, _ , _ = new_user.email.partition('@')
		new_user.put();
		return 0
	# Same as register_user, but takes the user to update as 
	# the first argument.
	# Arg1: user (ndb.Model user)
	# Arg2 - 6: same as 1-5 in register_user
	def update_user(self, user, p, e , fname, lname, u):
		user.password = p;
		user.email = e;
		user.first = fname;
		user.last = lname;
		user.university = u;
		user.login, _ , _ = new_user.email.partition('@')
		user.put();
	# This method takes the users login and password and makes
	# sure it's correct. returns 1 if good, 0 if pass/name combo
	# don't match. Arguments are as follows
	#1: entered login
	#2: entered password
	def check_login(self, l, p):
		#query user by login, just get back the count
		#if the count is 1, then we matched, otherwise we didn't
		match_count = User.query(User.login == l, User.password == p).count()
		return match_count

	# Grabs the full user object by the login. I'm thinking we use
	# this when the user properly authenticates, and we don't have 
	# their id.
	# Returns user object if it exists, otherwise returns None
	# Arg 1: User's login
	def fetch_user_by_login(self,l):
		user = User.query(User.login == l).get()
		if user is not None:
			return user
		else:
			return None
	# Checks if the user exists, returns true if yes, false if no
	# Arg1: User's login
	def does_user_exist(self, l):
		user = User.query(User.login == l).get()
		if user is not None:
			return True
		else:
			return False

	def fetch_user_by_id(self, id):
		user = User.query(User.key.integer_id() == id).get()
		if user is not None:
			return user
		else:
			return None






