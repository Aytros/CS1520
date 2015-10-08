modal = (function () {
	var html = '';

	var init = function(title, content) {
		html = '<div id="overlay" onclick="modal.close()"></div>'
				 + '<div id="modal-content">'
				 + '	<div id="close-modal" onclick="modal.close()">x</a></div>'
				 + '	<h3>' + title + '</h3>'
				 +			content
				 + '	</div>';
		//$('body').append(html);
	};

	var pop = function() {
		$('body').append(html);
		$('.datepicker').datepicker();
		//$('#overlay').css('visibility', 'visible');
		//$('#modal-content').css('visibility', 'visible');
	};

	var close = function() {
		$('#overlay').remove();
		$('#modal-content').remove();
		//$('#overlay').css('visibility', 'hidden');
		//$('#modal-content').css('visibility', 'hidden');
	};

	return {
		init : init,
		pop  : pop,
		close: close
	};

}());