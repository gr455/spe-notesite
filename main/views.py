from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Create your views here.


def homepage(request):
	logged_in = False
	course_count = range(0,Course.objects.count(),2)

	if request.user.is_authenticated:
		logged_in = True

	params = {"notes": Note.objects.order_by('-note_whenPublished')[:6],
			  "tutorials": Tutorial.objects.all,
			  "chapters": Chapter.objects.all,
			  "courses": Course.objects.all,
			  "logged_in": logged_in,
			  "range": course_count }

	return render(request = request,
				  template_name = "main/index.html",
				  context = params )


#Session Handling
def register(request):
	#send home if already logged in
	if request.user.is_authenticated:
		return redirect("/")

	err_msgs = None
	if request.method == "POST":
		info = NewUserForm(request.POST)
		if info.is_valid():
			email = info.cleaned_data.get('email')
			if User.objects.filter(email = email).exists():
				info.add_error('email', 'account with email already exists')
				err_msgs = info.errors.items
			else:
				user = info.save()
				user.is_active = True
				user.save()
				hashed = make_hash(user)
				# send_mail("Notesite sign up confirmation",
				 		   # f"Thank you {user.first_name} for registering with Notesite as {user.username}. Please click on the link below to activate your account \n\n {request.META['HTTP_HOST']}/users/validate/{user.username}/{hashed}",
				 		   # settings.EMAIL_HOST_USER,
				 		   # [user.email,])
				return redirect("/preconfirm")
		else:
			err_msgs = info.errors.items

	create_form = NewUserForm
	return render(request = request,
				  template_name = "main/register.html",
				  context = {"create_form": create_form,
				  			 "err_msgs": err_msgs})

#TODO: not be lazy and make a proper digest
def make_hash(user):
	hash =  hashlib.sha256(str.encode(user.username+user.password)).hexdigest()
	return hash

def activate_user(request, username, token):
	user = get_object_or_404(User, username = username)
	valid_token = make_hash(user)

	if not user.is_active and valid_token == token:
		user.is_active = True
		user.save()
		messages.success(request, f"User confirmation successful. Please login to proceed")
		return redirect('/login')
	else:
		return HttpResponse("The link is incorrect or the user is already validated")

def preconfirm(request):

	if request.user.is_active:
		messages.success(request, f"Account already activated")
		return redirect('/')

	return render(request = request,
				  template_name = "main/preconfirm.html",
				  context = {"logged_in": False})

def login_user(request):
	if request.user.is_authenticated:
		return redirect("/")
	err_msgs = None
	if request.method == "POST":
		info = AuthenticationForm(request, request.POST)
		if info.is_valid():
			username = info.cleaned_data.get('username')
			password = info.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user and user.is_active:
				messages.success(request, f"Logged in")
				login(request, user)
				return redirect("/")

		err_msgs = info.errors.items 

	login_form = AuthenticationForm()
	return render(request = request,
				  template_name = "main/login.html",
				  context = {"login_form":login_form,
				  			 "err_msgs": err_msgs})

def logout_user(request):
	if request.user.is_authenticated:
		logout(request)
		messages.info(request, "Logged out successfully")
	return redirect("/")