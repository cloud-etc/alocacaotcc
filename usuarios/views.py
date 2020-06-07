from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from alocar.utils import generate_hash_key
from .forms import *
from .models import PasswordReset
from django.contrib import messages

User = get_user_model()

@login_required
def index(request):
    template_name = 'usuarios/index.html'
    context = {}
    return render(request, template_name, context)


def register(request):
    template_name = 'usuarios/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('usuarios:index')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


# '''
# funcao para alterar senha na tela de login,
# com o usuario fora do sistema sem logar
# '''
def password_reset(request):
    template_name = 'usuarios/password_reset.html'
    if request.method == 'POST':
        form = PasswordResetForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            return redirect('usuarios:password_reset_confirm', key=user.key)
    else:
        form = PasswordResetForm()
    return render(request, template_name, { 'form': form })


# '''
# funcao para resetar senha
# com o usuario fora do sistema sem logar
# '''
def password_reset_confirm(request, key):
    template_name = 'usuarios/password_reset_confirm.html'
    context = {}
    reset = PasswordReset.objects.get(key=key)
    if request.method == 'POST':
        form = SetPasswordForm(user=reset.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            reset.confirmed = True
            reset.save()
            context['success'] = True
            return redirect('usuarios:login')
    else:
        context['form'] = SetPasswordForm(user=reset.user)
        context['key'] = reset.key
    return render(request, template_name, context)




# funcao para alterar dados
# da conta do usuario logado
@login_required
def edit(request):
    template_name = 'usuarios/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
            return redirect('usuarios:index')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

# '''
# funcao para alterar senha com o usuario ja logado no sistema
# '''
@login_required
def edit_password(request):
    template_name = 'usuarios/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso')
            return redirect('alocar:listalocacao')
    else:
        form = PasswordChangeForm(user = request.user)
    context['form'] = form
    return render(request, template_name, context)




# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import RegisterForm, EditAccountForm, PasswordResetForm
# from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm,
#     SetPasswordForm)
# from django.contrib.auth import authenticate, login, get_user_model
# from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from alocar.utils import generate_hash_key
# from .models import PasswordReset
# from django.contrib import messages
#
# User = get_user_model()
#
# @login_required
# def index(request):
#     template_name = 'usuarios/index.html'
#     context = {}
#     return render(request, template_name, context)
#
#
# def register(request):
#     template_name = 'usuarios/register.html'
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user = authenticate(
#                 username=user.username, password=form.cleaned_data['password1'])
#             login(request, user)
#             return redirect('usuarios:index')
#     else:
#         form = RegisterForm()
#     context = {
#         'form': form
#     }
#     return render(request, template_name, context)
#
# # '''
# # funcao para alterar senha na tela de login,
# # com o usuario fora do sistema sem logar
# # '''
# def password_reset(request):
#     template_name = 'usuarios/password_reset.html'
#     context = {}
#     form = PasswordResetForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         context['success'] = True
#     context['form'] = form
#     return render(request, template_name, context)
#
#
# def password_reset_confirm(request, key):
#     template_name = 'usuarios/password_reset_confirm.html'
#     context = {}
#     reset = get_object_or_404(PasswordReset, key=key)
#     form = SetPasswordForm(user=reset.user, data=request.POST or None)
#     if form.is_valid():
#         form.save()
#         context['success'] = True
#         return redirect('usuarios:login')
#     context['form'] = form
#     return render(request, template_name, context)
#
# # funcao para alterar dados
# # da conta do usuario logado
# @login_required
# def edit(request):
#     template_name = 'usuarios/edit.html'
#     context = {}
#     if request.method == 'POST':
#         form = EditAccountForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Os dados da sua conta foram alterados com sucesso')
#             return redirect('usuarios:index')
#     else:
#         form = EditAccountForm(instance=request.user)
#     context['form'] = form
#     return render(request, template_name, context)
#
# # '''
# # funcao para alterar senha com o usuario ja logado no sistema
# # '''
# @login_required
# def edit_password(request):
#     template_name = 'usuarios/edit_password.html'
#     context = {}
#     if request.method == 'POST':
#         form = PasswordChangeForm(data=request.POST, user = request.user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Senha alterada com sucesso')
#             return redirect('alocar:listalocacao')
#     else:
#         form = PasswordChangeForm(user = request.user)
#     context['form'] = form
#     return render(request, template_name, context)
