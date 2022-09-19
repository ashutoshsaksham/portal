from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from .forms import NgoSignUpForm, StudentSignUpForm,UserLoginForm
# from .decorators import user_not_authenticated
from .tokens import account_activation_token





def homepage(request):
        
    return render(
        request=request,
        template_name='../templates/login.html',
        )

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


# @user_not_authenticated
def register_student(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = StudentSignUpForm()

    return render(
        request=request,
        template_name="../templates/student_register.html",
        context={"form": form}
        )
# @user_not_authenticated
def register_ngo(request):
    if request.method == "POST":
        form = NgoSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = NgoSignUpForm()

    return render(
        request=request,
        template_name="../templates/ngo_register.html",
        context={"form": form}
        )




@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')





# @user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None and user.is_student:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("student")
            elif user is not None and user.is_ngo:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("ngo")
            else:
                messages.error(request,"Invalid username or password")
        else: 
            for error in list(form.errors.values()):            
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="../templates/login.html",
        context={"form": form}
        )

# def profile(request, username):
#     if request.method == "POST":
#         user = request.user
#         form = UserUpdateForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             user_form = form.save()
#             messages.success(request, f'{user_form.username}, Your profile has been updated!')
#             return redirect("profile", user_form.username)

#         for error in list(form.errors.values()):
#             messages.error(request, error)

#     user = get_user_model().objects.filter(username=username).first()
#     if user:
#         form = UserUpdateForm(instance=user)
#         return render(
#             request=request,
#             template_name="../templates/profile.html",
#             context={"form": form}
#             )
    
#     return redirect("homepage")

# @login_required
# def password_change(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your password has been changed")
#             return redirect('login')
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)

#     form = SetPasswordForm(user)
#     return render(request, 'password_reset_confirm.html', {'form': form})






@login_required
def student(request):
    return render(request,'../templates/student_dashboard.html')

@login_required
def ngo(request):
    return render(request,'../templates/ngo_dashboard.html')