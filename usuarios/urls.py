from __future__ import unicode_literals
from django.urls import path
from usuarios import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('', views.index, name="index"),
    path('entrar/', LoginView.as_view(template_name='usuarios/login.html'), name="login"),
    path('sair/', LogoutView.as_view(template_name='usuarios/login.html'), name="logout"),
    path('nova-senha/', views.password_reset, name="password_reset"),
    path('confirmar-nova-senha/<key>', views.password_reset_confirm, name="password_reset_confirm"),
    path('editar/', views.edit, name="edit"),
    path('editar-senha/', views.edit_password, name="edit_password"),
]