if ($('.error').text().length) {
	if ($('.error').text() === 'login') {
		alert('Username or password did not match!');
	} else alert('Username is taken. Please try again!');
	$('.error').text('');
}

$('.supbtn').click(function(e) {
	e.preventDefault();
	if ($('.name').val().length < 1) {
		alert('Please enter a name!');
	} else if ($('.email').val().length < 5) {
		alert('Please enter a valid email!');
	} else if ($('.userid').val().length < 1) {
		alert('Please enter username!');
	} else if ($('.dob').val().length < 10) {
		alert('Please enter date of birth!');
	} else if ($('.password').val().length < 8) {
		alert('Password must be at least 8 characters long!');
	} else if ($('.password').val() != $('.confirm').val()) {
		alert('Password and confirm password does not match!');
	} else {
		$('#signup').submit();
	}
});
