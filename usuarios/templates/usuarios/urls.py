from __future__ import unicode_literals
from django.urls import path
from usuarios import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('entrar/', LoginView.as_view(template_name='usuarios/login.html'), name="login"),
    path('saida/', LogoutView.as_view(), {'next_page':'core_home'}, name="logout"),
    path('cadastre-se/', views.register, name="register"),
    path('nova-senha/', views.password_reset, name="password_reset"),
    path('confirmar-nova-senha/(?P<key>\w+)/$', views.password_reset_confirm, name="password_reset_confirm"),
    path('editar/', views.edit, name="edit"),
    path('editar-senha/', views.edit_password, name="password"),
]