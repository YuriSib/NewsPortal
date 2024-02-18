from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from .views import BaseRegisterView, PersonalClassView, upgrade_me


urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout_confirm/', TemplateView.as_view(template_name='sign/logout_confirm.html'), name='logout_confirm'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('personal_acc/', PersonalClassView.as_view(template_name='sign/personal_acc.html'), name='personal_acc'),
    path('personal_acc/upgrade/', upgrade_me, name='upgrade')
]
