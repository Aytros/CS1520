var assignments, course_id, assignment_types;
	
$(document).ready(function() {
	getData();
	fillAssigTable();
	modal.init('Create New Assignment', getModalContent());
});

// ----------------- OBJECTS -------------------------------
function AssignmentType(name, id) {
	this.name = name;
	this.id = id;
}

function ReminderDate(year, month, day, hour, minute) {
	this.year = year;
	this.month = month;
	this.day = day;
	this.hour = hour;
	this.minute = minute;
}

function DueDate(year, month, day) {
	this.year = year;
	this.month = month;
	this.day = day;
}

function Assignment(name, course_id, at_name, at_id, r_date, d_date, details, curr_grade, tot_grade, link, complete) {
	this.name = name;
	this.course_id = course_id;
	this.assignment_type = new AssignmentType(at_name, at_id);
	this.due_date = d_date;
	this.reminder_date = r_date;
	this.details = details;
	this.curr_grade = curr_grade;
	this.tot_grade = tot_grade;
	this.link = link;
	this.complete = complete;
}

// ---------------- END OBJECTS ----------------------------

// ------------- HELPER FUNCTIONS --------------------------

function displayReminderDate(reminder_date) {
	var ampm = reminder_date.hour > 12 ? 'pm' : 'am';
	var display_hour = reminder_date.hour > 12 ? reminder_date.hour % 13 + 1 : reminder_date.hour;
	var display_minute = ('00' + reminder_date.minute).substr(-2);
  return reminder_date.month + '/' + reminder_date.day + '/' + reminder_date.year + ' at ' + display_hour + ':' + display_minute + ' ' + ampm
}

function validateNumeric(id) {
	var value = $('#'+id).val();
	var error_div = $('#'+id+'-error');
	if(isNaN(value)) {
		error_div.css('visibility', 'visible');
		$('#'+id).focus();
		return false;
	} else {
		error_div.css('visibility', 'hidden');
		return true;
	}
}
// Gets the user input from the "add new assignment" modal
// verifies the input and returns the input as an Assignment object
function getAssignmentFromModal() {
	var name, at_name, at_id, due_date, reminder_date, details, tot_grade, link;
	var date_arr, time_arr;

	// validate that the tot_grade is an integer value
	//TODOTODOTODO

	// get input from form
	name = $('#name').val();
	at_name = $('#type option:selected').text()
	at_id = $('#type option:selected').val()
	date_arr = $('#due-date').val().split('/');
	due_date = new DueDate(date_arr[2], date_arr[0], date_arr[1]);
	date_arr = $('#reminder-date').val().split('/');
	hour = $('#am-pm option:selected').val() === 'am' ? parseInt($('#hour option:selected').val()) : parseInt($('#hour option:selected').val()) + 12;
	minute = parseInt($('#minute option:selected').val());
	reminder_date = new ReminderDate(date_arr[2], date_arr[0], date_arr[1], hour, minute);
	details = $('#details').val();
	tot_grade = parseInt($('#total-points').val());
	link = $('#link').val();

	// create and return Assignment object if valid
	return new Assignment(name, course_id, at_name, at_id, reminder_date, due_date,	details, 0, tot_grade, link, false);
}

// Gets data from backend to populate the page with
function getData() {
	assignments = JSON.parse(document.getElementById('assignments').value);
	course_id = document.getElementById('course_id').value;
	assignment_types = JSON.parse(document.getElementById('assignment-types').value);
}

// Fill the assignment table with all of the object in
//  the "assignments" array
function fillAssigTable() {
	assig_table = $('#cpassig-table')
	tbl_container = $('#cpassig-table').parent();
	if(assignments.length === 0) {
		//assig_table.hide();
		//tbl_container.append('<strong>No Assignments</string>');
	}
	for(i = 0; i < assignments.length; i++) {
		addAssignmentToTable(assignments[i]);
		assig_table.show();
	}
}

