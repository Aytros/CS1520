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

	course_location = ndb.StringProperty()
	course_day_time = ndb.StringProperty()
	#This stuff is nullable
	recitation_location = ndb.StringProperty()
	recitation_day_time = ndb.StringProperty()
	#Professor info, we could use an object here
	professor_name = ndb.StringProperty()
	professor_email = ndb.StringProperty()
	professor_office_location = ndb.StringProperty()
	professor_office_hours = ndb.StringProperty()
	#TA info, we could use an object here
	ta_name = ndb.StringProperty()
	ta_email = ndb.StringProperty()
	ta_office_location = ndb.StringProperty()
	ta_office_hours = ndb.StringProperty()
	ta_link = ndb.StringProperty()
	course_link = ndb.StringProperty()
	syllabus = ndb.StringProperty()

class Assignment(ndb.Model):
	course_id = ndb.IntegerProperty()
	name = ndb.StringProperty()
	assignment_type_id = ndb.IntegerProperty()
	due_date = ndb.DateProperty(indexed=True)
	reminder_date = ndb.DateTimeProperty()
	details = ndb.StringProperty()
	link = ndb.StringProperty()
	current_grade = ndb.FloatProperty()
	total_grade = ndb.FloatProperty()
	complete = ndb.BooleanProperty()

class Assignment_Type(ndb.Model):
	name = ndb.StringProperty()
	course_id = ndb.IntegerProperty()
	quantity = ndb.IntegerProperty(indexed=False)
	percent_of_total = ndb.FloatProperty()

