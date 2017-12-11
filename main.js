/* Signup Form AJAX */
$('#signupForm').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	$('#user-phone-exists-error').css('display','none');
	$('#user-email-exists-error').css('display','none');
	submitBtn.prop('disabled', true);
	e.preventDefault();
	$.ajax({
		url: "{% url 'user_signup' %}", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var signup_response = jQuery.parseJSON(data);
			if (signup_response.register == "Success") {
				$('#register-modal').modal('hide');
				submitBtn.prop('disabled', false);
			}
			else if(signup_response.error == "True"){
				$('#register-modal').modal('hide');
				setTimeout(function() {
					$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
				}, 1000);
			}
		},/* end of Success */
		error: function(data) {
			$('#register-modal').modal('hide');
			setTimeout(function() {
				$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
			}, 1000);
		}/*  end of error */
	});/*./ajax*/
});
/* End of Signup Form */

/* Login form AJAX */
$('#loginform').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	submitBtn.prop('disabled', true);
	$('#no-user-error').css('display', 'none');
	$('#password-error').css('display', 'none');
	e.preventDefault();
	$.ajax({
		url: "{% url 'user_login' %}", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var login_response = jQuery.parseJSON(data);
			console.log(login_response);
			if (login_response.user == "nouser"){
				$('#no-user-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			}
			else if (login_response.user == "password wrong") {
				$('#password-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			} 
			else if ((login_response.user == "not active") && (login_response.user_phone)) {
				$('#login-modal').modal('hide');
				$('#OTP-modal').modal({backdrop:'static', keyboard:false,show:true});
				$('#verify-user-phone').html(login_response.user_phone);
				document.getElementById(formId).reset();
				submitBtn.prop('disabled', false);
			}
			else {
				if (login_response.login == "Failed") {
					alert("Invalid Login!");
				} else {
					document.getElementById(formId).reset();
					$('#login-modal').modal('hide');
					setTimeout(function() {
					location.reload();
					}, 400);
				}
			}/*./else*/
			submitBtn.prop('disabled', false);
			$('#spinner-login').css('display', 'none');
		},/* end of Success */
		error: function(data) {
			$('#loginModal').modal('hide');
			$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
		}/*  end of error */
	});/*./ajax*/
});
/*End of loin form AJAX */