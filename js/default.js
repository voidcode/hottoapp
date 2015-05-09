$(document).ready(function () {	
	window.pageScrollUp = function(){
		alert('pageScrollUp');
	}
	window.pageScrollDown = function(){
		alert('pageScrollDown');
		$('body').scrollTo('hr');
	}
});