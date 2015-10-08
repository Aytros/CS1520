function chooseAnswer(id) {
	var q = id.substring(0, id.indexOf("a"));
	var count = 1;
	
	var x = document.getElementById(q + 'a' + count);
	while (x) {
		x.style.backgroundColor = '#909090';
		count++;
		x = document.getElementById(q + 'a' + count);
	}
	
	x = document.getElementById(id);
	if (x) {
		x.style.backgroundColor = '#8080ff';
	}
	
	x = document.getElementById(q);
	x.value = id;
}