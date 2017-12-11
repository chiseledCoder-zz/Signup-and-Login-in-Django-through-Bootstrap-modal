def user_signup(request):
	response_data = {}
	if request.method == "POST" and request.is_ajax:
		user_name = request.POST['name']
		user_phone = request.POST['phone']
		user_email = request.POST['email']
		user_password = request.POST['password']
		user_full_name = user_name.split(' ')
		user_first_name = user_full_name[0]
		try:
			user_last_name = user_full_name[1]
		except:
			user_last_name = " "
		user_username = user_name.replace(" ", "").lower()
		url = "http://2factor.in/API/V1/"+2Factor_API_KEY+"/SMS/" + user_phone + "/AUTOGEN/OTPSEND"
		payload = ""
		response = requests.request("GET", url, data=payload)
		otp_data = response.json()
		new_user = User.objects.create(username=user_username, email=user_email, first_name=user_first_name, last_name=user_last_name)
		new_user.save()
		new_user.set_password(user_password)
		new_user.is_active = False
		new_user.save()
		log_user = authenticate(username=user_username, password=user_password)
		if log_user is not None:
			login(request, log_user)
		new_profile = UserAccount.objects.get_or_create(user=new_user, phone=user_phone, reward_id=reward_id_generator())
		for key,value in otp_data.items():
			if key == "Details":
				session_id = value
				get_profile = UserAccount.objects.get(user=new_user)
				get_profile.user_otp_session = session_id
				get_profile.save()
		response_data['register'] = "Success"
		message = "Hi Admin! New user "+ str(new_user.get_full_name()) +" has registered with you."
		if response_data['register'] == "Success":
			mail_admins(subject=str(new_user.id)+" new user registration!", message=message, fail_silently=False)
		response_data['user_phone'] = user_username
		return HttpResponse(JsonResponse(response_data))
	return HttpResponse(JsonResponse(response_data))

def user_login(request):
	username = password = ''
	response_data = {}
	if request.POST and request.is_ajax:
		phone = request.POST['phone']
		password = request.POST['password']
		try:
			get_user_by_phone = UserAccount.objects.get(phone=phone)
			user_phone = get_user_by_phone.phone
			username = get_user_by_phone.user.get_username()
			get_user = User.objects.get(username=username)
			if get_user.check_password(password):
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						response_data = {'login' : "Success"}
					else:
						url = "http://2factor.in/API/V1/"+API_KEY+"/SMS/" + user_phone + 
                         "/AUTOGEN/OTPSEND"
						payload = ""
						response = requests.request("GET", url, data=payload)
						otp_data = response.json()
						response_data['user'] = "not active"
						response_data['user_phone'] = user_phone
			else:
				response_data = {'user':"password wrong"}
		except UserAccount.DoesNotExist:
			response_data = {'user':"nouser"}
	else:
		username = password = ''
		response_data = {'login': "Failed"}
	return HttpResponse(JsonResponse(response_data))