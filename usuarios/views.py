from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from alocar.utils import generate_hash_key
from .forms import *
from .models import PasswordReset
from django.contrib import messages

User = get_user_model()


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
# funcao para resetar senha
# com o usuario fora do sistema sem logar
# '''
def password_reset_confirm(request, key):
    template_name = 'usuarios/password_reset_confirm.html'
    context = {}
    reset = PasswordReset.objects.get(key=key)
    # if request.method == 'POST':
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        password1 = form.cleaned_data.get("new_password1")
        password2 = form.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        else:
            form.save()
            reset.confirmed = True
            reset.save()
            context['success'] = True
            return redirect('usuarios:index')
    else:
        context['form'] = SetPasswordForm(user=reset.user)
        context['key'] = reset.key
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




@login_required
def index(request):
    template_name = 'usuarios/index.html'
    context = {}
    return render(request, template_name, context)