from django.urls import path
from django.contrib.auth import views as auth_views
from .import  views



urlpatterns=[
    path("", views.homepage, name="homepage"),
    path('register_student', views.register_student, name="register_student"),
    path('student', views.student, name='student'),
    path('ngo', views.ngo, name='ngo'),
    path('register_ngo', views.register_ngo, name="register_ngo"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    # path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    



    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="../templates/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="../templates/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="../templates/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="../templates/password_reset_done.html"), 
        name="password_reset_complete"),
]







'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''