// Add an assignment to the table
// Returns: -1 on failure and 0 on success
function addAssignmentToTable(assignment) {
	var assig_row_html = '<tr class="cpassig-row" onclick="expand(this, event);">'
										 + '	<td>' + assignment.name + '</td>'
										 + '	<td id="' + assignment.assignment_type.id + '">' + assignment.assignment_type.name + '</td>'
										 + '	<td>' + assignment.due_date.month + '/' + assignment.due_date.day + '/' + assignment.due_date.year + '</td>'
										 + '</tr>';
	var
	exp_row_html =  '<tr class="cpassig-expand-row">'
	exp_row_html += '	<td colspan="3">'
	exp_row_html += '		<strong>Details:</strong>'
	exp_row_html += '		<div class="expand-row-content">' + assignment.details
	if(assignment.reminder_date !== undefined && assignment.reminder_date !== null){
		exp_row_html += '		<br><strong>Reminder Set For:</strong> ' +	displayReminderDate(assignment.reminder_date);
	}
	if(assignment.link !== undefined && assignment.link !== null && assignment.link != ''){
		exp_row_html += '		<br><a href="' + assignment.link + '" target="_blank">Link</a>'
	}
	exp_row_html += '</div>'
	exp_row_html += '		<button class="button">Edit</button>'
	exp_row_html += '</tr>';
	$('#cpassig-table').append(assig_row_html);
	$('#cpassig-table').append(exp_row_html);
	return 0;
}

// Formats and returns an html string of the new assignment form.
// This is inserted into the modal.
function getModalContent() {
	var i = 0;
	new_assig_form_html =  '<div id="new-assig-info">'
	new_assig_form_html += '	<span class="form-label">Name:</span><input type="text" class="form-field" id="name" /><br>'
	new_assig_form_html += '	<span class="form-label">Type:</span>'
	new_assig_form_html += '	<select class="form-field" id="type">'
	for(i = 0; i < assignment_types.length; i++) {
		new_assig_form_html += '		<option value="' + assignment_types[i].id + '">' + assignment_types[i].name + '</option>'
	}
	new_assig_form_html += '	</select><br>'
	new_assig_form_html += '	<span class="form-label">Due Date:</span><input type="text" class="form-field datepicker" id="due-date" readonly="readonly" /><br>'
	new_assig_form_html += '	<span class="form-label">Reminder:</span><input type="text" class="form-field datepicker" id="reminder-date" readonly="readonly" />'
	new_assig_form_html += '	<select id="hour" class="form-field">'
	for(i = 1; i <= 12; i++) {
		new_assig_form_html += '	<option value="' + i + '">' + i + '</option>'
	}
	new_assig_form_html += '	</select>'
	new_assig_form_html += '	<select id="minute" class="form-field">'
	for(i = 0; i < 60; i+=5) {
		new_assig_form_html += '	<option value="' + i + '">' + ('00' + i).substr(-2) + '</option>'
	}
	new_assig_form_html += '	</select>'
	new_assig_form_html += '	<select id="am-pm" class="form-field">'
	new_assig_form_html += '		<option value="am">am</option>'
	new_assig_form_html += '		<option value="pm">pm</option>'
	new_assig_form_html += '	</select><br>'
	new_assig_form_html += '	<span class="form-label">Total Points:</span><input type="text" class="form-field" id="total-points" value="100" /><br>'
	new_assig_form_html += '	<div id="total-points-error">please enter numeric value</div>'
	new_assig_form_html += '	<span class="form-label">Details:</span><textarea rows="4" cols="50" class="form-field" id="details" /><br>'
	new_assig_form_html += '	<span class="form-label">Link:</span><input type="text" class="form-field" id="link" /><br>'
	new_assig_form_html += '	<br><br>'
	new_assig_form_html += '	<button class="button close-btn" onclick="saveAssignment();">Save</button>'
	new_assig_form_html += '</div>';
	return new_assig_form_html;
}

// ----------------------- END HELPER FUNCTIONS --------------------------

// --------------------- EVENT HANDLERS ----------------------------------

// Event handler for expanding a "Details" row in assignments table
function expand(sender, e) {
	var tbl_rows = document
		.getElementById('cpassig-table')
		.getElementsByTagName('tr');

	var expand_row = tbl_rows[sender.rowIndex + 1];
	if(expand_row) {
		var display = getComputedStyle(expand_row).getPropertyValue('display');
		if(display === 'none') {
			expand_row.style['display'] = 'table-row';
		} else {
			expand_row.style['display'] = 'none';
		}
	}
}

function saveAssignment() {
	var new_assig = getAssignmentFromModal();

	console.log(new_assig);

	$.ajax({
		url:"/coursepage.html",
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(new_assig),
		success:function(result){
			var saved_assig = JSON.parse(result);
			console.log(result);
			addAssignmentToTable(saved_assig);
    	modal.close();
    }
  });
}

// ---------------------- END EVENT HANDLERS ------------------------------
