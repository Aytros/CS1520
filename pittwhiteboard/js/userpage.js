$(document).ready(function() {
	var html = '<form action="" method="post">'
		+ '	<h5>Course Info</h5>'
		+ '	<table>'
		+ '		<tr>'
		+ '			<td>*Course Number:</td>'
		+ '			<td><input type="text" name="classnumber"></td>'
		+ '			<td>*Course Name:</td>'
		+ '			<td><input type="text" name="classname"></td>'
		+ '		</tr>'
		+ '		<tr><td colspan="2">&nbsp;</td></tr>'
		+ '		<tr>'
		+ '			<td>Course Location:</td>'
		+ '			<td><input type="text" name="courselocation"></td>'
		+ '			<td>Course Time:</td>'
		+ '			<td><input type="text" name="coursetime"></td>'
		+ '		</tr>'
		+ '		<tr>'
		+ '			<td>Recitation Location:</td>'
		+ '			<td><input type="text" name="reclocation"></td>'
		+ '			<td>Recitation Time:</td>'
		+ '			<td><input type="text" name="rectime"></td>'
		+ '		</tr>'
		+ '	</table>'
		+ '	<h5>Professor Info</h5>'
		+ '	<table>'
		+ '		<tr>'
		+ '			<td>*First Name:</td>'
		+ '			<td><input type="text" name="prof-fname"></td>'
		+ '			<td>*Last Name:</td>'
		+ '			<td><input type="text" name="prof-lname"></td>'
		+ '		</tr>'
		+ '		<tr>'
		+ '			<td>Office:</td>'
		+ '			<td><input type="text" name="prof-office"></td>'
		+ '			<td>Office Hours:</td>'
		+ '			<td><input type="text" name="prof-office-hours"></td>'
		+ '		</tr>'
		+ '		<tr>'
		+ '			<td>Email:</td>'
		+ '			<td><input type="text" name="prof-email"></td>'
		+ '		</tr>'
		+ '	</table>'
		+ '	<h5>TA Info</h5>'
		+ '	<table>'
		+ '		<tr>'
		+ '			<td>First Name:</td>'
		+ '			<td><input type="text" name="ta-fname"></td>'
		+ '			<td>Last Name:</td>'
		+ '			<td><input type="text" name="ta-lname"></td>'
		+ '		</tr>'
		+ '		<tr>'
		+ '			<td>Office:</td>'
		+ '			<td><input type="text" name="ta-office"></td>'
		+ '			<td>Office Hours:</td>'
		+ '			<td><input type="text" name="ta-office-hours"></td>'
		+ '		</tr>'
		+ '		<tr>'
		+ '			<td>Email:</td>'
		+ '			<td><input type="text" name="ta-email"></td>'
		+ '		</tr>'
		+ '	</table>'
		+ '	<input class="button" type="submit" name="submit" value="Submit">'
		+ '	<p><small>* Required Field</small></p>'
		+ '</form>';
	modal.init('Add Course', html);
});
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