class DB_Methods:

	# Takes a course_id and returns a list of assignments. Make
	# sure to check if the returned list is empty! 
	# Arg1: course id (int)
	def get_all_assignments_for_course(self, course_id):
		assignment_list = Assignment.query(Assignment.course_id == course_id).fetch(1000)
		return assignment_list

	# Takes a user and returns a list of assignments (course agnostic). 
	# This method is going to be a little more involved, because we take the
	# user, grab all their courses from their id, then use each of course ids
	# to find assignments
	# Make sure to check if the returned list is empty!
	# Arg1: user object (ndb.Model User)
	def get_all_assignments_for_user(self, user_id):
		course_list = self.get_courses_for_user(user_id)
		assignment_list = []
		total_list = []
		course_id_list = []
		#Grab all course ids, store them in a list
		for course in course_list:
			course_id_list.append(course.key.integer_id())
		#Query assigments that contain one of the courseids
		assignment_list = Assignment.query(
				Assignment.course_id in course_id_list
				)
		assignment_list.order('due_date')
		assignment_list.fetch(1000)		
		for assignment in assignment_list:
			total_list.append(assignment)
		return total_list

	def get_assignment_by_id(self, id):
		return Assignment.get_by_id(id)

	# Creates a new assignment
	# Arg1: course key
	# Arg2: name 
	# Arg3: assignment type key
	# Arg4: due date (date property)
	# Arg5: reminder date (date time property)
	# Arg6: details (String)
	# Arg7: total grade %
	# Arg8: link 
	def create_assignment(self, course_id, name, a_id, d_date, r_date, d, tot_grade, l):
		new_assignment = Assignment()
		new_assignment.course_id = course_id
		new_assignment.name = name
		new_assignment.assignment_type_id = a_id
		new_assignment.due_date = d_date
		new_assignment.reminder_date = r_date
		new_assignment.details = d
		new_assignment.current_grade = 0
		new_assignment.total_grade = tot_grade
		new_assignment.link = l
		new_assignment.complete = False
		new_assignment.put()

	# Takes an assignment and updates fields
	# Arg1: the assignment object id
	# Arg2-9: same as 1-8 in create_assignment
	# Arg10: the current grade
	def update_assingment(self, assign_id, course_id, name, a_id, d_date, r_date, d, tot_grade, l, cg):
		assignment = Assignment.get_by_id(assign_id)
		assignment.course_id = course_id
		assignment.name = name
		assignment.assignment_id = a_id
		assignment.due_date = d_date
		assignment.reminder_date = r_date
		assignment.details = d
		assignment.current_grade = g
		assignment.total_grade = tot_grade
		assignment.link = l
		assignment.put()

	# Creates an Assignment type
	# Arg1: name
	# arg2: course key
	# arg3: quantity
	# arg4: % of total
	def create_assignment_type(self, name, course_id, quantity, percent_of_total):
		assignment_type = Assignment_Type()
		assignment_type.name = name
		assignment_type.course_id = course_id
		assignment_type.quantity = quantity
		assignment_type.percent_of_total = percent_of_total
		return assignment_type.put()
	# Grabs all the assingmnet types for a course
	# arg1: course key
	def get_assignment_types_for_course(self, course_id):
		at_arr = []
		q = Assignment_Type.query(course_id in Assignment_Type.course_id).order(Assignment.name, Assignment_Type.percent_of_total)
		for at in q:
			at_arr.append(at)
		return at_arr

	#Grabs assignment type by the id 
	def get_assignment_type_by_id(self, id):
		return Assignment_Type.get_by_id(id)

	# This method takes a whole shit ton of arguments, some of which we will
	# have to handle null values for, then creates a course entry for it.
	# Here are the args, nullable values will be noted
	# Arg1: user key
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
	def create_course(self, user_id, name, number, c_loc, c_day, r_loc, r_day,
						p_name, p_email, p_loc, p_hours, ta_name, ta_email, 
						ta_loc, ta_hours, syllabus=None, c_link=None, ta_link=None):
		#new_user = User(parent=ndb.Key('University', u))	

		#new_course = Course(parent=ndb.Key('University', user.university))
		new_course = Course()
		new_course.name = name
		new_course.number = number
		new_course.user_ids = [user_id]
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
		new_course.course_link = c_link
		new_course.ta_link = ta_link
		new_course.syllabus = syllabus

		return new_course.put()

	# Shhhh... Don't tell anyone, but this is pretty much the exact same as
	# create_course, except that it also takes a course object argument, which
	# it updates, instead of creating a new one from scratch
	# Arg1: course object (ndb.Model course)
	# Arg2 - 15: Same as create_course's 1-14
	def update_course(self, course_id, user_id, name, number, c_loc, c_day, r_loc, r_day,
						p_name, p_email, p_loc, p_hours, ta_name, ta_email, 
						ta_loc, ta_hours):
		course = Course.get_by_id(course_id)
		course.name = name
		course.number = number
		course.user_ids = [user_id]
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
	# Arg1: course id
	# Arg2: user key
	def add_user_to_course(self, course_id, user_id):
		course = Course.get_by_id(course_id)
		#append the user id to the course list of user ids
		course.user_ids.append( user_id )
		#Overwrite the db entry
		course.put()

	# Send this method the user object that you want to get the courses for
	# It grabs that user's id, and queries the courses for courses containing
	# that user id, and returns the list of courses. Remember to check if
	# the return value is None!
	# Arg1: user key
	def get_courses_for_user(self, user_id):
		course_list = []
		q = Course.query(user_id == Course.user_ids).fetch(1000)
		for c in q:
			course_list.append(c)
		return course_list

	# This will return a course given the course's integer_id key.
	# Arg1: the course id
	def get_course_by_id(self, id):
		return Course.get_by_id(id)

	#	This method takes all the information a user needs to register
	# and creates a new DB entry for it. Returns 0 if things are all good.
	# Arguments are as follows:
	#1: user's password
	#2: user's email
	#3: user's first name
	#4: user's last name
	#5: user's university
	def register_user(self, p, e, fname,lname, u):
		#new_user = User(parent=ndb.Key('University', u))
		new_user = User()
		new_user.password = p;
		new_user.email = e;
		new_user.first = fname;
		new_user.last = lname;
		new_user.university = u;
		new_user.login, _ , _ = new_user.email.partition('@')
		return new_user.put();
		
	# Same as register_user, but takes the user to update as 
	# the first argument.
	# Arg1: user (ndb.Model user)
	# Arg2 - 6: same as 1-5 in register_user
	def update_user(self, user_id, p, e , fname, lname, u):
		user = User.get_by_id(user_id)
		user.password = p;
		user.email = e;
		user.first = fname;
		user.last = lname;
		user.university = u;
		user.login, _ , _ = user.email.partition('@')
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

	def fetch_user_by_id(self, id):
		return User.get_by_id(id)

	# Checks if the user exists, returns true if yes, false if no
	# Arg1: User's login
	def does_user_exist(self, l):
		user = User.query(User.login == l).get()
		if user is not None:
			return True
		else:
			return False


#---------------- ADMINISTRATIVE FUNCTIONS ---------------------------
	def clear_all_users(self):
		q = User.query()
		for user in q:
			user.key.delete()

	def clear_all_courses(self):
		q = Course.query()
		for course in q:
			course.key.delete()

	def clear_all_assignment_types(self):
		q = Assignment_Type.query()
		for at in q:
			at.key.delete()

	def clear_all_assignments(self):
		q = Assignment.query()
		for at in q:
			at.key.delete()

	def get_all_users(self):
		arr = []
		q = User.query()
		for u in q:
			arr.append(u)
		return arr;

	def get_all_courses(self):
		arr = []
		q = Course.query()
		for c in q:
			arr.append(c)
		return arr;

	def get_all_assignment_types(self):
		arr = []
		q = Assignment_Type.query()
		for a in q:
			arr.append(a)
		return arr;

	def get_all_assignments(self):
		arr = []
		q = Assignment.query()
		for a in q:
			arr.append(a)
		return arr;